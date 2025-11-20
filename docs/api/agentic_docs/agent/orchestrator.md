# orchestrator



<!-- BEGIN: auto:agentic_docs.agent.orchestrator.Orchestrator (hash=3b4602c1639ef30ddfaad904eeb954fcee743fa00bfb1fc341afd7a6b814ff2a) -->
### Orchestrator

**Summary**  
The `Orchestrator` class coordinates a documentation generation pipeline for codebases. It parses code symbols, embeds them for vector search, and uses an LLM to generate markdown documentation for each symbol.

**Parameters**  
- `config: dict`  
  A dictionary containing configuration parameters for the orchestrator including root directories, model paths, and LLM settings.

- `changed_only: bool = False` (optional)  
  If `True`, only processes changed symbols (ignores full reindexing). Defaults to `False` for full reindexing.

**Returns**  
- `None`  
  The `run()` method performs side effects (file writing) and does not return a value. The `_process_symbol()` method also returns `None` as it performs file writing or logging.

**Raises**  
- `FileNotFoundError`  
  Raised when attempting to read a code file that does not exist.

- `ValueError`  
  Raised when a symbol file path is not relative to the root directory.

- `Exception`  
  General exceptions during LLM processing or I/O operations.

**Examples**  
```python
config = {
    "root": "/path/to/codebase",
    "docs_root": "/path/to/docs",
    "llm_is_local": True,
    "llm_model_path": "/path/to/model.gguf",
    "max_workers": 4
}
orchestrator = Orchestrator(config)
orchestrator.run()
```

**See also**  
- `Embedder`  
- `QdrantStore`  
- `LocalLLM`  
- `APILLM`  
- `MarkdownWriter`
<!-- END: auto:agentic_docs.agent.orchestrator.Orchestrator -->

<!-- BEGIN: auto:agentic_docs.agent.orchestrator.Orchestrator.__init__ (hash=71beb20f890ef3938e68d4acd9ffde01cc1224c243f26ae699320a0eef28a2ea) -->
### `Agent.__init__`

**Summary**
Initializes a document processing agent with configuration parsing, file system setup, embedding model, vector store, LLM integration, and shutdown handling.

**Parameters**
- `config` (dict): Configuration dictionary containing all initialization parameters. Required keys include "root", "docs_root", "embed_model", "device", "llm_model_path", "llm_is_local", "llm_api_base", "llm_api_key", "n_ctx", and "n_gpu_layers".

**Returns**
- None: The method initializes the class instance but does not return a value.

**Raises**
- `KeyError`: Missing required configuration keys.
- `FileNotFoundError`: When `model_path` exists but is not a valid file.
- `ImportError`: Failed to import required modules.
- `OSError`: File system operations fail.
- `ValueError`: Invalid configuration values for parameters like `n_ctx` or `device`.
- `RuntimeError`: Failed to initialize LLM or embedding model.
- `Exception`: Any unhandled exceptions during initialization.

**Examples**
```python
from agentic_docs.agent import Agent

# Basic configuration
config = {
    "root": "/var/app/data",
    "docs_root": "docs",
    "embed_model": "intfloat/e5-base",
    "device": "cuda",
    "llm_is_local": True,
    "llm_model_path": "/models/llama-7b.gguf",
    "n_ctx": 8192
}

# Create agent instance
agent = Agent(config)

# Advanced remote LLM configuration
config_remote = {
    "llm_is_local": False,
    "llm_api_base": "https://api.example.com/v1",
    "llm_api_key": "your-secret-key"
}

agent_remote = Agent(config_remote)
```

**See also**
- `Embedder` for text embedding model implementation
- `QdrantStore` for vector database configuration
- `APILLM` and `LocalLLM` for LLM integration details
- `MarkdownWriter` for document output interface
<!-- END: auto:agentic_docs.agent.orchestrator.Orchestrator.__init__ -->

<!-- BEGIN: auto:agentic_docs.agent.orchestrator.Orchestrator.run (hash=f3f93e73eae8799d1b981a41266c6a7e49814b4684be19f6a6815d7941658bfa) -->
### `run`

**Summary**  
Orchestrates a full pipeline to parse a codebase, index and embed symbols, store them in a vector database, and generate documentation for non-module symbols by searching for contextual similarity.

**Parameters**  
- `self` (object): The instance of the class containing this method.  
- `changed_only: bool = False` (bool): If `True`, only symbols that have changed are processed. This affects the `index_repo` call by setting `all_ = not changed_only`.

**Returns**  
- `None`: The method performs in-place operations but does not return a value.

**Raises**  
- `Exception`: Any unhandled exceptions during parsing, embedding, storing, or processing symbols will propagate.  
- `Worker failed: <error>`: Exceptions raised during parallel processing (via `ThreadPoolExecutor`) are caught and logged.  

**Examples**  
```python
orchestrator = Orchestrator(root="/path/to/code", embedder=Embedder(), store=QdrantStore(), config={"max_workers": 4})
orchestrator.run(changed_only=False)  # Process all symbols
```

```python
orchestrator.run(changed_only=True)  # Process only changed symbols
```

```python
orchestrator = Orchestrator(config={"max_workers": 1})  # Force sequential execution
orchestrator.run()
```

**See also**  
- `index_repo`: Parses and indexes code symbols.  
- `embedder.encode`: Encodes symbols into vectors.  
- `store.add`: Stores embeddings in a vector database.  
- `_process_symbol`: Generates documentation for a symbol using contextual similarity.
<!-- END: auto:agentic_docs.agent.orchestrator.Orchestrator.run -->

<!-- BEGIN: auto:agentic_docs.agent.orchestrator.Orchestrator._process_symbol (hash=55b9039282bc964f44d9e725e89fe0640046bd35bcf67352d367e7403a51a634) -->
### `_process_symbol`

**Summary**
Processes a programming symbol by reading its source code, generating documentation using an LLM agent, and writing the result to a markdown file. Handles various error scenarios with fallback mechanisms.

**Parameters**
- `sym: Symbol` (Symbol): Represents the code symbol with attributes:
  - `file`: file path
  - `start`: start line number
  - `end`: end line number
  - `symbol_id`: unique identifier
  - `hash`: source code hash
  - `qualname`: qualified name
- `context_str: str` (str): Context string for the documentation generation agent

**Returns**
- (None): The method does not explicitly return any value

**Raises**
- `OSError`: If file reading fails
- `ValueError`: If path resolution fails
- Any exceptions from `agents.process_symbol()`

**Examples**
```python
# Assume sym is a Symbol instance with:
sym.file = "src/pkg/mod.py"
sym.start = 10
sym.end = 25
sym.qualname = "pkg.mod.Func"
context_str = "Generate API documentation for the Func class"

_process_symbol(sym, context_str)
```

**See also**
- `Symbol` class
- `agents.process_symbol()`
<!-- END: auto:agentic_docs.agent.orchestrator.Orchestrator._process_symbol -->

<!-- BEGIN: auto:agentic_docs.agent.orchestrator.Orchestrator._cleanup (hash=2c877a1160f993bb2c0ea98f3cc58e599aa3245bb5a6cb1c87898bc0dce3bde0) -->
### `_cleanup`

**Summary**  
Closes the `store` resource if it exists and is truthy. This method is used to ensure proper resource cleanup when the object is no longer needed, such as during object destruction or explicit cleanup.

**Parameters**  
- `self` (object): The instance of the class containing this method. Provides access to the `store` attribute.

**Returns**  
- `None`: This method does not return a value.

**Raises**  
- `Exception`: Any exceptions raised during the `store.close()` call are caught and ignored to prevent propagation.

**Examples**  
```python
class QdrantClient:
    def __init__(self):
        self.store = SomeResource()

    def _cleanup(self):
        """Clean up resources on exit."""
        if hasattr(self, 'store') and self.store:
            try:
                self.store.close()
                print("Closed Qdrant connection.")
            except Exception:
                pass
```

**See also**  
- `__del__`: Method called when an object is about to be destroyed.  
- `__enter__`/`__exit__`: Context manager methods for deterministic cleanup.
<!-- END: auto:agentic_docs.agent.orchestrator.Orchestrator._cleanup -->

<!-- BEGIN: auto:agentic_docs.agent.orchestrator.Orchestrator._signal_handler (hash=3edfc2c441a132d117b7ed240004f3bb7f7a0f8c64ab29f7c33b72d8eb0d1328) -->
### `_signal_handler`

**Summary**  
Handles interrupt signals (e.g., SIGINT, SIGTERM) by logging the signal, performing cleanup, and exiting the program gracefully.

**Parameters**  
- `signum` (`int`): The signal number received (e.g., `signal.SIGINT`).  
- `frame` (`frame`): The current stack frame. This parameter is not used in this implementation but is included to match the signature expected by the `signal` module.

**Returns**  
- `None`: This method does not return any value.

**Raises**  
- `SystemExit`: Raised by `sys.exit(0)`, indicating a normal termination.  
- Exceptions from `self._cleanup()`: If `self._cleanup()` contains logic that may raise errors, those exceptions will propagate.

**Examples**  
```python
import signal
import sys

class Worker:
    def __init__(self):
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, signum, frame):
        print(f"\nReceived signal {signum}. Cleaning up...")
        self._cleanup()
        sys.exit(0)

    def _cleanup(self):
        print("Performing cleanup...")
```

**See also**  
- `signal.signal()`  
- `sys.exit()`  
- `self._cleanup()`
<!-- END: auto:agentic_docs.agent.orchestrator.Orchestrator._signal_handler -->