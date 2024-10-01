# main.py
import logging
from typing import List

from goldenverba.components.document import Document  # Ensure this path is correct
from helper import KHHelper

# Configure root logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_documents() -> List[Document]:
    """
    Placeholder function to load or generate Document instances.

    :return: List of Document instances.
    """
    # TODO: Implement actual document loading logic
    # For demonstration, return an empty list or mock data
    return []

def main():
    """
    Main function to execute the document insertion process.
    """
    # Initialize KHHelper with default configurations
    helper = KHHelper()

    # Optionally, pass custom configurations
    # helper = KHHelper(mongo_uri="your_mongodb_uri_here", db_name="YourDB", collection_name="YourCollection")

    # Load or generate documents to insert
    documents = load_documents()

    # Insert documents into MongoDB
    helper.insert_documents_to_mongodb(documents)

if __name__ == "__main__":
    main()
