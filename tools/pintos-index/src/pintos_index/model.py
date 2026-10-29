"""The fact store. Every renderer reads only this shape, through index.json.

Node ids are clang USRs for C symbols, `file:<path>` for files, and
`asm:<path>:<label>` for asm labels that no C declaration names.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Literal

SymbolKind = Literal["function", "struct", "typedef", "macro", "field"]


@dataclass
class Param:
    name: str
    type: str
    writes: list[str] = field(default_factory=list)
    member_writes: list[dict] = field(default_factory=list)
    passed_to: list[dict] = field(default_factory=list)


@dataclass
class Symbol:
    usr: str
    name: str
    kind: SymbolKind
    file: str
    line: int
    signature: str
    comment: str | None = None
    defined: bool = True
    return_type: str | None = None
    params: list[Param] = field(default_factory=list)
    returns: list[dict] = field(default_factory=list)


@dataclass
class Candidate:
    usr: str
    ev: str
    rule: str


@dataclass
class Edge:
    kind: str
    src: str
    ev: str
    dst: str | None = None
    candidates: list[Candidate] | None = None
    col: int = 0
    attrs: dict = field(default_factory=dict)


@dataclass(frozen=True)
class EdgeKind:
    """How one edge kind is extracted and how renderers show it.

    `flow` marks kinds a flow view walks. `out_heading` and `in_heading` name
    the card section on the source and destination side. `label` is printed
    next to every fact of the kind.
    """

    name: str
    extracted_by: str
    flow: bool
    out_heading: str | None
    in_heading: str | None
    label: str | None = None


EDGE_KINDS: dict[str, EdgeKind] = {
    k.name: k
    for k in (
        EdgeKind("calls", "libclang CALL_EXPR with a direct callee", True, "Callees", "Callers"),
        EdgeKind("dispatches", "libclang CALL_EXPR through a function pointer, candidates by value flow", True, "Callees", "Callers"),
        EdgeKind("asm_calls", "regex over kernel .S files", True, "Callees", "Callers", "asm (not clang)"),
        EdgeKind("registers", "libclang DECL_REF_EXPR of a function stored or passed", False, "Registers", "Registered at"),
        EdgeKind("expands", "libclang MACRO_INSTANTIATION inside a function body", False, "Macros used", "Expanded in"),
        EdgeKind("includes", "libclang INCLUSION_DIRECTIVE", False, None, None),
        EdgeKind("field_of", "libclang FIELD_DECL in a record", False, None, "Fields"),
        EdgeKind("refs_type", "libclang parameter, return, field, and typedef types", False, "Types used", "Used by"),
    )
}


@dataclass
class Index:
    stamp: dict
    symbols: dict[str, Symbol]
    edges: list[Edge]
    refs: list[dict]

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), indent=1, ensure_ascii=False, sort_keys=True))

    @staticmethod
    def load(path: Path) -> Index:
        raw = json.loads(path.read_text())
        symbols = {
            u: Symbol(**{**s, "params": [Param(**p) for p in s["params"]]})
            for u, s in raw["symbols"].items()
        }
        edges = [
            Edge(**{**e, "candidates": None if e["candidates"] is None else [Candidate(**c) for c in e["candidates"]]})
            for e in raw["edges"]
        ]
        return Index(raw["stamp"], symbols, edges, raw["refs"])
