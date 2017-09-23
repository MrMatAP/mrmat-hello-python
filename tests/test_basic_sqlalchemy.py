#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import os
from mhpython.orm.sqlorm import SQLORMDao, SQLORMPerson, SQLORMGender, SQLORMBloodType, SQLORMCCType, SQLORMCompany, \
    SQLORMOccupation, SQLORMCity, SQLORMCountry


@pytest.fixture
def dao():
    if os.path.isfile('build/sqlorm.db'):
        os.unlink('build/sqlorm.db')
    return SQLORMDao('sqlite:///build/sqlorm.db')


def test_unique_attrs(dao):
    """
    Create two people with the same attributes in the database and check
    that the same attribute is only created exactly once.
    :param dao: The DAO object from the fixture
    :return: None
    """
    assert dao is not None
    session = dao.session()
    assert session is not None

    person1 = SQLORMPerson(
        givenname='Mathieu',
        middleinitial='M',
        surname='Imfeld',
        streetaddress='70 Dakota Crescent',
        zipcode='399944',
        emailaddress='foo@bar.com',
        username='mrmat',
        password='blah',
        telephonenumber='+65 9854 1234',
        ccnumber='4901 1101 1234 5637',
        cvv2='123',
        nationalid='S123456',
        domain='bobeli.org',
        kilograms='70',
        centimeters='174',
    )
    person1.gender(session, 'male')
    person1.bloodtype(session, 'A')
    person1.title(session, 'Mr')
    person1.cctype(session, 'VISA')
    person1.company(session, 'UBS')
    person1.occupation(session, 'IT')
    person1.city(session, 'Singapore', 'Dakota', 'Singapore', 'SG')
    session.add(person1)

    person2 = SQLORMPerson(
        givenname='Damian',
        surname='Prinzing',
        streetaddress='70 Dakota Crescent',
        zipcode='399944',
        emailaddress='eelync@bar.com',
        username='eelync',
        password='blah2',
        telephonenumber='+65 9854 1235',
        ccnumber='4901 1101 1234 5638',
        cvv2='124',
        nationalid='S123453',
        domain='swissotter.org',
        kilograms='69',
        centimeters='160',
    )
    person2.gender(session, 'male')
    person2.bloodtype(session, 'A')
    person2.title(session, 'Mr')
    person2.cctype(session, 'VISA')
    person2.company(session, 'UBS')
    person2.occupation(session, 'IT')
    person2.city(session, 'Singapore', 'Dakota', 'Singapore', 'SG')
    session.add(person2)

    session.commit()

    assert session.query(SQLORMPerson).count() == 2
    assert session.query(SQLORMGender).count() == 1
    assert session.query(SQLORMBloodType).count() == 1
    assert session.query(SQLORMCCType).count() == 1
    assert session.query(SQLORMCompany).count() == 1
    assert session.query(SQLORMOccupation).count() == 1
    assert session.query(SQLORMCity).count() == 1
    assert session.query(SQLORMCountry).count() == 1

    gender = session.query(SQLORMGender).one()
    assert len(gender.people_rel) == 2

    bloodtype = session.query(SQLORMBloodType).one()
    assert len(bloodtype.people_rel) == 2

    cctype = session.query(SQLORMCCType).one()
    assert len(cctype.people_rel) == 2

    company = session.query(SQLORMCompany).one()
    assert len(company.people_rel) == 2

    occupation = session.query(SQLORMOccupation).one()
    assert len(occupation.people_rel) == 2

    city = session.query(SQLORMCity).one()
    assert len(city.people) == 2

    assert city.country is not None
    assert len(city.country_rel.cities_rel) == 1
    assert city.country_rel.name == 'Singapore'
