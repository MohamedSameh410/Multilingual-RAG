from fastapi import FastAPI, APIRouter, Depends, UploadFile
from helpers.config import get_settings, settings
from controllers import DataController
from .schemas import ProcessRequest
import os

data_router = APIRouter()

@data_router.post("/uploadfile")
async def upload_file(file: UploadFile, app_settings: settings = Depends(get_settings)):
    
    data_controller = DataController()
    is_valid = data_controller.validate_file(file= file)
    check_dir = data_controller.check_dir()

    if is_valid and check_dir:
        await data_controller.save_file(file= file)
        return {"status": "success",
                "message": "File uploaded successfully",
                "file_id": data_controller.file_id
                }
    

@data_router.post("/processfile")
async def process_file(process_request: ProcessRequest):

    file_id = process_request.file_id

    return file_id