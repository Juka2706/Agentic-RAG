# embed



<!-- BEGIN: auto:agentic_docs.index.embed.Embedder (hash=7d226a7e8b29990ea36e16a918ab2e455f05d8b465b87ce9e1453c4c371b0547) -->
### `Embedder`

**Summary**  
The `Embedder` class provides a mechanism to generate sentence embeddings using the `sentence-transformers` library. It leverages a pre-trained model to convert lists of text strings into numerical embeddings (vectors). The class includes an in-memory cache to store previously computed embeddings, improving efficiency by avoiding redundant computations for the same input texts.

**Parameters**  
- `model_name` (str): Name of the pre-trained model (e.g., `"intfloat/e5-base-v2"`). Defaults to `"intfloat/e5-base-v2"`.  
- `device` (str): Device to run the model on (e.g., `"cpu"`, `"cuda"`). Defaults to `"cpu"`.  
- `texts` (List[str]): List of text strings to be encoded into embeddings.

**Returns**  
- (np.ndarray): A 2D NumPy array where each row corresponds to the embedding vector of the input text. The embeddings are stacked vertically (`np.vstack`) to form a single output array.

**Raises**  
- `ImportError`: If the `sentence-transformers` library is not installed.  
- Exceptions: If the `model.encode()` method (from `sentence-transformers`) raises errors (e.g., invalid input types, model errors).

**Examples**  
```python
from Embedder import Embedder

# Initialize with default model and CPU
embedder = Embedder()

# Encode a list of texts
embeddings = embedder.encode(["Hello, world!", "This is a test."])
print(embeddings.shape)  # e.g., (2, 768) for e5-base-v2
```

```python
# Use a different model and GPU
embedder = Embedder(model_name="bert-base-nli-meanpool", device="cuda")
embeddings = embedder.encode(["Sentence 1", "Sentence 2"])
```

```python
# First encode and cache
embedder.encode(["Hello", "World"])

# Reuse cached embeddings
embeddings = embedder.encode(["Hello", "World", "New text"])
print(embeddings.shape)  # (3, 768)
```

**See also**  
- `sentence-transformers`: [https://www.sbert.net](https://www.sbert.net)  
- `numpy`: [https://numpy.org](https://numpy.org)
<!-- END: auto:agentic_docs.index.embed.Embedder -->

<!-- BEGIN: auto:agentic_docs.index.embed.Embedder.__init__ (hash=ae4225a1e32622d4ea2f6f8f70583b40f2a20b5d80e0734d11babb8cf70881da) -->
### `Embedder.__init__`

**Summary**  
Initializes an `Embedder` instance by loading a pre-trained `SentenceTransformer` model and setting up an internal cache for embeddings.

**Parameters**  
- `model_name` (str): The name of the pre-trained model to load (default: `"intfloat/e5-base-v2"`).  
- `device` (str): The device to use for computation (default: `"cpu"`). Acceptable values include `"cpu"`, `"cuda"`, or `"mps"`.

**Returns**  
- (None): This method does not return a value.

**Raises**  
- `ImportError`: If `SentenceTransformer` is not available (e.g., the `sentence-transformers` package is not installed).  
- Other exceptions: May be raised by the `SentenceTransformer` constructor if model initialization fails (e.g., invalid model name, unsupported device).

**Examples**  
```python
# Use default model and CPU
embedder = Embedder()

# Specify a custom model and GPU
embedder = Embedder(model_name="sentence-transformers/all-MiniLM-L6-v2", device="cuda")
```

**See also**  
- `sentence-transformers` library documentation for model and device configuration details.
<!-- END: auto:agentic_docs.index.embed.Embedder.__init__ -->

<!-- BEGIN: auto:agentic_docs.index.embed.Embedder.encode (hash=0b5b6c103381555c74169303395e8f7a6ae9389e2511a041f3fddebec9c8b860) -->
### `encode`

**Summary**
The `encode` method converts a list of text documents into numerical embeddings using a pre-trained model. It utilizes an in-memory cache to store previously computed embeddings, avoiding redundant computations. The output is a single numpy array of embeddings stacked vertically.

**Parameters**
- `texts` (List[str]): A list of input text documents to be encoded. Each element is a string.
- `self._cache` (Dict[str, np.ndarray]): An internal dictionary used to store already computed embeddings for texts (key: text, value: embedding array).
- `self.model` (object): The embedding model used to compute embeddings. The model must have an `encode` method that accepts a list of texts and returns numpy arrays.

**Returns**
- (np.ndarray): A 2D numpy array of shape `(len(texts), embedding_dim)` where:
  - Rows correspond to individual texts.
  - Columns correspond to embedding dimensions.
  - Values are float values representing the numerical embeddings of the input texts.

**Raises**
- `AttributeError`: If `self.model` or `self._cache` is not properly initialized.
- `TypeError`: If `texts` is not a list of strings, or if `self.model.encode` expects different input types.
- `ValueError`: If `self.model.encode` fails (e.g., invalid input, unsupported parameters).
- `MemoryError`: If the model's output exceeds available memory.
- `KeyError`: If `self._cache` is accessed without being initialized (e.g., empty dictionary).

**Examples**
```python
from typing import List
import numpy as np

# Assume `Embedder` is initialized with a model
embedder = Embedder(model=some_pretrained_model)

texts = ["This is a test.", "Another example text."]
embeddings = embedder.encode(texts)
print(embeddings.shape)  # (2, 768)
```

```python
# First call: embeddings are computed and cached
embeddings1 = embedder.encode(texts)

# Second call: cached values are reused
embeddings2 = embedder.encode(texts)
assert np.array_equal(embeddings1, embeddings2)
```

```python
# Example with SentenceTransformer
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
embedder = Embedder(model=model)

texts = ["Python is great", "Java is also great"]
embeddings = embedder.encode(texts)
print(embeddings)  # 2D array of shape (2, 384)
```

**See also**
- `self.model.encode`: The method used to compute embeddings for the input texts.
<!-- END: auto:agentic_docs.index.embed.Embedder.encode -->