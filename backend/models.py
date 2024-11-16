from peewee import *

# Підключення до бази даних SQLite
db = SqliteDatabase('app.db')

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
    email = CharField(max_length=64, unique=True)
    at_home = BooleanField(default=False)

class Activity(BaseModel):
    user_id = ForeignKeyField(Users, backref='activities', on_delete='CASCADE')
    action = CharField(max_length=5)
    time = DateTimeField()

# Ініціалізація бази даних
db.connect()
db.create_tables([Users, Activity])
