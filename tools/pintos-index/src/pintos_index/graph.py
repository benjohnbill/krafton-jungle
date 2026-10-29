"""Read-side adjacency over index.json, shared by every renderer."""

from __future__ import annotations

from dataclasses import dataclass

from .model import EDGE_KINDS, Candidate, Edge, Index


@dataclass
class Hop:
    """One edge seen from one end. `other` is the node at the far end."""

    edge: Edge
    other: str | None
    candidate: Candidate | None = None


class Graph:
    def __init__(self, idx: Index):
        self.idx = idx
        self.out: dict[str, list[Hop]] = {}
        self.inc: dict[str, list[Hop]] = {}
        self.via_macro: dict[str, list[Hop]] = {}
        for e in idx.edges:
            if e.attrs.get("via_macro"):
                self.via_macro.setdefault(e.attrs["via_macro"], []).append(Hop(e, e.dst))
            if e.candidates is not None:
                self.out.setdefault(e.src, []).append(Hop(e, None))
                for c in e.candidates:
                    self.inc.setdefault(c.usr, []).append(Hop(e, e.src, c))
                continue
            self.out.setdefault(e.src, []).append(Hop(e, e.dst))
            if e.dst is not None:
                self.inc.setdefault(e.dst, []).append(Hop(e, e.src))

    def name(self, node: str | None) -> str:
        if node is None:
            return "?"
        s = self.idx.symbols.get(node)
        if s is not None:
            return s.name
        if node.startswith("asm:"):
            return node.rsplit(":", 1)[1]
        return node.removeprefix("file:")

    def flow_out(self, node: str) -> list[tuple[str, Hop]]:
        res = []
        for h in self.out.get(node, []):
            if not EDGE_KINDS[h.edge.kind].flow:
                continue
            if h.edge.candidates is not None:
                res += [(c.usr, Hop(h.edge, c.usr, c)) for c in h.edge.candidates]
            elif h.other is not None:
                res.append((h.other, h))
        return res

    def flow_in(self, node: str) -> list[tuple[str, Hop]]:
        return [(h.other, h) for h in self.inc.get(node, []) if EDGE_KINDS[h.edge.kind].flow and h.other]
