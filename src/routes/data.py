from fastapi import FastAPI, APIRouter, Depends, UploadFile, Request
from helpers.config import get_settings, settings
from controllers import DataController, ProcessController
from .schemas import ProcessRequest
from models import FileModel
import os

data_router = APIRouter()

@data_router.post("/uploadfile")
async def upload_file(request: Request, file: UploadFile, app_settings: settings = Depends(get_settings)):
    
    file_model = FileModel(db_client= request.app.db_client)
    data_controller = DataController()
    is_valid = data_controller.validate_file(file= file)
    check_dir = data_controller.check_dir()

    if is_valid and check_dir:
        await data_controller.save_file(file= file)
        file_id = data_controller.file_id
        file_db = await file_model.get_or_insert_file(file_id= file_id)
        return {"status": "success",
                "message": "File uploaded successfully",
                "file_id": file_id,
                "db_id": str(file_db._id)
                }
    

@data_router.post("/processfile")
async def process_file(process_request: ProcessRequest):

    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size

    process_controller = ProcessController()
    file_content = process_controller.get_file_content(file_id= file_id)
    file_chunks = process_controller.process_file_content(
        file_content= file_content,
        file_id= file_id,
        chunk_size= chunk_size,
        overlap_size= overlap_size
    )

    if file_chunks is None or len(file_chunks) == 0:
        return {"status": "error",
                "message": "Error processing file"
                }
    
    return file_chunks