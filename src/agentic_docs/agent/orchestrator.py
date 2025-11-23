"""Orchestrator for the Agentic RAG pipeline."""
from pathlib import Path
from typing import List, Optional
import os
import signal
import sys
import atexit
from tqdm import tqdm

from ..parsing.symbols import index_repo, Symbol
from ..index.embed import Embedder
from ..index.embed import Embedder

from ..agent.agents import DocumentationAgents
from ..io.markdown_writer import MarkdownWriter

class Orchestrator:
    def __init__(self, config: dict):
        self.config = config
        self.root = Path(config.get("root", "."))
        self.docs_root = Path(config.get("docs_root", "docs"))
        
        # Initialize components
        self.embedder = Embedder(
            model_name=config.get("embed_model", "intfloat/e5-base-v2"),
            device=config.get("device", "cpu")
        )
        
        self.embedder = Embedder(
            model_name=config.get("embed_model", "intfloat/e5-base-v2"),
            device=config.get("device", "cpu")
        )
        
        from ..index.store_qdrant import QdrantStore
        self.store = QdrantStore(index_path=self.root / ".qdrant")
        print("Using Qdrant vector store.")
        
        # Register cleanup handlers
        atexit.register(self._cleanup)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # LLM & Agents
        model_name = config.get("llm_model_name", "default")
        
        # Use API LLM
        from ..llm.api_llm import APILLM
        print(f"Using API LLM at {config.get('llm_api_base')}")
        llm = APILLM(
            base_url=config.get("llm_api_base"),
            api_key=config.get("llm_api_key"),
            model_name=model_name
        )
        self.agents = DocumentationAgents(llm)
        self.writer = MarkdownWriter(self.docs_root)

    def run(self, changed_only: bool = False):
        """Run the full pipeline."""
        print(f"Starting orchestration (changed_only={changed_only})...")
        
        # 1. Parse & Index
        print("Parsing codebase...")
        symbols = index_repo(str(self.root), all_=not changed_only, changed_only=changed_only)
        print(f"Found {len(symbols)} symbols.")
        
        # Embed and Store (Naive full re-index for now)
        # In a real incremental system, we'd check hashes.
        print("Embedding symbols...")
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
        
        print("Storing embeddings in Qdrant...")
        self.store.add(vectors, metadatas)
        self.store.add(vectors, metadatas)
        # self.store.save(self.root / ".index") # Qdrant saves automatically
        
        # 2. Generate & Write
        # For this MVP, we just process everything found.
        # In reality, we'd filter by 'changed' status.
        
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        # Default to 4 workers, or configurable
        max_workers = int(self.config.get("max_workers", 4))
        
        # Filter out modules first
        symbols_to_process = [s for s in symbols if s.kind != "module"]
        
        if max_workers <= 1:
            print("Generating documentation sequentially...")
            for sym in tqdm(symbols_to_process, desc="Generating docs", unit="symbol"):
                query_vec = self.embedder.encode([sym.docstring or sym.qualname])
                results = self.store.search(query_vec, k=3)
                context_str = "\n".join([f"- {r['qualname']}" for r in results if r['qualname'] != sym.qualname])
                
                self._process_symbol(sym, context_str)
        else:
            print(f"Generating documentation with {max_workers} workers...")
            
            # Retrieve context for all symbols first (with progress bar)
            symbol_contexts = []
            for sym in tqdm(symbols_to_process, desc="Retrieving context", unit="symbol"):
                query_vec = self.embedder.encode([sym.docstring or sym.qualname])
                results = self.store.search(query_vec, k=3)
                context_str = "\n".join([f"- {r['qualname']}" for r in results if r['qualname'] != sym.qualname])
                symbol_contexts.append((sym, context_str))
            
            # Generate in parallel (with progress bar)
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(self._process_symbol, sym, ctx) for sym, ctx in symbol_contexts]
                
                # Wait for completion with progress bar
                for future in tqdm(as_completed(futures), total=len(futures), desc="Generating docs", unit="symbol"):
                    try:
                        future.result()
                    except Exception as e:
                        print(f"\nWorker failed: {e}")

        print("Orchestration complete.")

    def _process_symbol(self, sym: Symbol, context_str: str):
        """Process a single symbol: generate docs, write."""
        # Read code
        # We need the actual code content. 
        # The symbol has start/end lines.
        try:
            file_content = Path(sym.file).read_text(encoding="utf-8").splitlines()
            code_segment = "\n".join(file_content[sym.start-1:sym.end])
        except Exception as e:
            print(f"Failed to read code for {sym.qualname}: {e}")
            return

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
                
                if self.config.get("dry_run"):
                    print(f"[Dry Run] Would write to {target_file}")
                else:
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
    
    def _cleanup(self):
        """Clean up resources on exit."""
        if hasattr(self, 'store') and self.store:
            try:
                self.store.close()
                print("Closed Qdrant connection.")
            except Exception:
                pass
    
    def _signal_handler(self, signum, frame):
        """Handle interrupt signals gracefully."""
        print(f"\nReceived signal {signum}. Cleaning up...")
        self._cleanup()
        sys.exit(0)
