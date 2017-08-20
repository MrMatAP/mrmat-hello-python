#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mhpython.orm.sqlorm import SQLORMDao, SQLORMBloodType, SQLORMPerson, SQLORMTitle, SQLORMGender


def test_basic_sqlalchemy():
    dao = SQLORMDao('sqlite:///build/sqlorm.db')
    assert dao is not None
    session = dao.session()
    assert session is not None

    blood_type = SQLORMBloodType(name='B')
    assert blood_type.id is None, 'blood type id is None before persisting it'
    session.add(blood_type)
    session.commit()
    assert blood_type.id is not None, 'blood type id is populated after persisting it'

    person = SQLORMPerson(
        givenname='Mathieu',
        middleinitial='M',
        surname='Imfeld',
        streetaddress='70 Dakota Crescent',
        zipcode='399940',
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
        gender=SQLORMGender(name='male'),
        bloodtype=SQLORMBloodType(name='A'),
        title=SQLORMTitle(name='Mr')
    )
    session.add(person)
    session.commit()
