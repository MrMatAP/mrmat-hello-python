from mongoengine import *


class MGCompany(Document):
    meta = { 'collection': 'companies' }

    name = StringField(required=True, unique=True)
