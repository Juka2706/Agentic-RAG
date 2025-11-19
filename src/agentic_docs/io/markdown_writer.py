"""Markdown writer with idempotent section updates."""
from pathlib import Path
import re
from typing import Optional

class MarkdownWriter:
    def __init__(self, docs_root: Path):
        self.docs_root = docs_root

    def _get_file_path(self, symbol_qualname: str) -> Path:
        # Map pkg.module.Class -> docs/api/pkg/module.md
        parts = symbol_qualname.split(".")
        if len(parts) < 2:
            # Top level module or weird case
            return self.docs_root / "api" / f"{parts[0]}.md"
        
        # pkg/module.md
        # If it's a class/func inside a module, we want the module page
        # We assume the first N-1 parts are the module path if the last is a class/func
        # But we need to know if the symbol IS a module.
        # For now, let's assume we write to the parent module's page.
        # If symbol is 'pkg.mod', we write to 'pkg/mod.md'
        # If symbol is 'pkg.mod.func', we write to 'pkg/mod.md'
        
        # Heuristic: try to find the module part.
        # Since we don't have the symbol kind here easily without passing it,
        # we might need to rely on the caller passing the target file or logic.
        # Let's assume the orchestrator handles the path or we do a simple mapping.
        
        # Simple mapping:
        # a.b.c -> a/b.md (c is symbol)
        # a.b -> a/b.md (module itself)
        
        return self.docs_root / "api" / "/".join(parts[:-1]) / f"{parts[-1]}.md" # This is wrong for class methods

    def get_target_path(self, symbol_qualname: str) -> Path:
        # Improved mapping:
        # We really want one page per module.
        # So we need to know where the module ends.
        # For now, let's assume the last part is the symbol, unless it's a module.
        # This is tricky without metadata.
        # Let's assume standard structure: package.module.Symbol
        parts = symbol_qualname.split(".")
        if len(parts) == 1:
             return self.docs_root / "api" / f"{parts[0]}.md"
        
        # Check if the second to last part is a module? 
        # Let's just use the first 2 parts as package/module if available?
        # Or just all parts except last?
        
        # Let's try: docs/api/path/to/module.md
        # We will rely on the orchestrator to pass the correct file path or 
        # we just use a flat structure for now to be safe?
        # No, let's do:
        # pkg.mod.Class -> pkg/mod.md
        # pkg.mod -> pkg/mod.md
        
        # We'll assume the caller knows the file path or we just append .md to the file path from the symbol.
        # Actually, the Symbol object has 'file'. We can use that!
        # But here we don't have the symbol object.
        # Let's just take the path as an argument in write_section.
        pass

    def write_section(self, file_path: Path, symbol_id: str, content: str, source_hash: str):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if file_path.exists():
            text = file_path.read_text(encoding="utf-8")
        else:
            text = f"# {file_path.stem}\n\n"

        # Markers
        start_marker = f"<!-- BEGIN: auto:{symbol_id} (hash={source_hash}) -->"
        end_marker = f"<!-- END: auto:{symbol_id} -->"
        
        # Regex to find existing section
        # We look for BEGIN: auto:symbol_id .*? END: auto:symbol_id
        pattern = re.compile(
            rf"<!-- BEGIN: auto:{re.escape(symbol_id)} \(hash=.*?>.*?<!-- END: auto:{re.escape(symbol_id)} -->",
            re.DOTALL
        )
        
        new_section = f"{start_marker}\n{content}\n{end_marker}"
        
        if pattern.search(text):
            text = pattern.sub(new_section, text)
        else:
            text += f"\n\n{new_section}"
            
        file_path.write_text(text, encoding="utf-8")
