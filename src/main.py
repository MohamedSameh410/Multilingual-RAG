from fastapi import FastAPI, Depends
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings, settings
from stores.llm import LLMProviderFactory


app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    
    app_settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(app_settings.MONGO_URL)
    app.db_client = app.mongo_conn[app_settings.MONGO_DB]

    # intialize the LLM provider
    llm_provider_factory = LLMProviderFactory(app_settings)

    # intialize the generation model
    app.generation_client = llm_provider_factory.create(provider= app_settings.GENERATION_MODEL)
    app.generation_client.set_generation_model(model_id= app_settings.GENERATION_MODEL_ID)

    # intialize the embedding model
    app.embedding_client = llm_provider_factory.create(provider= app_settings.EMBEDDING_MODEL)
    app.embedding_client.set_embedding_model(
        model_id= app_settings.EMBEDDING_MODEL_ID,
        embedding_size= app_settings.EMBEDDING_MODEL_SIZE
    )


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()
    

app.include_router(base.base_router)
app.include_router(data.data_router)
