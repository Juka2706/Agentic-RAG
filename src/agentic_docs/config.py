from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    root: str = "."
    src_root: str = "src"
    docs_root: str = "docs"
    embed_model: str = "intfloat/e5-base-v2"
    llm_model: str = "codellama-7b-instruct.Q4_K_M.gguf"
    vector: Literal["faiss", "qdrant"] = "faiss"
    k: int = 8
    budget_tokens: int = 200_000

settings = Settings()
