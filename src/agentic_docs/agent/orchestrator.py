"""Orchestrator for the Agentic RAG pipeline."""
from pathlib import Path
from typing import List, Optional
import os

from ..parsing.symbols import index_repo, Symbol
from ..index.embed import Embedder
from ..index.store_faiss import FAISSStore
from ..llm.local_llm import LocalLLM
from ..agent.agents import DocumentationAgents
from ..io.markdown_writer import MarkdownWriter

class Orchestrator:
    def __init__(self, config: dict):
        self.root = Path(config.get("root", "."))
        self.docs_root = Path(config.get("docs_root", "docs"))
        
        # Initialize components
        self.embedder = Embedder(
            model_name=config.get("embed_model", "intfloat/e5-base-v2"),
            device=config.get("device", "cpu")
        )
        self.store = FAISSStore(index_path=self.root / ".index")
        
        # LLM & Agents
        model_path = config.get("llm_model_path", "")
        is_local = config.get("llm_is_local", True)
        
        if not is_local:
            # Use API LLM
            from ..llm.api_llm import APILLM
            print(f"Using API LLM at {config.get('llm_api_base')}")
            llm = APILLM(
                base_url=config.get("llm_api_base"),
                api_key=config.get("llm_api_key"),
                model_name=model_path or "default" # Use model_path as model name for API
            )
            self.agents = DocumentationAgents(llm)
        elif model_path and Path(model_path).exists():
            # Use Local GGUF
            llm = LocalLLM(
                model_path=model_path,
                n_ctx=config.get("n_ctx", 4096),
                n_gpu_layers=config.get("n_gpu_layers", 0)
            )
            self.agents = DocumentationAgents(llm)
        else:
            print(f"Warning: No valid LLM configuration found. Generation will be disabled.")
            self.agents = None
        self.writer = MarkdownWriter(self.docs_root)

    def run(self, changed_only: bool = False):
        """Run the full pipeline."""
        print(f"Starting orchestration (changed_only={changed_only})...")
        
        # 1. Parse & Index
        symbols = index_repo(str(self.root), all_=not changed_only, changed_only=changed_only)
        print(f"Found {len(symbols)} symbols.")
        
        # Embed and Store (Naive full re-index for now)
        # In a real incremental system, we'd check hashes.
        texts = [s.docstring or s.signature or s.qualname for s in symbols]
        vectors = self.embedder.encode(texts)
        
        metadatas = [
            {
                "symbol_id": s.symbol_id,
                "qualname": s.qualname,
                "file": s.file,
                "hash": s.hash
            }
            for s in symbols
        ]
        
        self.store.add(vectors, metadatas)
        self.store.save(self.root / ".index")
        
        # 2. Generate & Write
        # For this MVP, we just process everything found.
        # In reality, we'd filter by 'changed' status.
        
        for sym in symbols:
            if sym.kind == "module": 
                continue # Skip modules for now, focus on classes/funcs
                
            print(f"Processing {sym.qualname}...")
            
            # Context retrieval
            # Find related symbols via vector search
            query_vec = self.embedder.encode([sym.docstring or sym.qualname])
            results = self.store.search(query_vec, k=3)
            
            context_str = "\n".join(
                [f"- {r['qualname']}" for r in results if r['qualname'] != sym.qualname]
            )
            
            # Read code
            # We need the actual code content. 
            # The symbol has start/end lines.
            try:
                file_content = Path(sym.file).read_text(encoding="utf-8").splitlines()
                code_segment = "\n".join(file_content[sym.start-1:sym.end])
            except Exception as e:
                print(f"Failed to read code for {sym.qualname}: {e}")
                continue

            # Generate
            if self.agents:
                try:
                    markdown = self.agents.process_symbol(
                        code=code_segment,
                        context=context_str,
                        existing_docs="" # TODO: Read existing docs if available
                    )
                    
                    # Write
                    # Determine target file
                    # For pkg.mod.Func, we want docs/api/pkg/mod.md
                    # We can use the symbol's file path to determine the doc path
                    try:
                        rel_path = Path(sym.file).relative_to(self.root / "src").with_suffix(".md")
                    except ValueError:
                        # Fallback for files outside src (e.g. tests)
                        rel_path = Path(sym.file).relative_to(self.root).with_suffix(".md")
                        
                    target_file = self.docs_root / "api" / rel_path
                    
                    self.writer.write_section(
                        file_path=target_file,
                        symbol_id=sym.symbol_id,
                        content=markdown,
                        source_hash=sym.hash
                    )
                except Exception as e:
                    print(f"Error processing {sym.qualname}: {e}")
            else:
                print(f"Skipping generation for {sym.qualname} (no LLM).")

        print("Orchestration complete.")
