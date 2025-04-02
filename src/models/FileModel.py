from .BaseDataModel import BaseDataModel
from .db_schemas.file import File

class FileModel(BaseDataModel):

    def __init__(self, db_client):
        super().__init__(db_client= db_client)
        self.collection = self.db_client["Files"]

    @classmethod
    async def create_instance(cls, db_client):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()

        if "Files" not in all_collections:
            self.collection = self.db_client["Files"]
            indexes = File.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name= index["name"],
                    unique= index["unique"]
                )

    async def insert_file(self, file: File):

        result = await self.collection.insert_one(file.dict(by_alias=True, exclude_unset=True))
        file._id = result.inserted_id

        return file

    async def get_or_insert_file(self, file_id: str):

        record = await self.collection.find_one({
            "file_id": file_id
        })

        # create a new record if it does not exist
        if record is None:
            file = File(file_id= file_id)
            file = await self.insert_file(file= file)

            return file
        
        return File(**record)
    
    async def get_file_record(self, file_id: str):

        record = await self.collection.find_one({
            "file_id": file_id
        })

        if record:
            return File(**record)
        
        return None
    
    async def get_all_files(self, page: int=1, page_size: int=10):

        # calculate the number of documents
        total_documents = await self.collection.count_documents({})

        # calculate the number of pages
        total_pages = total_documents // page_size
        if total_documents % page_size > 0:
            total_pages += 1

        # get the documents
        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        files = []
        # iterate over the cursor and convert documents to File objects
        async for document in cursor:
            files.append(File(**document))

        return files, total_pages

        
