#!/usr/bin/env bash
# ADR과 테스트를 ID로 오갑니다. 출력은 Zed 터미널에서 Ctrl+클릭하는 절대 경로:줄입니다.
# Zed task가 부릅니다: decision-links.sh <선택한 텍스트 또는 none> <지금 파일> <지금 줄>
#   선택한 ID(F23)        → 그 ID의 테스트와 인용한 ADR
#   ADR 파일, 선택 없음    → 그 ADR이 인용한 테스트 전부
#   테스트 파일, 선택 없음 → 커서가 있는 테스트를 인용한 ADR
set -euo pipefail
repo="$(cd "$(dirname "$0")/.." && pwd)/mini-react"
selected="${1:-none}"
file="${2:-}"
row="${3:-1}"
test_call="\b(it|test)(\.\w+)*\(\s*[\"'\`]"

find_by_id() {
  rg -n --no-heading -w -- "$1" "$repo/src" "$repo/docs/adr" || echo "(없음) $1"
}

if [[ "$selected" != "none" && -n "$selected" ]]; then
  find_by_id "$selected"
elif [[ "$file" == *.md ]]; then
  ids=$(grep -oP '\(테스트: \K[^)]*' "$file" | tr ',' '\n' | tr -d ' ' | sort -u)
  for id in $ids; do
    rg -n --no-heading "${test_call}${id}[\s:]" "$repo/src" || echo "(없음) $id"
  done
elif [[ "$file" == *.test.ts ]]; then
  id=$(head -n "$row" "$file" | grep -oP "${test_call}\K[A-Z][A-Z-]*\d+[a-z]?(?=[\s:])" | tail -1 || true)
  if [[ -z "$id" ]]; then
    echo "커서 위에 ID로 시작하는 테스트가 없습니다" >&2
    exit 1
  fi
  echo "$id"
  rg -n --no-heading -w -- "$id" "$repo/docs/adr" || echo "(인용한 ADR 없음) $id"
else
  echo "ID를 선택하거나, ADR 파일이나 테스트 파일에서 실행하세요" >&2
  exit 1
fi
