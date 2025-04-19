from ..LLMInterface import LLMInterface
from ..LLMEnums import OpenAIEnums
from openai import OpenAI
import logging

class OpenAIProvider(LLMInterface):

    def __init__(self, api_key: str, api_url: str = None,
                 input_max_characters: int = 1000,
                 output_max_tokens: int = 1000,
                 temperature: float = 0.1):
        
        self.api_key = api_key
        self.api_url = api_url

        self.input_max_characters = input_max_characters
        self.output_max_tokens = output_max_tokens
        self.temperature = temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(api_key= self.api_key, api_url= self.api_url,)

        self.logger = logging.getLogger(__name__)
        self.enums = OpenAIEnums

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.input_max_characters].strip()

    def generate_text(self, prompt, chat_history: list = [], max_output_tokens: int = None, temperature: float = None):

        if not self.client:
            self.logger.error("OpenAI client is not initialized.")
            return None
        
        if not self.generation_model_id:
            self.logger.error("Generation model ID is not set.")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.output_max_tokens
        temperature = temperature if temperature else self.temperature

        chat_history.append(self.construct_prompt(prompt= prompt, role= OpenAIEnums.USER.value))

        response = self.client.chat.completions.create(
            model= self.generation_model_id,
            messages= chat_history,
            max_tokens= max_output_tokens,
            temperature= temperature,
        )

        if not response or not response.choices or not response.choices[0].message or len(response.choices) == 0:
            self.logger.error("Failed to get response from OpenAI API.")
            return None
        
        return response.choices[0].message["content"]

    def embed_text(self, text: str, document_type: str = None):
        
        if not self.client:
            self.logger.error("OpenAI client is not initialized.")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model ID is not set.")
            return None
        
        response = self.client.embeddings.create(
            model= self.embedding_model_id,
            input= text,
        )

        if not response or not response.data or not response.data[0] or len(response.data[0].embedding) == 0:
            self.logger.error("Failed to get embedding from OpenAI API.")
            return None
        
        return response.data[0].embedding

    def construct_prompt(self, prompt: str, role: str):
        
        return {
            "role": role,
            "content": self.process_text(prompt)
        }
