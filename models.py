from peewee import *

db = SqliteDatabase("crypto.db")

class OrderBook(Model):
    index = IntegerField()
    price = FloatField()
    volume = FloatField()
    timestamp = IntegerField()
    type = TextField()
    pair = TextField()
    time_scraped = DateTimeField()


    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([OrderBook])


initialize()

