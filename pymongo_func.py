import pymongo
from datetime import datetime


client = pymongo.MongoClient("localhost", 27017)


def add_coin(str, user):
    client.ad.coins.insert_one(
        {
            "string": str,
            "time": datetime.utcnow(),
            "user": user,
        }
    )


def check(str):
    coin = client.ad.coins.find_one(str)
    if coin is None:
        return True
    return False