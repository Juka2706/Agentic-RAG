import click
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
