from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class DataChunk(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0)
    file_id: ObjectId

    @classmethod
    def get_idexes(cls):

        return [
            {
                "key": [
                    ("file_id", 1)
                ],
                "name": "chunk_file_id_index_1",
                "unique": False
            }
        ]


    model_config = {"arbitrary_types_allowed": True}

class RetrivedDocument(BaseModel):
    text: str
    score: float

    model_config = {"arbitrary_types_allowed": True}