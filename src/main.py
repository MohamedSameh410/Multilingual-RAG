from fastapi import FastAPI, Depends
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings, settings
from stores.llm import LLMProviderFactory
from stores.vectorDB.VectorDBProviderFactory import VectorDBProviderFactory


app = FastAPI()

async def app_startup():
    
    # startup the db connection
    app_settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(app_settings.MONGO_URL)
    app.db_client = app.mongo_conn[app_settings.MONGO_DB]

    # intialize the providers factory
    llm_provider_factory = LLMProviderFactory(app_settings)
    vector_db_provider_factory = VectorDBProviderFactory(app_settings)

    # intialize the generation model
    app.generation_client = llm_provider_factory.create(provider= app_settings.GENERATION_MODEL)
    app.generation_client.set_generation_model(model_id= app_settings.GENERATION_MODEL_ID)

    # intialize the embedding model
    app.embedding_client = llm_provider_factory.create(provider= app_settings.EMBEDDING_MODEL)
    app.embedding_client.set_embedding_model(
        model_id= app_settings.EMBEDDING_MODEL_ID,
        embedding_size= app_settings.EMBEDDING_MODEL_SIZE
    )

    # intialize the vector db client
    app.vector_db_client = vector_db_provider_factory.create(provider= app_settings.VECTOR_DB)
    app.vector_db_client.connect()


async def app_shutdown():
    # close the db connection
    app.mongo_conn.close()
    app.vector_db_client.disconnect()


app.router.lifespan.on_startup.append(app_startup)
app.router.lifespan.on_shutdown.append(app_shutdown)
    

app.include_router(base.base_router)
app.include_router(data.data_router)
