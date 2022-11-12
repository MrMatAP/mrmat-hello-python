"""
Unittests for mhp.pictures
"""

import unittest
from mhpython.pictures.picturefile import PictureFile
import imagehash


class HashTest(unittest.TestCase):
    testpicdir = 'var/test-pictures/'

    def setUp(self):
        self.badger = PictureFile(self.testpicdir, 'badger.jpg')
        self.badger_duplicate = PictureFile(self.testpicdir, 'badger_duplicate.jpg')
        self.badger_rotated90 = PictureFile(self.testpicdir, 'badger_rotated90.jpg')
        self.badger_rotated180 = PictureFile(self.testpicdir, 'badger_rotated180.jpg')
        self.badger_rotated270 = PictureFile(self.testpicdir, 'badger_rotated270.jpg')
        self.badger_resized = PictureFile(self.testpicdir, 'badger_resized.jpg')

    def test_hashes(self):

        #
        # Calculate hashes

        hashes = {}
        for image in [('badger', self.badger),
                      ('badger_duplicate', self.badger_duplicate),
                      ('badger_rotated90', self.badger_rotated180),
                      ('badger_rotated180', self.badger_rotated180),
                      ('badger_rotated270', self.badger_rotated270),
                      ('badger_resized', self.badger_resized)]:
            hashes[image[0]] = {}
            hashes[image[0]]['ahash'] = imagehash.average_hash(image[1].im)
            hashes[image[0]]['dhash'] = imagehash.dhash(image[1].im)
            hashes[image[0]]['phash'] = imagehash.phash(image[1].im)
            hashes[image[0]]['whash'] = imagehash.whash(image[1].im)
            hashes[image[0]]['whashdb4'] = imagehash.whash(image[1].im, mode='db4')

        table = "{:<20} {:<16} {:<16} {:<16} {:<16} {:<16}"
        print(table.format("IMG", "ahash", "dhash", "phash", "whash", "whashdb4"))
        for key in sorted(hashes.keys()):
            print(table.format(key,
                               str(hashes[key]['ahash']),
                               str(hashes[key]['dhash']),
                               str(hashes[key]['phash']),
                               str(hashes[key]['whash']),
                               str(hashes[key]['whashdb4'])))
