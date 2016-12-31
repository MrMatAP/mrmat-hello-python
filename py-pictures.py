#!/usr/bin/env python

"""
py-pictures.py - A Python utility to sort out our pictures

Our various photo libraries are a total mess. We use this to
catalogue them.
"""

import argparse
import logging
import os
import shutil
import uuid
import datetime
import subprocess
import tqdm
from pprint import pprint

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mhp.pictures import Base, Picture

from fnmatch import fnmatch
from PIL import Image
from PIL.ExifTags import TAGS
import piexif


#
# Establish logging

logging.basicConfig(level=logging.WARN, format="%(levelname)s - %(message)s")
LOG = logging.getLogger(__name__)

#
# Parse arguments

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', help='Be chatty', action='store_true')
parser.add_argument('--debug', help='Be very chatty', action='store_true')
parser.add_argument('-d', '--directory', help='Directory', required=True)
parser.add_argument('-t', '--target', help='Target Directory', default='/Volumes/Pictures')
parser.add_argument('-a', '--action', help='Action', default='show')
options = parser.parse_args()
if options.verbose:
    LOG.setLevel(logging.INFO)
if options.debug:
    LOG.setLevel(logging.DEBUG)


def getuuid():
    return str(uuid.uuid4()).replace('-', '')


def action_check(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for file in filenames:
            if fnmatch(file.lower(), "*.jpg"):
                has_exif = False
                has_imageuniqueid = False

                im = Image.open(os.path.join(dirpath, file))
                info = im.info
                if 'exif' in info:
                    has_exif = True
                    exif_dict = piexif.load(info['exif'])
                    if 'Exif' in exif_dict:
                        if piexif.ExifIFD.ImageUniqueID in exif_dict['Exif']:
                            has_imageuniqueid = True

                print("{: <20}: {!r: <5} {!r: <5}".format(file, has_exif, has_imageuniqueid))


def action_show(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for file in filenames:
            if fnmatch(file.lower(), "*.jpg"):
                im = Image.open(os.path.join(dirpath, file))
                rawexif = im._getexif()
                exif = {}
                for (k, v) in rawexif.items():
                    exif[TAGS.get(k)] = v

                imageuniqueid = exif['ImageUniqueID'] if 'ImageUniqueID' in exif else 'N/A'
                dateTimeOriginal = exif['DateTimeOriginal'] if 'DateTimeOriginal' in exif else 'N/A'
                dateTimeDigitized = exif['DateTimeDigitized'] if 'DateTimeDigitzed' in exif else 'N/A'

                print("{: <20}: {} {} {}".format(file, imageuniqueid, dateTimeOriginal, dateTimeDigitized))


def action_import(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for file in filenames:
            if fnmatch(file.lower(), "*.jpg"):
                im = Image.open(os.path.join(dirpath, file))
                info = im.info
                exif_dict = {}
                if 'exif' in info:
                    exif_dict = piexif.load(info['exif'])
                    if 'Exif' not in exif_dict:
                        exif_dict['Exif'] = {}
                    if piexif.ExifIFD.ImageUniqueID not in exif_dict['Exif']:
                        exif_dict['Exif'][piexif.ExifIFD.ImageUniqueID] = getuuid()
                else:
                    exif_dict['Exif'] = {}
                    exif_dict['Exif'][piexif.ExifIFD.ImageUniqueID] = getuuid()

                imageuniqueid = exif_dict['Exif'][piexif.ExifIFD.ImageUniqueID]
                if type(imageuniqueid) is bytes:
                    imageuniqueid = imageuniqueid.decode()
                exif_bytes = piexif.dump(exif_dict)
                im.save(os.path.join(dirpath, file), "jpeg", exif=exif_bytes)

                pic = Picture(imageuniqueid=imageuniqueid, originalpath=dirpath, originalname=file)
                session.add(pic)

                #
                # TODO: Must capture the file creation time here

                shutil.move(os.path.join(directory, file), os.path.join(options.target, imageuniqueid + '.jpg'))
                session.commit()

                print("{: <20}: {}".format(file, imageuniqueid))


def action_updatedb(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for file in filenames:
            if fnmatch(file.lower(), "*.jpg"):
                im = Image.open(os.path.join(dirpath, file))
                info = im.info
                exif_dict = piexif.load(info['exif'])
                imageuniqueid = exif_dict['Exif'][piexif.ExifIFD.ImageUniqueID].decode()

                pic = session.query(Picture).filter(Picture.imageuniqueid == imageuniqueid).one()
                if not pic:
                    LOG.error("Unable to find picture with ImageUniqueID {}".format(imageuniqueid))
                    continue

                dateTimeOriginal = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] if piexif.ExifIFD.DateTimeOriginal in exif_dict['Exif'] else None
                dateTimeDigitized = exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] if piexif.ExifIFD.DateTimeDigitized in exif_dict['Exif'] else None

                if dateTimeOriginal:
                    pic.datetimeoriginal = datetime.datetime.strptime(dateTimeOriginal.decode(), "%Y:%m:%d %H:%M:%S")
                if dateTimeDigitized:
                    pic.datetimedigitized = datetime.datetime.strptime(dateTimeDigitized.decode(), "%Y:%m:%d %H:%M:%S")
                session.commit()

                print("{: <20}: {} {}".format(file, pic.datetimeoriginal, pic.datetimedigitized))


def action_updatecreationtime(directory):

    #
    # Update the creation time from data stored in the database

    for pic in session.query(Picture).filter(Picture.datetimeoriginal.isnot(None)).all():
        f = os.path.join(directory, pic.imageuniqueid + '.jpg')
        creationtime = pic.datetimeoriginal.strftime("%m/%d/%Y %H:%M:%S")
        subprocess.run(['SetFile', '-d', "'" + creationtime + "'", f], check=True)
        print("{: <20}: {}".format(f, creationtime))


def action_updateexif(directory):

    #
    # Update the EXIF data from the database

    for pic in tqdm.tqdm(session.query(Picture).all()):
        f = os.path.join(directory, pic.imageuniqueid + '.jpg')
        im = Image.open(f)
        info = im.info
        exif_dict = piexif.load(info['exif'])

        dirty = False

        if pic.datetimeoriginal and piexif.ExifIFD.DateTimeOriginal not in exif_dict['Exif']:
            dateTimeOriginal = pic.datetimeoriginal.strftime("%Y:%m:%d %H:%M:%S").encode()
            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = dateTimeOriginal
            print("{: <20}: DateTimeOriginal {}".format(f, dateTimeOriginal))
            dirty = True

        if pic.datetimedigitized and piexif.ExifIFD.DateTimeDigitized not in exif_dict['Exif']:
            dateTimeDigitized = pic.datetimedigitized.strftime("%Y:%m:%d %H:%M:%S").encode()
            exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = dateTimeDigitized
            print("{: <20}: DateTimeDigitized {}".format(f, dateTimeDigitized))
            dirty = True

        if dirty:
            exif_bytes = piexif.dump(exif_dict)
            im.save(f, "jpeg", exif=exif_bytes)


#
# Main script

try:

    #
    # Make sure the source and target directories do exist before continuing

    if not os.path.exists(options.directory) or not os.path.isdir(options.directory):
        LOG.fatal("Directory {} does not exist".format(options.directory))
        exit(1)

    #
    # Connect to the database

    LOG.info("Connecting to the database")
    engine = create_engine('postgresql+psycopg2://pictures:pictures@infra.bobeli.org:15432/infradb', echo=False)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    Base.metadata.create_all(engine)

    if options.action == 'show':
        action_show(options.directory)

    elif options.action == 'check':
        action_check(options.directory)

    elif options.action == 'import':
        if not os.path.exists(options.target) or not os.path.isdir(options.target):
            LOG.fatal("Target path {} does not exist".format(options.target))
            exit(1)
        action_import(options.directory)

    elif options.action == 'updatedb':
        action_updatedb(options.directory)

    elif options.action == 'updatecreationtime':
        action_updatecreationtime(options.directory)

    elif options.action == 'updateexif':
        action_updateexif(options.directory)

    else:
        LOG.fatal('Invalid Action')
        exit(1)


except Exception as ex:
    LOG.fatal('{} - {}'.format(type(ex), ex))
else:
    LOG.debug('No exception occurred within the code block')
finally:
    LOG.debug('The finally block is always executed')
