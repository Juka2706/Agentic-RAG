from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    root: str = "."
    src_root: str = "src"
    docs_root: str = "docs"
    embed_model: str = "intfloat/e5-base-v2"
    llm_model_path: str = ""
    llm_api_base: str = "http://localhost:11434/v1"
    llm_api_key: str = "ollama"
    llm_is_local: bool = True
    llm_is_local: bool = True
    k: int = 8
    max_workers: int = 4
    budget_tokens: int = 200_000
    n_ctx: int = 4096
    n_gpu_layers: int = 0

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
