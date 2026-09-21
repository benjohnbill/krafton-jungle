#!/usr/bin/env python3
"""week4_issues_complete.csv -> benjohnbill/SW-AI-C 이슈 생성 (gh CLI 사용).

사용법:
    python3 make_week4_issues.py --dry-run
    python3 make_week4_issues.py
"""
import csv, json, re, subprocess, sys
from pathlib import Path

REPO = "benjohnbill/SW-AI-C"
WEEK = "4"      # 주차 변경 시 이 세 줄만 수정
ROOT = Path.home() / "dev/krafton-jungle/week04"
CSV = Path.home() / "dev/krafton-jungle/issue-template/week4_issues_complete.csv"
MARKER = "should not change the prototype"


def collect_sources():
    """파일명 -> (레포 기준 상대 경로, 구현할 함수 시그니처 목록, 문제 PDF 경로)"""
    table = {}
    for c in sorted(ROOT.glob("Data-Structures/*/Q*.c")):
        lines = c.read_text(encoding="utf-8", errors="replace").splitlines()
        protos = []
        for i, line in enumerate(lines):
            if MARKER not in line:
                continue
            for nxt in lines[i + 1:]:
                s = nxt.strip()
                if not s:
                    break
                if s.endswith(";") and s not in protos:
                    protos.append(s)
                else:
                    break
        pdfs = sorted(c.parent.glob("*.pdf"))
        table[c.name] = (
            c.relative_to(ROOT).as_posix(),
            protos,
            pdfs[0].relative_to(ROOT).as_posix() if pdfs else None,
        )
    return table


def build_body(title, sources):
    """'구현 - Qn_*.c' 항목만 본문을 채우고, 나머지는 빈 본문으로 둔다."""
    if not title.startswith("구현 - "):
        return ""
    fname = title.split(" - ", 1)[1].strip()
    if fname not in sources:
        print(f"⚠️  템플릿에서 파일을 찾지 못했습니다: {fname}", file=sys.stderr)
        return ""
    path, protos, pdf = sources[fname]
    parts = [f"`{path}`", "", "구현할 함수:", "", "```c"]
    parts += protos if protos else ["// 시그니처를 추출하지 못했습니다"]
    parts += ["```"]
    if pdf:
        parts += ["", f"문제 설명: `{pdf}`"]
    return "\n".join(parts)


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
        issue_title = f"[WEEK{WEEK}] {title}"
        body = build_body(title, sources)

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

    print(f"\n생성 {made}개 / 건너뜀 {skipped}개 / 실패 {failed}개")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
