from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import current_app as app


_mongo_client = None 

def get_mongo_client(uri):
    global _mongo_client
    if not _mongo_client:
        _mongo_client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        _mongo_client.admin.command('ping')

    except Exception as e:
        return e

    return _mongo_client

