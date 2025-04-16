from abc import ABC, abstractmethod
from typing import List

class VectorDBInterface(ABC):

    @abstractmethod
    def connect(self):
        """Connect to the vector database."""
        pass

    @abstractmethod
    def disconnect(self):
        """Disconnect from the vector database."""
        pass

    @abstractmethod
    def is_collection_exists(self, collection_name: str) -> bool:
        """Check if a collection exists in the vector database."""
        pass

    @abstractmethod
    def list_all_clollections(self) -> List:
        """Get all collections in the vector database."""
        pass

    @abstractmethod
    def get_collection_info(self, clolection_name: str) -> dict:
        """Get information about a specific collection."""
        pass

    @abstractmethod
    def create_collection(self, collection_name: str,
                          embedding_size: int,
                          do_reset: bool = False):
        """Create a new collection in the vector database with condition if it exists, you got the option to delet it and recreate."""
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str):
        """Delete a collection from the vector database."""
        pass

    @abstractmethod
    def insert_one(self, collection_name: str, text: str,
                   vector: list, metadata: dict = None, record_id: str = None):
        """Insert a single record into the collection."""
        pass

    @abstractmethod
    def insert_many(self, collection_name: str, texts: list,
                    vectors:list, metadata: list = None,
                    record_ids: list = None, batch_size: int = 50):
        """Insert multiple records into the collection."""
        pass

    @abstractmethod
    def search_by_vector(self, collection_name: str, vector: list, limit: int = 5):
        """Search for records in the collection based on a vector."""
        pass