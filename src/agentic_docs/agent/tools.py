from typing import Optional
from pathlib import Path
from langchain_core.tools import tool

@tool
def read_file(file_path: str) -> str:
    """Read the content of a file.
    
    Args:
        file_path: The absolute or relative path to the file.
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return f"Error: File {file_path} does not exist."
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {e}"

@tool
def list_directory(dir_path: str = ".") -> str:
    """List the contents of a directory.
    
    Args:
        dir_path: The path to the directory. Defaults to current directory.
    """
    try:
        path = Path(dir_path)
        if not path.exists():
            return f"Error: Directory {dir_path} does not exist."
        
        items = []
        for item in path.iterdir():
            prefix = "[DIR] " if item.is_dir() else "[FILE]"
            items.append(f"{prefix} {item.name}")
        return "\n".join(sorted(items))
    except Exception as e:
        return f"Error listing directory: {e}"

@tool
def search_code(query: str, root_dir: str = ".") -> str:
    """Search for a string in all files in the directory.
    
    Args:
        query: The string to search for.
        root_dir: The directory to search in.
    """
    try:
        import subprocess
        # Use grep to search recursively
        # -r: recursive
        # -n: line numbers
        # -I: ignore binary files
        result = subprocess.run(
            ["grep", "-rnI", query, root_dir],
            capture_output=True,
            text=True
        )
        if result.returncode != 0 and result.returncode != 1:
            return f"Error executing grep: {result.stderr}"
        
        output = result.stdout
        if not output:
            return "No matches found."
        
        # Limit output to avoid context window overflow
        lines = output.splitlines()
        if len(lines) > 50:
            return "\n".join(lines[:50]) + f"\n... ({len(lines) - 50} more matches)"
        return output
    except Exception as e:
        return f"Error searching code: {e}"
