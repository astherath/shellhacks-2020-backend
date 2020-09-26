from pymongo import MongoClient
from config.main import DB_URI


class Database:
    client: MongoClient = None


db = Database()


async def get_database():
    return db.client


def connect_to_mongo():
    db.client = MongoClient(DB_URI)


def close_connection_to_mongo():
    db.client.close()
