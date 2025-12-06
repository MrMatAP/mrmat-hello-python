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

import logging
from mhpython.indexable_classes import IndexableClass

logging.basicConfig(level=logging.DEBUG)


def test_single_indexable_class():
    IndexableClass.clear()
    person = IndexableClass('MrMat')
    assert person._uid is not None, 'Person has an UUID'
    assert person.name == 'MrMat', 'Person has a name'


def test_multiple_indexable_classes():
    IndexableClass.clear()
    people = ['MrMat', 'Eelyn', 'Jerome', 'Milena']
    for name in people:
        IndexableClass(name)

    assert IndexableClass.len() == len(people), f'There are {len(people)} people'
    assert IndexableClass['MrMat'] is not None, 'MrMat is a person'
    assert IndexableClass['MrMat'].name == 'MrMat', 'MrMat has a name'
    assert IndexableClass['Eelyn'].name == 'Eelyn', 'Eelyn has a name'

    for person in IndexableClass.iter():
        assert person.name in people, f'{person.name} is a person'
