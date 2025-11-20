# local_llm



<!-- BEGIN: auto:agentic_docs.llm.local_llm.LocalLLM (hash=d1fd02ca5768ec5b0a6de3d5c3733116b16414bc9da2c97fb2a1c23ad552805e) -->
### LocalLLM

**Summary**  
A class for running a local LLaMA model using the llama-cpp-python library. It provides methods for loading the model and generating text with configurable parameters.

**Parameters**  
- `model_path` (str): Required. The path to the local LLaMA model file (e.g., `.gguf` format).  
- `n_ctx` (int, default: 4096): Maximum context length for the model.  
- `n_gpu_layers` (int, default: 0): Number of GPU layers to offload (0 = CPU-only).  
- `temperature` (float, default: 0.1): Controls randomness in output (lower = more deterministic).  
- `max_tokens` (int, default: 1024): Maximum number of tokens to generate in a single response.  
- `stop` (List[str], default: `[]`): List of stop tokens to halt generation. Overrides default `self.stop`.  
- `**kwargs` (Any): Additional parameters for the base `LLM` class (e.g., logging, callbacks).

**Returns**  
- (str): The generated text output from the LLaMA model. The result is parsed from the model's response dictionary as `output["choices"][0]["text"]`.

**Raises**  
- `ImportError`: Raised if the `llama-cpp-python` library is not installed.  
- `Exception`: If the model fails to load (e.g., invalid `model_path`, incompatible file).  
- `KeyError`: If the model's response lacks the expected `"choices"` or `"text"` keys.

**Examples**  
```python
from llama_cpp import Llama
from your_module import LocalLLM

model = LocalLLM(model_path="/path/to/model.gguf", n_ctx=8192)
response = model._call(prompt="Hello, how are you?")
print(response)  # Outputs the generated text
```

```python
model = LocalLLM(
    model_path="/path/to/model.gguf",
    temperature=0.7,
    stop=[""],
    max_tokens=512
)
output = model._call(prompt="Explain quantum physics in simple terms.")
print(output)
```

```python
try:
    model = LocalLLM(model_path="invalid/path")
except ImportError:
    print("Llama-cpp not installed!")
except Exception as e:
    print(f"Model loading failed: {e}")
```

**See also**  
- `llama_cpp.Llama`: The underlying library for loading and running LLaMA models.  
- `LLM`: Base class for all language model implementations.
<!-- END: auto:agentic_docs.llm.local_llm.LocalLLM -->

<!-- BEGIN: auto:agentic_docs.llm.local_llm.LocalLLM.__init__ (hash=b176475b07f5c73de85fbd54765271cffbbfd5ad8f984e7e0fefed0f9747d070) -->
# `LocalLLM.__init__`

**Summary**
Initializes a local Llama model using the `llama-cpp-python` library. Validates the presence of the required library and configures the model with specified parameters.

**Parameters**
- `**kwargs` (`**dict[str, Any]`): Keyword arguments passed to the parent class constructor. These parameters are also forwarded to the `Llama` model initialization if they match the required attributes.

**Returns**
- `None`: The method does not return a value explicitly. It configures the instance's internal state via `self._model` and parent class attributes.

**Raises**
- `ImportError`: Raised if the `llama-cpp-python` library is not installed.
- `FileNotFoundError`: Raised if the specified `model_path` does not exist.
- `ValueError`: Raised if `n_ctx` or `n_gpu_layers` are invalid.
- `MemoryError`: Raised if the system lacks memory to load the model.
- `Exception`: General catch-all for other internal errors during model initialization.

**Examples**
```python
from agentic_docs.llm.local_llm import LocalLLM

model = LocalLLM(
    model_path="/path/to/model.gguf",
    n_ctx=4096,
    n_gpu_layers=32,
    verbose=False
)
```

```python
try:
    llm = LocalLLM(model_path="/invalid/path")
except ImportError:
    print("Llama-cpp not installed.")
except FileNotFoundError:
    print("Model file not found.")
except Exception as e:
    print(f"Model initialization failed: {e}")
```

**See also**
- `Llama` class from the `llama-cpp-python` library
- `agentic_docs.llm.local_llm.LocalLLM` base class documentation
<!-- END: auto:agentic_docs.llm.local_llm.LocalLLM.__init__ -->

<!-- BEGIN: auto:agentic_docs.llm.local_llm.LocalLLM._llm_type (hash=ca719431f8ec9a25f728b0bc248fbe54a9793e0cd23e7ae03b673bac723432fe) -->
### `_llm_type`

**Summary**  
The `_llm_type` method returns a fixed string `"local_llama"` to identify the type of language model (LLM) being used. This is likely used for internal classification, configuration, or compatibility checks within the `LocalLLM` class.

**Parameters**  
- None

**Returns**  
- `str`: A string representing the LLM type, which is hardcoded as `"local_llama"`.

**Raises**  
- None

**Examples**  
```python
llm_instance = LocalLLM()
print(llm_instance._llm_type())  # Output: "local_llama"
```

**See also**  
- `LocalLLM`: The class that contains this method.  
- `agentic_docs.llm.local_llm.LocalLLM`: The full module path for the class.
<!-- END: auto:agentic_docs.llm.local_llm.LocalLLM._llm_type -->

<!-- BEGIN: auto:agentic_docs.llm.local_llm.LocalLLM._call (hash=21bd3ca836139a73e798be69d581693631794b6f4769760e325e6f3e6a6bbfa0) -->
### `_call`

**Summary**
Generates text from a language model based on the provided prompt and optional parameters. This method handles stopping tokens, model execution, and returns the generated text.

**Parameters**
- `prompt` (str): The input text to generate from.
- `stop` (Optional[List[str]]): List of tokens to stop generation at. Defaults to class-level `self.stop` if not provided.
- `run_manager` (Optional[Any]): Execution context manager for tracking/monitoring.
- `**kwargs` (Any): Additional parameters for model customization.

**Returns**
- (str): The generated text from the model's first response choice.

**Raises**
- `KeyError`: When accessing `output["choices"]` or `output["choices"][0]["text"]` with missing keys.
- `IndexError`: When `output["choices"]` is empty or index 0 is out-of-bounds.
- `Model-specific exceptions`: Any exceptions raised by the underlying `self._model` call.
- `TypeError`: If `stop` is not a list when passed to the model.
- `ValueError`: If `max_tokens`, `temperature` parameters are invalid.

**Examples**
```python
response = llm_instance._call(
    prompt="What is the capital of France?",
    stop=[".", "France"]
)
print(response)  # Output: "Paris."
```

```python
response = llm_instance._call(
    prompt="Explain quantum physics",
    max_tokens=200,
    temperature=0.7,
    stop=[".", "quantum"]
)
print(response)  # Output: "Quantum physics..."
```

```python
response = llm_instance._call(
    prompt="Describe machine learning"
)
print(response)  # Uses class-level stop tokens
```

**See also**
- `self._model`: The underlying model implementation used for text generation.
<!-- END: auto:agentic_docs.llm.local_llm.LocalLLM._call -->

<!-- BEGIN: auto:agentic_docs.llm.local_llm.LocalLLM._identifying_params (hash=175df4122e0659e1ddbd1026c7fb9a2f3fdb099ff986532a3184bd3f2a697b47) -->
### `_identifying_params`

**Summary**
Returns a dictionary containing key configuration parameters that uniquely identify a local language model instance. These parameters are used for model identification, configuration tracking, and serialization purposes.

**Parameters**
- `self` (object): The instance of the `LocalLLM` class (implicit parameter)

**Returns**
- `Dict[str, Any]`: Dictionary containing:
  - `model_path` (str): Path to the local model file
  - `n_ctx` (int): Maximum context length (number of tokens) supported by the model
  - `temperature` (float): Sampling temperature for output randomness (0.0 to 1.0)

**Raises**
- None: This method does not raise exceptions as it only accesses instance variables

**Examples**
```python
model = LocalLLM()
print(model._identifying_params())
# Output: {'model_path': '/models/gpt2', 'n_ctx': 2048, 'temperature': 0.7}
```

**See also**
- `persist`: Method for saving model state
- `load`: Method for loading model state
<!-- END: auto:agentic_docs.llm.local_llm.LocalLLM._identifying_params -->