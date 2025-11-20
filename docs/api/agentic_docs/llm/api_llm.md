# api_llm



<!-- BEGIN: auto:agentic_docs.llm.api_llm.APILLM (hash=cf83398d8ce1bb2c3be124f970ec8cbf2c9e6db0fede949216798ff0c2366dd8) -->
### APILLM

**Summary**
The `APILLM` class is a wrapper for the `ChatOpenAI` class, providing a specialized interface for Agentic Retrieval-Augmented Generation (RAG) workflows. It initializes a connection to an OpenAI-like API endpoint with the specified model, authentication, and configuration parameters.

**Parameters**
- `base_url` (str): The base URL of the API endpoint (e.g., `https://api.openai.com/v1`).
- `api_key` (str): The API key required for authentication (e.g., OpenAI API key).
- `model_name` (str): The name of the model to use (e.g., `gpt-3.5-turbo`, `gpt-4`).
- `**kwargs` (dict): Optional additional parameters passed to the parent `ChatOpenAI` class.

**Returns**
- (APILLM): An instance of the `APILLM` class, which can be used to invoke model inference for Agentic RAG workflows.

**Raises**
- `TypeError`: If parameters like `base_url`, `api_ket`, or `model_name` are not of the expected type (`str`).
- `ValueError`: If the model name is invalid or unsupported.
- `AuthenticationError`: If the API key is invalid or missing.
- `ConnectionError`: If the API endpoint is unreachable or the server returns an error.
- `TimeoutError`: If the API request times out.
- `APIResponseError`: If the API returns an error (e.g., invalid request format, rate limits).

**Examples**
```python
from langchain import ChatOpenAI

# Initialize APILLM for an OpenAI endpoint
llm = APILLM(
    base_url="https://api.openai.com/v1",
    api_key="sk-1234567890abcdef",
    model_name="gpt-3.5-turbo"
)

# Use the LLM to generate a response
response = llm.invoke("What is the capital of France?")
print(response)
```

```python
llm = APILLM(
    base_url="https://api.example.com/v1",
    api_key="my_custom_api_key",
    model_name="gpt-4",
    temperature=0.7,  # Additional parameter passed to ChatOpenAI
    max_tokens=150
)
```

```python
from langchain.agents import AgentExecutor, create_tool_calls_agent
from langchain.tools import Tool

# Assume `retriever` is a pre-configured retriever
agent = create_tool_calls_agent(
    llm=llm,
    tools=[Tool(name="search", func=retriever)],
    verbose=True
)

# Execute an agentic workflow
result = agent.run("What are the latest developments in quantum computing?")
print(result)
```

**See also**
- `langchain.ChatOpenAI` for the parent class implementation.
<!-- END: auto:agentic_docs.llm.api_llm.APILLM -->

<!-- BEGIN: auto:agentic_docs.llm.api_llm.APILLM.__init__ (hash=4cca01486716fac115f2a77a1ce9616b6b33d95518c2597c0c99714b3d6ddcb3) -->
### `__init__`

**Summary**
Initializes an object by delegating to its parent class. This method configures an LLM integration by passing required parameters such as the base URL of the API endpoint, an API key, a model name, and any additional keyword arguments to the parent class's constructor.

**Parameters**
- `base_url` (str): The base URL of the LLM API endpoint (e.g., `https://api.example.com/v1`).
- `api_key` (str): The API key used for authentication with the LLM service.
- `model_name` (str): The name of the LLM model to use (e.g., `gpt-4`, `llama-3`).
- `**kwargs` (dict): Optional keyword arguments passed to the parent class's constructor. These may include parameters like `timeout`, `max_tokens`, `temperature`, etc.

**Returns**
- None

**Raises**
- `ValueError`: If required parameters (`base_url`, `api_key`, or `model_name`) are missing or invalid.
- `TypeError`: If the provided arguments are of incorrect types (e.g., non-string `base_url` or `api_key`).
- `ConnectionError` or `Timeout`: If the API endpoint is unreachable or the request times out.
- `AuthenticationError`: If the `api_key` is invalid or the authentication fails.

**Examples**
```python
# Example 1: Basic initialization
llm_instance = MyLLMClass(
    base_url="https://api.example.com/v1",
    api_key="your_api_key_here",
    model_name="gpt-4"
)

# Example 2: With additional parameters
llm_instance = MyLLMClass(
    base_url="https://api.example.com/v1",
    api_key="your_api_key_here",
    model_name="llama-3",
    temperature=0.7,
    max_tokens=512
)
```

**See also**
- Parent class documentation for details on the constructor and parameters.
<!-- END: auto:agentic_docs.llm.api_llm.APILLM.__init__ -->