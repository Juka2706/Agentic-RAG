"""Orchestrator for the Agentic RAG pipeline."""
from pathlib import Path
from typing import List, Optional
import os
import signal
import sys
import atexit
import re
from tqdm import tqdm

from ..parsing.symbols import index_repo, Symbol
from ..index.embed import Embedder
from ..agent.agents import DocumentationAgents
from ..io.markdown_writer import MarkdownWriter
from ..agent.tools import read_file, list_directory, search_code

class Orchestrator:
    def __init__(self, config: dict):
        self.config = config
        self.root = Path(config.get("root", "."))
        self.docs_root = Path(config.get("docs_root", "docs"))
        self.mode = config.get("mode", "static")
        
        # Initialize components
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
        
        # Tools for Agentic Mode
        self.tools = {
            "read_file": read_file,
            "list_directory": list_directory,
            "search_code": search_code
        }

    def run(self, changed_only: bool = False):
        """Run the full pipeline."""
        print(f"Starting orchestration (mode={self.mode}, changed_only={changed_only})...")
        
        # 1. Parse & Index
        print("Parsing codebase...")
        symbols = index_repo(str(self.root), all_=not changed_only, changed_only=changed_only)
        print(f"Found {len(symbols)} symbols.")
        
        # Embed and Store (Naive full re-index for now)
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
        
        # 2. Generate & Write
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        max_workers = int(self.config.get("max_workers", 4))
        symbols_to_process = [s for s in symbols if s.kind != "module"]
        
        if max_workers <= 1:
            print("Generating documentation sequentially...")
            for sym in tqdm(symbols_to_process, desc="Generating docs", unit="symbol"):
                self._process_symbol_with_context(sym)
        else:
            print(f"Generating documentation with {max_workers} workers...")
            # We do context retrieval inside the worker to avoid pre-fetching everything if not needed
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(self._process_symbol_with_context, sym) for sym in symbols_to_process]
                
                for future in tqdm(as_completed(futures), total=len(futures), desc="Generating docs", unit="symbol"):
                    try:
                        future.result()
                    except Exception as e:
                        print(f"\nWorker failed: {e}")

        print("Orchestration complete.")

    def _process_symbol_with_context(self, sym: Symbol):
        """Helper to retrieve context and process symbol."""
        # Retrieve context
        query_vec = self.embedder.encode([sym.docstring or sym.qualname])
        results = self.store.search(query_vec, k=3)
        context_str = "\n".join([f"- {r['qualname']}" for r in results if r['qualname'] != sym.qualname])
        
        self._process_symbol(sym, context_str)

    def _process_symbol(self, sym: Symbol, context_str: str):
        """Process a single symbol: generate docs, write."""
        try:
            file_content = Path(sym.file).read_text(encoding="utf-8").splitlines()
            code_segment = "\n".join(file_content[sym.start-1:sym.end])
        except Exception as e:
            print(f"Failed to read code for {sym.qualname}: {e}")
            return

        # Generate Analysis
        try:
            if self.mode == "agentic":
                analysis = self._run_agent_loop(code_segment, context_str)
            else:
                analysis = self.agents.analyze_code(code_segment, context_str)
            
            # Determine target file path FIRST
            try:
                rel_path = Path(sym.file).relative_to(self.root / "src").with_suffix(".md")
            except ValueError:
                rel_path = Path(sym.file).relative_to(self.root).with_suffix(".md")
            
            target_file = self.docs_root / "api" / rel_path
            
            # Check for existing docs (ONLY in Agentic Mode)
            existing_content = ""
            if self.mode == "agentic" and target_file.exists():
                existing_content = target_file.read_text(encoding="utf-8")
            
            # Generate or Update
            if existing_content:
                print(f"  [Update] Updating existing docs for {sym.qualname}")
                markdown = self.agents.update_docs(analysis, existing_content)
            else:
                action = "Create" if not target_file.exists() else "Overwrite"
                print(f"  [{action}] Generating new docs for {sym.qualname}")
                markdown = self.agents.generate_docs(analysis, "")
            
            markdown = self.agents.clean_output(markdown)
            
            # Write
            if self.config.get("dry_run"):
                # print(f"[Dry Run] Would write to {target_file}")
                pass
            else:
                self.writer.write_section(
                    file_path=target_file,
                    symbol_id=sym.symbol_id,
                    content=markdown,
                    source_hash=sym.hash
                )
        except Exception as e:
            print(f"Error processing {sym.qualname}: {e}")

    def _run_agent_loop(self, code: str, context: str) -> str:
        """Orchestrator-managed ReAct loop."""
        tool_names = ", ".join(self.tools.keys())
        tools_desc = "\n".join([f"- {name}: {tool.description}" for name, tool in self.tools.items()])
        
        scratchpad = ""
        
        # Limit iterations
        for i in range(5):
            # Ask Agent what to do
            output = self.agents.ask_agent(code, context, scratchpad, tool_names, tools_desc)
            
            # Append to scratchpad
            scratchpad += output
            
            # Check for Final Answer
            if "Final Answer:" in output:
                return output.split("Final Answer:")[-1].strip()
            
            # Check for Action
            action_match = re.search(r"Action:\s*(.*?)\nAction Input:\s*(.*)", output, re.DOTALL)
            if action_match:
                action = action_match.group(1).strip()
                action_input = action_match.group(2).strip()
                
                # Execute tool (Orchestrator does this!)
                if action in self.tools:
                    print(f"  [Orchestrator] Executing tool {action} with '{action_input}'")
                    try:
                        observation = self.tools[action].invoke(action_input)
                    except Exception as e:
                        observation = f"Error: {e}"
                else:
                    observation = f"Error: Tool '{action}' not found. Available tools: {tool_names}"
                
                scratchpad += f"\nObservation: {observation}\nThought:"
            else:
                return output.strip()
                
        return "Error: Agent exceeded maximum iterations without a final answer."
    
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
