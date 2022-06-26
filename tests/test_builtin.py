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
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#

"""
Tests for builtin Python functions
"""

int_array = [1, 2, 3, 101, 102, 103]
dict_array = [
    dict(id=1, name='one'),
    dict(id=2, name='two'),
    dict(id=3, name='three'),
    dict(id=101, name='one-hundred-and-one'),
    dict(id=102, name='one-hundred-and-two'),
    dict(id=103, name='one-hundred-and-three')
]


def test_filter_integers():
    """
    We can filter on a simple array of integers, but must remember to resolve the returned generator as a list
    """
    filtered_list = list(filter(lambda _: _ < 100, int_array))
    assert filtered_list == [1, 2, 3]


def test_filter_generator():
    """
    We can also use the filter on a simple array and use the returned generator directly
    """
    filtered_generator = filter(lambda _: _ < 100, int_array)
    assert isinstance(filtered_generator, filter)
    for entry in filtered_generator:
        assert entry < 100


def test_filter_complex():
    filtered_list = list(filter(lambda _: _.get('id') < 100, dict_array))
    assert len(filtered_list) == 3

