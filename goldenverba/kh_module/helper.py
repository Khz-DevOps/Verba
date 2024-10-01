# helper.py
import logging
from typing import List, Dict, Any, Optional

from goldenverba.components.document import Document  # Ensure this path is correct
from db_handler import MongoDBHandler
from config import get_mongo_uri

# Configure logging for this module
logger = logging.getLogger(__name__)

class KHHelper:
    def __init__(
        self,
        mongo_uri: Optional[str] = None,
        db_name: str = "Verba",
        collection_name: str = "chunked_documents",
    ):
        """
        Initializes the KHHelper instance and internally manages the MongoDBHandler.

        :param mongo_uri: MongoDB connection string. If not provided, fetched from environment variable.
        :param db_name: Name of the database.
        :param collection_name: Name of the collection.
        """
        self.mongo_uri = mongo_uri or get_mongo_uri()
        self.db_name = db_name
        self.collection_name = collection_name

    def insert_documents_to_mongodb(self, chunked_documents: List[Document]) -> None:
        """
        Inserts a list of documents with nested chunks into MongoDB using an internal MongoDBHandler.

        :param chunked_documents: List of Document instances to insert.
        """
        try:
            prepared_documents = self._prepare_documents(chunked_documents)
            if not prepared_documents:
                logger.info("No valid documents to insert after preparation.")
                return

            # Instantiate MongoDBHandler internally
            with MongoDBHandler(
                mongo_uri=self.mongo_uri,
                db_name=self.db_name,
                collection_name=self.collection_name
            ) as handler:
                handler.insert_documents(prepared_documents)
        except Exception as e:
            logger.error(f"Failed to insert documents: {e}")

    def _prepare_documents(self, chunked_documents: List[Document]) -> List[Dict[str, Any]]:
        """
        Converts Document instances to JSON-compatible dictionaries.

        :param chunked_documents: List of Document instances.
        :return: List of dictionaries ready for MongoDB insertion.
        """
        prepared = []
        for doc in chunked_documents:
            try:
                doc_dict = Document.to_json(doc)
                doc_dict["chunks"] = [chunk.to_json() for chunk in doc.chunks]
                prepared.append(doc_dict)
            except AttributeError as e:
                logger.warning(f"Skipping document due to missing attribute: {e}")
            except Exception as e:
                logger.warning(f"Skipping document due to unexpected error: {e}")
        return prepared
