"""
Unittests for mhp.pictures
"""

import unittest
from mhp.pictures import PictureFile
import imagehash


class HashTest(unittest.TestCase):
    def setUp(self):
        self.a = PictureFile('/Users/imfeldma/Desktop/test-pictures/', 'a.jpg')
        self.a_duplicate = PictureFile('/Users/imfeldma/Desktop/test-pictures', 'a_duplicate.jpg')
        self.a_rotated90 = PictureFile('/Users/imfeldma/Desktop/test-pictures', 'a_rotated90.jpg')
        self.a_rotated180 = PictureFile('/Users/imfeldma/Desktop/test-pictures', 'a_rotated180.jpg')
        self.a_rotated270 = PictureFile('/Users/imfeldma/Desktop/test-pictures', 'a_rotated270.jpg')
        self.a_resized = PictureFile('/Users/imfeldma/Desktop/test-pictures', 'a_resized.jpg')

    def test_hashes(self):

        #
        # Calculate hashes

        hashes = {}
        for image in [('a', self.a),
                      ('a_duplicate', self.a_duplicate),
                      ('a_rotated90', self.a_rotated180),
                      ('a_rotated180', self.a_rotated180),
                      ('a_rotated270', self.a_rotated270),
                      ('a_resized', self.a_resized)]:
            hashes[image[0]] = {}
            hashes[image[0]]['ahash'] = imagehash.average_hash(image[1].im)
            hashes[image[0]]['dhash'] = imagehash.dhash(image[1].im)
            hashes[image[0]]['phash'] = imagehash.phash(image[1].im)
            hashes[image[0]]['whash'] = imagehash.whash(image[1].im)
            hashes[image[0]]['whashdb4'] = imagehash.whash(image[1].im, mode='db4')

        table = "{:<12} {:<16} {:<16} {:<16} {:<16} {:<16}"
        print(table.format("IMG", "ahash", "dhash", "phash", "whash", "whashdb4"))
        for key in sorted(hashes.keys()):
            print(table.format(key,
                               str(hashes[key]['ahash']),
                               str(hashes[key]['dhash']),
                               str(hashes[key]['phash']),
                               str(hashes[key]['whash']),
                               str(hashes[key]['whashdb4'])))
