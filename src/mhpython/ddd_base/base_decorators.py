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

import functools

from .base_types import DDDAttribute

def make_orm_class(tablename: str):
    pass


def ddd_entity_tablename(tablename: str):
    def ddd_entity_decorator(cls):
        @functools.wraps(cls)
        def ddd_entity_wrapper(*args, **kwargs):
            cls.__tablename__ = tablename
            return cls
        return ddd_entity_wrapper
    return ddd_entity_decorator


def ddd_entity(tablename: str):
    def ddd_entity_decorator(cls):
        @functools.wraps(cls)
        def ddd_entity_wrapper(*args, **kwargs):
            attrs = {field: info for field, info in vars(cls).items() if isinstance(info, DDDAttribute)}
            for attr in attrs.keys():
                del cls.__dict__[attr]
                cls.__dict__[attr] = 'int'
            cls._orm_class = make_orm_class(tablename)
            return cls
        return ddd_entity_wrapper
    return ddd_entity_decorator


