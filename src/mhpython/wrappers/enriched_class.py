#  MIT License
#
#  Copyright (c) 2026 Mathieu Imfeld
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
#

import typing
import functools
import collections.abc

class Enricher:
    """
    A simple class to offer an interface for lookup up a key
    """

    def __init__(self, lookup_data: dict | None = None):
        self._lookup_data = lookup_data or dict()

    def lookup(self, key: str) -> str:
        return self._lookup_data[key]

T_Enricher = typing.TypeVar("T_Enricher", bound=Enricher)


def enriched_lookup(
    key: str | None = None,
) -> collections.abc.Callable[
    [collections.abc.Callable[["EnrichedBase[Enricher]"], str]],
    collections.abc.Callable[["EnrichedBase[Enricher]"], str],
]:
    """
    Decorator for property getters.

    If `key` is provided, the property's value is ignored and `self._enricher.lookup(key)`
    is returned.

    If `key` is None, the method name is used as the lookup key, and
    `self._enricher.lookup(func.__name__)` is returned.
    """

    def decorator(
        func: collections.abc.Callable[["EnrichedBase[Enricher]"], str],
    ) -> collections.abc.Callable[["EnrichedBase[Enricher]"], str]:
        @functools.wraps(func)
        def wrapper(self: "EnrichedBase[Enricher]") -> str:
            lookup_key = key if key is not None else func.__name__
            return self._enricher.lookup(lookup_key)

        # Optional: expose metadata for introspection/debugging
        wrapper._enriched_lookup_key = key  # type: ignore[attr-defined]
        return wrapper

    return decorator


class EnrichedBase(typing.Generic[T_Enricher]):
    """
    Base class for objects that can enrich properties via an Enricher instance.
    """

    def __init__(self, enricher: T_Enricher | None = None):
        self._enricher: T_Enricher = enricher or typing.cast(T_Enricher, Enricher())


T_EnrichedBase = typing.TypeVar("T_EnrichedBase", bound=EnrichedBase)


