#!/usr/bin/env python

"""
py-pg-to-mongo.py - A Python script to pull data from a PostgreSQL table towards Mongo
"""

import argparse
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mhporm.pg import PGPerson, PGCity, PGCompany

from mongoengine import connect, DoesNotExist
from mhporm.mg import MGPerson, MGCity, MGCompany, MGOccupation

#
# Establish logging

logging.basicConfig(level=logging.WARN, format="%(levelname)s - %(message)s")
LOG = logging.getLogger(__name__)

#
# Parse arguments

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', help='Be chatty', action='store_true')
parser.add_argument('--debug', help='Be very chatty', action='store_true')
options = parser.parse_args()
if options.verbose:
    LOG.setLevel(logging.INFO)
if options.debug:
    LOG.setLevel(logging.DEBUG)

try:

    #
    # Initialize SQLAlchemy for PG

    LOG.info("Connecting to PG")
    engine = create_engine('postgresql+psycopg2://hr:hr@infra.bobeli.org:15432/infradb', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    print("Number of people : %s" % session.query(PGPerson).count())

    #
    # Initialize MongoEngine

    LOG.info("Connecting to Mongo")
    connect('hr', host="infra.bobeli.org")

    LOG.info("Defining people")
    for person in session.query(PGPerson).limit(100).offset(100):

        #
        # Ensure we have a city defined

        try:
            city = MGCity.objects(
                name=person.city.name,
                state=person.city.state,
                country=person.city.country.name,
                code=person.city.country.code
            ).get()
        except DoesNotExist:
            city = MGCity(
                name=person.city.name,
                state=person.city.state,
                country=person.city.country.name,
                code=person.city.country.code
            ).save()
            print("Created city %s" % city.name)

        #
        # Ensure we have a company defined

        try:
            company = MGCompany.objects(
                name=person.company.name
            ).get()
        except DoesNotExist:
            company = MGCompany(
                name=person.company.name
            ).save()
            print("Created company %s" % company.name)

        #
        # Ensure we have an occupation defined

        try:
            occupation = MGOccupation.objects(
                name=person.occupation.name
            ).get()
        except DoesNotExist:
            occupation = MGOccupation(
                name=person.occupation.name
            ).save()
            print("Created occupation %s" % occupation.name)

        #
        # Define the person unless it already exists

        try:
            person = MGPerson.objects(
                guid=person.guid
            ).get()
        except DoesNotExist:
            person = MGPerson(
                givenname=person.givenname,
                middleinitial=person.middleinitial,
                streetaddress=person.streetaddress,
                surname=person.surname,
                zipcode=person.zipcode,
                emailaddress=person.emailaddress,
                username=person.username,
                password=person.password,
                telephonenumber=person.telephonenumber,
                maidenname=person.maidenname,
                birthday=person.birthday,
                ccnumber=person.ccnumber,
                cvv2=person.cvv2,
                ccexpires=person.ccexpires,
                nationalid=person.nationalid,
                upstracking=person.upstracking,
                vehicle=person.vehicle,
                domain=person.domain,
                kilograms=person.kilograms,
                centimeters=person.centimeters,
                latitude=person.latitude,
                longitude=person.longitude,
                guid=person.guid,

                gender=person.gender.name,
                bloodtype=person.bloodtype.name,
                title=person.title.name,
                cctype=person.cctype.name,
                city=city,
                company=company,
                occupation=occupation
            ).save()
            print("Created person %s %s %s" % (person.givenname, person.middleinitial, person.surname))

except Exception as ex:
    LOG.fatal('{} - {}'.format(type(ex), ex))
else:
    LOG.debug('No exception occurred within the code block')
finally:
    LOG.debug('The finally block is always executed')
