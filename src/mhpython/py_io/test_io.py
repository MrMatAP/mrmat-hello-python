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
        self.sample_text = 'Hi there, I am a fake constant in the IO unit test'
        self.sample_text_file = 'io-unittest.txt'
        if os.path.isfile(self.sample_text_file):
            os.unlink(self.sample_text_file)

        self.sample_dict = {'foo': 1, 'bar': 'two', 'baz': [1, 'quux', 'quz']}
        self.sample_json_file = 'io-unittest.json'
        if os.path.isfile(self.sample_json_file):
            os.unlink(self.sample_json_file)

    def tearDown(self):
        if os.path.isfile(self.sample_text_file):
            os.unlink(self.sample_text_file)

    def test_can_persist_simple_text(self):
        with open(self.sample_text_file, 'w', encoding='UTF-8') as f:
            f.write(self.sample_text)
        with open(self.sample_text_file, 'r', encoding='UTF-8') as g:
            text = g.readline()
        self.assertEqual(self.sample_text, text, 'The text read from the file is the same as we wrote')

    def test_can_persist_json(self):
        with open(self.sample_json_file, 'w', encoding='UTF-8') as f:
            json.dump(self.sample_dict, f)
        with open(self.sample_json_file, 'r', encoding='UTF-8') as g:
            j = json.load(g)
        self.assertEqual(self.sample_dict, j, 'The JSON read from the file is the same as we wrote')
        pprint(j)


if __name__ == '__main__':
    unittest.main()
