from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSerializable
from ..llm.prompts import CODE_EXPERT_PROMPT, DOCS_EXPERT_PROMPT, AGENT_PROMPT, UPDATE_DOCS_PROMPT
import re

class DocumentationAgents:
    def __init__(self, llm):
        self.llm = llm
        
        # Static Chains
        self.code_expert = CODE_EXPERT_PROMPT | llm | StrOutputParser()
        self.docs_expert = DOCS_EXPERT_PROMPT | llm | StrOutputParser()
        self.docs_updater = UPDATE_DOCS_PROMPT | llm | StrOutputParser()

    def analyze_code(self, code: str, context: str = "") -> str:
        """Analyze code using static chain."""
        return self.code_expert.invoke({"code": code, "context": context})

    def ask_agent(self, code: str, context: str, scratchpad: str, tool_names: str, tools_desc: str) -> str:
        """Single step of the agent reasoning (stateless)."""
        input_text = f"Code:\n```python\n{code}\n```\n\nContext:\n{context}"
        
        prompt = AGENT_PROMPT.format(
            input=input_text,
            agent_scratchpad=scratchpad,
            tool_names=tool_names,
            tools=tools_desc
        )
        
        response = self.llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)

    def generate_docs(self, analysis: str, existing_docs: str = "") -> str:
        """Generate docs from analysis."""
        return self.docs_expert.invoke({"analysis": analysis, "existing_docs": existing_docs})

    def update_docs(self, analysis: str, existing_docs: str) -> str:
        """Update existing docs based on analysis."""
        return self.docs_updater.invoke({"analysis": analysis, "existing_docs": existing_docs})

    def clean_output(self, text: str) -> str:
        """Clean the LLM output to remove thinking tags and markdown fences."""
        # Remove <think> blocks (common in reasoning models)
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        
        # Remove markdown code fences if the model wrapped the whole output
        text = text.strip()
        if text.startswith("```markdown"):
            text = text[11:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        return text.strip()
