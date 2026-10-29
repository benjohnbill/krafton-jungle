"""Symbol cards `symbols/<name>.md` and `INDEX.md` (FINAL C8, C9, C10)."""

from __future__ import annotations

import fnmatch
import tomllib
from collections import Counter
from pathlib import Path

from .graph import Graph, Hop
from .model import EDGE_KINDS, Index, Symbol

CARD_KINDS = ("function", "macro")


def scope(views_toml: Path) -> list[str]:
    return tomllib.loads(views_toml.read_text())["cards"]["scope"]


def card_names(idx: Index) -> dict[str, str]:
    """Card file name for every function and macro, whether or not it is rendered.

    Names are fixed over the whole kernel so a card keeps its name when the
    rendered scope grows.
    """
    syms = [s for s in idx.symbols.values() if s.kind in CARD_KINDS]
    dup = Counter(s.name for s in syms)
    return {
        s.usr: (s.name if dup[s.name] == 1 else f"{s.name}@{s.file.replace('/', '-')}") + ".md"
        for s in syms
    }


def in_scope(idx: Index, patterns: list[str]) -> list[Symbol]:
    out = [
        s for s in idx.symbols.values()
        if s.kind in CARD_KINDS and (s.kind != "function" or s.defined)
        and any(fnmatch.fnmatch(s.file, p) for p in patterns)
    ]
    return sorted(out, key=lambda s: (s.file, s.line))


class CardWriter:
    def __init__(self, idx: Index, rendered: dict[str, str]):
        self.idx = idx
        self.g = Graph(idx)
        self.rendered = rendered
        self.cited: set[str] = set()

    def ref(self, node: str | None) -> str:
        name = self.g.name(node)
        if node in self.rendered:
            return f"[`{name}`]({self.rendered[node]})"
        s = self.idx.symbols.get(node)
        return f"`{name}` ({self.ev(f'{s.file}:{s.line}')})" if s else f"`{name}`"

    def ev(self, ev: str) -> str:
        self.cited.add(ev.split(":", 1)[0])
        return f"`{ev}`"

    def label(self, kind: str) -> str:
        lab = EDGE_KINDS[kind].label
        return f" · {lab}" if lab else ""

    def _in_dispatch(self, h: Hop) -> str:
        e = h.edge
        return (f"- {self.ref(h.other)} at {self.ev(e.ev)}, indirect through {e.attrs['via']}"
                f"{_macro(e)} · candidate by rule {h.candidate.rule}, stored at {self.ev(h.candidate.ev)}")

    def _in_call(self, h: Hop) -> str:
        e = h.edge
        args = ", ".join(f"`{a}`" for a in e.attrs.get("args", [])) or "no arguments"
        return f"- {self.ref(h.other)} at {self.ev(e.ev)}{_macro(e)} · args {args}"

    def _in_register(self, h: Hop) -> str:
        return f"- {self.ev(h.edge.ev)} into {h.edge.attrs['into']} (in {self.ref(h.other)})"

    def _out_dispatch(self, h: Hop) -> str:
        e = h.edge
        cands = "; ".join(f"{self.ref(c.usr)} (rule {c.rule}, {self.ev(c.ev)})" for c in e.candidates) or "none found"
        return (f"- indirect call at {self.ev(e.ev)} through {e.attrs['via']}{_macro(e)}, "
                f"rule {e.attrs['rule']} · candidates: {cands}")

    def _out_register(self, h: Hop) -> str:
        return f"- {self.ref(h.other)} at {self.ev(h.edge.ev)} into {h.edge.attrs['into']}"

    def _plain(self, h: Hop) -> str:
        return f"- {self.ref(h.other)} at {self.ev(h.edge.ev)}{_macro(h.edge)}{self.label(h.edge.kind)}"

    def formatters(self, side: str) -> dict:
        """Line formatter per edge kind; every kind with a heading on that side has one."""
        if side == "in":
            return {"calls": self._in_call, "dispatches": self._in_dispatch, "registers": self._in_register,
                    "asm_calls": self._plain, "expands": self._plain, "field_of": self._plain, "refs_type": self._plain}
        return {"calls": self._plain, "dispatches": self._out_dispatch, "registers": self._out_register,
                "asm_calls": self._plain, "expands": self._plain, "refs_type": self._plain}

    def sections(self, hops: list[Hop], side: str) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        for kind in EDGE_KINDS.values():
            heading = kind.in_heading if side == "in" else kind.out_heading
            if heading is None:
                continue
            fmt = self.formatters(side)[kind.name]
            lines = [fmt(h) for h in sorted(hops, key=lambda h: (h.edge.ev, h.edge.col)) if h.edge.kind == kind.name]
            if lines:
                out.setdefault(heading, []).extend(lines)
        return out

    def card(self, s: Symbol) -> str:
        self.cited = {s.file}
        stamp = self.idx.stamp
        inc = self.sections(self.g.inc.get(s.usr, []), "in")
        out = self.sections(self.g.out.get(s.usr, []), "out")
        md = [
            f"# {s.name}",
            "",
            f"{s.kind} · `{s.file}:{s.line}`",
            "",
            "## Callers",
            "",
        ]
        callers = inc.pop("Callers", []) or inc.pop("Expanded in", [])
        md += callers or ["- none found in the kernel set"]
        for heading in ("Registered at", "Expanded in"):
            if heading in inc:
                md += ["", f"### {heading}", "", *inc.pop(heading)]
        md += ["", "## What it does", "", "```c", s.signature, "```", ""]
        if s.comment:
            md += ["comment (unverified):", "", *[f"> {l}" if l else ">" for l in s.comment.splitlines()], ""]
        if s.kind == "macro":
            made = [self._plain(h) if h.edge.kind != "dispatches" else self._out_dispatch(h)
                    for h in self.g.via_macro.get(s.name, [])]
            md += ["### Calls its body makes", "", *(made or ["- none"])]
        else:
            md += ["### Callees", "", *(out.pop("Callees", None) or ["- none"])]
        field_writes = [(p.name, w) for p in s.params for w in p.member_writes]
        if field_writes:
            md += ["", "### Field writes through parameters", ""]
            md += [f"- `{w['lhs']}` at {self.ev(w['ev'])}" for _, w in field_writes]
        for heading, lines in list(out.items()):
            md += ["", f"### {heading}", "", *lines]
        if s.kind == "function":
            md += self.arguments(s) + self.returns(s)
        hashes = stamp["file_hashes"]
        md += ["", "## Sources", "", f"Stamp: HEAD `{stamp['head'][:12]}`{' (dirty)' if stamp['dirty'] else ''}, generated {stamp['generated_at']}.", ""]
        md += ["| file | sha256 (16) |", "|---|---|"]
        md += [f"| `{f}` | `{hashes.get(f, 'not read')}` |" for f in sorted(self.cited)]
        return "\n".join(md) + "\n"

    def arguments(self, s: Symbol) -> list[str]:
        md = ["", "## Arguments", ""]
        if not s.params:
            return md + ["- none"]
        callers = [h for h in self.g.inc.get(s.usr, []) if h.edge.kind == "calls"]
        for i, p in enumerate(s.params):
            md += [f"### `{p.name or f'arg{i}'}` · `{p.type}`", ""]
            md.append("- (a) assigned: " + (", ".join(self.ev(w) for w in p.writes) or "never"))
            md.append("- (b) member writes: " + ("; ".join(f"`{w['lhs']}` at {self.ev(w['ev'])}" for w in p.member_writes) or "none"))
            md.append("- (c) passed to: " + ("; ".join(f"`{c['expr']}` as arg {c['arg']} of `{c['callee']}` at {self.ev(c['ev'])}" for c in p.passed_to) or "none"))
            args = [(h, h.edge.attrs.get("args", [])) for h in callers]
            md.append("- (d) caller arguments: " + (
                "; ".join(f"`{a[i]}` from {self.ref(h.other)} at {self.ev(h.edge.ev)}" for h, a in args if i < len(a)) or "no direct callers"))
            md.append("")
        return md

    def returns(self, s: Symbol) -> list[str]:
        md = ["## Return", "", f"`{s.return_type}`", ""]
        if s.return_type == "void" and not s.returns:
            return md
        md += [f"- {self.ev(r['ev'])} `return {r['expr']}`" if r["expr"] else f"- {self.ev(r['ev'])} `return`" for r in s.returns]
        return md


def _macro(e) -> str:
    return f" (via_macro `{e.attrs['via_macro']}`)" if e.attrs.get("via_macro") else ""


def render(idx: Index, out: Path, views_toml: Path) -> int:
    names = card_names(idx)
    syms = in_scope(idx, scope(views_toml))
    rendered = {s.usr: names[s.usr] for s in syms}
    w = CardWriter(idx, rendered)
    (out / "symbols").mkdir(parents=True, exist_ok=True)
    for s in syms:
        (out / "symbols" / names[s.usr]).write_text(w.card(s))
    write_index(idx, out, syms, names)
    return len(syms)


def write_index(idx: Index, out: Path, syms: list[Symbol], names: dict[str, str]) -> None:
    st = idx.stamp
    md = [
        "# Pintos code index",
        "",
        f"Generated {st['generated_at']} from HEAD `{st['head'][:12]}`{' (dirty)' if st['dirty'] else ''}. "
        f"Kernel set: {len(st['kernel_set']['c'])} C files. Facts come from libclang ({st['libclang']}); "
        "`asm (not clang)` facts come from the kernel .S files. Regenerate with `pintos-index`.",
        "",
        "One card per symbol. A card lists callers, callees, arguments, and return lines with `file:line`.",
    ]
    by_file: dict[str, list[Symbol]] = {}
    for s in syms:
        by_file.setdefault(s.file, []).append(s)
    for f, group in by_file.items():
        md += ["", f"## {f}", ""]
        md += [f"- [{s.name}](symbols/{names[s.usr]}) · {s.kind} · `{s.file}:{s.line}`" for s in group]
    views = sorted(p.name for p in (out / "views").glob("*.html")) if (out / "views").exists() else []
    if views:
        md += ["", "## Views", "", *[f"- [{v}](views/{v})" for v in views]]
    (out / "INDEX.md").write_text("\n".join(md) + "\n")
