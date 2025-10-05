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

from mhpython.functions import (
    function_with_extra_args,
    function_with_extra_kwargs,
    function_with_all_three,
)


def test_function_extra_args():
    (out_simple, out_args) = function_with_extra_args("foo", 1, 2, 3, "baz")
    assert out_simple == "foo"
    assert isinstance(
        out_args, tuple
    ), "*args arrives as a tuple in the function"
    assert out_args == (1, 2, 3, "baz")


def test_function_extra_kwargs():
    (out_simple, out_kwargs) = function_with_extra_kwargs(
        "foo", bar=1, qux="quuz"
    )
    assert out_simple == "foo"
    assert isinstance(
        out_kwargs, dict
    ), "**kwargs arrives as a dict in the function"
    assert out_kwargs == dict(bar=1, qux="quuz")


def test_function_with_all_three():
    (out_simple, out_args, out_kwargs) = function_with_all_three(
        "foo", 1, 2, 3, "baz", bar=1, qux="quuz"
    )
    assert out_simple == "foo"
    assert isinstance(
        out_args, tuple
    ), "*args arrives as a tuple in the function"
    assert isinstance(
        out_kwargs, dict
    ), "**kwargs arrives as a dict in the function"
    assert out_args == (1, 2, 3, "baz")
    assert out_kwargs == dict(bar=1, qux="quuz")
