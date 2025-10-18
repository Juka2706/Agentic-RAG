# Agentic RAG for Automated Markdown Documentation

This document contains: a complete project plan, milestones, tech stack, repo structure, and starter file templates with in-file instructions so you can initialize the repository immediately.

---

## 1) Project summary
**Goal** Build an agentic RAG system that parses a Python codebase and generates or updates **Markdown** API documentation under `docs/`, with selective regeneration based on git diffs and a lightweight dependency graph. Compare against three baselines (classical, non‑RAG LLM, static RAG).

**Outputs**
- Deterministic Markdown pages under `docs/api/...` with stable section markers.
- Optional MkDocs site.
- CI pipeline that proposes doc updates on PRs and applies on main.
- Evaluation reports comparing quality and efficiency versus baselines.

**Constraints** Linux, Python 3.11, local models where possible, minimal external services.

---

## 2) Milestones (6–8 weeks, part‑time)
**W1** Schema + parser
- Define `Symbol`/`Chunk` metadata.
- Implement AST parser, file walker, hashing.

**W2** Embeddings + index
- Build embed text constructor.
- Implement FAISS index + metadata side store.
- Search API + filters.

**W3** LLM writer (Markdown)
- Prompt templates, local LLM interface.
- Validators (parameters/returns/examples).
- Markdown writer with section guards.

**W4** Agent controller
- Git diff detector, impact analysis, dependency map.
- Budgeting and retry/refine loop.

**W5** CI + repo integration
- GitHub Actions for PR propose and main apply.
- Logging, config via Pydantic.

**W6** Baselines + eval harness
- Classical (pdoc/Sphinx), Non‑RAG LLM, Static RAG.
- Commit‑replay evaluation and reporting.

**W7–8 (optional)**
- MMR reranking, Qdrant backend, ablations, MkDocs publishing.

---

## 3) Tech stack
- **Parsing** `ast` (optionally `libcst` for comments)
- **Embeddings** `sentence-transformers` (e5/bge small)
- **Vector DB** `faiss-cpu` initially (optional `qdrant-client`)
- **LLM runtime** `llama-cpp-python` (CPU/GPU) or `vllm` (GPU)
- **Config** `pydantic-settings`
- **Eval** `pandas`, `matplotlib`
- **Docs site** `mkdocs`, `mkdocs-material`

---

## 4) Repository layout (create all files/directories)
```
agentic-md-docs/
  .gitignore
  .env.example
  LICENSE
  README.md
  CONTRIBUTING.md
  pyproject.toml
  setup.cfg
  Makefile
  mkdocs.yml                 # optional site
  docs/
    index.md
    style_guide.md
    api/.gitkeep
  examples/
    toy_repo/
      src/pkg/__init__.py
      src/pkg/module_a.py
  scripts/
    bootstrap.sh
    run_local_llm.sh
  .github/workflows/
    ci.yml
    pages.yml                # optional: publish MkDocs
  src/agentic_docs/
    __init__.py
    config.py
    cli.py
    logging_utils.py
    types.py
    parsing/
      __init__.py
      symbols.py
      relations.py
    index/
      __init__.py
      embed.py
      store_faiss.py
      store_qdrant.py
      search.py
      mmr.py
      metadata_store.py
    llm/
      __init__.py
      local_llm.py
      prompts.py
      validate.py
      writer_md.py
    agent/
      __init__.py
      diff.py
      impact.py
      planner.py
      orchestrator.py
      budget.py
    io/
      __init__.py
      fs.py
      git.py
      markdown_writer.py
      source_links.py
    eval/
      __init__.py
      metrics.py
      datasets.py
      run_bench.py
    baselines/
      __init__.py
      classical_pdoc.py
      nonrag_llm.py
      static_rag.py
  tests/
    test_parsing.py
    test_index.py
    test_writer_md.py
    test_agent.py
```

---

## 5) File templates and instructions
Paste the following contents into the corresponding files. Adjust TODOs.

### 5.1 Root files

**`.gitignore`**
```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
.env

# Build and cache
/.cache/
/.mypy_cache/
/.pytest_cache/
/.bench/

# Index/embeddings artifacts
/data/
/index/

# MkDocs site
/site/
```

**`.env.example`**
```ini
# Copy to .env and adjust
EMBED_MODEL=intfloat/e5-base-v2
LLM_MODEL=codellama-7b-instruct.Q4_K_M.gguf
VECTOR_BACKEND=faiss
DOCS_ROOT=docs
SRC_ROOT=src
```

**`LICENSE`**
```
MIT License

Copyright (c) 2025 <Your Name>

Permission is hereby granted, free of charge, to any person obtaining a copy ...
```

**`README.md`**
```markdown
# Agentic RAG for Markdown API Docs

Generates and maintains Markdown API docs (`docs/api/...`) from a Python codebase using an agentic RAG loop. Selective updates based on git diffs and a dependency map.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
cp .env.example .env
make index-all
make propose-md  # dry-run on toy repo
```

## Repo layout
- `src/agentic_docs`: core library and CLI
- `docs/`: generated Markdown
- `examples/toy_repo`: small repo for testing

## Baselines and evaluation
See `src/agentic_docs/baselines` and `src/agentic_docs/eval`.
```

**`CONTRIBUTING.md`**
```markdown
## Conventions
- Python 3.11, black + isort, flake8.
- Deterministic writes: only change sections whose source hash changed.
- Tests required for parsing, writer, and agent planning.
```

**`pyproject.toml`**
```toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "agentic-md-docs"
version = "0.1.0"
description = "Agentic RAG for generating Markdown API docs"
authors = [{name = "Your Name"}]
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
  "pydantic>=2.7",
  "pydantic-settings>=2.3",
  "sentence-transformers>=2.7",
  "faiss-cpu>=1.8",
  "numpy>=1.26",
  "markdown-it-py>=3.0",
  "jinja2>=3.1",
  "pyyaml>=6.0",
  "click>=8.1",
  "networkx>=3.2",
  "gitpython>=3.1",
  "llama-cpp-python>=0.2; platform_system != 'Windows'",
  "pandas>=2.2",
  "matplotlib>=3.8",
]

[project.optional-dependencies]
qdrant = ["qdrant-client>=1.9"]
dev = ["pytest", "black", "isort", "flake8", "mdformat"]

[project.scripts]
agentic-docs = "agentic_docs.cli:main"
```

**`setup.cfg`**
```ini
[flake8]
max-line-length = 100
exclude = .venv,build,site

[isort]
profile = black
```

**`Makefile`**
```make
.PHONY: format test index-all index-changed propose-md apply-md eval

format:
	black src tests
	isort src tests

test:
	pytest -q

index-all:
	agentic-docs index --all --root .

index-changed:
	agentic-docs index --changed-only --root .

propose-md:
	agentic-docs generate --changed-only --markdown --dry-run

apply-md:
	agentic-docs generate --changed-only --markdown --write

eval:
	agentic-docs eval --repo ./examples/toy_repo
```

**`mkdocs.yml`**
```yaml
site_name: Agentic MD Docs
theme:
  name: material
nav:
  - Home: index.md
  - Style Guide: style_guide.md
  - API:
      - pkg.module_a: api/pkg/module_a.md
markdown_extensions:
  - toc:
      permalink: true
```

**`docs/index.md`**
```markdown
# Project Documentation

This site hosts the generated API docs. See the API section in the navigation.
```

**`docs/style_guide.md`**
```markdown
# Markdown Style Guide (Generation)
- Headings: # module, ## class, ### method/function.
- Sections: Summary, Parameters, Returns, Raises, Examples, See also, Source.
- Use fenced code blocks for examples.
- Keep summaries under 2 sentences.
```

**`scripts/bootstrap.sh`**
```bash
#!/usr/bin/env bash
set -euo pipefail
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp -n .env.example .env || true
```

**`scripts/run_local_llm.sh`**
```bash
#!/usr/bin/env bash
# Example: download a GGUF and run llama.cpp server if desired
# TODO: implement according to your environment
```

**`.github/workflows/ci.yml`**
```yaml
name: ci
on:
  pull_request:
    paths: ["**/*.py", "docs/**"]
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -e .[dev]
      - run: make format
      - run: make test
      - name: Index changed files
        run: agentic-docs index --changed-only --root .
      - name: Propose docs (PR) or apply (main)
        run: |
          if [ "${{ github.event_name }}" = "pull_request" ]; then
            agentic-docs generate --changed-only --markdown --dry-run
          else
            agentic-docs generate --changed-only --markdown --write
          fi
```

**`.github/workflows/pages.yml`** (optional)
```yaml
name: docs
on:
  push:
    branches: [main]
jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -e . mkdocs mkdocs-material
      - run: agentic-docs generate --all --markdown --write
      - run: mkdocs gh-deploy --force
```

---

### 5.2 Core library

**`src/agentic_docs/__init__.py`**
```python
__all__ = [
    "config", "cli", "types",
]
```

**`src/agentic_docs/config.py`**
```python
from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    root: str = "."
    src_root: str = "src"
    docs_root: str = "docs"
    embed_model: str = "intfloat/e5-base-v2"
    llm_model: str = "codellama-7b-instruct.Q4_K_M.gguf"
    vector: Literal["faiss", "qdrant"] = "faiss"
    k: int = 8
    budget_tokens: int = 200_000

settings = Settings()  # reads from env
```

**`src/agentic_docs/types.py`**
```python
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Symbol:
    symbol_id: str
    kind: str  # module, class, function, method
    file: str
    qualname: str
    parent: Optional[str]
    signature: Optional[str]
    docstring: Optional[str]
    start: int
    end: int
    hash: str
    imports: List[str]
```

**`src/agentic_docs/logging_utils.py`**
```python
import logging

def get_logger(name: str = "agentic") -> logging.Logger:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    return logging.getLogger(name)
```

**`src/agentic_docs/cli.py`**
```python
import click
from .config import settings
from .parsing.symbols import index_repo
from .llm.writer_md import generate_markdown_for_changes
from .eval.run_bench import run_eval

@click.group()
def main():
    pass

@main.command()
@click.option("--all", "all_", is_flag=True, help="Index entire repo")
@click.option("--changed-only", is_flag=True, help="Index only changed files")
@click.option("--root", default=".")
def index(all_, changed_only, root):
    """Parse and index codebase."""
    index_repo(root=root, all_=all_, changed_only=changed_only)

@main.command()
@click.option("--changed-only", is_flag=True)
@click.option("--markdown", is_flag=True, default=True)
@click.option("--dry-run", is_flag=True)
@click.option("--write", is_flag=True)
def generate(changed_only, markdown, dry_run, write):
    generate_markdown_for_changes(changed_only=changed_only, dry_run=dry_run, write=write)

@main.command()
@click.option("--repo", required=True)
def eval(repo):
    run_eval(repo)

if __name__ == "__main__":
    main()
```

#### Parsing
**`src/agentic_docs/parsing/symbols.py`**
```python
"""Walk files, parse AST, extract Symbol records. TODO: implement full extraction."""
from pathlib import Path
import ast, hashlib
from ..types import Symbol

IGNORE = [".venv", "site-packages", "build", "dist"]

def _sha(s: str) -> str:
    import hashlib
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def collect_py_files(root: str) -> list[Path]:
    r = Path(root)
    files = []
    for p in r.rglob("*.py"):
        if any(x in p.parts for x in IGNORE):
            continue
        files.append(p)
    return files

def module_qualname(path: Path, src_root: Path) -> str:
    rel = path.relative_to(src_root).with_suffix("")
    return ".".join(rel.parts)

def parse_symbols_file(path: Path, src_root: Path) -> list[Symbol]:
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(path))
    mod = module_qualname(path, src_root)
    out: list[Symbol] = []

    class V(ast.NodeVisitor):
        def visit_ClassDef(self, n):
            start, end = n.lineno, n.end_lineno
            out.append(Symbol(
                symbol_id=f"{mod}.{n.name}", kind="class", file=str(path),
                qualname=f"{mod}.{n.name}", parent=mod, signature=None,
                docstring=ast.get_docstring(n), start=start, end=end,
                hash=_sha("\n".join(src.splitlines()[start-1:end])), imports=[],
            ))
            self.generic_visit(n)
        def visit_FunctionDef(self, n):
            start, end = n.lineno, n.end_lineno
            out.append(Symbol(
                symbol_id=f"{mod}.{n.name}", kind="function", file=str(path),
                qualname=f"{mod}.{n.name}", parent=mod, signature=None,
                docstring=ast.get_docstring(n), start=start, end=end,
                hash=_sha("\n".join(src.splitlines()[start-1:end])), imports=[],
            ))
            self.generic_visit(n)
    V().visit(tree)
    # module symbol
    out.append(Symbol(
        symbol_id=mod, kind="module", file=str(path), qualname=mod, parent=None,
        signature=None, docstring=ast.get_docstring(tree), start=1,
        end=src.count("\n")+1, hash=_sha(src), imports=[],
    ))
    return out

def index_repo(root: str, all_: bool, changed_only: bool):
    # TODO: integrate git diff and write vectors/metadata via index package
    pass
```

**`src/agentic_docs/parsing/relations.py`**
```python
"""Build lightweight dependency graph (imports, parent-child)."""
# TODO: implement using ast walk and networkx
```

#### Index & Retrieval
**`src/agentic_docs/index/embed.py`**
```python
"""Embedding interface using sentence-transformers."""
# TODO: model load, encode(texts)->np.ndarray
```

**`src/agentic_docs/index/store_faiss.py`**
```python
"""FAISS store: add vectors, search, persist to disk."""
# TODO: implement IndexFlatIP with ID mapping
```

**`src/agentic_docs/index/metadata_store.py`**
```python
"""Simple JSONL or SQLite store for Symbol metadata."""
# TODO: implement upsert and fetch by symbol_id
```

**`src/agentic_docs/index/search.py`**
```python
"""High-level search API returning neighbors with payloads."""
# TODO: glue embed + faiss + metadata
```

**`src/agentic_docs/index/mmr.py`**
```python
"""Optional MMR reranking."""
# TODO
```

#### LLM & Markdown generation
**`src/agentic_docs/llm/local_llm.py`**
```python
"""Local LLM wrapper for llama.cpp or vLLM."""
# TODO: load model, generate(prompt)->str
```

**`src/agentic_docs/llm/prompts.py`**
```python
MD_PROMPT = """
You will generate Markdown documentation for the target symbol.
Use sections: Summary, Parameters, Returns, Raises, Examples, See also, Source.
Return only Markdown for the section boundaries provided.
Target:\nkind: {kind}\nqualname: {qualname}\nsignature: {signature}\nExisting:\n{existing}\nContext:\n{context}
"""
```

**`src/agentic_docs/llm/validate.py`**
```python
"""Validators: parameter/return coverage, example import smoke test."""
# TODO
```

**`src/agentic_docs/llm/writer_md.py`**
```python
"""Coordinator to retrieve context and call Markdown writer for impacted symbols."""
# TODO: retrieve k, format prompt, call LLM, run validators, return diffs
```

#### Agent
**`src/agentic_docs/agent/diff.py`**
```python
"""Git diff helper: changed files, added/removed/modified symbols."""
# TODO: implement via GitPython or subprocess git
```

**`src/agentic_docs/agent/impact.py`**
```python
"""Compute impacted symbols from diffs + dependency graph."""
# TODO
```

**`src/agentic_docs/agent/planner.py`**
```python
"""Plan which symbols to regenerate within a token/time budget."""
# TODO
```

**`src/agentic_docs/agent/budget.py`**
```python
class Budget:
    def __init__(self, tokens: int):
        self.tokens = tokens
        self.used = 0
    def allow(self, n: int) -> bool:
        if self.used + n > self.tokens: return False
        self.used += n; return True
```

**`src/agentic_docs/agent/orchestrator.py`**
```python
"""End-to-end: index changes -> plan -> generate Markdown -> write sections."""
# TODO
```

#### IO utilities
**`src/agentic_docs/io/fs.py`**
```python
"""File helpers, atomic writes."""
# TODO
```

**`src/agentic_docs/io/git.py`**
```python
"""Small wrappers around git commands for SHA and permalinks."""
# TODO
```

**`src/agentic_docs/io/source_links.py`**
```python
"""Create GitHub permalinks for source line ranges."""
# TODO
```

**`src/agentic_docs/io/markdown_writer.py`**
```python
"""Upsert symbol sections with BEGIN/END markers and source-hash guards."""
# TODO: implement marker search, insert/update, idempotent writes
```

#### Evaluation & baselines
**`src/agentic_docs/eval/metrics.py`**
```python
"""Compute coverage and quality metrics on Markdown sections."""
# TODO
```

**`src/agentic_docs/eval/datasets.py`**
```python
"""Load target repos and commit sequences for evaluation."""
# TODO
```

**`src/agentic_docs/eval/run_bench.py`**
```python
"""Run baselines and agentic system across commits; output CSV/plots."""
# TODO
```

**`src/agentic_docs/baselines/classical_pdoc.py`**
```python
"""Run pdoc or Sphinx to produce reference docs (no generation)."""
# TODO
```

**`src/agentic_docs/baselines/nonrag_llm.py`**
```python
"""LLM over raw symbol source without retrieval; output Markdown sections."""
# TODO
```

**`src/agentic_docs/baselines/static_rag.py`**
```python
"""Fixed top-k retrieval pipeline; no agentic planning."""
# TODO
```

---

### 5.3 Tests

**`tests/test_parsing.py`**
```python
# TODO: assert symbols extracted with correct qualnames and spans
```

**`tests/test_index.py`**
```python
# TODO: round-trip encode/search returns expected symbol ids
```

**`tests/test_writer_md.py`**
```python
# TODO: upsert creates or updates sections deterministically with markers
```

**`tests/test_agent.py`**
```python
# TODO: given a diff, planner returns only impacted symbols under budget
```

---

## 6) First commands to run
```bash
# setup
bash scripts/bootstrap.sh

# index toy repo
make index-all

# dry-run generation of Markdown for changed symbols
make propose-md

# apply generated Markdown to docs/
make apply-md

# run tests
make test
```

## 7) Notes and pitfalls
- Use hash-based section guards to avoid noisy diffs.
- Keep prompts short; include signature + trimmed body + 2–3 neighbors.
- If validator fails, retry once with stricter instructions, else emit a template stub.
- On PRs, prefer artifacts over pushing commits to contributor branches.

