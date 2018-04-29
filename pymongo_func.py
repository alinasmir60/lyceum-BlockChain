import pymongo
import requests
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


def get_balance(id):
    bal = client.ad.coins.find({"id": {"$eq": id}}).count()
    if not bal:
        bal = 0
    return "{} ADCoins".format(str(bal))


def transfer(from_id, to_id, coin_id):
    balance = int(get_balance(from_id))
    if not from_id or not to_id or not coin_id:
        return "К сожалению, Вы не можете осуществить перевод. Заполните все поля"

    if not from_id.isdigit() or not to_id.isdigit():
        return "Вы ввели некоректный id"

    if from_id == to_id:
        return "Вы не можете перевести самому себе"

    if coin_id.isdigit():
        coin = int(coin_id)
        if coin <= 0:
            return "Некорректно введена сумма перевода"
    else:
        return "Некорректно введена сумма перевода"

    if coin > balance:
        if balance == 0:
            return "У вас нет средств на счёте."
        else:
            return "У вас недостаточно средств."

    id_coins = [i["_id"] for i in client.ad.coins.find({"user": {"$eq": from_id}})[:coin]]

    for i in id_coins:
        client.ad.log.insert_one(
            {
                "coin": i,
                "from": from_id,
                "to": to_id,
                "time": datetime.utcnow()
            }
        )

        client.ad.coins.update({"id": i}, {"&set": {"user": to_id}})
    return "Вы перевели {} ADCoin {}".format(coin_id, to_id)


def get_name_vk():
    vk_address = "https://api.vk.com/method/users.get"
    params = {"user_ids": str(id),
              "v": "5.74"}
    try:
        answer = requests.get(vk_address, params=params).json()["response"][0]
        return " ".join((answer["first_name"], answer["last_name"]))
    except:
        return "Пользователь не найден"


def get_top():
    sort = {'$sort': {'total': -1}}
    agr = client.ad.coins.aggregate([{'$group': {'_id': '$user', 'total': {'$sum': 1}}}, sort])
    name = list(agr)[:10]
    top = []
    for i in range(len(name)):
        top.append((i+1, get_name_vk(name[i]["_id"]), name[i]["total"]))
    return top
