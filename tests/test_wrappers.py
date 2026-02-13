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

import mhpython.wrappers

def test_inversion():

    @mhpython.wrappers.inversion
    def return_true():
        return True

    @mhpython.wrappers.inversion
    def return_false():
        return False

    assert not return_true()
    assert return_false()


def test_enriched_lookup():
    # Test with explicit key
    enricher = mhpython.wrappers.Enricher({"custom_key": "custom_value"})

    class TestClass(mhpython.wrappers.EnrichedBase):
        @mhpython.wrappers.enriched_lookup(key="custom_key")
        def some_property(self):
            pass

    obj = TestClass(enricher)
    assert obj.some_property() == "custom_value"

    # Test with method name as key
    enricher2 = mhpython.wrappers.Enricher({"another_property": "method_name_value"})

    class TestClass2(mhpython.wrappers.EnrichedBase):
        @mhpython.wrappers.enriched_lookup()
        def another_property(self):
            pass

    obj2 = TestClass2(enricher2)
    assert obj2.another_property() == "method_name_value"
