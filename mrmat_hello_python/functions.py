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

import sys


def function_with_extra_args(simple: str, *args):
    """
    A star argument comes across as a tuple for all remaining attibutes
    """
    print('function_with_extra_args:')
    print(f'Simple   = {type(simple)}')
    print(f'*args    = {type(args)}')


def function_with_extra_kwargs(simple: str, **kwargs):
    """
    A double-star argument comes across as a dict and it only accepts named attributes.
    Note that it is not required to be called kwargs
    """
    print('function_with_extra_kwargs:')
    print(f'Simple   = {type(simple)}')
    print(f'*kwargs    = {type(kwargs)}')


def function_with_all_three(simple: str, *args, **kwargs):
    """
    All three can be combined, but order matters. args must come before kwargs. ** parameters MUST come after *params
    """
    print('function_with_all_three:')
    print(f'Simple   = {type(simple)}')
    print(f'*args    = {type(args)} [{len(args)}]')
    print(f'*kwargs    = {type(kwargs)} [{len(kwargs)}]')


if __name__ == '__main__':
    function_with_extra_args('foo', 1, 2, 3, 4, 5, 'baz')
    function_with_extra_kwargs('foo', bar='baz', quz='quux')
    function_with_all_three('foo', 1, 2, 3, 4, 5, bar='baz', quz='quux')
    sys.exit(0)
