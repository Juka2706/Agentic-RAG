"""LangChain wrapper for API-based LLMs (e.g. Ollama via OpenAI protocol)."""
from typing import Any, List, Optional, Dict
from langchain_openai import ChatOpenAI
from pydantic import Field

class APILLM(ChatOpenAI):
    """Wrapper around ChatOpenAI for Agentic RAG."""
    
    def __init__(self, base_url: str, api_key: str, model_name: str, **kwargs):
        super().__init__(
            base_url=base_url,
            api_key=api_key,
            model=model_name,
            **kwargs
        )
