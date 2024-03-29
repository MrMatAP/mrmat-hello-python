
#  MIT License
#
#  Copyright (c) 2022 Mathieu Imfeld
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

import pytest


def test_list_type():
    simple_list = ['one', 'two', 'three']
    assert type(simple_list) is list, 'The type of a list is "list"'

    empty_list = []
    assert type(empty_list) is list, 'An empty list is also a list'

    str_list_direct = 'spam'
    assert type(str_list_direct) is str, 'A string is also a list'
    assert str_list_direct[0] == 's', 'Characters in a simple string can be extracted using their index'
    with pytest.raises(AttributeError) as excinfo:
        str_list_direct.pop()
        assert "'str' object has no attribute 'pop'" in str(excinfo.value), \
            'But we cannot use the list-specific methods'

    str_list = list('spam')
    assert type(str_list) is list, 'We can also cast a string to be a list'
    assert str_list[0] == 's', 'Characters can still be extracted using their index'
    assert str_list.pop() == 'm', 'The list-specific methods are now available'


def test_list_mixed():
    mixed_list = ['one', 2, 'three']
    assert type(mixed_list) is list, 'A list can contain mixed types'
    assert type(mixed_list[0]) is str, 'The first element of the list is a string'
    assert type(mixed_list[1]) is int, 'The second element of the list is an integer'
    assert type(mixed_list[2]) is str, 'The third element of the list is a string'


def test_list_nested():
    nested_list = ['one', ['a', 'b', 'c'], {'foo': 'bar'}]
    assert type(nested_list[1]) is list, 'Lists can be nested'
    assert type(nested_list[2]) is dict, 'A dict can be nested in a list too'
    assert nested_list[2]['foo'] == 'bar', 'We can access the nested dict element using literal values'
    key = 'foo'
    assert nested_list[2][key] == 'bar', 'We can access the nested dict element using variable values'


def test_list_comprehension():
    base_list = ['foo', 'bar', 'baz']
    comprehended_list = [e for e in base_list]
    assert comprehended_list == base_list, 'The comprehended list is the same as the base list'
    filtered_list = [e for e in base_list if e == 'bar']
    assert filtered_list == ['bar'], 'The filtered list consists of the single filtered element'
    filtered_list = [e for e in base_list if e in ['foo', 'bar']]
    assert filtered_list == ['foo', 'bar'], 'The filtered list consists of the range of filtered elements'
    filtered_list = [e for e in base_list if e in ['bar', 'foo']]
    assert filtered_list == ['foo', 'bar'], 'The filtered list consists of the range of unordered filtered elements'
    filtered_list = [e for e in base_list if e in ['quuz']]
    assert filtered_list == [], 'The filtered list contains no element if there was no match of the filtered elements'

    mapped_list = list(map(lambda e: e[::-1], base_list))   # Note the interesting trick for reversing a string
    assert mapped_list == ['oof', 'rab', 'zab'], 'The mapped list contains elements passed through a lambda'

