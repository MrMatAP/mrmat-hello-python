from mongoengine import *


class MGCity(Document):
    meta = {'collection': 'cities'}

    name = StringField(required=True)
    state = StringField()
    country = StringField(required=True)
    code = StringField(required=True)
