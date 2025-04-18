from fastapi import FastAPI, APIRouter, status, Request
from fastapi.responses import JSONResponse
from routes.schemas.rag import PushRequest, SearchRequest
from models import FileModel, DataChunkModel
from controllers import RAGController
from bson.objectid import ObjectId
import logging

logger = logging.getLogger('uvicorn.error')

rag_router = APIRouter()

@rag_router.post("/index/push/{file_id}")
async def index_file(request: Request, file_id: str, push_request: PushRequest):
    
    file_model = await FileModel.create_instance(db_client= request.app.db_client)
    file = await file_model.get_or_insert_file(file_id= file_id)

    if not file:
        return JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content= {
                "signal": "project not found",
            }
        )
    
    chunk_model = await DataChunkModel.create_instance(db_client= request.app.db_client)
    
    rag_controller = RAGController(
        vector_db_client= request.app.vector_db_client,
        generation_client= request.app.generation_client,
        embedding_client= request.app.embedding_client,
    )
    
    has_records = True
    page_no = 1
    inserted_items = 0
    idx = 0

    while has_records:
        page_chunks = await chunk_model.get_file_chunks(file_id= file.id, page_no= page_no)

        if len(page_chunks):
            page_no += 1

        if not page_chunks or len(page_chunks) == 0:
            has_records = False
            break

        chunk_ids = list(range(idx, idx + len(page_chunks)))
        idx += len(page_chunks)

        is_inserted = rag_controller.index_into_vector_db(
            file= file,
            chunks= page_chunks,
            do_reset= push_request.do_reset,
            chunks_ids= chunk_ids
        )

        if not is_inserted:
            return JSONResponse(
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
                content= {
                    "signal": "data not inserted into vector db"
                }
            )
        
        inserted_items += len(page_chunks)
    
    logger.info(f"file.id: {file.id}, type: {type(file.id)}")
    return JSONResponse(
        content= {
            "signal": "data inserted into vector db",
            "inserted_items": inserted_items,
        }
    )

@rag_router.get("/index/info/{file_id}")
async def get_file_index_info(request: Request, file_id: str):

    file_model = await FileModel.create_instance(db_client= request.app.db_client)
    file = await file_model.get_or_insert_file(file_id= file_id)

    rag_controller = RAGController(
        vector_db_client= request.app.vector_db_client,
        generation_client= request.app.generation_client,
        embedding_client= request.app.embedding_client,
    )

    collection_info = rag_controller.get_vector_db_collection_info(file= file)

    return JSONResponse(
        content= {
            "signal": "collection info retrieved successfully",
            "collection_info": collection_info
        }
    )

@rag_router.post("/index/search/{file_id}")
async def search_index(request: Request, file_id: str, search_request: SearchRequest):
    
    file_model = await FileModel.create_instance(db_client= request.app.db_client)
    file = await file_model.get_or_insert_file(file_id= file_id)

    rag_controller = RAGController(
        vector_db_client= request.app.vector_db_client,
        generation_client= request.app.generation_client,
        embedding_client= request.app.embedding_client,
    )

    results = rag_controller.search_vector_db_collection(file= file, text= search_request.text, limit= search_request.limit)

    if not results:
        return JSONResponse(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            content= {
                "signal": "search failed",
            }
        )
    
    return JSONResponse(
        content= {
            "signal": "search successful",
            "result": [result.dict() for result in results],
        }
    )