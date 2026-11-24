"""Build the study-site copies of the teach-bot lessons.

Each output in this directory is the original that the study site copies byte
for byte (benjohnbill.github.io AGENTS.md, "Copies"). Edit the lesson, run
this script, then copy the outputs to study/week13/mini-webserver/lessons/.

    python3 publish/build.py

Base: ../teach/publish/build.py.
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
    html = html.replace("\n<pre>", f"\n{HINT}\n<pre>")
    html = html.replace("</body>", "</div>\n</body>", 1)
    html = rewrite_links(html)
    if "../" in html:
        raise SystemExit(f"{source}: a relative link to ../ is left")
    (TEACH / "publish" / slug).write_text(html, encoding="utf-8")
    print(f"{source} -> publish/{slug}")


for source, slug in PAGES.items():
    build(source, slug)
