from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class File(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    file_id: str = Field(..., min_length=1)

    model_config = {"arbitrary_types_allowed": True}