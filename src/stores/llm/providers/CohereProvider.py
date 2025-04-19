from ..LLMInterface import LLMInterface
from ..LLMEnums import CohereEnums, DocumentTypeEnums
import cohere
import logging

class CohereProvider(LLMInterface):

    def __init__(self, api_key: str,
                 input_max_characters: int = 1000,
                 output_max_tokens: int = 1000,
                 temperature: float = 0.1):
        
        self.api_key = api_key

        self.input_max_characters = input_max_characters
        self.output_max_tokens = output_max_tokens
        self.temperature = temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = cohere.ClientV2(api_key= self.api_key)

        self.logger = logging.getLogger(__name__)

        self.enums = CohereEnums

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list = [], max_output_tokens: int = None, temperature: float = None):
        
        if not self.client:
            self.logger.error("Cohere client is not initialized.")
            return None
        
        if not self.generation_model_id:
            self.logger.error("Generation model ID is not set.")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.output_max_tokens
        temperature = temperature if temperature else self.temperature

        chat_history.append(self.construct_prompt(prompt= prompt, role= CohereEnums.USER.value))

        response = self.client.chat(
            model= self.generation_model_id,
            messages= chat_history,
            max_tokens= max_output_tokens,
            temperature= temperature,
        )

        if not response or not response.message or not response.message.content[0].text or len(response.message.content[0].text) == 0:
            self.logger.error("No response from Cohere client.")
            return None
        
        return response.message.content[0].text
    
    def embed_text(self, text: str, document_type: str = None):
        
        if not self.client:
            self.logger.error("Cohere client is not initialized.")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model ID is not set.")
            return None
        
        input_type = CohereEnums.DOCUMENT.value if document_type == DocumentTypeEnums.DOCUMENT.value else CohereEnums.QUERY.value

        response = self.client.embed(
            model= self.embedding_model_id,
            texts= [self.process_text(text)],
            input_type= input_type,
            embedding_types=["float"],
        )

        # may raise an error here because of the difference between the Cohere docs and the actual API response
        # if this happens, make it float_ and try again
        if not response or not response.embeddings or not response.embeddings.float or len(response.embeddings.float[0]) == 0:
            self.logger.error("Failed to get embedding from Cohere API.")
            return None
        
        return response.embeddings.float[0]

    def construct_prompt(self, prompt: str, role: str):
        
        return {
            "role": role,
            "content": self.process_text(prompt)
        }