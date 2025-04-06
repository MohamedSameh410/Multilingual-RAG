from fastapi import FastAPI, APIRouter, Depends, UploadFile, Request
from helpers.config import get_settings, settings
from controllers import DataController, ProcessController
from .schemas import ProcessRequest
from models import FileModel, DataChunkModel
from models.db_schemas.data_chunk import DataChunk
from bson.objectid import ObjectId
import os
import logging

logger = logging.getLogger('uvicorn.error')
data_router = APIRouter()

@data_router.post("/uploadfile")
async def upload_file(request: Request, file: UploadFile, app_settings: settings = Depends(get_settings)):
    
    file_model = await FileModel.create_instance(db_client= request.app.db_client)
    data_controller = DataController()
    is_valid = data_controller.validate_file(file= file)
    check_dir = data_controller.check_dir()

    if is_valid and check_dir:
        await data_controller.save_file(file= file)
        file_id = data_controller.file_id
        await file_model.get_or_insert_file(file_id= file_id)
        return {"status": "success",
                "message": "File uploaded successfully",
                "file_id": file_id
                }
    

@data_router.post("/processfile")
async def process_file(request: Request, process_request: ProcessRequest):

    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_resrt = process_request.do_reset

    file_model = await FileModel.create_instance(db_client= request.app.db_client)
    file_db = await file_model.get_or_insert_file(file_id= file_id)

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
    
    file_chunks_db_records = [
        DataChunk(
            chunk_text= chunk.page_content,
            chunk_metadata= chunk.metadata,
            chunk_order= i + 1,
            file_id= file_db.id
        )
        for i, chunk in enumerate(file_chunks)
    ]

    data_chunk_model = await DataChunkModel.create_instance(db_client= request.app.db_client)

    if do_resrt:
        await data_chunk_model.delete_data_chunks_by_fileId(file_id= file_db.id)
    
    num_records = await data_chunk_model.insert_many_data_chunks(data_chunks= file_chunks_db_records)
    
    return {
        "message": "File processed successfully",
        "inserted chunks": num_records
    }


@data_router.post("/processAllFiles")
async def process_all_files(request: Request, process_request: ProcessRequest):
    
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_resrt = process_request.do_reset

    file_model = await FileModel.create_instance(db_client= request.app.db_client)

    files, _ = await file_model.get_all_files()
    files_ids = [
        file.file_id for file in files
    ]

    if len(files_ids) == 0:
        return {"status": "error",
                "message": "No files to process"
                }
    
    process_controller = ProcessController()

    data_chunk_model = await DataChunkModel.create_instance(db_client= request.app.db_client)

    if do_resrt:
        await data_chunk_model.delete_data_chunks()

    num_records = 0
    num_files = 0
    for file_id in files_ids:
        file_db = await file_model.get_file_record(file_id= file_id)

        file_content = process_controller.get_file_content(file_id= file_id)

        if file_content is None:
            logger.error(f"Error while processing file: {file_id}")
            continue

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
        
        file_chunks_db_records = [
            DataChunk(
                chunk_text= chunk.page_content,
                chunk_metadata= chunk.metadata,
                chunk_order= i + 1,
                file_id= file_db.id
            )
            for i, chunk in enumerate(file_chunks)
        ]

        
        num_records += await data_chunk_model.insert_many_data_chunks(data_chunks= file_chunks_db_records)
        num_files += 1
    
    return {
        "message": "File processed successfully",
        "inserted chunks": num_records,
        "processed files": num_files
    }


def convert_objectid_to_str(document):
    if isinstance(document, dict):
        return {key: str(value) if isinstance(value, ObjectId) else value for key, value in document.items()}
    elif isinstance(document, list):
        return [convert_objectid_to_str(item) for item in document]
    return document

@data_router.post("/getChunks_byFileId/{file_id}")
async def get_chunks_by_fileId(request: Request, file_id: str):

    data_chunk_model = await DataChunkModel.create_instance(db_client= request.app.db_client)
    chunks_by_fileId = await data_chunk_model.get_all_chunks_by_file_id(file_id= file_id)

    return {
        "message": "Data chunks retrieved successfully",
        "chunks": convert_objectid_to_str(chunks_by_fileId)
    }