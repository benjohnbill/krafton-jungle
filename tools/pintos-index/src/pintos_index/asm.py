"""`asm_calls` edges from kernel .S files (FINAL C14). Not clang facts.

Patterns: `call <sym>`, and `movabs $<sym>, %reg` followed by `call *%reg`
with no label between them; that edge's evidence is the movabs line, where
the symbol is named. Any other `call *%reg` is kept as unresolved.
"""

from __future__ import annotations

import re
from pathlib import Path

from .model import Edge, Symbol

LABEL = re.compile(r"^\s*([A-Za-z_.$][\w.$]*):")
GLOBL = re.compile(r"^\s*\.globl\s+([A-Za-z_][\w]*)")
CALL = re.compile(r"^\s*call\s+([A-Za-z_][\w]*)\s*$")
CALL_REG = re.compile(r"^\s*call\s+\*%(\w+)\s*$")
MOVABS = re.compile(r"^\s*movabs\s+\$([A-Za-z_][\w]*)\s*,\s*%(\w+)\s*$")


def _code_lines(text: str) -> list[tuple[int, str]]:
    text = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        out.append((n, line))
    return out


def extract(root: Path, files: list[str], symbols: dict[str, Symbol]) -> list[Edge]:
    by_name: dict[str, str] = {}
    for s in symbols.values():
        if s.kind == "function" and (s.name not in by_name or s.defined):
            by_name[s.name] = s.usr
    edges = []
    for f in files:
        lines = _code_lines((root / f).read_text())
        globl = {m.group(1) for _, l in lines if (m := GLOBL.match(l))}
        current = None
        loaded: dict[str, tuple[str, int]] = {}
        for n, line in lines:
            lab = LABEL.match(line)
            if lab:
                loaded.clear()
                if lab.group(1) in globl or current is None:
                    current = lab.group(1)
                continue
            src = by_name.get(current, f"asm:{f}:{current}")
            if m := MOVABS.match(line):
                loaded[m.group(2)] = (m.group(1), n)
            elif m := CALL.match(line):
                edges.append(_edge(src, f, n, m.group(1), by_name, {}))
            elif m := CALL_REG.match(line):
                hit = loaded.get(m.group(1))
                if hit:
                    edges.append(_edge(src, f, hit[1], hit[0], by_name, {"call_at": f"{f}:{n}"}))
                else:
                    edges.append(Edge("asm_calls", src, f"{f}:{n}", None, attrs={"unresolved": f"*%{m.group(1)}"}))
    return edges


def _edge(src: str, f: str, n: int, sym: str, by_name: dict[str, str], attrs: dict) -> Edge:
    dst = by_name.get(sym)
    if dst is None:
        attrs = {**attrs, "unresolved": sym}
    return Edge("asm_calls", src, f"{f}:{n}", dst, attrs={**attrs, "label": "asm (not clang)"})
