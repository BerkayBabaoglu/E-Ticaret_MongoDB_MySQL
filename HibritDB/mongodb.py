from pymongo import MongoClient
from django.conf import settings

def get_mongodb_client(): #mongodb'ye baglanti saglar. host ve port bilgileri settings.oy dosyasindan alinir.
    """Returns a MongoDB client instance"""
    return MongoClient(
        host=settings.MONGODB_HOST,
        port=settings.MONGODB_PORT
    )

def get_mongodb_database(): #veritabanina baglanir.
    """Returns a MongoDB database instance"""
    client = get_mongodb_client()
    return client[settings.MONGODB_DATABASE]

def get_mongodb_collection(collection_name): #collection name'i dondurur.
    """Returns a MongoDB collection instance"""
    db = get_mongodb_database()
    return db[collection_name] 