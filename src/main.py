from fastapi import FastAPI, Depends
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings, settings


app = FastAPI()

@app.on_event("startup")
async def startup_db_client(app_settings: settings = Depends(get_settings)):
    
    app.mongo_conn = AsyncIOMotorClient(app_settings.MONGO_URI)
    app.db = app.mongo_conn[app_settings.MONGO_DB]


@app.on_event("shutdown")
async def shutdown_db_client(app: FastAPI):
    app.mongo_conn.close()
    

app.include_router(base.base_router)
app.include_router(data.data_router)
