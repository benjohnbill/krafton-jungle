"""PROTOTYPE, throwaway. Question: what form should a flow view take?

Three variants of fault-flow on one page, switched by ?variant=A|B|C and a
bottom bar (arrow keys too). A toggle switches the expand rule between
"expand only vm/ and userprog/" and "expand everything".

  A  layered flow diagram: columns = call depth, callers left of the root
  B  subsystem lanes: rows = directory, columns = call depth
  C  the current fold tree, same expand rule (baseline)

Run:  uv run python prototype/flow_form.py
Out:  week09/.code-index/views/prototype-flow-form.html (wiped by the next build)
"""

from __future__ import annotations

import html
from fnmatch import fnmatch
from pathlib import Path

from pintos_index.build import DEFAULT_PINTOS, TOOL_DIR
from pintos_index.cards import card_names, in_scope, scope
from pintos_index.graph import Graph
from pintos_index.model import Index
from pintos_index.views import CSS, FlowView

OUT = DEFAULT_PINTOS.parent / ".code-index"
SPEC = {"name": "fault-flow", "root": "page_fault", "root_file": "userprog/exception.c",
        "title": "page_fault 흐름", "sub": "", "callee_depth": 4, "caller_depth": 2}
EXPAND = ["vm/*", "userprog/*"]

idx = Index.load(OUT / "index.json")
g = Graph(idx)
names = card_names(idx)
cards = {s.usr: names[s.usr] for s in in_scope(idx, scope(TOOL_DIR / "views.toml"))}
S = idx.symbols
root = FlowView(idx, SPEC, cards).root()


def file_of(n: str) -> str:
    return S[n].file if n in S else n.split(":")[1] if n.startswith("asm:") else ""


def expands(n: str, rule: bool) -> bool:
    return n == root or not rule or any(fnmatch(file_of(n), p) for p in EXPAND)


def collect(rule: bool):
    """Nodes at their shortest depth (callers negative) and every edge between shown nodes.
    The expand rule limits only the callee side."""
    depth = {root: 0}
    edges: dict[tuple[str, str], object] = {}
    for sign, step, limit in ((1, g.flow_out, SPEC["callee_depth"]), (-1, g.flow_in, SPEC["caller_depth"])):
        front = [root]
        for d in range(1, limit + 1):
            nxt = []
            for n in front:
                if sign > 0 and not expands(n, rule):
                    continue
                for o, h in sorted(step(n), key=lambda x: (x[1].edge.ev, x[1].edge.col)):
                    key = (n, o) if sign > 0 else (o, n)
                    edges.setdefault(key, h)
                    if o not in depth:
                        depth[o] = sign * d
                        nxt.append(o)
            front = nxt
    return depth, edges


BW, BH, GX, GY = 250, 40, 56, 12


def box(n: str, x: float, y: float, rule: bool) -> str:
    s = S.get(n)
    at = f"{s.file}:{s.line}" if s else file_of(n)
    cls = "node" + (" root" if n == root else "") + ("" if expands(n, rule) else " stop")
    label = html.escape(g.name(n))
    inner = (f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}"/>'
             f'<text class="nm" x="{x + 10}" y="{y + 17}">{label}</text>'
             f'<text class="loc" x="{x + 10}" y="{y + 32}">{html.escape(at)}</text>'
             f"<title>{label} · {html.escape(at)}{'' if expands(n, rule) else ' · 펼치지 않음'}</title>")
    if n in cards:
        return f'<a href="../symbols/{html.escape(cards[n])}" class="{cls}">{inner}</a>'
    return f'<g class="{cls}">{inner}</g>'


def arrows(pos: dict, depth: dict, edges: dict) -> str:
    out = []
    for (a, b), h in edges.items():
        if a not in pos or b not in pos:
            continue
        (xa, ya), (xb, yb) = pos[a], pos[b]
        kind = "ind" if h.edge.kind == "dispatches" else "asm" if h.edge.kind == "asm_calls" else "dir"
        tip = html.escape(f"{g.name(a)} → {g.name(b)} · {h.edge.ev}" + (f" · 간접, 규칙 {h.candidate.rule}" if h.candidate else ""))
        if xb > xa:
            x1, y1, x2, y2 = xa + BW, ya + BH / 2, xb, yb + BH / 2
            c = (x2 - x1) / 2
            d = f"M{x1},{y1} C{x1 + c},{y1} {x2 - c},{y2} {x2},{y2}"
        else:  # same column or backwards: loop around the right side
            x1, y1, x2, y2 = xa + BW, ya + BH / 2, xb + BW, yb + BH / 2
            r = 30 + abs(y2 - y1) / 8
            d = f"M{x1},{y1} C{x1 + r},{y1} {x2 + r},{y2} {x2 + 6},{y2}"
            kind += " back"
        out.append(f'<path class="e {kind}" d="{d}" marker-end="url(#m-{kind.split()[0]})"><title>{tip}</title></path>')
    return "".join(out)


def svg(pos: dict, depth: dict, edges: dict, extra: str = "") -> str:
    w = max(x for x, _ in pos.values()) + BW + 60
    h = max(y for _, y in pos.values()) + BH + 20
    markers = "".join(f'<marker id="m-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                      f'<path d="M0,0 L10,5 L0,10 z" class="mk {k}"/></marker>' for k in ("dir", "ind", "asm"))
    return (f'<div class="scroll"><svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{markers}</defs>{extra}'
            f'<g>{arrows(pos, depth, edges)}</g><g>{"".join(box(n, x, y, RULE) for n, (x, y) in pos.items())}</g></svg></div>')


def order_columns(depth: dict, edges: dict) -> dict[int, list[str]]:
    """Columns by depth; each column sorted by the mean row of its neighbours toward the root."""
    cols: dict[int, list[str]] = {}
    for n, d in depth.items():
        cols.setdefault(d, []).append(n)
    rank = {root: 0.0}
    for ds in (range(1, max(cols) + 1), range(-1, min(cols) - 1, -1)):
        for d in ds:
            prev = d - 1 if d > 0 else d + 1
            def key(n):
                ps = [rank[p] for (a, b) in edges for p, q in ((a, b), (b, a)) if q == n and depth.get(p) == prev and p in rank]
                return (sum(ps) / len(ps) if ps else 1e9, g.name(n))
            cols[d].sort(key=key)
            for i, n in enumerate(cols[d]):
                rank[n] = float(i)
    return cols


def variant_a(depth, edges) -> str:
    cols = order_columns(depth, edges)
    lo = min(cols)
    pos = {}
    for d, ns in cols.items():
        for i, n in enumerate(ns):
            pos[n] = (20 + (d - lo) * (BW + GX), 34 + i * (BH + GY))
    heads = "".join(f'<text class="colh" x="{20 + (d - lo) * (BW + GX)}" y="18">'
                    f'{"부르는 쪽 " + str(-d) if d < 0 else "시작" if d == 0 else "깊이 " + str(d)}</text>' for d in cols)
    return svg(pos, depth, edges, heads)


LANES = ["asm", "userprog", "vm", "filesys", "threads", "devices", "lib", "include"]


def variant_b(depth, edges) -> str:
    cols = order_columns(depth, edges)
    lo = min(cols)
    lane = lambda n: "asm" if n.startswith("asm:") or file_of(n).endswith(".S") else file_of(n).split("/")[0]
    cells: dict[tuple[str, int], list[str]] = {}
    for d, ns in cols.items():
        for n in ns:
            cells.setdefault((lane(n), d), []).append(n)
    used = [l for l in LANES if any(k[0] == l for k in cells)] + sorted({k[0] for k in cells} - set(LANES))
    pos, bands, y = {}, [], 30
    for i, l in enumerate(used):
        rows = max(len(v) for k, v in cells.items() if k[0] == l)
        hgt = rows * (BH + GY) + 16
        bands.append(f'<rect class="lane{i % 2}" x="0" y="{y}" width="100%" height="{hgt}"/>'
                     f'<text class="laneh" x="8" y="{y + 18}">{l}/</text>')
        for (ln, d), ns in cells.items():
            if ln == l:
                for j, n in enumerate(ns):
                    pos[n] = (110 + (d - lo) * (BW + GX), y + 8 + j * (BH + GY))
        y += hgt
    heads = "".join(f'<text class="colh" x="{110 + (d - lo) * (BW + GX)}" y="18">'
                    f'{"부르는 쪽 " + str(-d) if d < 0 else "시작" if d == 0 else "깊이 " + str(d)}</text>' for d in cols)
    return svg(pos, depth, edges, "".join(bands) + heads)


def variant_c(rule: bool) -> str:
    v = FlowView(idx, SPEC, cards)
    base_out, base_in = v.g.flow_out, v.g.flow_in
    v.g.flow_out = lambda n: base_out(n) if expands(n, rule) else []
    page = v.render()
    return page[page.index("<section>"):page.index('<details class="meta">')]


EXTRA_CSS = """
.wrap{max-width:none; padding:32px 16px 120px}
.v{display:none}
""" + ",".join(f"body[data-v={v}][data-r={r}] .v{v}.r{r}" for v in "ABC" for r in ("on", "off")) + """{display:block}
.scroll{overflow-x:auto; border:1px solid var(--line)}
svg{display:block; font-family:var(--font-code)}
.node rect{fill:var(--surface); stroke:var(--ink-2); stroke-width:1}
.node.root rect{stroke:var(--ink); stroke-width:2.5}
.node.stop rect{fill:var(--surface-2); stroke:var(--line); stroke-dasharray:4 3}
a.node:hover rect{stroke:var(--s2); stroke-width:2}
.nm{font-size:13px; font-weight:600; fill:var(--ink)} .node.stop .nm{fill:var(--ink-2); font-weight:500}
.loc{font-size:10.5px; fill:var(--muted)}
.colh{font-size:12px; fill:var(--muted)}
.laneh{font-size:13px; font-weight:600; fill:var(--ink-2)}
.lane0{fill:var(--surface-2); opacity:.55} .lane1{fill:transparent}
.e{fill:none; stroke:var(--muted); stroke-width:1.2; opacity:.75}
.e.ind{stroke:var(--s3); stroke-width:1.6} .e.asm{stroke:var(--s4); stroke-width:1.6}
.e.back{stroke-dasharray:3 3}
.e:hover{opacity:1; stroke-width:2.5}
.mk.dir{fill:var(--muted)} .mk.ind{fill:var(--s3)} .mk.asm{fill:var(--s4)}
.legend{display:flex; flex-wrap:wrap; gap:6px 14px; font-size:.8rem; color:var(--ink-2); align-items:center}
.ctl{display:flex; gap:8px; align-items:center; font-size:.85rem}
.ctl button{font:inherit; padding:2px 10px; border:1px solid var(--line); background:var(--surface); color:var(--ink); cursor:pointer}
.ctl button[aria-pressed=true]{background:var(--ink); color:var(--bg)}
#bar{position:fixed; left:50%; bottom:18px; transform:translateX(-50%); display:flex; gap:10px; align-items:center;
  padding:8px 14px; background:#111; color:#fff; border-radius:999px; box-shadow:0 4px 18px rgba(0,0,0,.35); font-family:var(--font-code); font-size:13px; z-index:9}
#bar button{background:none; border:0; color:#fff; font-size:18px; cursor:pointer; padding:0 6px}
"""

VARIANTS = {"A": "층별 흐름도", "B": "서브시스템 레인", "C": "지금의 접기 트리"}

body = []
counts = {}
for rule in (True, False):
    RULE = rule
    depth, edges = collect(rule)
    counts[rule] = (len(depth), len(edges))
    r = "ron" if rule else "roff"
    body.append(f'<div class="v vA r {r}">{variant_a(depth, edges)}</div>')
    body.append(f'<div class="v vB r {r}">{variant_b(depth, edges)}</div>')
    body.append(f'<div class="v vC r {r}">{variant_c(rule)}</div>')

(on_n, on_e), (off_n, off_e) = counts[True], counts[False]
page = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Flow Form Prototype</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;600;700&display=swap">
<style>{CSS}{EXTRA_CSS}</style></head>
<body data-v="A" data-r="on"><div class="wrap">
<header><h1 class="dh">page_fault 흐름 · 형태 시제품</h1>
<p class="sub">PROTOTYPE, 버릴 코드. 같은 사실(index.json)을 세 형태로 그림. 나가는 호출 4단계, 들어오는 호출 2단계.</p>
<div class="ctl">펼침 규칙
 <button data-r="on" aria-pressed="true">vm/ · userprog/ 만 펼침 ({on_n}개 · 화살표 {on_e})</button>
 <button data-r="off" aria-pressed="false">모두 펼침 ({off_n}개 · 화살표 {off_e})</button></div>
<div class="legend"><span>━ 직접 호출</span><span style="color:var(--s3)">━ 간접 호출(후보)</span><span style="color:var(--s4)">━ asm (not clang)</span>
<span>┅ 뒤로 가는 호출</span><span>점선 상자 = 보이지만 펼치지 않음</span><span>상자 클릭 = 카드, 마우스 올림 = file:line</span></div>
</header>
{''.join(body)}
</div>
<div id="bar"><button id="prev" aria-label="이전">‹</button><span id="lbl"></span><button id="next" aria-label="다음">›</button></div>
<script>
const V = {list(VARIANTS)!r}, N = {VARIANTS!r};
const b = document.body, q = new URLSearchParams(location.search);
function setV(v) {{ b.dataset.v = v; document.getElementById('lbl').textContent = v + ' (' + N[v] + ')';
  q.set('variant', v); history.replaceState(null, '', '?' + q); }}
function step(k) {{ setV(V[(V.indexOf(b.dataset.v) + k + V.length) % V.length]); }}
document.getElementById('prev').onclick = () => step(-1);
document.getElementById('next').onclick = () => step(1);
addEventListener('keydown', e => {{ if (e.target.closest('input,textarea,[contenteditable]')) return;
  if (e.key === 'ArrowLeft') step(-1); if (e.key === 'ArrowRight') step(1); }});
document.querySelectorAll('.ctl button').forEach(x => x.onclick = () => {{ b.dataset.r = x.dataset.r;
  document.querySelectorAll('.ctl button').forEach(y => y.setAttribute('aria-pressed', y === x)); }});
setV(V.includes(q.get('variant')) ? q.get('variant') : 'A');
</script></body></html>
"""
dest = OUT / "views" / "prototype-flow-form.html"
dest.write_text(page)
print(dest, f"rule on {counts[True]}, off {counts[False]}")
