from os import getenv
from pymongo import MongoClient

SERVICE_MONGO_CONNECTION = getenv('SERVICE_MONGO_CONNECTION', None)
DOCUMENT_KEY = "currentStatus"


def get_collection():
    if SERVICE_MONGO_CONNECTION is None:
        raise Exception("SERVICE_MONGO_CONNECTION is missing in the environment.")

    client = MongoClient(SERVICE_MONGO_CONNECTION)
    return client["status"]


async def get_current_status():
    c = get_collection()
    record = c.find_one({"_id": DOCUMENT_KEY})
    return record.status if record is not None else None


def set_current_status(status):
    c = get_collection()
    c.find_one_and_update(
        {"_id": DOCUMENT_KEY},
        {"$set": {"status": status}},
        upsert=True
    )
