"""LangChain wrapper for local LLMs."""
from typing import Any, List, Optional, Dict
try:
    from langchain_core.language_models import LLM
except ImportError:
    from langchain.llms.base import LLM
from pydantic import Field

try:
    from llama_cpp import Llama
except ImportError:
    Llama = None

class LocalLLM(LLM):
    model_path: str
    n_ctx: int = Field(default=4096)
    n_gpu_layers: int = Field(default=0)
    temperature: float = Field(default=0.1)
    max_tokens: int = Field(default=1024)
    stop: List[str] = Field(default_factory=list)
    
    _model: Any = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if Llama is None:
            raise ImportError("llama-cpp-python is not installed")
        self._model = Llama(
            model_path=self.model_path,
            n_ctx=self.n_ctx,
            n_gpu_layers=self.n_gpu_layers,
            verbose=False
        )

    @property
    def _llm_type(self) -> str:
        return "local_llama"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> str:
        stop_tokens = stop or self.stop
        output = self._model(
            prompt,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            stop=stop_tokens,
            echo=False
        )
        return output["choices"][0]["text"]

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {
            "model_path": self.model_path,
            "n_ctx": self.n_ctx,
            "temperature": self.temperature
        }
