"""Build the study-site copies of the teach-bot lessons.

Each output in this directory is the original that the study site copies byte
for byte (benjohnbill.github.io AGENTS.md, "Copies"). Edit the lesson, run
this script, then copy the outputs to study/week13/mini-webserver/lessons/.

    python3 publish/build.py

Base: ../teach/publish/build.py.
"""

import html as htmllib
import json
import re
from pathlib import Path

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import CLexer

TEACH = Path(__file__).resolve().parent.parent
ASSETS = TEACH / "assets"
HOME = '<a class="home" href="https://benjohnbill.github.io/">← 학습 기록</a>'
HINT = '<p class="scroll-hint" data-scroll-hint>옆으로 밀어 보기 →</p>'
SITE_CSS = '<link rel="stylesheet" href="https://benjohnbill.github.io/assets/site.css">'

# source file (relative to TEACH) -> published slug
PAGES = {
    "lessons/0001-map-and-cost.html": "l1-map-and-cost.html",
    "lessons/0002-clienthello-fingerprint.html": "l2-clienthello-fingerprint.html",
    "lessons/0003-http-volume.html": "l3-http-volume.html",
}
# quiz answers he gave in his local lesson pages, if any (publish/answers.json)
ANSWERS_FILE = Path(__file__).resolve().parent / "answers.json"
ANSWERS = json.loads(ANSWERS_FILE.read_text(encoding="utf-8")) if ANSWERS_FILE.exists() else {}
SEED_JSON = json.dumps(ANSWERS, ensure_ascii=False).replace("</", "<\\/")


def rewrite_links(html: str) -> str:
    for source, slug in PAGES.items():
        name = Path(source).name
        folder = Path(source).parent.name
        html = html.replace(f'href="../{folder}/{name}"', f'href="{slug}"')
        html = html.replace(f'href="{name}"', f'href="{slug}"')
    return html


RAINBOW = 3  # bracket colors b0..b2 by depth, as in his editor


def color_code(match: re.Match) -> str:
    """Color one <pre> block of C like his Neovim theme orchid (see site-bridge.css)."""
    code = htmllib.unescape(match.group(1))
    spans = highlight(code, CLexer(), HtmlFormatter(nowrap=True)).rstrip("\n")
    # orchid colors storage words like flow words, and constants (CONN_DROP) apart
    for word in ("struct", "static", "const", "enum", "sizeof"):
        spans = spans.replace(f'<span class="k">{word}</span>', f'<span class="kd">{word}</span>')
    spans = re.sub(r'<span class="n">([A-Z][A-Z0-9_]+)</span>', r'<span class="no">\1</span>', spans)
    depth = 0

    def bracket(char: str) -> str:
        nonlocal depth
        if char in "([{":
            depth += 1
            return f'<span class="b{(depth - 1) % RAINBOW}">{char}</span>'
        depth -= 1
        return f'<span class="b{depth % RAINBOW}">{char}</span>'

    def punct(m: re.Match) -> str:
        return "".join(bracket(ch) if ch in "()[]{}" else f'<span class="p">{ch}</span>' for ch in m.group(1))

    spans = re.sub(r'<span class="p">(.*?)</span>', punct, spans)
    return f'<pre class="hl">{spans}</pre>'


def build(source: str, slug: str) -> None:
    html = (TEACH / source).read_text(encoding="utf-8")
    bridge = (ASSETS / "site-bridge.css").read_text(encoding="utf-8")
    style_link = '<link rel="stylesheet" href="../assets/style.css">'
    if style_link not in html:
        raise SystemExit(f"{source}: missing {style_link}")
    html = html.replace(style_link, f"{SITE_CSS}\n<style>\n{bridge}</style>")
    if 'name="viewport"' not in html:
        html = html.replace(
            '<meta charset="utf-8">\n',
            '<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n',
            1,
        )
    seed_tag = '<script src="../assets/quiz.js"></script>'
    if seed_tag in html and ANSWERS:
        html = html.replace(seed_tag, f"<script>window.QUIZ_SEED = {SEED_JSON};</script>\n{seed_tag}")
    for script in ("stepper.js", "quiz.js"):
        tag = f'<script src="../assets/{script}"></script>'
        if tag in html:
            code = (ASSETS / script).read_text(encoding="utf-8")
            html = html.replace(tag, f"<script>\n{code}</script>")
    html = html.replace("<body>\n", f'<body>\n<div class="wrap">\n{HOME}\n', 1)
    html = re.sub(r"<pre>(.*?)</pre>", color_code, html, flags=re.S)
    html = html.replace('\n<pre class="hl">', f'\n{HINT}\n<pre class="hl">')
    html = html.replace("</body>", "</div>\n</body>", 1)
    html = rewrite_links(html)
    if "../" in html:
        raise SystemExit(f"{source}: a relative link to ../ is left")
    (TEACH / "publish" / slug).write_text(html, encoding="utf-8")
    print(f"{source} -> publish/{slug}")


for source, slug in PAGES.items():
    build(source, slug)
