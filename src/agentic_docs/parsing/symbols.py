"""Walk files, parse AST, extract Symbol records."""
from pathlib import Path
import ast
import hashlib
from typing import List, Optional
from ..types import Symbol

IGNORE = [".venv", "site-packages", "build", "dist", "__pycache__", ".git", ".idea", ".vscode"]

def _sha(s: str) -> str:
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
    try:
        rel = path.relative_to(src_root).with_suffix("")
        return ".".join(rel.parts)
    except ValueError:
        return path.stem

def _get_decorators(node: ast.AST) -> List[str]:
    decs = []
    if hasattr(node, 'decorator_list'):
        for d in node.decorator_list:
            if isinstance(d, ast.Name):
                decs.append(d.id)
            elif isinstance(d, ast.Attribute):
                decs.append(f"{d.value.id}.{d.attr}" if isinstance(d.value, ast.Name) else d.attr)
            elif isinstance(d, ast.Call):
                if isinstance(d.func, ast.Name):
                    decs.append(d.func.id)
                elif isinstance(d.func, ast.Attribute):
                     decs.append(f"{d.func.value.id}.{d.func.attr}" if isinstance(d.func.value, ast.Name) else d.func.attr)
    return decs

def _get_signature(node: ast.AST) -> Optional[str]:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        args = []
        # Handle args
        for arg in node.args.args:
            a = arg.arg
            if arg.annotation:
                a += f": {ast.unparse(arg.annotation)}"
            args.append(a)
        if node.args.vararg:
            args.append(f"*{node.args.vararg.arg}")
        if node.args.kwarg:
            args.append(f"**{node.args.kwarg.arg}")
        
        sig = f"({', '.join(args)})"
        if node.returns:
            sig += f" -> {ast.unparse(node.returns)}"
        return sig
    return None

def parse_symbols_file(path: Path, src_root: Path) -> list[Symbol]:
    try:
        src = path.read_text(encoding="utf-8")
        tree = ast.parse(src, filename=str(path))
    except Exception as e:
        print(f"Error parsing {path}: {e}")
        return []

    mod = module_qualname(path, src_root)
    out: list[Symbol] = []
    lines = src.splitlines()

    class V(ast.NodeVisitor):
        def visit_ClassDef(self, n):
            start, end = n.lineno, n.end_lineno
            # Extract source segment for hashing
            segment = "\n".join(lines[start-1:end])
            
            out.append(Symbol(
                symbol_id=f"{mod}.{n.name}", 
                kind="class", 
                file=str(path),
                qualname=f"{mod}.{n.name}", 
                parent=mod, 
                signature=None,
                docstring=ast.get_docstring(n), 
                start=start, 
                end=end,
                hash=_sha(segment), 
                imports=[], # TODO: Extract imports if needed
                decorators=_get_decorators(n)
            ))
            # Visit methods
            for item in n.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    self.visit_Method(item, f"{mod}.{n.name}")
            
            # Don't generic_visit to avoid double counting methods if we handled them
            # But we might want nested classes? For now, keep simple.

        def visit_Method(self, n, parent_qualname):
            start, end = n.lineno, n.end_lineno
            segment = "\n".join(lines[start-1:end])
            out.append(Symbol(
                symbol_id=f"{parent_qualname}.{n.name}", 
                kind="method", 
                file=str(path),
                qualname=f"{parent_qualname}.{n.name}", 
                parent=parent_qualname, 
                signature=_get_signature(n),
                docstring=ast.get_docstring(n), 
                start=start, 
                end=end,
                hash=_sha(segment), 
                imports=[],
                decorators=_get_decorators(n)
            ))

        def visit_FunctionDef(self, n):
            # Top level functions only (if not visited by ClassDef)
            # We can check if it's already in out? Or just rely on traversal order.
            # The standard NodeVisitor visits children. 
            # If we are at top level, parent is module.
            start, end = n.lineno, n.end_lineno
            segment = "\n".join(lines[start-1:end])
            out.append(Symbol(
                symbol_id=f"{mod}.{n.name}", 
                kind="function", 
                file=str(path),
                qualname=f"{mod}.{n.name}", 
                parent=mod, 
                signature=_get_signature(n),
                docstring=ast.get_docstring(n), 
                start=start, 
                end=end,
                hash=_sha(segment), 
                imports=[],
                decorators=_get_decorators(n)
            ))

    # We need a custom visitor to handle the parent context properly
    # or just iterate top level nodes
    
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            V().visit_ClassDef(node)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            V().visit_FunctionDef(node)

    # module symbol
    out.append(Symbol(
        symbol_id=mod, kind="module", file=str(path), qualname=mod, parent=None,
        signature=None, docstring=ast.get_docstring(tree), start=1,
        end=len(lines)+1, hash=_sha(src), imports=[], decorators=[]
    ))
    return out

def index_repo(root: str, all_: bool = True, changed_only: bool = False) -> List[Symbol]:
    """
    Main entry point to parse the repository.
    For now, 'all_' is assumed True or we just parse everything.
    'changed_only' logic would go here (git diff).
    """
    src_root = Path(root)
    # If src folder exists, use it as root for package names
    if (src_root / "src").exists():
        package_root = src_root / "src"
    else:
        package_root = src_root

    files = collect_py_files(str(src_root))
    all_symbols = []
    
    print(f"Indexing {len(files)} files in {src_root}...")
    
    for f in files:
        syms = parse_symbols_file(f, package_root)
        all_symbols.extend(syms)
        
    return all_symbols
