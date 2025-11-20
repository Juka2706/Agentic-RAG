# Agentic-RAG Architecture

## System Overview

Agentic-RAG is an automated documentation generation system that uses RAG (Retrieval-Augmented Generation) with multi-agent LLMs to create high-quality Markdown API documentation from Python codebases.

## Architecture Diagram

```mermaid
graph TB
    subgraph "User Interface"
        CLI[CLI Commands]
    end
    
    subgraph "Core Orchestration"
        ORCH[Orchestrator]
        CONFIG[Configuration]
    end
    
    subgraph "Parsing Layer"
        PARSER[Symbol Parser]
        AST[AST Analysis]
        FILES[File Scanner]
    end
    
    subgraph "Indexing Layer"
        EMBED[Embedder<br/>sentence-transformers]
        VECTOR[Vector Store<br/>Qdrant]
    end
    
    subgraph "LLM Layer"
        LLMROUTER{LLM Router}
        LOCAL[Local LLM<br/>llama-cpp-python]
        API[API LLM<br/>Ollama/OpenAI]
    end
    
    subgraph "Agent Layer"
        CODEAGENT[Code Expert Agent<br/>Analysis]
        DOCSAGENT[Docs Expert Agent<br/>Generation]
    end
    
    subgraph "Output Layer"
        WRITER[Markdown Writer<br/>Idempotent Updates]
        DOCS[Generated Docs]
    end
    
    subgraph "External Services"
        QDRANT_DB[(Qdrant DB<br/>Local/Server)]
        OLLAMA[Ollama Server]
        OPENAI[OpenAI API]
    end
    
    CLI -->|agentic-docs index| ORCH
    CLI -->|agentic-docs generate| ORCH
    CONFIG --> ORCH
    
    ORCH -->|1. Parse| PARSER
    PARSER --> AST
    PARSER --> FILES
    AST -->|Symbols| ORCH
    
    ORCH -->|2. Embed| EMBED
    EMBED -->|Vectors| VECTOR
    VECTOR <-->|Store/Search| QDRANT_DB
    
    ORCH -->|3. Generate| LLMROUTER
    LLMROUTER -->|Local Model| LOCAL
    LLMROUTER -->|API Model| API
    API --> OLLAMA
    API --> OPENAI
    
    LLMROUTER --> CODEAGENT
    LLMROUTER --> DOCSAGENT
    
    VECTOR -->|Context Retrieval| CODEAGENT
    CODEAGENT -->|Analysis| DOCSAGENT
    DOCSAGENT -->|Markdown| ORCH
    
    ORCH -->|4. Write| WRITER
    WRITER -->|Sections| DOCS
    
    style CLI fill:#e1f5ff
    style ORCH fill:#fff4e1
    style PARSER fill:#f0e1ff
    style EMBED fill:#e1ffe1
    style VECTOR fill:#e1ffe1
    style LLMROUTER fill:#ffe1e1
    style CODEAGENT fill:#ffe1e1
    style DOCSAGENT fill:#ffe1e1
    style WRITER fill:#fff4e1
```

## Data Flow

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Orchestrator
    participant Parser
    participant Embedder
    participant Qdrant
    participant Agent
    participant LLM
    participant Writer
    
    User->>CLI: agentic-docs index
    CLI->>Orchestrator: run(changed_only=False)
    
    Orchestrator->>Parser: index_repo(root)
    Parser->>Parser: Scan Python files
    Parser->>Parser: AST analysis
    Parser-->>Orchestrator: List[Symbol]
    
    Orchestrator->>Embedder: encode(symbols)
    Embedder-->>Orchestrator: vectors
    
    Orchestrator->>Qdrant: add(vectors, metadata)
    Qdrant-->>Orchestrator: ✓ Stored
    
    User->>CLI: agentic-docs generate
    CLI->>Orchestrator: run(changed_only=False)
    
    loop For each symbol
        Orchestrator->>Qdrant: search(symbol_embedding, k=3)
        Qdrant-->>Orchestrator: Related symbols
        
        Orchestrator->>Agent: process_symbol(code, context)
        Agent->>LLM: Code Expert Prompt
        LLM-->>Agent: Analysis
        Agent->>LLM: Docs Expert Prompt
        LLM-->>Agent: Markdown documentation
        Agent-->>Orchestrator: Cleaned markdown
        
        Orchestrator->>Writer: write_section(file, symbol_id, content)
        Writer->>Writer: Check hash guard
        Writer->>Writer: Update section
        Writer-->>Orchestrator: ✓ Written
    end
    
    Orchestrator-->>CLI: Complete
    CLI-->>User: Done
```

## Component Details

### 1. **CLI Layer** (`cli.py`)
- Entry point for user commands
- Handles command-line arguments
- Manages configuration overrides
- Commands: `index`, `generate`

### 2. **Orchestrator** (`agent/orchestrator.py`)
- **Core pipeline manager**
- Coordinates all components
- Manages parallel execution
- Handles cleanup and signals
- **Key Features**:
  - ThreadPoolExecutor for parallel generation
  - Automatic Qdrant lock cleanup
  - Progress bars via tqdm
  - Signal handlers (SIGINT/SIGTERM)

### 3. **Parsing Layer** (`parsing/symbols.py`)
- **Symbol Parser**: Extracts code symbols via AST
- **Metadata Extraction**:
  - Function/class signatures
  - Docstrings
  - Decorators
  - Line ranges
  - File paths
  - Content hashes (SHA-256)

### 4. **Indexing Layer**
- **Embedder** (`index/embed.py`):
  - Uses `sentence-transformers` (e5-base-v2)
  - Encodes text to 768-dim vectors
  - In-memory caching
  
- **Qdrant Store** (`index/store_qdrant.py`):
  - Local disk-based vector DB
  - Automatic retry with lock cleanup
  - Context manager support
  - Cosine similarity search

### 5. **LLM Layer**
- **Local LLM** (`llm/local_llm.py`):
  - Wraps `llama-cpp-python`
  - Supports GGUF models
  - Configurable context size and GPU layers
  
- **API LLM** (`llm/api_llm.py`):
  - Wraps `langchain-openai`
  - Compatible with Ollama and OpenAI
  - Configurable base URL and API key

### 6. **Agent Layer** (`agent/agents.py`)
- **Code Expert Agent**:
  - Analyzes code structure
  - Identifies key concepts
  - Determines complexity
  
- **Docs Expert Agent**:
  - Generates clean Markdown
  - Uses retrieved context
  - Structured output (no thinking tags)
  - Follows documentation standards

### 7. **Output Layer** (`io/markdown_writer.py`)
- **Markdown Writer**:
  - Idempotent section updates
  - Hash-based change detection
  - Preserves manual edits
  - Section guards: `<!-- BEGIN: auto:symbol_id -->`

## Configuration

### Environment Variables
```bash
# LLM Configuration
LLM_IS_LOCAL=False
LLM_MODEL_PATH=qwen3:8b
LLM_API_BASE=http://localhost:11434/v1
LLM_API_KEY=ollama

# Performance
MAX_WORKERS=4

# Embedding
EMBED_MODEL=intfloat/e5-base-v2
DEVICE=cpu
```

### CLI Arguments
```bash
# Indexing
agentic-docs index --root . --all

# Generation
agentic-docs generate \
  --api \
  --model-path "qwen3:8b" \
  --api-base "http://localhost:11434/v1" \
  --workers 8 \
  --dry-run
```

## Concurrency Model

```mermaid
graph LR
    subgraph "Main Thread"
        MT[Orchestrator]
        PARSE[Parse All]
        EMBED[Embed All]
        RETRIEVE[Retrieve Context<br/>Sequential]
    end
    
    subgraph "Worker Pool"
        W1[Worker 1<br/>LLM Call]
        W2[Worker 2<br/>LLM Call]
        W3[Worker 3<br/>LLM Call]
        W4[Worker 4<br/>LLM Call]
    end
    
    MT --> PARSE
    PARSE --> EMBED
    EMBED --> RETRIEVE
    RETRIEVE -->|Submit Tasks| W1
    RETRIEVE -->|Submit Tasks| W2
    RETRIEVE -->|Submit Tasks| W3
    RETRIEVE -->|Submit Tasks| W4
    
    W1 -->|Results| MT
    W2 -->|Results| MT
    W3 -->|Results| MT
    W4 -->|Results| MT
```

**Key Design Decisions**:
- **Qdrant access is sequential** (main thread only) to avoid lock contention
- **LLM generation is parallel** via ThreadPoolExecutor
- **Configurable worker count** (default: 4)
- **Automatic cleanup** on interruption

## Performance Characteristics

| Phase | Parallelization | Bottleneck |
|-------|----------------|------------|
| Parsing | Sequential | I/O (file reading) |
| Embedding | Batched | CPU/GPU (model inference) |
| Vector Search | Sequential | Qdrant lock |
| LLM Generation | Parallel | API/Model latency |
| Writing | Sequential | I/O (file writing) |

**Optimization Opportunities**:
- ✅ Parallel LLM generation (implemented)
- ✅ Progress bars for feedback (implemented)
- ⏳ Incremental indexing (hash-based change detection)
- ⏳ Server-mode Qdrant for concurrent access
- ⏳ Batch embedding for better GPU utilization

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| CLI Framework | Click |
| AST Parsing | Built-in `ast` module |
| Embeddings | Sentence Transformers |
| Vector DB | Qdrant (local/server) |
| LLM Orchestration | LangChain |
| Local LLM | llama-cpp-python |
| API LLM | OpenAI SDK |
| Progress Bars | tqdm |
| Configuration | pydantic-settings |

## File Structure

```
src/agentic_docs/
├── cli.py                 # CLI entry point
├── config.py              # Configuration management
├── agent/
│   ├── agents.py          # Multi-agent orchestration
│   └── orchestrator.py    # Pipeline manager
├── parsing/
│   └── symbols.py         # AST-based symbol extraction
├── index/
│   ├── embed.py           # Sentence-transformers wrapper
│   └── store_qdrant.py    # Qdrant vector store
├── llm/
│   ├── local_llm.py       # Local GGUF model wrapper
│   ├── api_llm.py         # API LLM wrapper
│   └── prompts.py         # Agent prompts
└── io/
    └── markdown_writer.py # Idempotent Markdown writer
```

## CI/CD Integration

### GitLab CI Pipeline
```yaml
stages:
  - index
  - propose
  - apply

index:
  script:
    - agentic-docs index --all

propose-docs:
  script:
    - agentic-docs generate --changed-only

apply-docs:
  script:
    - git add docs/
    - git commit -m "docs: update API documentation"
```

## Future Enhancements

1. **Incremental Updates**: Only re-generate changed symbols
2. **Server-Mode Qdrant**: Support concurrent access
3. **Streaming Output**: Show LLM generation in real-time
4. **Multi-Language Support**: Extend to JavaScript, TypeScript, Go
5. **Custom Templates**: User-defined documentation formats
6. **Context Window Management**: Automatic chunking for large files
