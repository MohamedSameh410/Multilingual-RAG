from fastapi import FastAPI, APIRouter, Depends
from helpers.config import get_settings, settings
import os

base_router = APIRouter()

@base_router.get("/")
async def welcome(app_settings: settings = Depends(get_settings)):

    app_name = app_settings.APP_NAME
    return {
        "app name": app_name,
        }