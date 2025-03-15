from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class File(BaseModel):
    _id: Optional[ObjectId]
    file_id: str = Field(..., min_length=1)

    class config:
        arbitrary_types_allowed = True