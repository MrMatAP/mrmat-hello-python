from mongoengine import Document, StringField, DateTimeField, FloatField, UUIDField, ReferenceField
from .mongo_city import MongoCity
from .mongo_company import MongoCompany
from .mongo_occupation import MongoOccupation


class MongoPerson(Document):
    """
    Person record in the Mongo database
    """
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
    city = ReferenceField(MongoCity)
    company = ReferenceField(MongoCompany)
    occupation = ReferenceField(MongoOccupation)
