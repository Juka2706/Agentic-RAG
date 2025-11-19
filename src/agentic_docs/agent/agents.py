from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSerializable
from ..llm.prompts import CODE_EXPERT_PROMPT, DOCS_EXPERT_PROMPT

class DocumentationAgents:
    def __init__(self, llm):
        self.llm = llm
        self.code_expert = CODE_EXPERT_PROMPT | llm | StrOutputParser()
        self.docs_expert = DOCS_EXPERT_PROMPT | llm | StrOutputParser()

    def analyze_code(self, code: str, context: str = "") -> str:
        return self.code_expert.invoke({"code": code, "context": context})

    def generate_docs(self, analysis: str, existing_docs: str = "") -> str:
        return self.docs_expert.invoke({"analysis": analysis, "existing_docs": existing_docs})

    def process_symbol(self, code: str, context: str = "", existing_docs: str = "") -> str:
        """Orchestrates the full pipeline for a single symbol."""
        analysis = self.analyze_code(code, context)
        markdown = self.generate_docs(analysis, existing_docs)
        return markdown
