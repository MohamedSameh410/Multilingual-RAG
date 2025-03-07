from fastapi import FastAPI, APIRouter
import os

router = APIRouter()

@router.get("/")
async def welcome():
    app_name = os.getenv("APP_NAME")
    return {
        "app name": app_name,
        }