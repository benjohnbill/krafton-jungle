"""Candidate lists for indirect calls (FINAL C2, C15).

Rules, by what the callee expression reads:
  a   a struct field: every function stored into that field
  a'  a global or static variable or array: every function stored into it
  b   a local or a parameter: trace its stores, then a / a' / b again
  c   fallback when a trace meets a value it cannot follow: every
      address-taken function of the same type
`fwd` marks a candidate that reached the sink through parameter forwarding.
"""

from __future__ import annotations

from .extract import Facts
from .model import Candidate, Edge


def _sink_rule(sink: tuple, facts: Facts) -> str:
    if sink[0] == "field":
        return "a"
    if sink[0] == "var":
        v = facts.vars.get(sink[1])
        return "b" if v is not None and v.local else "a'"
    return "b"


def resolve(facts: Facts) -> list[Edge]:
    taken: dict[str, tuple[str, int]] = {}
    for stores in facts.stores.values():
        for st in stores:
            for v in _flatten(st.value):
                if v[0] == "func":
                    taken.setdefault(v[1], (v[2], v[3]))
    for r in facts.refs:
        if r["ctx"] != "call":
            f, line, col = r["at"].rsplit(":", 2)
            taken.setdefault(r["usr"], (f"{f}:{line}", int(col)))

    def walk(v: tuple, rule: str, fwd: bool, seen: set, out: dict[str, Candidate]) -> bool:
        """Adds candidates reachable from value v. Returns True when the trace is incomplete."""
        kind = v[0]
        if kind == "func":
            out.setdefault(v[1], Candidate(v[1], v[2], rule + ("+fwd" if fwd else "")))
            return False
        if kind == "null":
            return False
        if kind == "multi":
            return any([walk(x, rule, fwd, seen, out) for x in v[1]])
        if kind not in ("var", "field", "param"):
            return True
        if v in seen:
            return False
        seen.add(v)
        incomplete = kind == "param" and v[1] in taken
        stores = facts.stores.get(v, [])
        if not stores and kind != "field":
            return True
        for st in stores:
            hop_fwd = fwd or kind == "param"
            if walk(st.value, _sink_rule(v, facts), hop_fwd, seen, out):
                incomplete = True
        return incomplete

    edges = []
    for site in facts.dispatch_sites:
        out: dict[str, Candidate] = {}
        root_rule = _sink_rule(site.callee, facts) if site.callee[0] in ("var", "field", "param") else "c"
        incomplete = walk(site.callee, root_rule, False, set(), out) or not out
        if incomplete:
            for usr, (ev, _) in sorted(taken.items()):
                if facts.fn_types.get(usr) == site.fn_type:
                    out.setdefault(usr, Candidate(usr, ev, "c"))
        attrs = {
            "rule": root_rule + ("+c" if incomplete and root_rule != "c" else ""),
            "via": facts.sink_names.get(site.callee, "expression"),
            "fn_type": site.fn_type,
        }
        if site.via_macro:
            attrs["via_macro"] = site.via_macro
        edges.append(
            Edge("dispatches", site.src, site.ev, None, sorted(out.values(), key=lambda c: c.usr), site.col, attrs)
        )
    return edges


def _flatten(v: tuple) -> list[tuple]:
    return [x for sub in v[1] for x in _flatten(sub)] if v[0] == "multi" else [v]

