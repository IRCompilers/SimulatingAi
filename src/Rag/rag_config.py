from pydantic import BaseModel


class RagConfig(BaseModel):
    use_persistence: bool
    use_llm: bool
    gemini_api_key: str
