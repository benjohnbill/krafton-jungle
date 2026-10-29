"""Static HTML views from views.toml (FINAL C11, C17), styled after benjohnbill.github.io."""

from __future__ import annotations

import html
import tomllib
from pathlib import Path

from .cards import card_names, in_scope, scope
from .graph import Graph, Hop
from .model import EDGE_KINDS, Index

# Tokens copied from benjohnbill.github.io/assets/site.css so a view opened
# from disk or through Aside renders without the network.
CSS = """
:root{color-scheme:light dark;
  --font-head:"Pretendard Variable",Pretendard,"IBM Plex Sans KR",system-ui,sans-serif;
  --font-body:"IBM Plex Sans KR",system-ui,-apple-system,sans-serif;
  --font-code:"IBM Plex Mono","IBM Plex Sans KR",ui-monospace,Menlo,monospace;
  --bg:#FFFFFF; --surface:#FFFFFF; --surface-2:#F5F5F5; --ink:#111111; --ink-2:#3F3F3F; --muted:#737373; --line:#DEDEDE;
  --s2:#0A7165; --s3:#453AA6; --s3-soft:#E5E3F7; --s4:#7E6416; --s4-soft:#F5EEDA}
@media (prefers-color-scheme:dark){:root{
  --bg:#0B0B0B; --surface:#0B0B0B; --surface-2:#171717; --ink:#EDEDED; --ink-2:#B4B4B4; --muted:#858585; --line:#2A2A2A;
  --s2:#4FC5B3; --s3:#A398F3; --s3-soft:#1B1836; --s4:#D8B65E; --s4-soft:#2A2312}}
*{box-sizing:border-box}
html{font-size:19px}
body{margin:0; background:var(--bg); color:var(--ink); font-family:var(--font-body); font-size:17px; line-height:1.85; word-break:keep-all; overflow-wrap:break-word}
a{color:var(--s2)}
.dh{font-family:var(--font-head); font-weight:700}
.wrap{max-width:900px; margin:0 auto; padding:56px 16px 90px; display:flex; flex-direction:column; gap:30px}
header{display:flex; flex-direction:column; gap:10px; padding-bottom:22px; border-bottom:3px solid var(--ink)}
h1{margin:0; font-size:1.95rem; line-height:1.2}
.sub{margin:0; color:var(--ink-2)}
h2{margin:0 0 10px; font-size:1.25rem}
section{border:1px solid var(--line); padding:18px 18px 20px}
ul.tree{list-style:none; margin:0; padding:0}
ul.tree ul.tree{margin-left:10px; padding-left:14px; border-left:1px solid var(--line)}
.row{display:flex; flex-wrap:wrap; align-items:baseline; gap:4px 10px; padding:3px 0; font-size:.85rem}
.fn{font-family:var(--font-code); font-size:16px; font-weight:600; color:var(--ink)}
a.fn{text-decoration:none; border-bottom:1px solid var(--line)}
a.fn:hover{border-color:var(--ink-2)}
.b{font-family:var(--font-code); font-size:13px; line-height:1.5; padding:0 7px; border:1px solid var(--line); color:var(--ink-2); background:var(--surface-2); white-space:nowrap}
.b.ind{background:var(--s3-soft); color:var(--s3); border-color:transparent}
.b.asm{background:var(--s4-soft); color:var(--s4); border-color:transparent}
.at{font-family:var(--font-code); font-size:13px; color:var(--muted); overflow-wrap:anywhere}
details.fold > summary{list-style:none; cursor:pointer}
details.fold > summary::-webkit-details-marker{display:none}
details.fold > summary .row::before{content:"›"; font-family:var(--font-code); color:var(--muted); display:inline-block; transition:transform .12s ease}
details.fold[open] > summary .row::before{transform:rotate(90deg)}
details.fold > summary:hover{background:var(--surface-2)}
.tog::after{content:"펼치기"} details.fold[open] > summary .tog::after{content:"접기"}
.seen{font-family:var(--font-code); font-size:13px; color:var(--muted)}
details.meta{border:1px solid var(--line); padding:10px 16px}
details.meta summary{cursor:pointer; font-family:var(--font-code); font-size:13px; color:var(--ink-2)}
details.meta pre{font-family:var(--font-code); font-size:13px; line-height:1.6; color:var(--muted); white-space:pre-wrap; overflow-wrap:anywhere; margin:8px 0 0}
@media (max-width:520px){ul.tree ul.tree{margin-left:4px; padding-left:9px}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""


class FlowView:
    def __init__(self, idx: Index, spec: dict, cards: dict[str, str]):
        self.idx, self.spec, self.cards = idx, spec, cards
        self.g = Graph(idx)

    def root(self) -> str:
        hits = [s for s in self.idx.symbols.values()
                if s.kind == "function" and s.name == self.spec["root"] and s.defined
                and s.file == self.spec.get("root_file", s.file)]
        if len(hits) != 1:
            raise SystemExit(f"view {self.spec['name']}: root {self.spec['root']} matched {len(hits)} functions")
        return hits[0].usr

    def fn(self, node: str) -> str:
        name = html.escape(self.g.name(node))
        if node in self.cards:
            return f'<a class="fn" href="../symbols/{html.escape(self.cards[node])}">{name}</a>'
        return f'<span class="fn">{name}</span>'

    def tags(self, h: Hop) -> str:
        e = h.edge
        out = []
        if e.kind == "dispatches":
            out.append(f'<span class="b ind">간접 · 규칙 {html.escape(h.candidate.rule)}</span>')
        elif EDGE_KINDS[e.kind].label:
            out.append(f'<span class="b asm">{html.escape(EDGE_KINDS[e.kind].label)}</span>')
        if e.attrs.get("via_macro"):
            out.append(f'<span class="b">via_macro {html.escape(e.attrs["via_macro"])}</span>')
        out.append(f'<span class="at">{html.escape(e.ev)}</span>')
        if h.candidate is not None:
            out.append(f'<span class="at">등록 {html.escape(h.candidate.ev)}</span>')
        return "".join(out)

    def tree(self, node: str, step, depth: int) -> str:
        """Nested list in reading order. A node's children are shown once; later rows point up."""
        if depth == 0:
            return ""
        items = []
        for other, h in sorted(step(node), key=lambda x: (x[1].edge.ev, x[1].edge.col, self.g.name(x[0]))):
            row = f'<div class="row">{self.fn(other)}{self.tags(h)}'
            if other in self.expanded:
                items.append(f'<li>{row}<span class="seen">위에서 펼침</span></div></li>')
                continue
            self.expanded.add(other)
            kids = self.tree(other, step, depth - 1)
            if not kids:
                self.expanded.discard(other)
                items.append(f"<li>{row}</div></li>")
                continue
            items.append(f'<li><details class="fold"{" open" if depth == self.top else ""}><summary>{row}'
                         f'<span class="b tog"></span></div></summary>{kids}</details></li>')
        return f'<ul class="tree">{"".join(items)}</ul>' if items else ""

    def render(self) -> str:
        root = self.root()
        sym = self.idx.symbols[root]
        st = self.idx.stamp
        sections = []
        for n, (label, step, depth) in enumerate(
            (("들어오는 호출", self.g.flow_in, self.spec["caller_depth"]),
             ("나가는 호출", self.g.flow_out, self.spec["callee_depth"])), 1):
            self.top, self.expanded = depth, {root}
            body = self.tree(root, step, depth) or '<p class="sub">없음</p>'
            sections.append(f'<section><h2 class="dh">{n}. {label} · 깊이 {depth}</h2>'
                            f'<div class="row">{self.fn(root)}<span class="at">{html.escape(sym.file)}:{sym.line}</span></div>{body}</section>')
        meta = stamp_meta(st) + "\nedges: calls, dispatches (candidates), asm_calls; containment is not a flow edge"
        return page(self.spec, ''.join(sections), meta)


def page(spec: dict, body: str, meta: str) -> str:
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(spec['title'])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;600;700&display=swap">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header>
  <h1 class="dh">{html.escape(spec['title'])}</h1>
  <p class="sub">{html.escape(spec['sub'])}</p>
</header>
{body}
<details class="meta"><summary>생성 정보</summary><pre>{html.escape(meta)}</pre></details>
</div>
</body>
</html>
"""


def stamp_meta(st: dict) -> str:
    return (f"HEAD {st['head']}{' (dirty)' if st['dirty'] else ''}\ngenerated {st['generated_at']}\n"
            f"libclang {st['libclang']}\nflag {st['extra_flag']}")


class StructsView:
    """One section per struct in the spec: fields in declaration order, each
    field's type linked when it is a struct in the same view, then the
    functions whose signature names the struct (refs_type)."""

    def __init__(self, idx: Index, spec: dict, cards: dict[str, str]):
        self.idx, self.spec, self.cards = idx, spec, cards
        self.g = Graph(idx)

    def lookup(self, name: str) -> str:
        hits = [s.usr for s in self.idx.symbols.values() if s.kind == "struct" and s.name == name]
        if len(hits) != 1:
            raise SystemExit(f"view {self.spec['name']}: struct {name} matched {len(hits)} structs")
        return hits[0]

    def fn(self, usr: str) -> str:
        name = html.escape(self.g.name(usr))
        if usr in self.cards:
            return f'<a class="fn" href="../symbols/{html.escape(self.cards[usr])}">{name}</a>'
        return f'<span class="fn">{name}</span>'

    def render(self) -> str:
        shown = {self.lookup(n): n for n in self.spec["structs"]}
        fields: dict[str, list] = {}
        types: dict[str, list[str]] = {}
        users: dict[str, list] = {}
        for e in self.idx.edges:
            if e.kind == "field_of" and e.dst in shown:
                fields.setdefault(e.dst, []).append(e)
            elif e.kind == "refs_type" and e.dst in shown:
                src = self.idx.symbols.get(e.src)
                if src and src.kind == "field":
                    types.setdefault(e.src, []).append(e.dst)
                elif src and src.kind == "function" and src.defined:
                    users.setdefault(e.dst, []).append(e)
        line = lambda e: (e.ev.rsplit(":", 1)[0], int(e.ev.rsplit(":", 1)[1]), e.col)
        sections = []
        for n, (usr, name) in enumerate(shown.items(), 1):
            s = self.idx.symbols[usr]
            rows = []
            for e in sorted(fields.get(usr, []), key=line):
                f = self.idx.symbols[e.src]
                links = "".join(f'<a class="b" href="#{html.escape(shown[t])}">→ {html.escape(shown[t])}</a>' for t in types.get(e.src, []))
                anon = '<span class="b">anonymous union</span>' if e.attrs.get("anonymous") else ""
                rows.append(f'<li><div class="row"><span class="fn">{html.escape(f.name)}</span>'
                            f'<code class="at">{html.escape(f.signature)}</code>{anon}{links}<span class="at">{html.escape(e.ev)}</span></div></li>')
            fns = sorted({(self.g.name(e.src), e.src) for e in users.get(usr, [])})
            used = " ".join(self.fn(u) for _, u in fns) or '<span class="sub">없음</span>'
            sections.append(f'<section id="{html.escape(name)}"><h2 class="dh">{n}. {html.escape(s.signature)}</h2>'
                            f'<div class="row"><span class="at">{html.escape(s.file)}:{s.line}</span></div>'
                            f'<ul class="tree">{"".join(rows)}</ul>'
                            f'<h3 class="sub">시그니처에 쓰는 함수 {len(fns)}</h3><div class="row">{used}</div></section>')
        meta = stamp_meta(self.idx.stamp) + "\nfields: field_of; types: refs_type from fields; users: refs_type from function signatures"
        return page(self.spec, "".join(sections), meta)


VIEW_KINDS = {"flow": FlowView, "structs": StructsView}


def render(idx: Index, out: Path, views_toml: Path) -> int:
    specs = tomllib.loads(views_toml.read_text()).get("view", [])
    names = card_names(idx)
    cards = {s.usr: names[s.usr] for s in in_scope(idx, scope(views_toml))}
    (out / "views").mkdir(parents=True, exist_ok=True)
    for spec in specs:
        view = VIEW_KINDS[spec["kind"]](idx, spec, cards)
        (out / "views" / f"{spec['name']}.html").write_text(view.render())
    return len(specs)
