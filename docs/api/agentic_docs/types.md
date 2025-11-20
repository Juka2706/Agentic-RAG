# types



<!-- BEGIN: auto:agentic_docs.types.Symbol (hash=b373c6f3d64e87b7b5bb80281c99585e2c7513915465418e5dd32d34df07fb1b) -->
# Symbol

**Summary**  
The `Symbol` class represents metadata for symbols in a codebase, such as modules, classes, functions, or methods. It stores information like the symbol's identity, source file location, documentation, and related constructs (e.g., imports, decorators).

**Parameters**  
- `symbol_id` (str): A unique identifier for the symbol (e.g., `func123`, `class456`).  
- `kind` (str): Type of the symbol (e.g., `module`, `class`, `function`, `method`).  
- `file` (str): Absolute or relative file path where the symbol is defined.  
- `qualname` (str): Fully qualified name of the symbol (e.g., `module.submodule.Class`).  
- `parent` (Optional[str]): Name of the parent symbol (e.g., a class's parent class).  
- `signature` (Optional[str]): Function/method signature (e.g., `def foo(x: int) -> None:`).  
- `docstring` (Optional[str]): Docstring content of the symbol (e.g., `"""This function does something."""`).  
- `start` (int): Starting position in the file (e.g., line number or byte offset).  
- `end` (int): Ending position in the file.  
- `hash` (str): Hash of the symbol's content (e.g., for caching or deduplication).  
- `imports` (List[str]): List of modules/dependencies imported by the symbol.  
- `decorators` (List[str]): List of decorators applied to the symbol (e.g., `@decorator`).

**Returns**  
- (): This class itself is returned as an instance when constructed.

**Raises**  
- `TypeError`: If attributes are assigned invalid types (e.g., a `start` value that is not an `int`).  
- `AttributeError`: If attributes are accessed before they are initialized (e.g., if the class lacks an `__init__` method and attributes are not pre-assigned).  
- `ValueError`: If constraints are violated (e.g., `start > end` for line numbers).  
- `KeyError`: If the `qualname` is used as a dictionary key and the symbol is not found.

**Examples**  
```python
symbol = Symbol(
    symbol_id="func123",
    kind="function",
    file="example.py",
    qualname="example.add",
    start=10,
    end=20,
    docstring="Adds two numbers.",
    decorators=["@staticmethod"],
    imports=["math"],
)
```

```python
print(symbol.kind)       # Output: "function"
print(symbol.docstring)  # Output: "Adds two numbers."
print(symbol.imports)    # Output: ["math"]
```

```python
assert symbol.start < symbol.end, "Start position must be less than end position"
```

**See also**  
- `Symbol` class documentation for more details on usage.
<!-- END: auto:agentic_docs.types.Symbol -->