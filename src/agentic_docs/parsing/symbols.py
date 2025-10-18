"""Walk files, parse AST, extract Symbol records. TODO: implement full extraction."""
from pathlib import Path
import ast
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
    print(f"[stub] index_repo(all={all_}, changed_only={changed_only}, root={root})")
