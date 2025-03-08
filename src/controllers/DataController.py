from .BaseController import BaseController
from fastapi import UploadFile
import re
import os
import aiofiles

class DataController(BaseController):

    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024 #Convert fron MB to bytes

    def validate_file(self, file: UploadFile):
        
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False
        
        if file.size > (self.app_settings.FILE_MAX_SIZE * self.size_scale):
            return False
        
        return True
    
    def check_dir(self):
        
        if not os.path.exists(self.files_dir):
            os.makedirs(self.files_dir)
        
        return True
    
    async def save_file(self, file: UploadFile):
        
        cleaned_filename = self.clean_filename(file.filename)
        file_path = os.path.join(self.files_dir, cleaned_filename)
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read((self.app_settings.FILE_CHUNK_SIZE) * self.size_scale):
                await f.write(chunk)
        
    def clean_filename(self, filename: str):

        removed_special_chars = re.sub(r"[^a-zA-Z0-9.]", "_", filename.lower())
        cleaned_filename = re.sub(r"\s+", "_", removed_special_chars)

        return cleaned_filename