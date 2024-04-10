from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from logger import setup_rotating_logger


_mongo_client = None 
_logger = setup_rotating_logger()


def get_mongo_client(uri):
    global _mongo_client
    if not _mongo_client:
        _mongo_client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        _mongo_client.admin.command('ping')
        _logger.info("Pinged your deployment. You successfully connected to MongoDB!")

    except Exception as e:
        _logger.warning("Error while connecting to monogodb, %s", e)

    return _mongo_client

