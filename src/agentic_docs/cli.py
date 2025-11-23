import click
import os
from .agent.orchestrator import Orchestrator

@click.group()
def main():
    pass

@main.command()
@click.option("--all", "all_", is_flag=True, help="Index entire repo")
@click.option("--changed-only", is_flag=True, help="Index only changed files")
@click.option("--root", default=".")
def index(all_, changed_only, root):
    """Parse and index codebase."""
    from .config import settings
    
    # Override settings with CLI args if provided
    if root != ".":
        settings.root = root
        
    # Convert settings to dict for Orchestrator
    config = settings.dict()
    
    orch = Orchestrator(config)
    orch.run(changed_only=changed_only)

@main.command()
@click.option("--changed-only", is_flag=True)
@click.option("--markdown", is_flag=True, default=True)
@click.option("--dry-run", is_flag=True)
@click.option("--write", is_flag=True)
@click.option("--model", help="Model Name for API (e.g. qwen2.5-coder:latest)")
@click.option("--api-base", help="API Base URL (default: http://localhost:11434/v1)")
@click.option("--api-key", help="API Key (default: ollama)")
@click.option("--workers", type=int, default=4, help="Number of parallel workers")
def generate(changed_only, markdown, dry_run, write, model, api_base, api_key, workers):
    """Generate documentation."""
    from .config import settings
    
    if model:
        settings.llm_model_name = model
    if api_base:
        settings.llm_api_base = api_base
    if api_key:
        settings.llm_api_key = api_key
    if workers:
        settings.max_workers = workers
        
    config = settings.dict()
    config["dry_run"] = dry_run
    
    orch = Orchestrator(config)
    orch.run(changed_only=changed_only)

if __name__ == "__main__":
    main()
