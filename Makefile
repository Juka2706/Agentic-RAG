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
