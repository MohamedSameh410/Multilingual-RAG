from abc import ABC, abstractmethod

class LLMInterface(ABC):

    @abstractmethod
    def set_generation_model(self, model_id: str):
        """
        Set the generation model to be used.
        """
        pass

    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        """
        Set the embedding model to be used.
        """
        pass

    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list = [], max_output_tokens: int = None, temperature: float = None):
        """
        Generate text based on the provided prompt.
        """
        pass

    @abstractmethod
    def embed_text(self, text: str, document_type: str = None):
        """
        Embed the provided text.
        param document_type: The type of document to embed(user query || chunk).
        """
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        """
        Construct a prompt for the LLM.
        """
        pass