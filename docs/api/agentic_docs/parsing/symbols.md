# symbols



<!-- BEGIN: auto:agentic_docs.parsing.symbols._sha (hash=60ebce47ff3613e0d13f8b9690ec40824446e7cdcc06969caa4150a809c36d6a) -->
# `_sha`

**Summary**  
Computes the SHA-256 hash of a given input string and returns its hexadecimal representation.

**Parameters**  
- `s` (`str`): The input string to be hashed. This should be a valid UTF-8 encodable string.

**Returns**  
- (`str`): A 64-character hexadecimal string representing the SHA-256 hash of the input string.

**Raises**  
- `UnicodeEncodeError`: If the input string contains characters that cannot be encoded using UTF-8.
- `AttributeError`: If the input is not a string (e.g., passed as an integer, float, or other non-string type).

**Examples**
```python
result = _sha("hello")
print(result)
# Output: 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

```python
result = _sha("test@example.com")
print(result)
# Output: 10c537c43629152f9f5732d244f9e36b5466319f32f882c40e4eb12c0995775b
```

```python
try:
    _sha(123)
except AttributeError as e:
    print(f"Error: {e}")
# Output: Error: 'int' object has no attribute 'encode'
```

**See also**  
- `hashlib.sha256` for more information on SHA-256 hashing.
<!-- END: auto:agentic_docs.parsing.symbols._sha -->

<!-- BEGIN: auto:agentic_docs.parsing.symbols.collect_py_files (hash=a20e502a79e929351517823076cd82afc7260556f1aa696f20a63555aa42ed20) -->
### `collect_py_files`

**Summary**
Recursively collects all Python source files (`*.py`) under the specified root directory, excluding files in directories listed in the `IGNORE` list.

**Parameters**
- `root` (str): The root directory path from which to start the recursive search for `.py` files.

**Returns**
- (list[Path]): A list of `Path` objects representing all `.py` files found under the `root` directory, excluding those in directories listed in `IGNORE`.

**Raises**
- `TypeError`: If the `root` parameter is not a string.
- `NameError`: If the `IGNORE` variable is not defined in the current scope.

**Examples**
```python
from agentic_docs.utils import collect_py_files
from pathlib import Path

# Assuming IGNORE is defined as a list of directory names to exclude
IGNORE = ["tests", "build", "venv"]

files = collect_py_files("/path/to/project")
for file in files:
    print(file.name)
```

**See also**
- `pathlib.Path`: Used for path manipulation and file system operations.
- `IGNORE`: A global or module-level list of directory names to exclude from the search.
<!-- END: auto:agentic_docs.parsing.symbols.collect_py_files -->

<!-- BEGIN: auto:agentic_docs.parsing.symbols.module_qualname (hash=0e75f21867d552bfd4becf5b72c5a6885fc555dfe292be4fc95997f111880d80) -->
### module_qualname

**Summary**  
Generates a Python-like module name (qualified name) from a given file path relative to a source root directory. If the file path is not nested within the source root, it defaults to using the file's stem (filename without extension) as the module name.

**Parameters**  
- `path` (`Path`): The absolute or relative path to the file for which the module name is generated.  
- `src_root` (`Path`): The root directory (source root) used to compute the relative path.

**Returns**  
- (`str`): A string representing the module name, composed by joining the relative path parts with dots. If the path is invalid relative to `src_root`, it returns the file's stem.

**Raises**  
- `ValueError`: If the `path` is not nested within the `src_root`. This exception is caught and handled internally.

**Examples**  
```python
from pathlib import Path

src_root = Path("/project/src")
path = Path("/project/src/module/submodule.py")
print(module_qualname(path, src_root))  # Output: "module.submodule"
```

```python
src_root = Path("/project/src")
path = Path("/project/other/file.py")
print(module_qualname(path, src_root))  # Output: "file"
```

```python
src_root = Path("/project/src")
path = Path("/project/src/data/config")
print(module_qualname(path, src_root))  # Output: "data.config"
```

```python
src_root = Path("/project/src")
path = Path("/project/src/main.py")
print(module_qualname(path, src_root))  # Output: "main"
```

**See also**  
- `Path.relative_to()`  
- `Path.stem`  
- `Path.with_suffix()`
<!-- END: auto:agentic_docs.parsing.symbols.module_qualname -->

<!-- BEGIN: auto:agentic_docs.parsing.symbols._get_decorators (hash=a0fd4ddb0b6ad767b2c013b9a3d20e04afe337ff6b50f5e76db821466fc22218) -->
### `_get_decorators`

**Summary**  
Extracts the names of decorators applied to a given Python AST node. Handles `ast.Name`, `ast.Attribute`, and `ast.Call` decorator types, returning a list of strings representing the names of the decorators.

**Parameters**  
- `node` (ast.AST): The AST node from which to extract decorators. The node must have a `decorator_list` attribute.

**Returns**  
- List[str]: A list of strings, each representing the name of a decorator. The names may include dot-separated parts for nested attributes.

**Raises**  
- AttributeError: If the node lacks a `decorator_list` attribute.  
- TypeError: If the node’s `decorator_list` contains unexpected types (e.g., `ast.List`, `ast.Tuple`, or other non-AST objects).

**Examples**  
```python
@decorator
def func():
    pass
```
**Input**: AST node for `func` (with `decorator_list` containing `ast.Name(id='decorator')`).  
**Output**: `['decorator']`

```python
@DecoratorClass.decorator_method
class MyClass:
    pass
```
**Input**: AST node for `MyClass` (with `decorator_list` containing `ast.Attribute(value=ast.Name(id='DecoratorClass'), attr='decorator_method')`).  
**Output**: `['DecoratorClass.decorator_method']`

```python
@decorator()
class MyClass:
    pass
```
**Input**: AST node for `MyClass` (with `decorator_list` containing `ast.Call(func=ast.Name(id='decorator'))`).  
**Output**: `['decorator']`

```python
@Decorator().method()
def func():
    pass
```
**Input**: AST node for `func` (with `decorator_list` containing `ast.Call(func=ast.Attribute(value=ast.Name(id='Decorator'), attr='method'))`).  
**Output**: `['Decorator.method']`

**See also**  
- `ast.Name`, `ast.Attribute`, `ast.Call` for details on decorator expressions in Python AST.
<!-- END: auto:agentic_docs.parsing.symbols._get_decorators -->

<!-- BEGIN: auto:agentic_docs.parsing.symbols._get_signature (hash=78e76c6f716222c695ab2c8ba4d752002439dcc3927d15e12ec7b75501a1d7cd) -->
### `_get_signature`

**Summary**  
Extracts the function signature (including parameters and return type annotations) from an AST node representing a Python function or async function.

**Parameters**  
- `node` (`ast.AST`): An AST node representing a Python function or async function. Must be an instance of `ast.FunctionDef` or `ast.AsyncFunctionDef`.

**Returns**  
- `Optional[str]`: A string representing the function signature in the format `(arg1: type, arg2, *vararg, **kwarg) -> return_type` if the node is a function or async function. Returns `None` if the node is not a function or async function.

**Raises**  
- `AttributeError`: If the AST node lacks expected attributes or is not a `FunctionDef`/`AsyncFunctionDef`.  
- `ImportError` or `AttributeError`: If the code is run in a Python version before 3.10, where `ast.unparse()` is not available.

**Examples**  
```python
import ast
from typing import Optional

# Parse a function definition
source_code = "def add(a: int, b: int) -> int: pass"
tree = ast.parse(source_code)
func_node = tree.body[0]  # Get the FunctionDef node

signature = _get_signature(func_node)
print(signature) 
# Output: "(a: int, b: int) -> int"
```

```python
source_code = "async def async_add(a: int, b: int) -> int: pass"
tree = ast.parse(source_code)
func_node = tree.body[0]  # Get the AsyncFunctionDef node

signature = _get_signature(func_node)
print(signature)
# Output: "(a: int, b: int) -> int"
```

```python
source_code = "def example(*args, **kwargs): pass"
tree = ast.parse(source_code)
func_node = tree.body[0]

signature = _get_signature(func_node)
print(signature)
# Output: "(*args, **kwargs)"
```

```python
source_code = "def example(a: int, b: str): pass"
tree = ast.parse(source_code)
func_node = tree.body[0]

signature = _get_signature(func_node)
print(signature)
# Output: "(a: int, b: str)"
```

**See also**  
- `ast.unparse` for converting AST nodes to Python source strings.  
- `ast.FunctionDef`, `ast.AsyncFunctionDef` for representing function nodes in the AST.
<!-- END: auto:agentic_docs.parsing.symbols._get_signature -->

<!-- BEGIN: auto:agentic_docs.parsing.symbols.parse_symbols_file (hash=43fbb708e6bcd46dcaeb0a32a32765cbf172d381931d3f5efcf67b7f9d2a50ce) -->
### `parse_symbols_file`

**Summary**  
Parses a Python source file to extract symbols (classes, functions, modules) into a structured format. Uses the AST to analyze the source code and collect metadata such as qualified names, docstrings, decorators, and line positions.

**Parameters**
- `path` (`Path`): Path to the Python source file to parse. Must be a valid `.py` file.
- `src_root` (`Path`): Root directory used to determine the module's qualified name (e.g., `pkg.module`).

**Returns**  
- `list[Symbol]`: A list of `Symbol` objects representing the parsed symbols from the file. Each `Symbol` includes the symbol's name, kind, file path, qualified name, parent, signature, docstring, line range, hash, and other metadata.

**Raises**  
- `Exception`: Any error during parsing (e.g., invalid syntax or file not found) is caught and handled silently by returning an empty list.

**Examples**  
```python
from pathlib import Path
from agentic_docs.types import Symbol
from your_module import parse_symbols_file

file_path = Path("example.py")
src_root = Path("src")
symbols = parse_symbols_file(file_path, src_root)
for symbol in symbols:
    print(symbol.qualname, symbol.kind)
```

**See also**  
`Symbol` class for detailed attributes and usage examples.
<!-- END: auto:agentic_docs.parsing.symbols.parse_symbols_file -->

<!-- BEGIN: auto:agentic_docs.parsing.symbols.index_repo (hash=edacbff8653be6866c840f961690b0e1fef8b14995801993b7f3703dec96987e) -->
### `index_repo`

**Summary**  
Indexes a Python repository by collecting all Python files from the specified root directory (or its `src` subdirectory, if present), and parses each file to extract symbols. Returns a list of all identified symbols.

**Parameters**  
- `root` (`str`): The root directory of the repository to index.  
- `all_` (`bool`, default `True`): If `True`, parse all files; if `False`, parse only specific files (currently unused).  
- `changed_only` (`bool`, default `False`): If `True`, filter to only process files that have changed (currently unused).  

**Returns**  
- `List[Symbol]`: A list of symbol objects extracted from Python files in the repository. Each `Symbol` represents a Python entity (e.g., class, function, variable).

**Raises**  
- `FileNotFoundError`: If the provided `root` or `src` directory does not exist.  
- `PermissionError`: If the script lacks permissions to access files/directories.  
- `OSError`: For general file system errors (e.g., invalid paths).  
- `SyntaxError` or `ParserError`: If `parse_symbols_file` fails to parse Python code (e.g., malformed syntax).  
- `TypeError`: If inputs (e.g., `root`) are not of the expected type.  

**Examples**  
```python
symbols = index_repo("/path/to/repo")
print(f"Found {len(symbols)} symbols in the repository.")
```

```python
# This currently does nothing, but would be used if 'changed_only' logic is implemented.
symbols = index_repo("/path/to/repo", changed_only=True)
```

```python
# Use the 'src' directory as the root
symbols = index_repo("/path/to/repo", all_=False)
```

**See also**  
- `collect_py_files`: Function used to gather Python files within the repository.  
- `parse_symbols_file`: Function used to extract symbols from individual Python files.
<!-- END: auto:agentic_docs.parsing.symbols.index_repo -->