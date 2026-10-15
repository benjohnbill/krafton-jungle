#!/usr/bin/env python3
"""week8_issues_complete.csv -> benjohnbill/pintos-userprog 이슈 생성 (gh CLI).

week6 용 make_week06_issues.py 와 같은 흐름. 다른 점은 본문 수집기뿐이다:
테스트 행은 레포에서 그 테스트의 .c 위치를 찾아 경로와 실행 라벨(week08 의 로컬
GNUmakefile)을 넣는다. 구현 방법에 대한 힌트는 넣지 않는다.

사용법:
    python3 make_week08_issues.py --dry-run
    python3 make_week08_issues.py
"""
import csv, json, subprocess, sys
from pathlib import Path

REPO = "benjohnbill/pintos-userprog"
WEEK = "8"
ROOT = Path.home() / "dev/krafton-jungle/week08"
CSV = Path.home() / "dev/krafton-jungle/issue-template/week8_issues_complete.csv"

GITBOOK = "https://casys-kaist.github.io/pintos-kaist/project2"
STUDY = {
    "학습 - kaist gitbook Project2 UserPrograms": f"{GITBOOK}/introduction.html",
    "학습 - kaist gitbook Project2 FAQ": f"{GITBOOK}/FAQ.html",
}
# userprog 빌드의 TEST_SUBDIRS (pintos/userprog/Make.vars) + extra 의 dup2
TEST_DIRS = ["tests/userprog", "tests/userprog/no-vm", "tests/filesys/base",
             "tests/threads", "tests/userprog/dup2"]


def collect_tests():
    """테스트 이름 -> pintos/ 아래 디렉터리. .ck 가 있는 것만 테스트로 친다."""
    found = {}
    for d in TEST_DIRS:
        for ck in (ROOT / "pintos" / d).glob("*.ck"):
            found.setdefault(ck.stem, d)
    return found


def build_body(title, tests):
    if title in STUDY:
        return STUDY[title]
    if not title.startswith("테스트 - "):
        return ""
    name = title[len("테스트 - "):].removesuffix(" (extra)")
    d = tests.get(name)
    if d is None:
        print(f"⚠️  레포에서 테스트를 찾지 못했습니다: {name}", file=sys.stderr)
        return ""
    lines = [f"`pintos/{d}/{name}.c` · 기대 출력 `{name}.ck`", ""]
    if d.endswith("dup2"):
        lines += ["extra: `pintos/userprog/Make.vars` 의 EXTRA2 블록을 켜야 빌드·채점된다."]
    else:
        lines += ["### 실행", "", "```",
                  f"make dr_{name}      # 컨테이너: 빌드 + 이 테스트 하나",
                  "make dcheck            # 전체 (userprog make check)", "```"]
    return "\n".join(lines)


def existing_titles():
    out = subprocess.run(
        ["gh", "issue", "list", "--repo", REPO, "--state", "all",
         "--limit", "500", "--json", "title"],
        capture_output=True, text=True, check=True).stdout
    return {row["title"] for row in json.loads(out)}


def main():
    dry = "--dry-run" in sys.argv
    tests = collect_tests()

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
        body = build_body(title, tests)
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
