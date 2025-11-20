# store_qdrant



<!-- BEGIN: auto:agentic_docs.index.store_qdrant.QdrantStore (hash=7ea358835b74e597ea6fb4101d82c1369ac5f05b4e6d8d7620b4195ba775d1b6) -->
# QdrantStore

**Summary**
The `QdrantStore` class provides a Python wrapper for interacting with a Qdrant vector database. It handles connection management, collection creation, vector storage with metadata, and similarity search operations. The class includes retry logic for lock contention, automatic data persistence, and process cleanup for stale lock files.

**Parameters**
- `index_path` (Optional[Path]): Path to the Qdrant data directory. Defaults to "./qdrant_data".
- `collection_name` (str): Name of the vector collection. Defaults to "codebase".
- `dim` (int): Dimensionality of the vectors. Defaults to 768.
- `max_retries` (int): Maximum retry attempts for connection issues. Defaults to 3.

**Returns**
- (None): The `__init__` method sets up the client and collection, but does not return a value.
- (None): The `add()` method modifies the collection in-place and does not return a value.
- (List[Dict[str, Any]]): The `search()` method returns a list of search results with metadata and scores.
- (None): The `save()` and `load()` methods are no-ops as data is persisted automatically.

**Raises**
- `RuntimeError`: Raised if the connection to Qdrant fails after max_retries attempts.
- `ValueError`: Raised when vectors and metadatas have mismatched lengths.
- `Exception`: General exception for subprocess failures during stale lock cleanup.

**Examples**
```python
from qdrant_store import QdrantStore
import numpy as np

# Initialize store
store = QdrantStore(dim=768)

# Add vectors with metadata
vectors = np.random.rand(5, 768)
metadata = [{"source": "doc1"}, {"source": "doc2"}, ...]
store.add(vectors, metadata)

# Search similar vectors
results = store.search(np.random.rand(768), k=3)
for result in results:
    print(result['source'], result['score'])
```

**See also**
- `qdrant-client`: The Qdrant Python client library used for vector operations
- `uuid`: Used for generating unique identifiers for stored vectors
- `subprocess`: Used for process termination during stale lock cleanup
<!-- END: auto:agentic_docs.index.store_qdrant.QdrantStore -->

<!-- BEGIN: auto:agentic_docs.index.store_qdrant.QdrantStore.__init__ (hash=f847a5bc8e98744442226cf1c1c9db43674d69bc80cfdda63852a2cbaac77839) -->
### `QdrantStore.__init__`

**Summary**
Initializes a connection to a Qdrant vector database instance, ensuring the specified collection exists. Handles retry logic for connection failures and manages collection creation if necessary.

**Parameters**
- `index_path` (Optional[Path]): Optional path to the Qdrant data directory. Defaults to `"./qdrant_data"`.
- `collection_name` (str): Name of the Qdrant collection to use. Defaults to `"codebase"`.
- `dim` (int): Dimension of the vectors (e.g., 768 for embeddings). Default is 768.
- `max_retries` (int): Maximum number of retry attempts for connecting to Qdrant. Default is 3.

**Returns**
- (QdrantStore): The initialized `QdrantStore` instance.

**Raises**
- `RuntimeError`: If the Qdrant client fails to connect (e.g., due to stale locks or invalid paths).
- `Exception`: If the collection creation fails (e.g., invalid parameters, permission issues).

**Examples**
```python
from agentic_docs.index.store_qdrant import QdrantStore

# Example 1: Default configuration
store = QdrantStore()
# Uses index_path "./qdrant_data", collection "codebase", dim 768, max_retries=3

# Example 2: Custom configuration
store = QdrantStore(
    index_path="/data/qdrant",
    collection_name="my_collection",
    dim=512,
    max_retries=5
)
```

**See also**
- `QdrantClient`: The underlying client used to interact with the Qdrant server.
- `_cleanup_stale_locks`: Internal method for cleaning up stale locks (not publicly exposed).
<!-- END: auto:agentic_docs.index.store_qdrant.QdrantStore.__init__ -->

<!-- BEGIN: auto:agentic_docs.index.store_qdrant.QdrantStore._cleanup_stale_locks (hash=1f698f3632b0cdcd45b03db40b9c0445ce6eebb42ce5648e14ac96ba0c64a402) -->
### `_cleanup_stale_locks`

**Summary**
Cleans up stale lock files and kills zombie processes related to `agentic-docs`.

**Parameters**
- `self`: Class instance (assumed to have `index_path` attribute of type `Path` from `pathlib`).

**Returns**
- `None`

**Raises**
- `PermissionError`: When attempting to delete a protected lock file.
- `OSError`: For general file operation failures.
- `subprocess.CalledProcessError`: If `pgrep` fails.
- `subprocess.TimeoutExpired`: If the command times out.
- `PermissionError`: If the user cannot kill a process.
- `OSError`: If the PID is invalid or process doesn't exist.

**Examples**
```python
class ResourceManager:
    def __init__(self, index_path):
        self.index_path = index_path

    def shutdown(self):
        self._cleanup_stale_locks()
        # Additional cleanup logic...

# Usage
manager = ResourceManager(Path("/var/data/index"))
manager.shutdown()
```

**See also**
- `pathlib.Path.unlink()`
- `subprocess.run()`
<!-- END: auto:agentic_docs.index.store_qdrant.QdrantStore._cleanup_stale_locks -->

<!-- BEGIN: auto:agentic_docs.index.store_qdrant.QdrantStore.__enter__ (hash=e11a445075fd069ec109fdc8dc6c2a9d84abeace416080321d935fd1a1d3e401) -->
### `__enter__`

**Summary**  
The `__enter__` method is part of the context manager protocol and is called when entering the runtime context. It returns the instance of the class (`self`), allowing it to be used within the `with` block.

**Parameters**  
- `self` (`agentic_docs.index.store_qdrant.QdrantStore`): The instance of the class that implements the context manager.

**Returns**  
- `agentic_docs.index.store_qdrant.QdrantStore`: Returns the instance of the class, which can be used within the `with` block.

**Raises**  
- None

**Examples**  
```python
with QdrantStore(...) as qdrant:
    qdrant.do_something()  # Uses the instance returned by __enter__
```

**See also**  
- `__exit__`: The method that is called when exiting the runtime context.
<!-- END: auto:agentic_docs.index.store_qdrant.QdrantStore.__enter__ -->

<!-- BEGIN: auto:agentic_docs.index.store_qdrant.QdrantStore.__exit__ (hash=81ec8a74a7a13b0ced4a251cb655b22780904286ae9ee3f162690425abccd927) -->
### `__exit__`

**Summary**
The `__exit__` method is part of the context manager protocol and ensures that the `close()` method is invoked when exiting a `with` block. It facilitates resource cleanup and exception handling.

**Parameters**
- `exc_type` (type): The type of exception that occurred during the execution of the context block. If no exception occurred, it is `None`.
- `exc_val` (Exception): The actual exception instance raised during execution. If no exception occurred, it is `None`.
- `exc_tb` (Traceback): The traceback object associated with the exception. If no exception occurred, it is `None`.

**Returns**
- (None): The method implicitly returns `None`.

**Raises**
- `Exception`: If the `close()` method called via `self.close()` raises an exception. The `__exit__` method does not handle these exceptions; they are propagated up.

**Examples**
```python
with QdrantStore(host="localhost", port=6333) as store:
    store.add_documents(documents)
# __exit__ is called automatically, triggering store.close()
```

**See also**
- `__enter__`: The method called when entering a `with` block.
- `close()`: The method responsible for releasing resources.
<!-- END: auto:agentic_docs.index.store_qdrant.QdrantStore.__exit__ -->

<!-- BEGIN: auto:agentic_docs.index.store_qdrant.QdrantStore.close (hash=36f205e39d370455c31c9d05e183af4b6812e6c5c3acc6b18e08222a269e5ed4) -->
### `close`

**Summary**  
Closes the Qdrant client if it has been initialized. This method ensures that the underlying client is properly closed, while silently handling any exceptions that may occur during the process.

**Parameters**  
- None

**Returns**  
- `None`

**Raises**  
- Does not raise any exceptions. All exceptions during the closing process are silently caught and ignored.

**Examples**  
```python
qdrant_client = QdrantClient(host="localhost", port=6333)
qdrant_client.close()  # Safely closes the client

# Example with a non-initialized client
qdrant_client = QdrantClient(host="localhost", port=6333)
qdrant_client.client = None
qdrant_client.close()  # Does nothing, no exceptions
```

**See also**  
- `QdrantClient` constructor for initialization details.
<!-- END: auto:agentic_docs.index.store_qdrant.QdrantStore.close -->

<!-- BEGIN: auto:agentic_docs.index.store_qdrant.QdrantStore.add (hash=65c85940e8e1ec1b20b349dcc051219ae1491a5ab51c3e8973eaaffd5d4fbc22) -->
### `add`

**Summary**
Adds multiple vectors along with their associated metadata to a Qdrant collection. Validates that the input vectors and metadata arrays have the same length, generates unique UUIDs for each vector, and constructs point objects for storage in the Qdrant vector database.

**Parameters**
- `vectors` (`np.ndarray`): A 2D numpy array where each row represents a vector (shape: `(n, d)`), with `n` being the number of vectors and `d` the dimensionality of each vector.
- `metadatas` (`List[Dict[str, Any]]`): A list of dictionaries where each dictionary contains metadata for the corresponding vector. The length of this list must match the number of vectors.

**Returns**
- `None`: The method does not return any value. It performs an in-place upsert operation using the Qdrant client.

**Raises**
- `ValueError`: Raised when the number of vectors and metadata entries do not match, ensuring data consistency.
- `Exception`: May include connection failures, invalid collection names, or schema mismatches during the `upsert` operation.

**Examples**
```python
import numpy as np
from qdrant_client import QdrantClient
from some_module import QdrantStore

# Initialize the Qdrant store
client = QdrantClient(host="localhost", port=6333)
store = QdrantStore(client, collection_name="my_collection")

# Prepare vectors and metadata
vectors = np.array([[1.0, 2.0], [3.0, 4.0]])
metadatas = [{"source": "doc1"}, {"source": "doc2"}]

# Add vectors to the collection
store.add(vectors, metadatas)
```

**See also**
- `QdrantClient`: The Qdrant client library for interacting with the Qdrant vector database.
- `upsert`: The method used to add or update points in a Qdrant collection.
<!-- END: auto:agentic_docs.index.store_qdrant.QdrantStore.add -->

<!-- BEGIN: auto:agentic_docs.index.store_qdrant.QdrantStore.search (hash=362da1b45d1fef36e17c636f17b6fdcee9bc5d340a7d65decfc5dfb16433184e) -->
### `search`

**Summary**
Performs a vector similarity search in a Qdrant vector database, returning the top-k most similar items along with their scores and payloads.

**Parameters**
- `query_vector` (np.ndarray): A NumPy array representing the query vector. Supports 1D or 2D inputs (batched vectors).
- `k` (int, default: 5): Maximum number of nearest neighbors to retrieve from the collection.

**Returns**
- (List[Dict[str, Any]]): A list of dictionaries containing:
  - The original payload data stored for each item (`hit.payload`)
  - A `score` key indicating the similarity score between the query and the item

**Raises**
- `AttributeError`: If `self.client` does not have a `query_points` method.
- `ValueError`: If `query_vector` is not a 1D/2D NumPy array or has incompatible dimensions.
- `TypeError`: If `query_vector` cannot be converted to a list (e.g., non-array input).
- `QdrantAPIException`: If Qdrant client encounters errors (e.g., invalid collection name, connection issues).

**Examples**
```python
import numpy as np
from your_module import QdrantStore

store = QdrantStore(collection_name="my_collection")
query_vector = np.array([0.1, 0.2, 0.3])  # 1D vector
results = store.search(query_vector, k=3)
for result in results:
    print(result["score"], result["payload"])
```

**See also**
- `QdrantStore` class documentation for client setup and collection management.
<!-- END: auto:agentic_docs.index.store_qdrant.QdrantStore.search -->

<!-- BEGIN: auto:agentic_docs.index.store_qdrant.QdrantStore.save (hash=c4dc0b0b8e9f45a8cfced46b12c0c1c91c13e4d4c4f8633a3028e1e86b1fc283) -->
### `save`

**Summary**  
The `save` method is a no-operation (no-op) placeholder for persisting data to a specified path. However, the comment indicates that **Qdrant handles persistence automatically** using the path provided during object initialization (`__init__`). Thus, this method does not perform any actual file-saving logic and is likely either redundant or a stub for future implementation.

**Parameters**  
- `path` (`Path`): A `pathlib.Path` object representing the directory path where data should be persisted. However, the comment suggests this parameter is **not used** (since Qdrant persists to the path defined in `__init__`).

**Returns**  
- `None`: The method does not return any value since it is a no-op.

**Raises**  
- None: The method does not raise exceptions explicitly.  
- Potential issues: If the method were to be implemented (e.g., for custom persistence), exceptions such as `IOError`, `PermissionError`, or `ValueError` might be raised during file operations.

**Examples**  
```python
from pathlib import Path

# Example 1: Call save (no actual action)
store = QdrantStore(path=Path("/data/qdrant"))
store.save(Path("/data/qdrant"))  # No-op

# Example 2: Future implementation (hypothetical)
def save(self, path: Path):
    # Custom logic to save data to `path`
    pass
```

**See also**  
- `QdrantStore.__init__`: Initializes the persistence path for Qdrant.
<!-- END: auto:agentic_docs.index.store_qdrant.QdrantStore.save -->

<!-- BEGIN: auto:agentic_docs.index.store_qdrant.QdrantStore.load (hash=ec0455ae60f47a42a662de075f3c6795decf3458bf6e69ddd1a20045fed71c45) -->
### `load`

**Summary**  
The `load` method is intended to load data from a specified path, but the current implementation does nothing. According to the comment, Qdrant automatically loads data from the path provided in the constructor (`__init__`). This suggests the method may be a placeholder for future implementation or subclassing.

**Parameters**  
- `path` (`Path`): A path object (e.g., from `pathlib.Path`) indicating the storage location. Note that this path is already handled during initialization, making this parameter potentially redundant.

**Returns**  
- `None`: The method does not return any value.

**Raises**  
- No exceptions are raised as the method is currently a no-op. Future implementations may raise exceptions such as `FileNotFoundError`, `PermissionError`, or `ValueError`.

**Examples**  
```python
store = QdrantStore(path="some/path")
store.load("another/path")  # No action occurs
```

**See also**  
- `__init__`: The constructor that initializes the Qdrant store with a specified path.
<!-- END: auto:agentic_docs.index.store_qdrant.QdrantStore.load -->