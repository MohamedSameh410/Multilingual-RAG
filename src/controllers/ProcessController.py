from .BaseController import BaseController
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models.enums import ProcessingEnums
import os

class ProcessController(BaseController):

    def __init__(self):
        super().__init__()

    def get_file_extension(self, file_id: str):

        return os.path.splitext(file_id)[-1]
    
    def get_file_loader(self, file_id: str):

        file_extension = self.get_file_extension(file_id= file_id)
        file_path = os.path.join(self.files_dir, file_id)

        if file_extension == ProcessingEnums.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
        
        if file_extension == ProcessingEnums.PDF.value:
            return PyMuPDFLoader(file_path)
        
        return None
    
    def get_file_content(self, file_id: str):

        loader = self.get_file_loader(file_id= file_id)
        content = loader.load()
        return content
    
    def process_file_content(self, file_content: list, file_id: str,
                             chunk_size: int=100, overlap_size: int=20):
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size= chunk_size,
            overlap_size= overlap_size,
            length_function= len,
        )

        file_content_texts = [
            rec.page_content for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata for rec in file_content
        ]

        chunks = text_splitter.create_documents(
            file_content_texts, 
            metadatas= file_content_metadata
        )
