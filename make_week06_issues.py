#!/usr/bin/env python3
"""week6_issues_complete.csv -> benjohnbill/SW-AI-malloc-lab 이슈 생성 (gh CLI).

week5 용 make_week05_issues.py 와 같은 흐름. 다른 점은 본문 수집기뿐이다:
week6 의 CSV 에는 문제별 설명이 없고 과제는 malloc-lab/mm.c 하나다. 그래서 본문에는
파일 경로와 실행 명령만 넣는다. 구현 방법에 대한 힌트는 넣지 않는다.

사용법:
    python3 make_week06_issues.py --dry-run
    python3 make_week06_issues.py
"""
import csv, json, re, subprocess, sys
from pathlib import Path

REPO = "benjohnbill/SW-AI-malloc-lab"
WEEK = "6"
ROOT = Path.home() / "dev/krafton-jungle/week06"
CSV = Path.home() / "dev/krafton-jungle/issue-template/week6_issues_complete.csv"

TRACE_ROW = re.compile(r"^테스트 - (?P<stem>.+)-bal\.rep -> valid yes$")


def collect_traces():
    """traces/<이름>-bal.rep 의 <이름> 집합. CSV 의 trace 이름이 레포에 있는지 대조한다."""
    return {p.name[: -len("-bal.rep")] for p in (ROOT / "malloc-lab/traces").glob("*-bal.rep")}


def build_body(title, traces):
    if title.startswith("구현 - "):
        return "`malloc-lab/mm.c`"
    m = TRACE_ROW.match(title)
    if m:
        stem = m["stem"]
        if stem not in traces:
            print(f"⚠️  레포에서 trace 를 찾지 못했습니다: {stem}", file=sys.stderr)
            return ""
        return "\n".join([
            f"`malloc-lab/traces/{stem}-bal.rep`", "",
            "### 실행", "",
            "```",
            f"make r_{stem}       # 호스트 실행 (valid yes 확인)",
            f"make dr_{stem}      # 컨테이너 실행",
            "```",
        ])
    if title.startswith("테스트 - perf index"):
        return "\n".join([
            "```",
            "make score        # 기본 11개 trace 전체. 끝의 Perf index 줄이 (util) + (thru)",
            "```",
        ])
    return ""


def existing_titles():
    out = subprocess.run(
        ["gh", "issue", "list", "--repo", REPO, "--state", "all",
         "--limit", "500", "--json", "title"],
        capture_output=True, text=True, check=True).stdout
    return {row["title"] for row in json.loads(out)}


def main():
    dry = "--dry-run" in sys.argv
    traces = collect_traces()

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
        body = build_body(title, traces)
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
