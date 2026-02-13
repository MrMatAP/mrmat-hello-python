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
#

def can_greet(cls):
    """
    A class decorator injecting a greet method. Can be used for something interface-like (although that goes against
    the original Python Zen, which favours duck-typing
    """
    if 'greet' in vars(cls):
        raise TypeError(f'{cls.__name__} already defines greet()')

    def greet(self):
        return f'Hello {self.name}'

    # This works, cls.greet = greet
    setattr(cls, 'greet', greet)  # But this appears to be recommended

    return cls


@can_greet
class Greeting:
    """
    A class initialised with a name, decorated to receive a greet method
    """

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name
