"""Build the study-site copies of lessons and references.

Each output in this directory is the original that the study site copies byte
for byte (benjohnbill.github.io AGENTS.md, "Copies"). Edit the lesson or
reference, run this script, then copy the outputs to study/week13/.

    python3 publish/build.py
"""

import json
from pathlib import Path

TEACH = Path(__file__).resolve().parent.parent
ASSETS = TEACH / "assets"
HOME = '<a class="home" href="https://benjohnbill.github.io/">← 학습 기록</a>'
HINT = '<p class="scroll-hint" data-scroll-hint>옆으로 밀어 보기 →</p>'
SITE_CSS = '<link rel="stylesheet" href="https://benjohnbill.github.io/assets/site.css">'

# source file (relative to TEACH) -> published slug
PAGES = {
    "lessons/0001-connection-setup-and-fd.html": "l1-connection-setup.html",
    "lessons/0002-socket-lookup-and-receive-buffer.html": "l2-receive-buffer.html",
    "lessons/0003-close-and-failure.html": "l3-close-and-failure.html",
    "reference/syscall-lanes.html": "syscall-lanes.html",
}
SITE_WEEK = "https://benjohnbill.github.io/study/week13/"
# quiz answers he gave on 2026-11-20 in his local lesson pages (read from that browser's localStorage)
ANSWERS = json.loads((Path(__file__).resolve().parent / "answers.json").read_text(encoding="utf-8"))
for entry in ANSWERS.values():
    entry.setdefault("date", "2026-11-20")
SEED_JSON = json.dumps(ANSWERS, ensure_ascii=False).replace("</", "<\\/")


def rewrite_links(html: str) -> str:
    for source, slug in PAGES.items():
        name = Path(source).name
        folder = Path(source).parent.name
        html = html.replace(f'href="../{folder}/{name}"', f'href="{slug}"')
        html = html.replace(f'href="{name}"', f'href="{slug}"')
    # lab notes (week13/lab/pages/) are copied to the site under the same name
    html = html.replace('href="../../pages/', f'href="{SITE_WEEK}')
    return html


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
    # his own picks and predictions, read from his local lesson pages (publish/answers.json)
    seed_tag = '<script src="../assets/quiz.js"></script>'
    if seed_tag in html:
        html = html.replace(seed_tag, f"<script>window.QUIZ_SEED = {SEED_JSON};</script>\n{seed_tag}")
    for script in ("stepper.js", "quiz.js", "flow-lanes.js"):
        tag = f'<script src="../assets/{script}"></script>'
        if tag in html:
            code = (ASSETS / script).read_text(encoding="utf-8")
            html = html.replace(tag, f"<script>\n{code}</script>")
    html = html.replace("<body>\n", f'<body>\n<div class="wrap">\n{HOME}\n', 1)
    html = html.replace("\n<pre>", f"\n{HINT}\n<pre>")
    html = html.replace("</body>", "</div>\n</body>", 1)
    html = rewrite_links(html)
    if "../" in html:
        raise SystemExit(f"{source}: a relative link to ../ is left")
    (TEACH / "publish" / slug).write_text(html, encoding="utf-8")
    print(f"{source} -> publish/{slug}")


for source, slug in PAGES.items():
    build(source, slug)
