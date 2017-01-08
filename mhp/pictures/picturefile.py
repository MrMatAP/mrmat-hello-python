import os
import uuid
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import piexif
import imagehash


class PictureFile:

    def get_imageuniqueid(self):
        if type(self.exif_dict_raw['Exif'][piexif.ExifIFD.ImageUniqueID]) is bytes:
            return self.exif_dict_raw['Exif'][piexif.ExifIFD.ImageUniqueID].decode()
        return self.exif_dict_raw['Exif'][piexif.ExifIFD.ImageUniqueID]

    def parse(self):
        exif_dict_parsed = {}
        for key in self.exif_dict_raw:
            exif_dict_parsed[key] = {}
        for key in ['0th', '1st', 'Exif']:
            for (k, v) in self.exif_dict_raw[key].items():
                exif_dict_parsed[key][TAGS[k]] = v.decode() if type(v) is bytes else v
        return exif_dict_parsed

    def save(self):
        if not self.dirty:
            return
        exif_bytes = piexif.dump(self.exif_dict_raw)
        self.im.save(self.file, "jpeg", exif=exif_bytes)

    def __init__(self, d, f):
        self.file = os.path.join(d, f)
        self.im = Image.open(self.file)

        self.exif_dict_raw = {}
        self.exif_dict_parsed = {}
        self.dirty = False

        stat = os.stat(self.file)
        self.datetimecreated = datetime.fromtimestamp(stat.st_birthtime)
        self.datetimemodified = datetime.fromtimestamp(stat.st_mtime)
        self.datetimeaccessed = datetime.fromtimestamp(stat.st_atime)

        # It is likely going to be more efficient to calculate this only when required
        # self.ahash = imagehash.average_hash(self.im)
        # self.phash = imagehash.phash(self.im)
        # self.dhash = imagehash.dhash(self.im)
        # self.whashhaar = imagehash.whash(self.im)
        # self.whashdb4 = imagehash.whash(self.im, mode='db4')

        if 'exif' not in self.im.info:
            self.exif_dict_raw['Exif'] = {}
            self.exif_dict_raw['Exif'][piexif.ExifIFD.ImageUniqueID] = str(uuid.uuid4()).replace('-', '')
            self.exif_dict_raw['Exif'][piexif.ExifIFD.DateTimeOriginal] = self.datetimecreated.strftime("%Y:%m:%d %H:%M:%S").encode()
            self.exif_dict_raw['Exif'][piexif.ExifIFD.DateTimeDigitized] = self.datetimecreated.strftime("%Y:%m:%d %H:%M:%S").encode()
            self.exif_dict_raw['Exif'][40962] = self.im.size[0]
            self.exif_dict_raw['Exif'][40963] = self.im.size[1]
            self.dirty = True
        else:
            self.exif_dict_raw = piexif.load(self.im.info['exif'])

            if piexif.ExifIFD.ImageUniqueID not in self.exif_dict_raw['Exif']:
                self.exif_dict_raw['Exif'][piexif.ExifIFD.ImageUniqueID] = str(uuid.uuid4()).replace('-', '')
                self.dirty = True
            if piexif.ExifIFD.DateTimeOriginal not in self.exif_dict_raw['Exif']:
                self.exif_dict_raw['Exif'][piexif.ExifIFD.DateTimeOriginal] = self.datetimecreated.strftime(
                    "%Y:%m:%d %H:%M:%S").encode()
                self.dirty = True
            if piexif.ExifIFD.DateTimeDigitized not in self.exif_dict_raw['Exif']:
                self.exif_dict_raw['Exif'][piexif.ExifIFD.DateTimeDigitized] = self.datetimecreated.strftime(
                    "%Y:%m:%d %H:%M:%S").encode()
                self.dirty = True
            if piexif.ExifIFD.PixelXDimension not in self.exif_dict_raw['Exif'] or self.exif_dict_raw['Exif'][piexif.ExifIFD.PixelXDimension] != self.im.size[0]:
                self.exif_dict_raw['Exif'][piexif.ExifIFD.PixelXDimension] = self.im.size[0]
                self.dirty = True
            if piexif.ExifIFD.PixelYDimension not in self.exif_dict_raw['Exif'] or self.exif_dict_raw['Exif'][piexif.ExifIFD.PixelYDimension] != self.im.size[1]:
                self.exif_dict_raw['Exif'][piexif.ExifIFD.PixelYDimension] = self.im.size[1]
                self.dirty = True


