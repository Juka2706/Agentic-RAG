# config



<!-- BEGIN: auto:agentic_docs.config.Settings (hash=3bf3dcd49aecd593ec611985ea83108ca483ecdc12aebedbdfd1e6e63eb2ab06) -->
### `Settings`

**Summary**
The `Settings` class is a configuration management class that defines default parameters for an application and loads environment variables from a `.env` file. It uses the `BaseSettings` class from the pydantic library to provide type validation and environment variable loading capabilities.

**Parameters**
- `root` (str): Root directory for the project. Default value is `"."`.
- `src_root` (str): Path to the source code directory. Default value is `"src"`.
- `docs_root` (str): Path to the documentation directory. Default value is `"docs"`.
- `embed_model` (str): Pretrained model name for embeddings. Default value is `"intfloat/e5-base-v2"`.
- `llm_model_path` (str): Path to a local LLM model. Default value is an empty string.
- `llm_api_base` (str): Base URL for the LLM API. Default value is `"http://localhost:11434/v1"`.
- `llm_api_key` (str): API key for LLM authentication. Default value is `"ollama"`.
- `llm_is_local` (bool): Whether the LLM is running locally. Default value is `True`.
- `k` (int): Number of top results to return. Default value is `8`.
- `max_workers` (int): Maximum concurrent tasks/workers. Default value is `4`.
- `budget_tokens` (int): Token budget for processing tasks. Default value is `200_000`.
- `n_ctx` (int): Maximum context length for the model. Default value is `4096`.
- `n_gpu_layers` (int): Number of model layers to offload to GPU. Default value is `0`.

**Returns**
- `Settings`: An instance of the `Settings` class with all parameters loaded from the `.env` file or their default values if not present.

**Raises**
- `FileNotFoundError`: Raised if the `.env` file is missing.
- `pydantic.ValidationError`: Raised if environment variables cannot be parsed into the expected types.
- `ValueError`: Raised during type conversion if the environment variable does not match the expected type.
- `OSError`: Raised for I/O errors when reading the `.env` file.

**Examples**
```python
from your_module import Settings

# Use default configuration
settings = Settings()
print(settings.root)       # Output: .
print(settings.llm_api_base)  # Output: http://localhost:11434/v1

# Override settings via .env file
# Create a .env file with:
# LLM_API_BASE=https://api.example.com/v1
# LLM_API_KEY=my_secret_key
# LLM_IS_LOCAL=False
settings = Settings()
print(settings.llm_api_base)  # Output: https://api.example.com/v1
print(settings.llm_is_local)  # Output: False
```

**See also**
- [pydantic BaseSettings Documentation](https://docs.pydantic.dev/latest/concepts/settings/) for details on environment variable loading and validation.
<!-- END: auto:agentic_docs.config.Settings -->