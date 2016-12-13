from mongoengine import *


class MGOccupation(Document):
    meta = {'collection': 'occupations'}

    name = StringField(required=True, unique=True)
