from mongoengine import *
from .mgcity import MGCity
from .mgcompany import MGCompany
from .mgoccupation import MGOccupation


class MGPerson(Document):
    meta = {'collection': 'people'}

    givenname = StringField(required=True)
    middleinitial = StringField(required=True)
    surname = StringField(required=True)
    streetaddress = StringField()
    zipcode = StringField()
    emailaddress = StringField()
    username = StringField()
    password = StringField()
    telephonenumber = StringField()
    maidenname = StringField()
    birthday = DateTimeField()
    ccnumber = StringField()
    cvv2 = StringField()
    ccexpires = StringField()
    nationalid = StringField()
    upstracking = StringField()
    vehicle = StringField()
    domain = StringField()
    kilograms = StringField()
    centimeters = StringField()
    latitude = FloatField()
    longitude = FloatField()
    guid = UUIDField(unique=True)

    gender = StringField(max_length=6, choices=('female', 'male'))
    bloodtype = StringField(max_length=3, choices=('B+', 'AB-', 'O-', 'A-', 'AB+', 'O+', 'A+', 'B-'))
    title = StringField(max_length=3, choices=('Mr.', 'Mrs.', 'Ms.', 'Dr.'))
    cctype = StringField(max_length=10, choices=('Visa', 'MasterCard'))
    city = ReferenceField(MGCity)
    company = ReferenceField(MGCompany)
    occupation = ReferenceField(MGOccupation)
