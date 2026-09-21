#!/usr/bin/env python3
"""week5_issues_complete.csv -> benjohnbill/SW-AI-C-debugging 이슈 생성 (gh CLI).

week4 용 make_week_issues.py 와 같은 흐름. 다른 점은 소스 수집기뿐이다:
week5 는 challenges/NN_name/bug.c 하나가 한 문제이고, 문제 설명은 PDF 가 아니라
bug.c 상단 주석의 [시나리오] / [기대 동작] 이다. [증상]·gdb 레시피·TODO 는
정답 힌트라서 이슈 본문에 넣지 않는다.

사용법:
    python3 make_week05_issues.py --dry-run
    python3 make_week05_issues.py
"""
import csv, json, re, subprocess, sys, textwrap
from pathlib import Path

REPO = "benjohnbill/SW-AI-C-debugging"
WEEK = "5"
ROOT = Path.home() / "dev/krafton-jungle/week05"
CSV = Path.home() / "dev/krafton-jungle/issue-template/week5_issues_complete.csv"

# CSV 와 레포의 이름이 다른 항목. 이슈 제목은 레포 기준으로 맞춘다.
RENAME = {"16_off_by_one_string": "16_unused_cap_overflow"}


def header_sections(text):
    """상단 블록 주석에서 제목 줄과 [시나리오]/[기대 동작] 절만 뽑는다."""
    m = re.match(r"\s*/\*(.*?)\*/", text, re.S)
    if not m:
        return None, {}
    lines = [re.sub(r"^\s*\*\s?", "", l) for l in m.group(1).splitlines()]
    title = next((l.strip() for l in lines if l.strip()), "")
    sections, cur = {}, None
    for l in lines:
        s = l.strip()
        if s.startswith("[") and s.endswith("]"):
            cur = s[1:-1]
            sections[cur] = []
        elif cur:
            sections[cur].append(l.rstrip())
    return title, sections


def collect_sources():
    """챌린지 이름 -> (레포 기준 경로, 제목 줄, 절 dict)"""
    table = {}
    for c in sorted(ROOT.glob("challenges/*/bug.c")):
        name = c.parent.name
        title, sections = header_sections(c.read_text(encoding="utf-8", errors="replace"))
        table[name] = (c.relative_to(ROOT).as_posix(), title, sections)
    return table


def build_body(title, sources):
    if not title.startswith("구현 - "):
        return "", title
    name = title.split(" - ", 1)[1].strip()
    name = RENAME.get(name, name)
    fixed_title = f"구현 - {name}"
    if name not in sources:
        print(f"⚠️  레포에서 챌린지를 찾지 못했습니다: {name}", file=sys.stderr)
        return "", fixed_title
    path, head, sections = sources[name]
    parts = [f"`{path}`", "", f"**{head}**"]
    for key in ("시나리오", "기대 동작"):
        body = textwrap.dedent("\n".join(sections.get(key, []))).strip("\n")
        if body:
            parts += ["", f"### {key}", "", body]
    parts += [
        "", "### 실행", "",
        "```", f"make g_{name}       # 호스트 gdb", f"make dr_{name}      # 컨테이너 실행 (수정 후 exit 0 확인)", "```",
    ]
    return "\n".join(parts), fixed_title


def existing_titles():
    out = subprocess.run(
        ["gh", "issue", "list", "--repo", REPO, "--state", "all",
         "--limit", "500", "--json", "title"],
        capture_output=True, text=True, check=True).stdout
    return {row["title"] for row in json.loads(out)}


def main():
    dry = "--dry-run" in sys.argv
    sources = collect_sources()

    rows = []
    with CSV.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            t = (row.get("title") or "").strip()
            if t:
                rows.append(t)

    print(f"📋 Week {WEEK} 이슈 {len(rows)}개, 대상 레포 {REPO}")
    seen = set() if dry else existing_titles()
    if not dry:
        print(f"📌 기존 이슈 {len(seen)}개")

    made = skipped = failed = 0
    for idx, title in enumerate(rows, 1):
        body, title = build_body(title, sources)
        issue_title = f"[WEEK{WEEK}] {title}"

        if dry:
            print(f"\n[{idx:2d}/{len(rows)}] {issue_title}")
            if body:
                print("\n".join("    " + l for l in body.splitlines()))
            made += 1
            continue

        if issue_title in seen:
            print(f"⏭️  [{idx:2d}/{len(rows)}] {issue_title} (이미 존재)")
            skipped += 1
            continue

        r = subprocess.run(
            ["gh", "issue", "create", "--repo", REPO,
             "--title", issue_title, "--body-file", "-"],
            input=body, capture_output=True, text=True)
        if r.returncode == 0:
            print(f"✅ [{idx:2d}/{len(rows)}] {issue_title}  {r.stdout.strip()}")
            made += 1
        else:
            print(f"❌ [{idx:2d}/{len(rows)}] {issue_title}\n   {r.stderr.strip()}")
            failed += 1

    print(f"\n생성 {made} · 스킵 {skipped} · 실패 {failed}")


if __name__ == "__main__":
    main()
