"""Prompts for the agentic documentation generation."""
from langchain_core.prompts import PromptTemplate

CODE_EXPERT_PROMPT = PromptTemplate(
    input_variables=["code", "context"],
    template="""You are a Senior Python Engineer (Code Expert).
Your task is to analyze the following Python code and its context to understand its behavior, parameters, return values, and potential exceptions.

Context (related symbols):
{context}

Code to Analyze:
```python
{code}
```

Provide a detailed technical analysis including:
1. Summary of functionality.
2. Parameters (name, type, description).
3. Return value (type, description).
4. Exceptions raised.
5. Usage examples.

Analysis:
"""
)

DOCS_EXPERT_PROMPT = PromptTemplate(
    input_variables=["analysis", "existing_docs"],
    template="""You are a Technical Writer (Documentation Expert).
Your task is to generate high-quality Markdown API documentation based on the technical analysis provided by the Code Expert.

Technical Analysis:
{analysis}

Existing Documentation (if any):
{existing_docs}

Generate the Markdown documentation following this structure:
### `SymbolName`

**Summary**
...

**Parameters**
- `name` (type): description

**Returns**
- (type): description

**Raises**
- `Exception`: description

**Examples**
```python
...
```

**See also**
...

CRITICAL INSTRUCTIONS:
1. Output ONLY the Markdown content.
2. DO NOT output any "thinking" process, reasoning, or internal monologue.
3. DO NOT output any conversational text like "Here is the documentation".
4. DO NOT wrap the output in markdown code blocks (e.g. ```markdown ... ```). Just output the raw markdown.
"""
)

AGENT_PROMPT = PromptTemplate(
    input_variables=["input", "agent_scratchpad", "tool_names", "tools"],
    template="""You are a Senior Python Engineer (Research Agent).
Your task is to analyze the provided Python code to understand its behavior, parameters, return values, and potential exceptions.
You have access to tools to read files and search the codebase if you need more context (e.g. to understand a custom type or a called function).

Tools Available:
{tools}

Use the following format:

Question: the input code to analyze
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the detailed technical analysis of the code (same format as the Code Expert).

Begin!

Question: Analyze the following code:
{input}


Thought:{agent_scratchpad}"""
)

UPDATE_DOCS_PROMPT = PromptTemplate(
    input_variables=["analysis", "existing_docs"],
    template="""You are a Technical Editor (Documentation Maintainer).
Your task is to UPDATE existing documentation to reflect changes in the code, based on a new technical analysis.

Existing Documentation:
{existing_docs}

New Technical Analysis of Code:
{analysis}

Instructions:
1. Compare the New Analysis with the Existing Documentation.
2. Identify what has changed (new parameters, changed return types, new exceptions, logic changes).
3. UPDATE the Existing Documentation to reflect these changes.
4. PRESERVE the existing style, tone, and any manual additions (like examples or detailed descriptions) that are still valid.
5. DO NOT rewrite the entire document if not necessary. Just edit the relevant sections.
6. Output the FULL updated Markdown content.

CRITICAL INSTRUCTIONS:
1. Output ONLY the Markdown content.
2. DO NOT output any "thinking" process.
3. DO NOT output "Here is the updated doc".
4. DO NOT wrap output in markdown code blocks.
"""
)
