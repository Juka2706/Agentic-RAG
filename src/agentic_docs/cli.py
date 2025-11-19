import click
import os
from .agent.orchestrator import Orchestrator
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
@click.option("--model-path", help="Path to LLM model file or Model Name for API")
@click.option("--api", is_flag=True, help="Use API-based LLM (e.g. qwen3:8b)")
@click.option("--api-base", help="API Base URL (default: http://localhost:11434/v1)")
@click.option("--api-key", help="API Key (default: ollama)")
def generate(changed_only, markdown, dry_run, write, model_path, api, api_base, api_key):
    """Generate documentation."""
    from .config import settings
    
    if model_path:
        settings.llm_model_path = model_path
    if api:
        settings.llm_is_local = False
    if api_base:
        settings.llm_api_base = api_base
    if api_key:
        settings.llm_api_key = api_key
        
    config = settings.dict()
    orch = Orchestrator(config)
    orch.run(changed_only=changed_only)

@main.command()
@click.option("--repo", required=True)
def eval(repo):
    run_eval(repo)

if __name__ == "__main__":
    main()
