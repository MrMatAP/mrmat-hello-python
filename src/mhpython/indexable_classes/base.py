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

import abc
import uuid
import typing
import logging

class IndexableBaseClass(abc.ABC):
    """
    A base class providing indexing and management of class instances.

    This class serves as a framework for maintaining a collection of its
    instances and accessing them through class-level methods. It provides
    utility methods to manage and query objects of the same class without
    the need for external data structures.

    """
    _data: typing.MutableSet[typing.Self]
    _log: logging.Logger = logging.getLogger(__name__)

    def __init__(self):
        """
        Any initalised subclass adds itself to the data structure.
        """
        self._data.add(self)

    def __init_subclass__(cls):
        """
        Initialise the subclass, specifically the data structure holding the
        instances.
        """
        cls._data = set()

    def __class_getitem__(cls, name: str) -> typing.Self:
        return next(filter(lambda p: p.name == name, cls._data))

    @classmethod
    def len(cls) -> int:
        return len(cls._data)

    @classmethod
    def iter(cls) -> typing.Iterator[typing.Self]:
        return iter(cls._data)

    @classmethod
    def clear(cls):
        cls._data.clear()

    @abc.abstractmethod
    def __hash__(self) -> int:
        """
        If the underlying data is a set then a hash function is required. That
        hash function depends on the fields the class holds through, it must
        be defined in the subclass
        """
        pass



class IndexableClass(IndexableBaseClass):
    """
    An implementation
    """

    def __init__(self, name: str, uid: uuid.UUID = None):
        self._name = name
        self._uid = uid or uuid.uuid4()
        super().__init__()

    @property
    def uid(self) -> uuid.UUID:
        return self._uid

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name={self.name}, uid={self.uid})'

    def __hash__(self) -> int:
        """
        A hash function that considers an object uniquess by its unique identifier.

        Returns:
            hash over the unique identifier
        """
        return hash(self._uid)

