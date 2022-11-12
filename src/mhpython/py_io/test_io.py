"""
Unittests for Python IO
"""

import unittest
import os
import json
from pprint import pprint


class IO(unittest.TestCase):
    """
    There are no constants in Python
    """

    def setUp(self):
        self.SAMPLETEXT = 'Hi there, I am a fake constant in the IO unit test'
        self.SAMPLETEXTFILE = 'io-unittest.txt'
        if os.path.isfile(self.SAMPLETEXTFILE):
            os.unlink(self.SAMPLETEXTFILE)

        self.SAMPLEDICT = { 'foo': 1, 'bar': 'two', 'baz': [ 1, 'quux', 'quz']}
        self.SAMPLEJSONFILE = 'io-unittest.json'
        if os.path.isfile(self.SAMPLEJSONFILE):
            os.unlink(self.SAMPLEJSONFILE)

    def tearDown(self):
        if os.path.isfile(self.SAMPLETEXTFILE):
            os.unlink(self.SAMPLETEXTFILE)

    def test_can_persist_simple_text(self):
        f = open(self.SAMPLETEXTFILE, 'w')
        f.write(self.SAMPLETEXT)
        f.close()

        g = open(self.SAMPLETEXTFILE, 'r')
        text = g.readline()
        g.close()

        self.assertEqual(self.SAMPLETEXT, text, 'The text read from the file is the same as we wrote')

    def test_can_persist_json(self):
        f = open(self.SAMPLEJSONFILE, 'w')
        json.dump(self.SAMPLEDICT, f)
        f.close()

        g = open(self.SAMPLEJSONFILE, 'r')
        j = json.load(g)
        g.close()

        self.assertEqual(self.SAMPLEDICT, j, 'The JSON read from the file is the same as we wrote')
        pprint(j)


if __name__ == '__main__':
    unittest.main()
