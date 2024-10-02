# helper.py
import logging
from typing import Any, Dict, List, Optional

from goldenverba.kh_module.models import GPTTopic
from goldenverba.server.types import DataBatchPayload, FileConfig

from .config import get_mongo_uri
from .db_handler import MongoDBHandler

from goldenverba.components.document import \
    Document  # Ensure this path is correct

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
        Also converts chunks to GPTTopic objects for logging or further processing.

        :param chunked_documents: List of Document instances to insert.
        """
        try:
            prepared_documents = self._prepare_documents(chunked_documents)
            if not prepared_documents:
                logger.info("No valid documents to insert after preparation.")
                return

            # Convert chunks to GPTTopic objects
            all_chunks = [chunk.to_json() for doc in chunked_documents for chunk in doc.chunks]
            gpttopics = self.convert_chunks_to_gpttopics(all_chunks)
            logger.info(f"Converted {len(gpttopics)} chunks to GPTTopic objects.")

            # Example: Log GPTTopics or perform additional operations
            for gpttopic in gpttopics:
                logger.debug(f"GPTTopic: {gpttopic}")

            # Instantiate MongoDBHandler internally and insert documents
            with MongoDBHandler(
                mongo_uri=self.mongo_uri,
                db_name=self.db_name,
                collection_name="gpttopics"
            ) as handler:
                handler.insert_documents(gpttopics)
                
            # Instantiate MongoDBHandler internally and insert documents
            with MongoDBHandler(
                mongo_uri=self.mongo_uri,
                db_name=self.db_name,
                collection_name=self.collection_name
            ) as handler:
                handler.insert_documents(prepared_documents)
        except Exception as e:
            logger.error(f"Failed to insert documents: {e}")


    def convert_chunks_to_gpttopics(self, chunks: List[Dict[str, Any]]) -> List[GPTTopic]:
        """
        Converts a list of chunk dictionaries into a list of GPTTopic objects.

        :param chunks: List of dictionaries representing chunks.
        :return: List of GPTTopic instances.
        """
        gpttopics = []
        for chunk in chunks:
            try:
                # Create GPTTopic instance by unpacking chunk dict
                gpttopic = GPTTopic(**chunk)
                gpttopics.append(gpttopic)
            except TypeError as te:
                logger.warning(f"Type error while converting chunk to GPTTopic: {te}. Chunk data: {chunk}")
            except Exception as e:
                logger.warning(f"Unexpected error while converting chunk to GPTTopic: {e}. Chunk data: {chunk}")
        return gpttopics
    
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

    def log_to_db(self, text_log_record: str) -> None:
        """
        Logs a string to the database.

        :param text_log_record: String to log.
        """
        try:
            with MongoDBHandler(
                mongo_uri=self.mongo_uri,
                db_name=self.db_name,
                collection_name="logs",
            ) as handler:
                handler.insert_document({"text": text_log_record})
        except Exception as e:
            logger.error(f"Failed to log to database: {e}")
            
            
    def log_batch_data_payload(self, batch_data: DataBatchPayload) -> None:
        """
        Logs a string to the database.

        :param text_log_record: String to log.
        """
        if (batch_data is not None):
            doc = {
                "t":'batch_data_payload',
                "chunk":batch_data.chunk,
                "isLastChunk":batch_data.isLastChunk,
                "total":batch_data.total,
                "fileID":batch_data.fileID,
                "order":batch_data.order,
                "credentials":{
                    "deployment":batch_data.credentials.deployment,
                    "url":batch_data.credentials.url,
                    "key":batch_data.credentials.key,
                }
            }
        else:
            doc = {
                "t":'batch_data_payload',
                "batch_data_payload":"None"
            }
            
        try:
            with MongoDBHandler(
                mongo_uri=self.mongo_uri,
                db_name=self.db_name,
                collection_name="logs",
            ) as handler:
                handler.insert_document(doc)
        except Exception as e:
            logger.error(f"Failed to log to database: {e}")
            
    def log_fileConfig(self, fileConfig: FileConfig) -> None:
        """
        Logs a string to the database.

        :param text_log_record: String to log.
        """
        if (fileConfig is not None):
            doc = {
                "t":'fileConfig',
                "fileID":fileConfig.fileID,
                "filename":fileConfig.filename,
                "isURL":fileConfig.isURL,
                "overwrite":fileConfig.overwrite,
                "extension":fileConfig.extension,
                "source":fileConfig.source,
                "content":fileConfig.content,
                "file_size":fileConfig.file_size,
                "metadata":fileConfig.metadata
            }
        else:
            doc = {
                "t":'fileConfig',
                "fileConfig":"None"
            }

        try:
            with MongoDBHandler(
                mongo_uri=self.mongo_uri,
                db_name=self.db_name,
                collection_name="logs",
            ) as handler:
                handler.insert_document(doc)
        except Exception as e:
            logger.error(f"Failed to log to database: {e}")
            
            