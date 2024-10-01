# config.py
import os

def get_mongo_uri() -> str:
    """
    Retrieves the MongoDB URI from the environment variable 'MONGO_URI'.
    Defaults to 'mongodb://localhost:27017/' if not set.
    """
    return os.getenv("MONGO_URI", "mongodb+srv://Tamer:Soft_123@chatbot.vulyc.mongodb.net/?retryWrites=true&w=1")
