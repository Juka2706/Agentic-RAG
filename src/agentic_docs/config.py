from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    root: str = "."
    src_root: str = "src"
    docs_root: str = "docs"
    embed_model: str = "intfloat/e5-base-v2"
    llm_model_name: str = "qwen2.5-coder:latest"
    llm_api_base: str = "http://localhost:11434/v1"
    llm_api_key: str = "ollama"

    k: int = 8
    max_workers: int = 4
    budget_tokens: int = 200_000
    n_ctx: int = 4096
    n_gpu_layers: int = 0
    
    # Agent Mode
    mode: str = "static"  # "static" or "agentic"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
