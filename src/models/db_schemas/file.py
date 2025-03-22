from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class File(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    file_id: str = Field(..., min_length=1)

    @classmethod
    def get_indexes(cls):

        return [
            {
                "key": [
                    ("file_id", 1)
                ],
                "name": "file_id_index_1",
                "unique": True
            }
        ]

    model_config = {"arbitrary_types_allowed": True}