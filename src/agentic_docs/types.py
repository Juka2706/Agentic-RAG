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
    decorators: List[str]
