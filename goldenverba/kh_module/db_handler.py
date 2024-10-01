# db_handler.py
import logging
from typing import List, Dict, Any, Optional

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, BulkWriteError
from config import get_mongo_uri

# Configure logging for this module
logger = logging.getLogger(__name__)

class MongoDBHandler:
    def __init__(
        self,
        mongo_uri: Optional[str] = None,
        db_name: str = "Verba",
        collection_name: str = "chunked_documents"
    ):
        """
        Initializes the MongoDBHandler instance.

        :param mongo_uri: MongoDB connection string. If not provided, fetched from environment variable.
        :param db_name: Name of the database.
        :param collection_name: Name of the collection.
        """
        self.mongo_uri = mongo_uri or get_mongo_uri()
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None

    def __enter__(self):
        """
        Establishes the MongoDB connection when entering the context.
        """
        try:
            self.client = MongoClient(self.mongo_uri)
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
            logger.info("Successfully connected to MongoDB.")
            return self
        except ConnectionFailure as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the MongoDB connection when exiting the context.
        """
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")

    def insert_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Inserts a list of dictionaries into MongoDB.

        :param documents: List of dictionaries ready for MongoDB insertion.
        """
        if not documents:
            logger.info("No documents provided for insertion.")
            return

        db = self.client[self.db_name]
        collection = db[self.collection_name]

        try:
            result = collection.insert_many(documents, ordered=False)
            logger.info(f"Inserted {len(result.inserted_ids)} documents into '{self.collection_name}' collection.")
        except BulkWriteError as bwe:
            logger.error(f"Bulk write error occurred: {bwe.details}")
        except Exception as e:
            logger.error(f"An error occurred while inserting documents: {e}")
