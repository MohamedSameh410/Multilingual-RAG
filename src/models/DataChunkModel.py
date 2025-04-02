from .BaseDataModel import BaseDataModel
from .db_schemas.data_chunk import DataChunk
from bson.objectid import ObjectId
from pymongo import InsertOne

class DataChunkModel(BaseDataModel):

    def __init__(self, db_client):
        super().__init__(db_client= db_client)
        self.collection = self.db_client["DataChunks"]

    @classmethod
    async def create_instance(cls, db_client):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()

        if "DataChunks" not in all_collections:
            self.collection = self.db_client["DataChunks"]
            indexes = DataChunk.get_idexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name= index["name"],
                    unique= index["unique"]
                )


    async def insert_data_chunk(self, data_chunk: DataChunk):

        result = await self.collection.insert_one(data_chunk.dict(by_alias=True, exclude_unset=True))
        data_chunk._id = result.inserted_id

        return data_chunk
    
    async def get_data_chunk(self, data_chunk_id: str):
        
        result = await self.collection.find_one({"_id": ObjectId(data_chunk_id)})

        if result is None:
            return None
        
        return DataChunk(**result)
    
    async def insert_many_data_chunks(self, data_chunks: list, batch_size: int= 100):

        inserted_chunks = 0
        for i in range(0, len(data_chunks), batch_size):
            batch = data_chunks[i: i + batch_size]
            operations = [
                InsertOne(data_chunk.dict(by_alias=True, exclude_unset=True))
                for data_chunk in batch
            ]

            await self.collection.bulk_write(operations)
            inserted_chunks = inserted_chunks + len(batch)

        return inserted_chunks
    
    async def delete_data_chunks_by_fileId(self, file_id: ObjectId):

        result = await self.collection.delete_many({"file_id": file_id})
        return result.deleted_count
    
    async def delete_data_chunks(self):

        result = await self.collection.delete_many({})
        return result.deleted_count
    
    async def get_all_chunks_by_file_id(self, file_id: str):
        return await self.collection.find({
            "file_id": ObjectId(file_id) if isinstance(file_id, str) else file_id
        }).to_list(length= None)