from mongoengine import *


class MongoOccupation(Document):
    meta = {'collection': 'occupations'}

    name = StringField(required=True, unique=True)
