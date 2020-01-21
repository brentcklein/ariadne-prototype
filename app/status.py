from pymongo import MongoClient
DOCUMENT_KEY = "currentStatus"


def get_collection():
    client = MongoClient()  # Currently just using the default address of mongod running locally
    return client["status"]['statuses']


async def get_current_status():
    c = get_collection()
    record = c.find_one({"_id": DOCUMENT_KEY})
    return record['status'] if record is not None else None


def set_current_status(status):
    c = get_collection()
    c.update_one(
        {"_id": DOCUMENT_KEY},
        {"$set": {"status": status}},
        upsert=True
    )
