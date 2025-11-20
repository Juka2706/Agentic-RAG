# agents



<!-- BEGIN: auto:agentic_docs.agent.agents.DocumentationAgents (hash=c5852b1cba5490cce0434d0225e35b2033d474a881b157ea3c3ac42cc57537a9) -->
### `DocumentationAgents`

**Summary**
A class that leverages language model chains to analyze code and generate documentation for symbols. It provides methods to clean LLM output and orchestrate the full documentation generation process.

**Parameters**
- `llm` (Chain): A LangChain-compatible chain representing the language model. Expected to handle prompt templating, LLM invocation, and output parsing.

**Returns**
- `DocumentationAgents`: An instance of the class with initialized chains for code analysis and documentation generation.

---

### `analyze_code(code: str, context: Optional[str] = None) -> str`

**Summary**
Analyzes provided code using the `code_expert` chain to generate insights about its structure, functionality, and dependencies.

**Parameters**
- `code` (str): The source code to be analyzed.
- `context` (Optional[str]): Additional contextual information to guide the analysis (e.g., project scope, API constraints).

**Returns**
- `str`: The analysis result from the `code_expert` chain, typically containing structured insights about the code.

---

### `generate_docs(analysis: str, existing_docs: Optional[str] = None) -> str`

**Summary**
Generates human-readable documentation based on the analysis of code and any existing documentation.

**Parameters**
- `analysis` (str): The analysis output from `analyze_code`, used to inform the documentation content.
- `existing_docs` (Optional[str]): Pre-existing documentation to be merged with newly generated content.

**Returns**
- `str`: The generated documentation string, formatted according to the `docs_expert` chain's instructions.

---

### `_clean_output(text: str) -> str`

**Summary**
Removes extraneous text and markdown formatting from LLM outputs, ensuring clean, structured documentation.

**Parameters**
- `text` (str): The raw output from the LLM chain requiring cleanup.

**Returns**
- `str`: The cleaned text with:
  - Thinking/processing blocks removed (`"Think: ..."`).
  - Markdown code fences (```) stripped.
  - Other formatting artifacts eliminated.

**Raises**
- `re.error`: If regex patterns in cleaning are invalid (e.g., due to typos like `r'<tool_call>'` in the original code).

---

### `process_symbol(code: str, context: Optional[str] = None, existing_docs: Optional[str] = None) -> str`

**Summary**
Orchestrates the full documentation generation workflow: analyzing code, generating docs, and cleaning output.

**Parameters**
- `code` (str): The source code to document.
- `context` (Optional[str]): Contextual information for analysis.
- `existing_docs` (Optional[str]): Pre-existing documentation to merge with generated content.

**Returns**
- `str`: Final cleaned documentation string ready for use.

**Examples**
```python
agent = DocumentationAgents(llm=llm_chain)
docs = agent.process_symbol(
    code="def add(a, b):\n    return a + b",
    context="Math utility functions for a calculator app",
    existing_docs="See also: subtract()"
)
print(docs)
```

**See also**
- `analyze_code`: For detailed code analysis before documentation.
- `generate_docs`: For generating documentation from analysis results.
<!-- END: auto:agentic_docs.agent.agents.DocumentationAgents -->

<!-- BEGIN: auto:agentic_docs.agent.agents.DocumentationAgents.__init__ (hash=e54901fa8a71c38c52dfacd8289b72394802c019047c7e11684f300e66deca1c) -->
### `agentic_docs.agent.Agent.__init__`

**Summary**
Initializes an agent with a language model and creates two expert prompt chains for code analysis and documentation generation.

**Parameters**
- `llm` (LangChain LLM object): The language model instance used for generating responses. Expected to be compatible with LangChain's prompt chaining system (e.g., `ChatOpenAI`, `ChatAnthropic`, etc.)

**Returns**
- `None`: The constructor does not return a value. It initializes instance attributes (`self.llm`, `self.code_expert`, `self.docs_expert`) instead.

**Raises**
- `TypeError`: If the `llm` parameter is not a compatible LangChain LLM object.
- `ValueError`: If `CODE_EXPERT_PROMPT`/`DOCS_EXPERT_PROMPT` are invalid templates.
- `Exception`: Any errors during prompt chain construction (e.g., invalid template syntax, missing parameters).

**Examples**
```python
from langchain.chat_models import ChatOpenAI
from agentic_docs.agent import Agent

llm = ChatOpenAI(model_name="gpt-3.5-turbo")
agent = Agent(llm)

# Code analysis
code_response = agent.code_expert.invoke("How to fix this Python error?")
print(code_response)

# Documentation generation
doc_response = agent.docs_expert.invoke("Generate documentation for this function")
print(doc_response)
```

**See also**
- `CODE_EXPERT_PROMPT` (agentic_docs)
- `DOCS_EXPERT_PROMPT` (agentic_docs)
- `StrOutputParser` (langchain.output_parsers)
<!-- END: auto:agentic_docs.agent.agents.DocumentationAgents.__init__ -->

<!-- BEGIN: auto:agentic_docs.agent.agents.DocumentationAgents.analyze_code (hash=7157b85b5492289956e4ad49cb88711048da7d63a9ccbf56f7b720859e050a1d) -->
### `analyze_code`

**Summary**
The `analyze_code` method is a wrapper for invoking a code analysis expert (`self.code_expert`) with the provided code and context. It passes these parameters as a dictionary to the `invoke` method of the `code_expert`, which performs tasks like syntax checking, documentation generation, or semantic analysis.

**Parameters**
- `code` (str): The source code to be analyzed. This is a required parameter.
- `context` (str, optional): Additional information or background context for the code analysis. Defaults to an empty string if not provided.

**Returns**
- (str): The result of the code analysis, returned as a string. The exact content depends on the implementation of `self.code_expert.invoke()`. It could include error messages, suggestions, documentation, or structural analysis results.

**Raises**
- `AttributeError`: If `self.code_expert` is not properly initialized or does not have an `invoke` method.
- `TypeError`: If the `code` or `context` parameters are not strings.
- `RuntimeError`: Any exceptions raised during the execution of `code_expert.invoke()`, such as invalid input or internal errors.
- `ValueError`: If the input code is invalid (e.g., malformed syntax), depending on the `code_expert` implementation.

**Examples**
```python
result = agent.analyze_code(
    code="def add(a, b):\n    return a + b",
    context="A function to sum two integers"
)
print(result)
# Output might be: "The 'add' function is syntactically correct and follows PEP8 guidelines."
```

```python
result = agent.analyze_code(
    code="import os\nos.system('ls')",
    context="A script to list directory contents"
)
print(result)
# Output might be: "The code executes a system command. Ensure it's secure in production environments."
```

```python
result = agent.analyze_code(code="print('Hello, world!')")
print(result)
# Output might be: "The code is valid Python and outputs 'Hello, world!' upon execution."
```

**See also**
- `code_expert` for details about the code analysis expert implementation.
<!-- END: auto:agentic_docs.agent.agents.DocumentationAgents.analyze_code -->

<!-- BEGIN: auto:agentic_docs.agent.agents.DocumentationAgents.generate_docs (hash=15572dfeec6bac725d33075319083a2c162f21169c7ac308ac685d56f6fc6190) -->
### `generate_docs`

**Summary**  
Generates documentation based on an analysis and optional existing documentation, by invoking an internal `docs_expert` agent.

**Parameters**  
- `analysis` (str): A string containing the analysis or instructions for generating the document.  
- `existing_docs` (str, optional): A string representing pre-existing documentation to be combined with the new analysis. Defaults to an empty string.

**Returns**  
- (str): The output string generated by the `docs_expert.invoke` method. Represents the finalized documentation based on the provided analysis and existing documents.

**Raises**  
- `AttributeError`: If `self.docs_expert` is not properly initialized (e.g., missing the `invoke` method).  
- `TypeError`: If the input parameters (e.g., malformed analysis or existing_docs) are invalid.  
- `ValueError`: If the input is incomplete or invalid (e.g., empty `analysis`).  
- Other exceptions raised by the `docs_expert.invoke` method.

**Examples**  
```python
agent = DocumentationAgents()
result = agent.generate_docs(analysis="User authentication flow analysis", existing_docs="")
print(result)
```

```python
agent = DocumentationAgents()
result = agent.generate_docs(
    analysis="Update API endpoints for v2",
    existing_docs="API v1 documentation: https://example.com/v1-docs"
)
print(result)
```

```python
try:
    result = agent.generate_docs(analysis="", existing_docs="some content")
except ValueError as e:
    print(f"Invalid analysis: {e}")
```

**See also**  
- `docs_expert` - The agent responsible for generating documentation.
<!-- END: auto:agentic_docs.agent.agents.DocumentationAgents.generate_docs -->

<!-- BEGIN: auto:agentic_docs.agent.agents.DocumentationAgents._clean_output (hash=1beea1be6fdb36d3e10dd996f93db7052f4e65d18aec32243f65ef120b72cec2) -->
### `_clean_output`

**Summary**  
Cleans the input text by removing markdown code fences (````...```) and any leading/trailing whitespace. This is useful for sanitizing outputs from large language models to extract only the relevant content.

**Parameters**  
- `text` (str): The input string containing potential markdown code fences and extraneous whitespace.

**Returns**  
- (str): The cleaned string with markdown code fences removed and leading/trailing whitespace stripped.

**Examples**  
```python
cleaned = _clean_output("```python\nprint('Hello')\n```  Extra spaces")
# Output: "print('Hello')"
```

**See also**  
- `strip()`: For removing leading/trailing whitespace.  
- `re.sub()`: Used internally to remove markdown code fences.
<!-- END: auto:agentic_docs.agent.agents.DocumentationAgents._clean_output -->

<!-- BEGIN: auto:agentic_docs.agent.agents.DocumentationAgents.process_symbol (hash=2a17bec9f098724bb8f66ca6b7479fdf08852087ccccad95c39869a9322524f9) -->
### `process_symbol`

**Summary**  
Orchestrates the full pipeline for processing a single code symbol. It analyzes the provided code, generates documentation using the analysis and existing documentation, and returns the cleaned markdown output.

**Parameters**  
- `code` (str): The code string to be analyzed (e.g., a function, class, or snippet).  
- `context` (str, optional): Additional context for analysis. Defaults to an empty string.  
- `existing_docs` (str, optional): Pre-existing documentation to merge or extend with new analysis. Defaults to an empty string.  

**Returns**  
- (str): The final cleaned markdown output after analysis and documentation generation.  

**Raises**  
- `Exception`: Any exceptions raised by `analyze_code`, `generate_docs`, or `_clean_output` are propagated as-is.  

**Examples**  
```python
result = processor.process_symbol(
    code="def square(x): return x ** 2",
    context="Math utilities for data processing",
    existing_docs="# Square Function\nCalculates square of a number."
)
```

```python
result = processor.process_symbol(
    code="class User:\n    def __init__(self, name):\n        self.name = name"
)
```

```python
result = processor.process_symbol(
    code="def multiply(a, b):\n    return a * b",
    existing_docs="# Multiply Function\nMultiplies two numbers."
)
```

**See also**  
- `analyze_code`  
- `generate_docs`  
- `_clean_output`
<!-- END: auto:agentic_docs.agent.agents.DocumentationAgents.process_symbol -->