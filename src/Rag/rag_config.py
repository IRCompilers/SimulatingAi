from pydantic import BaseModel


class RagConfig(BaseModel):
    use_persistence: bool
    use_llm: bool
