MD_PROMPT = """You will generate Markdown documentation for the target symbol.
Use sections: Summary, Parameters, Returns, Raises, Examples, See also, Source.
Return only Markdown for the section boundaries provided.
Target:
kind: {kind}
qualname: {qualname}
signature: {signature}
Existing:
{existing}
Context:
{context}
"""
