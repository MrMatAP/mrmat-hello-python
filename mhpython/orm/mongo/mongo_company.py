from mongoengine import *


class MongoCompany(Document):
    meta = {'collection': 'companies'}

    name = StringField(required=True, unique=True)
