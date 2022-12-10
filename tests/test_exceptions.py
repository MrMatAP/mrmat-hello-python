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


def test_exception_with_finally():
    handled_in_except = False
    handled_in_else = False
    handled_in_finally = False
    try:
        raise ValueError()
    except ValueError:
        handled_in_except = True
    else:
        # The else block is executed when no exception was raised in the try block
        # IDEA is clever enough to understand that this code is unreachable
        handled_in_else = True
    finally:
        # The finally block is executed in all cases
        handled_in_finally = True

    assert handled_in_except
    assert not handled_in_else
    assert handled_in_finally


def test_exception_with_else():
    handled_in_except = False
    handled_in_else = False
    handled_in_finally = False
    try:
        # We run without problem
        pass
    except ValueError:
        handled_in_except = True
    else:
        # The else block is executed when no exception was raised in the try block
        handled_in_else = True
    finally:
        # The finally block is executed in all cases
        handled_in_finally = True

    assert not handled_in_except
    assert handled_in_else
    assert handled_in_finally
