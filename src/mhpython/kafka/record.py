#  MIT License
#
#  Copyright (c) 2025 Mathieu Imfeld
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
import enum
import datetime
import uuid
import dataclasses
import json


class JsonCustomEncoder(json.JSONEncoder):
    """
    Handles the JSON Encoding of otherwise unserializable dataclass objects
    """

    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


class JsonCustomDecoderWithObjectPairsHook(json.JSONDecoder):
    """
    Handles the JSON decoding of otherwise unserializable dataclass objects
    This variant of custom decoding uses the object_pairs_hook method of the JSONDecoder

    Verdict: The object_pairs_hook appears slightly more logical to use than the object_hook method
    """

    def __init__(
        self,
        *,
        object_hook=None,
        parse_float=None,
        parse_int=None,
        parse_constant=None,
        strict=True,
        object_pairs_hook=None,
    ):
        super().__init__(
            object_hook=object_hook,
            parse_float=parse_float,
            parse_int=parse_int,
            parse_constant=parse_constant,
            strict=strict,
            object_pairs_hook=JsonCustomDecoderWithObjectPairsHook.object_pairs_hook,
        )

    @classmethod
    def object_pairs_hook(
        cls, object_pairs: typing.List[typing.Tuple[str, typing.Any]]
    ):
        parsed = {}
        for key, value in object_pairs:
            match key:
                case 'uid':
                    parsed[key] = uuid.UUID(value)
                case 'timestamp':
                    parsed[key] = datetime.datetime.fromisoformat(value)
                case 'region':
                    parsed[key] = RegionEnum(value)
                case _:
                    parsed[key] = value
        return parsed


class JsonCustomDecoderWithObjectHook(json.JSONDecoder):
    """
    Handles the JSON decoding of otherwise unserializable dataclass objects
    This variant of custom decoding uses the object_hook method of the JSONDecoder

    Verdict: The object_pairs_hook appears slightly more logical to use than the object_hook method
    """

    def __init__(
        self,
        *,
        object_hook=None,
        parse_float=None,
        parse_int=None,
        parse_constant=None,
        strict=True,
        object_pairs_hook=None,
    ):
        super().__init__(
            object_hook=JsonCustomDecoderWithObjectHook.object_hook,
            parse_float=parse_float,
            parse_int=parse_int,
            parse_constant=parse_constant,
            strict=strict,
            object_pairs_hook=object_pairs_hook,
        )

    @classmethod
    def object_hook(cls, object_pairs: typing.Dict[str, typing.Any]):
        parsed = {}
        for key, value in object_pairs.items():
            match key:
                case 'uid':
                    parsed[key] = uuid.UUID(value)
                case 'timestamp':
                    parsed[key] = datetime.datetime.fromisoformat(value)
                case 'region':
                    parsed[key] = RegionEnum(value)
                case _:
                    parsed[key] = value
        return parsed


@enum.unique
class RegionEnum(enum.StrEnum):
    NA = 'NA'
    EMEA = 'EMEA'
    APAC = 'APAC'


@dataclasses.dataclass
class DataclassRecord:
    """
    A dataclass record that can be serialised and deserialised
    """

    uid: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)
    timestamp: datetime.datetime = dataclasses.field(
        default_factory=datetime.datetime.now
    )
    name: str = dataclasses.field(default='Hello World')
    region: RegionEnum = dataclasses.field(default=RegionEnum.EMEA)

    @classmethod
    def serialize_key(cls, key: RegionEnum) -> bytes:
        return key.value.encode('utf-8')

    @classmethod
    def deserialize_key(cls, key: bytes) -> RegionEnum:
        return RegionEnum(key.decode('utf-8'))

    @classmethod
    def serialize(cls, value: typing.Self) -> bytes:
        return json.dumps(dataclasses.asdict(value), cls=JsonCustomEncoder).encode(
            'utf-8'
        )

    @classmethod
    def deserialize(cls, value: bytes) -> typing.Self:
        return cls(
            **json.loads(
                value.decode('utf-8'), cls=JsonCustomDecoderWithObjectPairsHook
            )
        )
