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
        title='Mr'
    )
    person1.gender(session, 'male')
    person1.bloodtype(session, 'A')
    session.add(person1)
    session.commit()

    #
    # Now add a second person with the same blood type

    person2 = SQLORMPerson(
        givenname='Eelyn',
        surname='Chen-Imfeld',
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
        title='Mrs'
    )
    person2.gender(session, 'female')
    person2.bloodtype(session, 'A')
    session.add(person2)
    session.commit()

    bloodtypes = session.query(SQLORMBloodType).filter(SQLORMBloodType.name.is_('A')).all()
    for bt in bloodtypes:
        people = bt.people_rel
        for p in people:
            print("{}: {}".format(bt.name, p.givenname))
