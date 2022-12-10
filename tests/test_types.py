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

from dataclasses import dataclass, FrozenInstanceError


@dataclass(frozen=True)
class ImmutableName:
    name: str


class Name:
    """A class that is ignorant about equality"""
    def __init__(self, name: str):
        self.name = name


class EqName(Name):
    """A class that knows about its equality"""
    def __eq__(self, other):
        return other.name == self.name

    def __hash__(self):
        return self.name.__hash__()


def test_sets():
    s1 = {'foo', 'bar', 'baz'}
    assert s1 == {'foo', 'bar', 'baz'}

    try:
        e1 = s1[0]
    except TypeError:
        assert True, 'sets cannot be iterated over'

    # Sets can contain objects that are ignorant about their hash equality
    try:
        s2 = {Name(n) for n in ['Mat', 'Eelyn', 'Mr Tree', 'Badgie']}
        for e in s2:
            e.name = 'Someone'
    except ValueError:
        assert False, 'sets should be able to contain objects that are ignorant about equality'
    else:
        assert True, 'sets can contain objects that are ignorant about equality'

    # TODO: Don't understand why this is possible. It ignores equality
    # try:
    #     s3 = {EqName(n) for n in ['Mat', 'Eelyn', 'Mr Tree', 'Badgie']}
    #     for e in s3:
    #         e.name = 'Someone'
    # except ValueError:
    #     assert True, 'sets cannot contain objects that are aware about equality'
    # else:
    #     assert False, 'sets should not contain objects that are aware about equality'

    try:
        s4 = {ImmutableName('Mat'), ImmutableName('Eelyn'), ImmutableName('Mr Tree'), ImmutableName('Badgie')}
        for e in s4:
            e.name = 'Jerome'
    except FrozenInstanceError:
        assert True, 'set elements must not be mutable'
    else:
        assert False, 'set elements cannot have objects aware about hash equality'
