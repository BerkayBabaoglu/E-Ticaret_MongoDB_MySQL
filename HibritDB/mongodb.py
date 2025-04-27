from pymongo import MongoClient
from django.conf import settings

def get_mongodb_client():
    """Returns a MongoDB client instance"""
    return MongoClient(
        host=settings.MONGODB_HOST,
        port=settings.MONGODB_PORT
    )

def get_mongodb_database():
    """Returns a MongoDB database instance"""
    client = get_mongodb_client()
    return client[settings.MONGODB_DATABASE]

def get_mongodb_collection(collection_name):
    """Returns a MongoDB collection instance"""
    db = get_mongodb_database()
    return db[collection_name] 