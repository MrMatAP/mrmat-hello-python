#!/usr/bin/env python

"""
py-pg-to-mongo.py - A Python script to pull data from a PostgreSQL table towards Mongo
"""

import argparse
import logging
import concurrent.futures

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

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


def mgupload(offset, limit):
    print("Dealing with chunk at offset %s" % offset)
    localsession = Session()
    for person in localsession.query(PGPerson).limit(limit).offset(offset):

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

    Session.remove()


def run():
    try:

        #
        # Initialize SQLAlchemy for PG

        LOG.info("Connecting to PG")
        engine = create_engine('postgresql+psycopg2://hr:hr@infra.bobeli.org:15432/infradb', echo=False)
        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)

        #
        # Initialize MongoEngine

        LOG.info("Connecting to Mongo")
        connect('hr', host="infra.bobeli.org")

        #
        # Establish the number of people we will upload per thread

        topsession = Session()
        peoplecount = topsession.query(PGPerson).limit(10000).count()
        perthread = peoplecount / 5
        print("Will upload %s people per thread to a calculated total of %s and actual total %s" %
              (perthread, perthread * 5, peoplecount))
        Session.remove()

        LOG.info("Defining people")
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:

            future_to_chunk = {executor.submit(mgupload(offset * perthread, perthread)): offset for offset in range(0, 5)}
            for future in concurrent.futures.as_completed(future_to_chunk):
                chunk = future_to_chunk[future]
                print("chunk %s has completed" % chunk)

    except Exception as ex:
        LOG.fatal('{} - {}'.format(type(ex), ex))
    else:
        LOG.debug('No exception occurred within the code block')
    finally:
        LOG.debug('The finally block is always executed')


if __name__ == '__main__':
    run()
