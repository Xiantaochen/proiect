import redis
import json
import pymongo

redis_client  = redis.Redis(host="localhost", port= 6379, db=0)
mongo_client = pymongo.MongoClient()
collection  = mongo_client.room.lianjia

while True:
    key, value = redis_client.blpop("lianjia:items")
    print(key)
    print(json.loads(value))
    d = json.loads(value)
    collection.insert(d)