from peewee import *


class Users(Model):
    email = CharField(max_length=64)
    at_home = BooleanField(default=False)


class Activity(Model):
    user_id = ForeignKeyField(model = Users)
    action = CharField(max_length=5)
    time = DateTimeField()