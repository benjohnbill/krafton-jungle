# 팀 이슈 초안 (user가 직접 올림)

제목: `make lint`가 도구 실패를 "위반 없음"으로 보고함 (scripts/convention.py)

---

## 현상

`clang-format`이나 `clang-tidy`가 실행 중 실패해도 `make lint`가
`lint: 위반 없음`을 출력하고 exit 0으로 끝납니다. 검사가 돌지 않았는데 통과로 보입니다.

## 원인

`scripts/convention.py`가 `subprocess.run()`의 `returncode`를 읽지 않습니다.

- `check_layout()` (`:60-66`): `clang-format --dry-run`의 stderr만 파싱. 도구가 실패해도 "모양 0줄"로 셈
- `tidy_one()` (`:96-106`): 출력 줄만 반환. 종료 코드는 버림
- 컴파일 에러(`clang-diagnostic-error`)도 "naming"으로 분류됨 (`:131` 부근)

## 재현

실패하는 가짜 도구를 PATH 앞에 둡니다.

```sh
mkdir -p /tmp/fakebin
printf '#!/bin/sh\nexit 2\n' > /tmp/fakebin/clang-format
printf '#!/bin/sh\nexit 2\n' > /tmp/fakebin/clang-tidy
chmod +x /tmp/fakebin/*
PATH=/tmp/fakebin:$PATH python3 scripts/convention.py lint; echo "exit=$?"
# 출력: lint: 위반 없음
# exit=0
```

## 제안

1. 두 함수에서 `proc.returncode`를 확인하고, 위반 0건이어도 도구가 0이 아닌 코드로 끝나면 "도구 실패"로 따로 보고 + exit 2
   (clang-format `--dry-run`은 위반이 있어도 0을 반환하니 0이 아닌 값은 실패로 봐도 됨. clang-tidy는 `--warnings-as-errors=*` 때문에 위반 시 1을 반환하므로, 출력에 진단이 없는데 0이 아니면 실패로 판단)
2. `clang-diagnostic-error`는 "naming"이 아니라 "컴파일 에러"로 분류

나중에 lint를 CI나 hook에 연결하려면 이 수정이 먼저 필요합니다. 지금 상태로 연결하면 도구가 깨졌을 때 초록불이 켜집니다.
