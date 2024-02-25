#  MIT License
#
#  Copyright (c) 2024 Mathieu Imfeld
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import typing
import uuid
import dataclasses
import pydantic
import pydantic.fields
import pydantic_core

from sqlalchemy.orm import Mapped

from mhpython import ORMBase

UniqueIdentifier = typing.TypeVar('UniqueIdentifier', bound=uuid.UUID)


@dataclasses.dataclass
class DDDAttribute:
    schema: typing.Optional[pydantic.fields.FieldInfo] = None
    orm: typing.Optional[Mapped] = None


class DDDMeta(type):

    def __new__(cls, name, bases, dct):
        # Parse the class declaration and resolve types
        tablename = dct['__tablename__']
        global_ns = globals()
        fields = {attr: (DDDMeta._resolve_type(global_ns, dct['__annotations__'][attr]), info)
                  for attr, info in dct.items() if isinstance(info, DDDAttribute)}

        # Clean up
        del dct['__tablename__']
        for ddd_attr in fields:
            del dct[ddd_attr]
            del dct['__annotations__'][ddd_attr]

        # Create schema and ORM class
        schema_class = DDDMeta._make_schema_class(name=f'{dct["__qualname__"]}Schema',
                                                  module=dct['__module__'],
                                                  fields=fields)
        dct['_schema_class'] = schema_class
        orm_class = DDDMeta._make_orm_class(name=f'{dct["__qualname__"]}ORM',
                                            module=dct['__module__'],
                                            tablename=tablename,
                                            fields=fields)
        dct['_orm_class'] = orm_class
        dct['_synchronise'] = DDDMeta._make_synchronise()
        dct['__init__'] = DDDMeta._make_init(fields)
        for field, getter in DDDMeta._make_getters(fields).items():
            dct[field] = getter

        # Instantiate the class
        instance = super().__new__(cls, name, bases, dct)
        return instance

    @staticmethod
    def _resolve_type(global_ns: typing.Dict, annotation: typing.Type) -> str:
        if annotation.__module__ == 'builtins':
            return annotation.__name__
        if annotation.__module__ in global_ns:
            return f'{annotation.__module__}.{annotation.__name__}'
        elif annotation.__name__ in global_ns:
            return annotation.__name__
        raise AttributeError(f'Type {annotation.__name__} is not imported')

    @staticmethod
    def _make_synchronise() -> typing.Callable:
        synchronise_fn = (
            f'def _synchronise(self):\n'
            f'  for field in self._schema.model_fields.keys():\n'
            f'    setattr(self._orm, field, getattr(self._schema, field))\n'
        )
        dynamic_compiler_ns = {}
        exec(synchronise_fn, globals(), dynamic_compiler_ns)
        return dynamic_compiler_ns['_synchronise']

    @staticmethod
    def _make_init(fields: typing.Dict[str, typing.Tuple[str, DDDAttribute]]) -> typing.Callable:
        mandatory_args = {}
        optional_args = {}
        optional_args_with_factory = {}
        for field, (annotation, info) in fields.items():
            if info.schema.default_factory is not None:
                optional_args_with_factory[field] = (annotation, info)
            elif info.schema.default is not pydantic_core.PydanticUndefined:
                optional_args[field] = (annotation, info)
            else:
                mandatory_args[field] = (annotation, info)

        arg_spec = ['self']
        for arg, (annotation, info) in mandatory_args.items():
            arg_spec.append(f'{arg}: {annotation}')
        for arg, (annotation, info) in optional_args.items():
            arg_spec.append(f'{arg}: {annotation} = {info.schema.default}')
        for arg, (annotation, info) in optional_args_with_factory.items():
            arg_spec.append(f'{arg}: {annotation} = None')

        data_init_spec = ([f'{field}={field}' for field in mandatory_args.keys()] +
                         [f'{field}={field}' for field in optional_args.keys()])
        init_fn = (
            f'def __init__({", ".join(arg_spec)}):\n'
            f'  self._schema = self._schema_class({", ".join(data_init_spec)})\n'
            f'  self._orm = self._orm_class({", ".join(data_init_spec)})\n'
            '  self._synchronise()\n'
        )
        dynamic_compiler_ns = {}
        exec(init_fn, globals(), dynamic_compiler_ns)
        return dynamic_compiler_ns['__init__']

    @staticmethod
    def _make_getters(fields: typing.Dict[str, typing.Tuple[str, DDDAttribute]]) -> typing.Dict[str, typing.Callable]:
        getters = {}
        for field, (annotation, info) in fields.items():
            getter_fn = (
                f'@property\n'
                f'def {field}(self) -> {annotation}:\n'
                f'  return self._schema.{field}'
            )
            dynamic_compiler_ns = {}
            exec(getter_fn, globals(), dynamic_compiler_ns)
            getters[field] = dynamic_compiler_ns[field]
        return getters

    @staticmethod
    def _make_fn(name: str,
                 args: typing.Dict | None,
                 body: typing.List | None,
                 return_type: str | None) -> typing.Callable:
        wrapper_locals = {}
        if args is None:
            args = []
        return_annotation = ''
        if return_type is not None:
            wrapper_locals['_return_type'] = return_type
            return_annotation = '-> _return_type'
        args = ','.join(args)
        body = '\n'.join(f'  {line}' for line in body)

        fn = f"  def {name}(self, {args}){return_annotation}:\n  {body}"
        local_vars = ', '.join(wrapper_locals.keys())
        wrapper = f"def __make_fn__({local_vars}):\n{fn}\n  return {name}"
        ns = {}
        exec(wrapper, None, ns)
        return ns['__make_fn__'](**wrapper_locals)

    @staticmethod
    def _make_schema_class(name: str,
                           module: str,
                           fields: typing.Dict[str, typing.Tuple[str, DDDAttribute]]) -> typing.Type:
        schema_annotations = {}
        schema_defaults = {}
        for field, (annotation, default) in fields.items():
            schema_annotations[field] = annotation
            schema_defaults[field] = default.schema
        return type(name,
                    (pydantic.BaseModel,),
                    {
                        '__module__': module,
                        '__annotations__': schema_annotations,
                        **schema_defaults
                    })

    @staticmethod
    def _make_orm_class(name: str,
                        module: str,
                        tablename: str,
                        fields: typing.Dict[str, typing.Tuple[str, DDDAttribute]]) -> typing.Type:
        orm_annotations = {}
        orm_defaults = {}
        for field, (annotation, default) in fields.items():
            orm_annotations[field] = f'Mapped[{annotation}]'
            orm_defaults[field] = default.orm
        return type(name,
                    (ORMBase,), {
                        '__module__': module,
                        '__tablename__': tablename,
                        '__annotations__': orm_annotations,
                        **orm_defaults
                    })
