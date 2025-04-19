from enum import Enum

class LLMEnums(Enum):

    OPENAI = "OPENAI"
    COHERE = "COHERE"


class OpenAIEnums(Enum):

    SYSTEM = "system"
    DEVELOPER = "developer"
    USER = "user"
    ASSISTANT = "assistant"


class CohereEnums(Enum):

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

    DOCUMENT = "search_document"
    QUERY = "search_query"

class DocumentTypeEnums(Enum):

    QUERY = "query"
    DOCUMENT = "document"