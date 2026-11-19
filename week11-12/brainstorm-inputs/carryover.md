# 저장소 사이에 이어진 규칙 (Pintos 2개 + mini 3개)

조사일 2026-11-18. 읽기만 했고, 저장소에는 아무것도 바꾸지 않았습니다.
층과 표시는 `layer-table.md`와 같습니다.

층: 1 코드베이스 · 2 정적 (lint, typecheck, 컴파일러, 테스트, CI, ID 검사) · 3 검증 (실제 실행, sanitizer, 시연) · 4 문서 · 5 사람.
강제되나: ✓ 아무도 고르지 않아도 도구가 실패시키거나 막음 · △ 누가 실행할 때만 · ✗ 문서뿐 · ? 확인 못 함.

## 읽은 상태

| # | 저장소 | 로컬 clone | 읽은 기준 | 비고 |
|---|---|---|---|---|
| 1 | pintos-userprog (`benjohnbill/pintos-userprog`, private, 2026-10-15 생성) | `week08`, 로컬 브랜치 `benjohnbill` | `origin/main` `900aff9` (2026-10-21) | `origin/develop`과 내용이 같음 (`git diff` 비어 있음) |
| 2 | Pintos VM (`Pintos-W9-10-T6-VM/Pintos-W9-10-T6-VM`, 조직 소유 private, 2026-10-23 생성) | `week09`, 로컬 브랜치 `CJG` | `origin/main` `b250bd1` (2026-10-26) | 기본 브랜치는 `main`. 팀 작업은 `origin/develop` `f296e71` (2026-11-06)에 쌓였고 `main`에는 10-26 뒤로 병합이 없음. `develop`에서만 다른 규칙은 행에 따로 적음 |
| 3 | mini-react | `week11-12/mini-react` | `origin/main` `a6df9f7` | `layer-table.md`와 같음 |
| 4 | mini-redis | `week11-12/mini-redis` | `origin/main` `1a64bd7` (2026-11-18) | `layer-table.md` 조사 뒤 커밋이 더 있음 |
| 5 | mini-dbms | `week11-12/mini-dbms` | `origin/main` `921223e` | `layer-table.md`와 같음 |

Pintos 두 저장소의 `CLAUDE.md`(둘 다)와 `GLOSSARY.md`(week09)는 로컬에만 있고 `.git/info/exclude`로 git에서 빠져 있습니다. 어느 브랜치의 이력에도 없습니다. `AGENTS.md`는 두 저장소의 어느 브랜치에도 없습니다.

## A. 층 표: Pintos 두 저장소

### GitHub 설정 요약

| 저장소 | ruleset | branch protection | 필수 check | workflow | 기타 |
|---|---|---|---|---|---|
| pintos-userprog | 없음 (`[]`, `rules/branches/main`도 `[]`) | `main`, `develop` 모두 없음 (404) | 없음 | 저장소 파일에는 없음. Actions 목록에 `Copilot cloud agent` (dynamic) 하나 | merge, squash, rebase 모두 허용, `delete_branch_on_merge: false`, `security_and_analysis: null` |
| Pintos VM | ? (403: "Upgrade to GitHub Pro or make this repository public to enable this feature.") | ? (`main`, `develop` 모두 같은 403) | ? | 없음 (Actions workflow 0개) | merge, squash, rebase 모두 허용, `delete_branch_on_merge: false`, `security_and_analysis: null` |

PR 리뷰 이력:

| 저장소 | PR | 사람 승인 | 그 밖 |
|---|---|---|---|
| pintos-userprog | 15개 (#104–#118, 13개 병합, 2개 닫힘) | 0건 (`reviewDecision`이 모두 빈 값) | 11개 PR에 Copilot 리뷰 요청. 모두 "quota limit"으로 리뷰 못 함. #115는 `JSY-remove` → `main`으로 바로 병합 |
| Pintos VM | 20개 (#1–#4, #153–#168, 모두 병합) | 15개 PR이 `APPROVED` (본문 "LGTM", "lgtv", "Good merge" 등). #1–#4, #165는 승인 없이 병합 | 8개 PR에 Copilot 리뷰 요청, 모두 quota로 실패. PR 번호가 #4 다음 #153으로 건너뜀 |

### pintos-userprog (week08)

| 규칙 | 지금 층 | 어디에 있나 | 강제되나 | 사람이 읽어야 하나 |
|---|---|---|---|---|
| 코드 모양: Linux 스타일, 스페이스 4칸, 함수만 다음 줄 중괄호, `case`는 `switch`와 같은 깊이, 80열 (A1–A6) | 2 정적 + 4 문서 | `.clang-format`; `make format`, `make lint` (`scripts/convention.py`); `.devcontainer/devcontainer.json`의 `editor.formatOnSave`; `CONVENTION.md` A | △ (`make lint`는 손으로 실행. CI 없음. 저장 시 포맷은 Dev Container의 VS Code에서만) | 아니오 |
| 한 줄 본문에도 중괄호 (A3) | 2 정적 | `.clang-tidy` `readability-braces-around-statements`; clangd 경고; `make lint` | △ | 아니오 |
| 이름 형식: 함수·변수·구조체 snake_case, 상수 매크로·enum 값 대문자 (B1, B2) | 2 정적 | `.clang-tidy` `readability-identifier-naming`; clangd; `make lint` | △ | 아니오 |
| Pintos 관용 이름 예외 (앞 `_`, 끝 `_`, upstream 매크로 이름) | 2 정적 | `.clang-tidy`의 `IgnoredRegexp` | △ | 아니오 |
| 이름 검사 범위: `threads/ devices/ userprog/ filesys/`. `lib/`, `vm/`은 이름 검사 밖. 모양 검사는 `tests/`, `utils/` 밖 | 1 코드베이스 | `scripts/convention.py` `LINT_DIRS`, `format_files()`; `CONVENTION.md` 명령 | ✓ (`make lint`를 실행하면 이 범위만 봄) | 아니오 |
| `make lint`는 위반이 있으면 0이 아닌 코드로 끝남 | 2 정적 | `Makefile`, `scripts/convention.py` | △ | 아니오 |
| 다른 파일에서 부르는 함수는 `모듈_동사[_목적어]`, `static`은 `동사_목적어` (C1) | 4 문서 + 5 사람 | `CONVENTION.md` C1 | ✗ ("도구가 못 잡는다. 리뷰에서 본다") | 사람 |
| 동사 표 (`init`, `create`/`destroy`, `open`/`close`, `get`/`set`, `add`/`remove`, `find`/`lookup`, `is_`/`has_`) (C2) | 4 문서 + 5 사람 | `CONVENTION.md` C2 | ✗ | 사람 |
| 변수는 명사, 범위가 넓을수록 길게, `_cnt`, `size`/`cnt` 구분, `bool`은 `is_`/`has_` (C3) | 4 문서 + 5 사람 | `CONVENTION.md` C3 | ✗ | 사람 |
| 같은 개념은 같은 이름 표 (`fd`, `struct file *file`, `status`, `buffer`/`length`, `tid`/`pid`, `uaddr`) (C4) | 4 문서 + 5 사람 | `CONVENTION.md` C4 | ✗ | 사람 |
| 구조체에 `typedef` 금지 (C5), 숫자 상수에 이름 (C6) | 4 문서 + 5 사람 | `CONVENTION.md` C5, C6 | ✗ | 사람 |
| C 규칙은 리뷰에서 보거나 AI에게 이 문서 기준으로 diff 검토를 맡김 | 4 문서 + 5 사람 | `CONVENTION.md` 명령 절 | ✗ | 사람, 에이전트 |
| 같은 도구 버전 (clangd, clang-format 21.1.8, clang-tidy 21.1.6) | 2 정적 + 4 문서 | `.devcontainer/Dockerfile` (`ec608a9`가 고정 버전 설치); `CONVENTION.md` 설정 | Dev Container ✓ / 그 밖 ✗ (`pip install`을 직접 해야 함) | 사람 |
| `.c`, `.h`는 스페이스 4칸, 80열, 끝 공백 제거, 끝 줄바꿈 | 2 정적 | `.editorconfig` | △ (EditorConfig를 읽는 에디터에서만) | 아니오 |
| 전체 포맷 커밋을 blame에서 건너뜀 | 4 문서 | `.git-blame-ignore-revs` (`a039ceb`); `CONVENTION.md` 전체 포맷 커밋 | △ (각자 `git config`. GitHub blame 화면은 자동) | 사람 |
| PR 본문 형식: 작업 내용, 변경 사항, 테스트 결과 (통과/전체, 신규 통과, 실패), 리뷰 요청, 체크리스트 (최신 master 반영, 빌드 경고 없음, 기존 통과 테스트 유지, 디버깅 출력 정리) | 4 문서 | `.github/pull_request_template.md` | ✗ | 사람 |
| 테스트는 `pintos/userprog`에서 `make check` (userprog, filesys/base, no-vm, threads 회귀) | 3 검증 | PR 템플릿 주석; Pintos `tests/` | △ (CI 없음) | 사람 |
| 모든 테스트를 icount로 병렬 실행하고 팀 계획 페이지의 체크를 맞춤 | 3 검증 + 5 사람 | `make ptest`, `make pcheck`; `scripts/plan-check.py` (study site의 `team-plan.json`을 읽고 Firebase에 씀) | △ | 사람 |
| Project 1 기준선에서 바꾼 것은 실행 비트와 `PINTOS_QEMU_EXTRA` 둘뿐. 최종 확인은 icount 없이 | 4 문서 | `README.md` 기준선 절 | ✗ | 사람 |
| `main` 직접 push, force push, 삭제 금지 | 규칙 없음 | 문서 규칙 없음; ruleset `[]`, protection 404 | ✗ | 해당 없음 |
| PR 승인 | 규칙 없음 | 문서 규칙 없음. 사람 승인 0건, Copilot 리뷰는 quota로 실패 | ✗ | 해당 없음 |
| 커밋 메시지 형식 | 규칙 없음 | 문서 규칙 없음. 이력에 영어 문장(benjohnbill)과 `feat:`, `fix(userprog):` 형식(Hannuri Song, JSZeroDev)이 섞여 있음 | ✗ | 해당 없음 |

### Pintos VM (week09)

| 규칙 | 지금 층 | 어디에 있나 | 강제되나 | 사람이 읽어야 하나 |
|---|---|---|---|---|
| 코드 모양 A1–A6, 중괄호, 이름 형식 B1–B2 | 2 정적 + 4 문서 | `.clang-format`, `.clang-tidy` (week08과 같은 파일); `make lint`, `make format`; Dev Container 저장 시 포맷; `CONVENTION.md` | △ (CI 없음) | 아니오 |
| 이름 검사 범위에 `vm/`을 더함 | 1 코드베이스 | `scripts/convention.py` `LINT_DIRS` | ✓ (실행하면) | 아니오 |
| 이름 짓는 규칙 C1–C6 | 4 문서 + 5 사람 | `CONVENTION.md` C (week08과 같은 글) | ✗ | 사람 |
| Pintos가 준 인터페이스 이름은 유지하고, 새 이름만 컨벤션을 따름 | 4 문서 | `README.md` "Explain the reason in code" | ✗ | 사람 |
| 같은 도구 버전, Dev Container | 2 정적 + 4 문서 | `.devcontainer/` (week08과 같은 파일); `CONVENTION.md` 설정 | Dev Container ✓ / 그 밖 ✗ | 사람 |
| `.editorconfig`, 모든 텍스트 파일 LF | 2 정적 | `.editorconfig`; `.gitattributes` (`* text=auto eol=lf`) | `.gitattributes` ✓ / `.editorconfig` △ | 아니오 |
| 전체 포맷 커밋 blame 숨김 | 4 문서 | `.git-blame-ignore-revs` (`284caf0`) | △ | 사람 |
| 브랜치: `main`, `develop`, `CJG`, `YYJ`, `SHW`. 개인 브랜치 → `develop` → `main` 순서로 PR | 4 문서 | `README.md` "Five branches. One workflow."; PR 템플릿 컨벤션 절 | ? (설정 403) | 사람 |
| 개인 브랜치는 `develop`에서 만들고 병합 뒤에도 지우지 않음 | 4 문서 | `README.md`; 저장소 설정 `delete_branch_on_merge: false` | ✗ (설정은 자동 삭제를 하지 않을 뿐) | 사람 |
| 작업 전과 PR 병합 전에 최신 `develop`을 개인 브랜치에 merge, 충돌은 개인 브랜치에서 해결 | 4 문서 | `README.md`; PR 템플릿 체크리스트 | ✗ | 사람 |
| merge commit으로 병합 | 4 문서 | `README.md`; PR 템플릿 | ✗ (저장소는 squash, rebase도 허용) | 사람 |
| `main`, `develop`에 직접 push, force push, 삭제 금지 | 4 문서 | `README.md` ("보호 대상: main·develop의 강제 push와 삭제 차단", "실제 GitHub 설정은 별도로 확인") | ? (설정 API 403) | 사람 |
| 필수 승인 0명. 작성자가 자기 PR을 병합할 수 있음. 그래도 담당에게 리뷰 요청 | 4 문서 + 5 사람 | `README.md` "Review together"; PR 템플릿 | ✗ (승인 15/20건은 사람이 고른 것) | 사람 |
| 커밋 첫 줄은 변경 목적과 결과의 한국어 요약, 본문은 `파일 / Create·Update·Delete·Fix: 함수 / 설명`, 한 커밋 한 목적 | 4 문서 | `README.md` "Commit with context"; PR 템플릿 | ✗ | 사람 |
| PR 제목은 변경 목적을 요약한 한국어 문장 | 4 문서 | `README.md`; PR 템플릿 첫 줄 주석 | ✗ | 사람 |
| 요청하지 않은 AI 공동 작성자 표시나 홍보 서명을 커밋과 PR에 넣지 않음 | 4 문서 | `README.md`; PR 템플릿 | ✗ | 사람, 에이전트 |
| 코드 주석에 `[CJG]`, `[YYJ]`, `[SHW]`와 동작 이유, 후속 작업은 `TODO [브랜치] #이슈` | 4 문서 | `README.md`; PR 템플릿 | ✗ | 사람 |
| 관련 없는 파일 전체 포맷 변경을 섞지 않음, 디버깅 출력 제거 | 4 문서 | `README.md`; PR 템플릿 체크리스트 | ✗ | 사람 |
| 공통 함수와 구조체를 바꾸기 전에 이슈나 PR에서 범위를 공유하고, 선행 PR과 병합 순서를 기록 | 4 문서 + 5 사람 | `README.md` "Shared code"; PR 템플릿 "공통 코드 영향" | ✗ | 사람 |
| PR 본문: 변경 요약, 담당 범위, 검증 표 (`make lint`, VM 빌드, VM 테스트, 회귀, COW; PASS/FAIL/미실행), 공통 코드 영향, 체크리스트 12줄 | 4 문서 | `.github/pull_request_template.md` (93줄) | ✗ | 사람 |
| 테스트 프로그램과 기대값, 수정 금지로 지정된 제공 코드는 바꾸지 않음 | 4 문서 | `README.md` "Quality"; PR 템플릿 체크리스트 | ✗ | 사람 |
| VM 테스트는 `pintos/vm`에서 `make check`. 미구현 실패와 회귀를 나눠 기록 | 3 검증 + 4 문서 | `README.md`; Pintos `tests/` | △ (CI 없음) | 사람 |
| 병렬 테스트 `make fast` (icount), `make fcheck` (icount 없음). 최종 확인은 plain `make check` | 3 검증 | `origin/develop`의 `Makefile` (`4045cbc`, `5338c5c`, PR #154). `origin/main`에는 없음 | △ | 아니오 |
| 구현은 직접 하고, AI는 개념 설명, 힌트, 코드 읽기, 리뷰, 디버깅에 씀. AI를 써도 책임은 작성자 | 4 문서 + 5 사람 | `README.md` "Learning is a deliverable" | ✗ | 사람 |
| `make pcheck`, `make ptest` (week08)는 없앰 | 1 코드베이스 | `Makefile` 주석 ("they wrote to the week08 team plan page") | ✓ (target 없음) | 아니오 |

### 층별 개수

한 행이 두 층이면 두 층에 모두 셌습니다.

- pintos-userprog: 행 22개. 1 코드베이스 1 · 2 정적 7 · 3 검증 2 · 4 문서 10 · 5 사람 6. "규칙 없음" 행 3개. 강제 칸이 ✗로 시작하는 행 10개 (규칙 없음 3개 포함).
- Pintos VM: 행 25개. 1 코드베이스 2 · 2 정적 3 · 3 검증 2 · 4 문서 21 · 5 사람 4. 강제 칸이 ✗로 시작하는 행 15개, ?로 시작하는 행 2개.

## B. 저장소 사이의 이어짐

표시: R1 pintos-userprog · R2 Pintos VM · R3 mini-react · R4 mini-redis · R5 mini-dbms. 날짜는 author date, SHA는 그 저장소에서 처음 더한 커밋.
"같은 파일?"은 내용 비교 결과입니다 (md5, `diff`, 같은 줄 수).

### B1. 두 저장소 이상에 있는 파일과 설정

| 항목 | 처음 | 이후 저장소 (처음 커밋) | 같은 파일? | 층 변화 |
|---|---|---|---|---|
| `.clang-format` | R1 2026-10-15 `6c6c899` | R2 10-23 `cb48ce8`; R4 11-13 `cd6e4e7` ("Pintos 팀 레포의 clang-format과 clang-tidy 설정을 가져와"); R5 11-16 `e8c57ac` | R1=R2 md5 같음. R2→R4 첫 주석 1줄만 다름 (3줄 diff). R4=R5 md5 같음 | R1, R2: 2 △ (`make lint` 손으로, CI 없음) → R4, R5: 2 ✓ (`make verify`와 CI가 `make lint` 실행, R4 `79e49f3` 11-13부터) |
| `.clang-tidy` | R1 10-15 `6c6c899` | R2 `cb48ce8`; R4 `cd6e4e7`; R5 `e8c57ac` | R1=R2 md5 같음. R4는 `readability-identifier-length` (3글자 미만 금지, `fd`·`n` 예외)를 더하고 Pintos 관용 이름 예외를 뺌 (32줄 diff). R4=R5 md5 같음 | △ → ✓ (위와 같음). 이름 길이는 R4에서 4 문서 → 2 정적으로 일부 옮김 |
| `scripts/convention.py` + `make lint`, `make format` | R1 10-15 `cb4a8fb` | R2 `cb48ce8`; R4 `cd6e4e7`; R5 `e8c57ac` | R1→R2 6줄 diff (`vm` 추가). R2→R4 138줄 diff (대상 경로, `.clang-format-ignore`, Markdown 물결표 검사 `fa25cba` 11-15, PostgreSQL 헤더 처리). R4→R5 29줄 diff (`demo/`, PostgreSQL 처리 뺌) | △ → ✓ |
| `.git-blame-ignore-revs` | R1 10-15 `2ecb5a2` | R2 `98d399a`; R4 `39317e7` | 같은 형식, 저장소마다 자기 포맷 커밋 SHA. R2는 주석을 한국어로 바꿈 | 4 △ 그대로. R3에는 없음 (포맷 커밋 없음). R5에서 끊김 |
| `.editorconfig` | R1 10-15 `6c6c899` | R2 `cb48ce8` | 같은 파일 (`diff` 비어 있음) | 2 △. R3에서 끊김 |
| `.devcontainer/` (고정 clang 버전 포함) | R1 10-15 `7f88707` (기준선 import), 고정 버전은 `ec608a9` | R2 10-26 `05af662` (Snoopykid) | `devcontainer.json`, `Dockerfile` 모두 같음 | 2 (Dev Container ✓). R3에서 끊김. R4, R5는 도구 버전을 `CONVENTION.md` 문서와 CI의 `pip install`로만 고정 (로컬 ✗, CI ✓) |
| `.gitattributes` (`* text=auto eol=lf`) | R2 10-26 `05af662` (Snoopykid) | R3 11-09 `b099606` (안다빈); R5 11-16 `e8c57ac` (안다빈) | R2=R5 md5 같음. R3는 첫 줄은 같고 md5가 다름 | 2 ✓ 그대로. R4에는 없음 (R4에서 끊겼다가 R5에서 다시 생김) |
| `.github/pull_request_template.md` | R1 10-15 `7f88707` (다른 팀 기준선에서 import, `4a50cae`가 테스트 줄 수정) | R2 10-26 `05af662` (Snoopykid; 내용은 David `ca61d80` 10-24 문서 갱신과 함께); R3 11-06 `da5dbdd` | 세 저장소 모두 다른 글. 이어진 것: "테스트 결과" 칸 (R1 통과/전체 → R2 PASS/FAIL/미실행 표 → R3 `AGENTS.md`의 `⏭️ 미실행` 표), "최신 대상 브랜치 반영" 체크 | 4 ✗ 그대로. R4에서 끊김 (R4, R5는 템플릿 없음) |
| `CONVENTION.md` | R1 10-15 `6c6c899` (코드 규칙만) | R2 10-23 `cb48ce8`; R3 11-06 `34d7752`; R4 11-13 `d13bf46`; R5 11-16 `e0a2ab3` | R1→R2 2줄 diff (복사). R3은 새로 씀 (팀 절차 규칙 1–9 + TS 규칙). R4 첫 판의 번호 규칙 2, 3, 4, 5, 6은 R3과 글자가 같고, 코드 절은 Pintos 규칙을 해요체로 다시 씀 (R3과 같은 줄 14/55). R5 첫 판은 R4와 같은 줄 36/62, 번호 규칙 2–6, 8이 R4와 같음 | 아래 B2 |
| `CLAUDE.md` | R1 로컬만 (`.git/info/exclude`, 파일 시각 2026-10-22) | R2 로컬만; R3 11-06 `4ea5446` (git에 넣음); R4 11-13 `d13bf46`; R5 11-16 `e0a2ab3` | R3=R4=R5 한 줄 `@AGENTS.md`로 같음. Pintos의 로컬 `CLAUDE.md`는 개인 tutor 지시라 내용이 다름 | 개인 파일 (git 밖) → 팀 파일 (4 문서) |
| `GLOSSARY.md` | R2 로컬만 (`.git/info/exclude`, 파일 시각 2026-10-26) | R3 11-07 `4a67a5a`; R4 11-13 `d13bf46`; R5 11-16 `e0a2ab3` | 내용은 저장소마다 다름 (R3→R4 첫 판 줄 유사도 0.12, R4→R5 0.16). 형식 "용어 \| 뜻 \| 코드" 표는 R3에서 정함 | 개인 → 4 문서 ✗ 그대로 |
| `AGENTS.md` | R3 11-06 `4ea5446` | R4 11-13 `73e257d`; R5 11-16 `e0a2ab3` | R3→R4 새로 씀 (같은 줄 1/8; PR 본문 표 대신 skill 설정). R4→R5 같은 줄 9/11 (issue tracker와 triage 줄만 PRD로 바꿈) | 4 ✗ 그대로 |
| `docs/agents/` (`issue-tracker.md`, `triage-labels.md`, `domain.md`) | R4 11-13 `73e257d` | R5 `e0a2ab3` | 복사 후 수정 (줄 유사도 0.56, 0.78, 0.89) | 4 ✗ 그대로. R3은 이 설정을 저장소 밖 개인 `CLAUDE.md`에 둠 |
| `docs/adr/` | R3 11-06 `9f91987` | R4 11-13 `934e072`; R5 `e0a2ab3` (`.gitkeep`만) | 형식이 바뀜: R3 번호 붙은 ADR → 11-11 폴더별, 결정 한 문장 + CAUTION + 인용 두 줄. R4 평평한 폴더, 번호 없음, 두 칸 표. R5는 R4 형식 | R3 2 ✓ (인용 줄 형식 검사) → R4, R5 2 ✓ (문단 라벨만 검사) |
| 결정을 바꾸면 새 ADR + `superseded by` | R3 `CONVENTION.md` | R4 `CONVENTION.md`, `docs/agents/domain.md`; R5 같음 | 같은 문장 (`결정을 바꿀 때는 새 ADR을 쓰고, 옛 ADR의 status를 superseded by <새 ADR 파일 이름>으로 바꿉니다.`) | 4 ✗ 그대로 |
| 결정과 테스트를 ID로 잇는 검사 | R3 11-09 `882b9d9` `scripts/check-decision-links.mjs` | R4 11-13 `f3fe0d3` `scripts/check-ids.py`; R5 11-16 `e8c57ac` | R3→R4 다른 언어로 새로 씀 (목적 같음: ID 중복, 인용된 ID와 ADR 파일이 있는지). R4=R5 md5 같음 | 2 ✓ (CI) 그대로 |
| 요구사항 표 (`근거` 칸) | R3 11-11 `85776ca` `docs/requirements/` | R4 `d13bf46` `docs/requirements.md`; R5 `e0a2ab3` | 같은 생각, 파일은 새로 씀 | 2 ✓ (근거 칸 ADR 이름 검사) 그대로 |
| CI workflow (`ci.yml`) | R3 11-06 `23f5040` (npm) | R4 11-13 `f8026fd` (`make verify`); R5 11-16 `e8c57ac` | R3→R4 새로 씀. R5 첫 판은 R4에서 `libsqlite3-dev` 설치 줄 하나만 뺀 것. 지금 R5는 macOS matrix와 `make tsan`을 더함 | R1, R2에는 CI 없음 → R3 2 ✓ + required check ✓ → R4, R5 2 ✓ (required check 없음, 실패해도 병합은 막지 않음) |
| `make verify` 한 명령 | R4 11-13 `f3fe0d3` | R5 `e8c57ac` | Makefile은 245줄 diff (프로젝트가 다름). 구성 (C11 `-Werror`, ASan, UBSan, ID 검사, `make lint`)은 같음 | 2 + 3 ✓ (CI) 그대로 |
| `tests/acutest.h` | R4 11-13 `f3fe0d3` | R5 `e8c57ac` | vendored 파일 | 1 그대로 |
| `.clang-format-ignore` | R4 11-13 `cd6e4e7` | R5 `e8c57ac` | 11줄 diff (가져온 파일 목록이 다름) | 2 ✓ (lint 제외) 그대로 |
| `compile_flags.txt` | R4 | R5 | 비교 안 함 | 2 (에디터 clangd) |
| Markdown 물결표는 `\~` | R4 11-15 `fa25cba` | R5 `e8c57ac` | `convention.py`의 같은 함수 | 2 ✓ 그대로 |
| 측정 기록 규칙 (파일 이름, 한 파일 한 측정, frontmatter, 고치지 않음) | R4 `CONVENTION.md` 측정 기록 | R5 `CONVENTION.md` 측정 기록 | 같은 절을 줄여 옮김 (R5는 `records` 칸 더함) | 4 ✗ 그대로. R4에만 있는 "기록용 측정 3회 이상" (`071e9a0`, 2 △)은 R5에 없음 |
| 오너가 PR에 밝히면 승인 없이 병합 | R4 11-13 `487b14f` (PR #3) | R5 `e0a2ab3` | 같은 문장 | 4 + 5 ✗ 그대로 |
| GitHub ruleset | R3 11-06 14:55 `main-protection` 생성 | R4 11-18 03:09 `Ruleset` 생성 | 다른 설정 (`layer-table.md` 요약 표). R1 없음, R2 ? (403), R5 없음 | R3 2 ✓ (PR, 승인 1, stale 승인 무효, merge만, required check) → R4 2 ✓ (PR, 삭제와 force push 금지만, 승인 0, 관리자 `always` 우회) → R5 규칙 없음 |
| Copilot PR 리뷰 요청 | R1 10-15 (#104) | R2, R3, R4, R5 모든 저장소 | 설정 위치는 확인 못 함 | 5 사람 (자동 리뷰어)인데 거의 모든 요청이 quota로 실패. 실제 리뷰가 나온 것은 R4 #47 하나 |

### B2. 두 저장소 이상에 있는 규칙 (글로 된 것)

| 규칙 | 처음 | 이후 저장소 | 같은 글? | 층 변화 |
|---|---|---|---|---|
| 다른 파일에서 부르는 함수는 `모듈_동사` | R1 `CONVENTION.md` C1 (10-15) | R2 C1; R4 이름 2; R5 이름 2 | R1=R2 같음. R4는 해요체로 다시 쓰고 예시를 `store_set`으로 바꿈 | 4 + 5 ✗ 그대로. R3에는 없음 (TS, `create<결과>From<입력>`) |
| 동사의 뜻을 하나로 고정하는 동사 표 | R1 C2 | R2 C2; R3 이름 (TS 동사 11개); R4 이름 3; R5 이름 3 | 표 형식은 이어지고, 동사 목록은 저장소마다 다름 (R3 `find`=undefined, `get`=Error 던짐; R4 `delete` 추가) | 4 + 5 ✗ 그대로 |
| 변수는 명사, 범위가 넓을수록 길게 | R1 C3 | R2 C3; R3 이름 ("변수는 명사로 짓고, 쓰이는 범위가 넓을수록 길게 짓습니다"); R4 이름 1은 "담는 것의 역할을 단어로" | R3은 같은 뜻의 다른 글 | R1–R3 4 ✗ → R4, R5 이름 길이 3글자 미만은 2 ✓ (`clang-tidy`), 3글자 이상 줄임말은 4 ✗ |
| 같은 개념은 같은 이름 표 | R1 C4 | R2 C4; R3 이름 (표 대신 `GLOSSARY.md`를 따름); R4 이름 4 (표 14줄); R5 이름 4 | R4 표 형식(개념, 이름, 쓰지 않는 이름)은 R1과 같음. `fd` 행은 R1→R4→R5 이어짐 | 4 ✗ 그대로. R4에서 `fd`는 `clang-tidy` 예외 목록(2)에도 들어감 |
| 구조체 `typedef` 금지 | R1 C5 | R2 C5; R4 이름 5; R5 이름 5 | 같은 이유 문장 ("`struct`가 보여야 값인지 구조체인지 바로 안다") | 4 ✗ 그대로 |
| 숫자 상수에 이름 | R1 C6 | R2 C6; R3 이름; R4 이름 5; R5 이름 5 | 다른 글, 같은 뜻 | 4 ✗ 그대로 |
| 개인 브랜치를 병합 뒤에도 유지 | R2 `README.md` (David `ca61d80` 10-24) | R3 `CONVENTION.md` 1; R4 1; R5 1 | R3 이후 같은 문장. R2와는 다른 글 | 4 ✗ 그대로 (모든 저장소 `delete_branch_on_merge: false`) |
| PR 전에 통합 브랜치의 최신 내용을 개인 브랜치에 merge | R1 PR 템플릿 체크 "최신 master 반영" | R2 `README.md`, PR 템플릿 (`develop`); R3 `CONVENTION.md` 2 (`git merge origin/main`); R4 2; R5 2 | R3=R4=R5 같은 글 | 4 ✗ 그대로 (R3 required check `strict: false`) |
| merge commit으로 병합 | R2 `README.md` | R3 3; R4 3; R5 3 | R3=R4=R5 같은 글 | R2 4 ✗ → R3 2 ✓ (ruleset `allowed_merge_methods: [merge]`) → R4, R5 4 ✗ |
| `main` 직접 push와 force push 금지, PR로만 | R2 `README.md` ("`main`, `develop`에 직접 Push하거나 강제 Push하지 않습니다") | R3 `CONVENTION.md` 1 ("`main`은 PR로만"); R4 1; R5 1 | R3 이후 같은 글 | R2 4 (설정 ?) → R3 2 ✓ → R4 4 ✗ (11-18 03:09부터 2 ✓) → R5 4 ✗ |
| 필수 승인 수 | R2 `README.md` "0명" | R3 3 "승인 1건"; R4 3 (승인 1건 + 오너 예외); R5 3 (R4와 같음) | 숫자가 0 → 1로 바뀜 | R2 4 → R3 2 ✓ (관리자 PR 병합 우회 있음) → R4 4 ✗ (ruleset 승인 0) → R5 4 ✗ |
| 승인 뒤 diff가 바뀌면 다시 승인 | R3 3 | R4 3; R5 3 | 같은 글 | R3 2 ✓ (`dismiss_stale_reviews_on_push`) → R4, R5 4 ✗ |
| 커밋 첫 줄은 변경 목적과 결과의 한국어 문장 | R2 `README.md` "Commit with context" | R3 5; R4 5; R5 5 | R3 이후 같은 글 (예시 문장만 다름). R2의 본문 형식 (`파일 / Create·Update…`)은 R3에서 끊김. R3부터 "매일 커밋" 더함 | 4 ✗ 그대로 |
| PR 제목은 목적을 요약한 한국어 문장 | R2 `README.md`, PR 템플릿 주석 | R3 PR 템플릿 첫 줄 주석 | 다른 글 | 4 ✗. R4에서 끊김 (템플릿 없음) |
| 생성 파일, 비밀 정보를 PR에서 뺌 | R2 PR 템플릿 체크 "불필요한 디버깅 출력·생성 파일·인증 정보를 제외" | R3 6; R4 6; R5 6 | R3 이후 같은 글 | 4 + 5 ✗ 그대로 (secret scanning은 R3–R5 `disabled`, R1, R2 `null`) |
| AI를 써도 작성자가 설명하고 책임짐 | R2 `README.md` ("AI를 활용한 경우에도 변경 내용과 검증에 대한 책임은 작성자가 집니다") | R3 6 ("AI가 작성했든 팀원이 작성했든 원리를 말로 설명할 수 있어야"); R4 6; R5 6 | R3 이후 같은 글 | 5 ✗ 그대로 |
| `main` CI가 실패하면 본 사람이 먼저 되돌리거나 고침 | R3 4 | R4 4; R5 4 | 같은 글 | 5 ✗ 그대로 |
| 규칙 파일도 PR과 승인 1건으로 바꾸고, GitHub 설정은 승인 뒤 오너가 반영 | R3 8 | R4 8; R5 8 | R3은 "이 파일과 ADR", R4와 R5는 "이 파일" | R3 2 ✓ (ruleset) → R4, R5 4 + 5 ✗ |
| 테스트는 공개 함수를 부르고 기대값을 직접 적음 | R3 테스트 | R4 테스트; R5 테스트 | 같은 뜻 | 4 + 5 ✗ 그대로 |
| 테스트 ID는 저장소 전체에서 하나 | R3 (`T1` 형식, `check-decision-links.mjs`) | R4 (`[T1]`, `check-ids.py`); R5 | 형식이 바뀜 | 2 ✓ 그대로 |
| 에이전트는 변경 전에 `CONVENTION.md`, `GLOSSARY.md`를 읽음 | R3 `AGENTS.md` (`fc887e0`, `5353e67`) | R4 `AGENTS.md`; R5 `AGENTS.md` | 같은 뜻, 다른 문장 | 4 ✗ 그대로 |
| PR 본문에 실행하지 않은 검사는 미실행으로 표시 | R2 PR 템플릿 ("PASS / FAIL / 미실행") | R3 `AGENTS.md` ("Mark the rest `⏭️ 미실행`") | 다른 글 | 4 ✗. R4에서 끊김 |
| Pintos 테스트 기대값과 제공 코드를 바꾸지 않음 | R2 `README.md`, PR 템플릿 | (이어지지 않음) | | R2에서 끊김 |

### B3. 다음 저장소로 이어지지 않은 것

| 항목 | 있던 저장소 | 끊긴 저장소 | 비고 |
|---|---|---|---|
| `make pcheck`, `make ptest`, `scripts/plan-check.py` (팀 계획 페이지 Firebase 동기화) | R1 | R2 | R2 `Makefile` 주석이 이유를 적음 |
| `PINTOS_QEMU_EXTRA`와 icount 병렬 실행 | R1 (`make ptest`), R2 `develop` (`make fast`, `make fcheck`) | R2 `main`, R3 | R2에서는 `main`에 오지 않음 |
| `.editorconfig` | R1, R2 | R3 | R3–R5 없음 |
| `.devcontainer/` | R1, R2 | R3 | Pintos 환경 파일 |
| 커밋 본문 형식 `파일 / Create·Update·Delete·Fix: 함수 / 설명` | R2 | R3 | R3은 첫 줄 규칙만 |
| 코드 주석의 브랜치 표기 `[CJG]` 등, `TODO [브랜치] #이슈` | R2 | R3 | |
| 통합 브랜치 `develop` | R1, R2 | R3 | R3–R5는 개인 브랜치 → `main` |
| "AI 공동 작성자 표시를 넣지 않음" (팀 문서) | R2 | R3 | R3–R5 팀 문서에는 없음. 개인 `week11-12/CLAUDE.md`와 메모리에만 있음 |
| "구현은 직접 하고 AI는 설명과 리뷰에" | R2 | R3 | R3–R5는 강의 규칙상 AI 생성 허용 |
| PR 템플릿 | R1, R2, R3 | R4 | R4, R5 없음 |
| 새 세션 리뷰 (작성하지 않은 세션이 diff 검토) | R3 (`CONVENTION.md` 에이전트, PR 템플릿) | R4 | R4, R5의 `CONVENTION.md`, `AGENTS.md`에 없음 |
| PR 본문 테스트 수 표, mermaid, 함수 이름 트리 | R3 `AGENTS.md` | R4 | |
| `retarget-stacked-prs.yml` (쌓은 PR base 자동 이동) | R3 (`5107a22` 11-09) | R4 | |
| `deploy-pages.yml` | R3 (`90ca9fa` 11-09) | R4 | |
| required status check | R3 (`code`) | R4 | R4, R5 CI는 필수 아님 |
| ruleset 승인 1건, stale 승인 무효, merge만 | R3 | R4 | R4 ruleset은 승인 0, 셋 다 허용 |
| `.gitattributes` | R2, R3 | R4 | R5에서 다시 생김 |
| `.git-blame-ignore-revs` | R1, R2, R4 | R5 | R5에는 전체 포맷 커밋이 없음 (처음부터 같은 도구로 씀) |
| 마일스톤 6단계, 보드 카드 규칙 (`CONVENTION.md` 7의 카드, Status, `레포` 필드) | R4 | R5 | R5는 마일스톤 없이 "작업 흐름" 4단계와 PRD |
| `overview.md`에 Redis 방식을 적지 않음, `spec.md`의 `## Redis와 대조` 절 | R4 | R5 | R5는 해당 규칙 없음 |
| 기록용 측정 3회 이상 (`cache_bench.py` `RECORD_RUNS_MIN`) | R4 | R5 | |
| ruleset (어떤 것이든) | R3, R4 | R5 | R5 `[]` |

## C. 에이전트와 규칙 파일이 처음 들어온 때

"첫 커밋 뒤"는 그 저장소 `origin/main`의 root commit author date 기준입니다. R3–R5의 root는 GitHub가 저장소를 만들 때 생긴 `Initial commit` (2026-11-05 18:51–18:52)이라, 첫 작업 커밋 기준도 함께 적었습니다.

| 저장소 | root commit | 첫 작업 커밋 | 파일 | 처음 커밋 | 작성자 (git log 이름) | root 뒤 | 첫 작업 커밋 뒤 |
|---|---|---|---|---|---|---|---|
| pintos-userprog | `7f88707` 2026-10-15 19:27 (기준선 import) | 같음 | `CONVENTION.md` | `6c6c899` 10-15 20:47 | benjohnbill | 0일 (1시간 20분) | 0일 |
| | | | `.github/` (PR 템플릿) | `7f88707` 10-15 19:27 | benjohnbill | 0일 (import에 포함) | 0일 |
| | | | `AGENTS.md`, `GLOSSARY.md`, `docs/adr/` | 없음 | | | |
| | | | `CLAUDE.md` | git에 없음 (로컬, exclude) | | | |
| Pintos VM | `05af662` 2026-10-26 13:59 (Snoopykid, "Project 3 baseline without inherited project history") | `cb48ce8` 2026-10-23 22:04 (author date가 root보다 이름. committer date는 모두 10-26 13:59, Snoopykid) | `CONVENTION.md` | `cb48ce8` 10-23 22:04 | benjohnbill | root보다 2.7일 앞 (author date) | 0일 |
| | | | `.github/` (PR 템플릿) | `05af662` 10-26 13:59 | Snoopykid | 0일 | 2.7일 |
| | | | `AGENTS.md`, `docs/adr/` | 없음 | | | |
| | | | `CLAUDE.md`, `GLOSSARY.md` | git에 없음 (로컬, exclude) | | | |
| mini-react | `d1c451e` 2026-11-05 18:51 | `da5dbdd` 11-06 14:27 | `.github/` | `da5dbdd` 11-06 14:27 | benjohnbill | 0.8일 | 0일 |
| | | | `AGENTS.md`, `CLAUDE.md` | `4ea5446` 11-06 14:32 | benjohnbill | 0.8일 | 0일 (5분) |
| | | | `CONVENTION.md` | `34d7752` 11-06 19:22 | benjohnbill | 1.0일 | 0.2일 |
| | | | `docs/adr/` | `9f91987` 11-06 19:22 | benjohnbill | 1.0일 | 0.2일 |
| | | | `GLOSSARY.md` | `4a67a5a` 11-07 13:35 | benjohnbill | 1.8일 | 1.0일 |
| mini-redis | `444ee75` 2026-11-05 18:51 | `73e257d` 11-13 00:28 | `AGENTS.md` | `73e257d` 11-13 00:28 | benjohnbill | 7.2일 | 0일 |
| | | | `CLAUDE.md`, `CONVENTION.md`, `GLOSSARY.md` | `d13bf46` 11-13 00:31 | benjohnbill | 7.2일 | 0일 (3분) |
| | | | `.github/` (CI) | `f8026fd` 11-13 00:48 | benjohnbill | 7.2일 | 0일 (20분) |
| | | | `docs/adr/` | `934e072` 11-13 16:09 | benjohnbill | 7.9일 | 0.7일 |
| mini-dbms | `fe69033` 2026-11-05 18:52 | `e0a2ab3` 11-16 13:56 | `AGENTS.md`, `CLAUDE.md`, `CONVENTION.md`, `GLOSSARY.md`, `docs/adr/` | `e0a2ab3` 11-16 13:56 | benjohnbill | 10.8일 | 0일 |
| | | | `.github/` (CI) | `e8c57ac` 11-16 15:54 | 안다빈 | 10.9일 | 0.1일 |

Pintos VM의 이력: `origin/main`의 모든 커밋은 committer가 Snoopykid, committer date가 2026-10-26 13:59:34–13:59:43입니다. author date는 10-23–10-26으로 그대로입니다. root `05af662`의 메시지는 한 줄 "Project 3 baseline without inherited project history"이고 본문이 없습니다.

## D. 절차와 규칙을 바로잡은 흔적

OS 로직과 제품 로직의 버그 수정은 뺐습니다. "뒤에 규칙이나 검사가 생겼나"의 판정은 그 저장소 `origin/main`에서 찾은 커밋과 설정만 근거로 합니다.

| # | 저장소 | 날짜 | SHA 또는 PR | 한 줄 인용 | 뒤에 규칙이나 검사가 생겼나 |
|---|---|---|---|---|---|
| 1 | mini-redis | 2026-11-18 | `741d157` (안다빈 03:10), `d64ae63` (DavinAn6 03:17) | "PR 없이 main에 올라간 커밋 4개(826d036, ed68db2, ba4623a, 4a68f94)를 되돌립니다" | 예, 설정. ruleset `Ruleset`이 03:09:43에 생성됨 (되돌림 커밋 1분 전). PR 필수, 삭제와 force push 금지. 관리자 우회 `always`. 되돌린 4개는 11-17 18:37–19:30에 안다빈이 `main`에 직접 올림 |
| 2 | mini-react | 2026-11-06 | `da5dbdd`, `4ea5446`, `2d01d6e`, `c982451` | `main` 첫 부모 이력의 PR 없는 커밋 4개 (14:27–14:39, API상 연결된 PR 없음) | 예, 설정. ruleset `main-protection`이 14:55에 생성됨. 이후 `main` 첫 부모 이력에 PR 없는 커밋 없음. 커밋 메시지에 "실수"라는 말은 없음 |
| 3 | mini-redis | 2026-11-17 | PR #32 (닫힘), `b554dbb` | "제가 원리를 설명할 수 없는 변경이라 파기합니다. 측정 방식 통일은 새 PR로 올립니다." | 예. 같은 날 `776dc54` "커밋하지 않은 변경이 있는 측정은 기록하지 않는다는 규칙" (4 ✗), `0049cb2` 기록용 측정 3회 이상 규칙 (4), `071e9a0` `--output` 측정이 3회 미만이면 실패 (2 △) |
| 4 | mini-redis | 2026-11-15 | `5c5e1b0` | "리뷰에서 나온 측정 기록의 커밋 값과 결론 문장을 바로잡고" | 예, 2일 뒤 `776dc54` "측정 기록의 commit을 스크립트 출력에서 옮겨 적고" (4 ✗). `cache_bench.py`는 커밋하지 않은 변경을 출력만 함 |
| 5 | mini-redis | 2026-11-15 | `4a27f25` | "ID 검사가 문단 형식의 ADR을 만나면 실패해, 표로 옮기지 않은 결정 행의 인용이 검사 없이 지나가지 않게 합니다" | 예, 검사 (2 ✓). 직전 `1691330`이 ADR을 표로 바꾼 뒤 남은 빈틈 |
| 6 | mini-redis | 2026-11-15 | `fa25cba` | "GitHub가 범위의 물결표 사이를 취소선으로 그리지 않도록 Markdown의 ~를…" | 예, 검사 (2 ✓, `make lint`와 CI). mini-dbms로 이어짐 |
| 7 | mini-redis | 2026-11-13 | `67783b8`, `93528a4` | "서버의 변수 이름을 역할로 풀어 쓰고, POSIX 이름 fd는 이름 길이 검사에서 예외로 둡니다" | 검사가 먼저 생김 (`cd6e4e7` 같은 날, `readability-identifier-length`). 이 두 커밋은 그 검사를 통과하려고 이름을 고친 것 |
| 8 | mini-redis | 2026-11-13 | `487b14f` (PR #3) | "오너가 PR에 밝히면 승인 없이 병합할 수 있도록 병합 규칙에 예외를 추가합니다" | 규칙을 문서에 맞춤 (4). PR #1, #2는 이 규칙 전에 승인 없이 병합됨. 승인 수 설정은 0 그대로 |
| 9 | mini-redis | 2026-11-13 | `e4990b7` | "README 커밋에 함께 들어간 Makefile 변경을 되돌립니다" | 아니오 |
| 10 | mini-redis | 2026-11-15 | `f3d8fb4` | "리뷰에서 나온 규칙 위반을 고쳐 용어, 빈 줄, 테스트 ID 인용이 규칙과 맞게 합니다" | 아니오. 용어와 `return` 앞 빈 줄은 4 ✗ 그대로. 인용 검사는 이미 있었음 |
| 11 | mini-redis | 2026-11-18 | `96b60db`, `c1d4080`; PR #35, #44 댓글 | "#37과 #35가 먼저 병합되어 서버 측정 기록 번호를 011, 012로 옮겼습니다" | 아니오. 번호 충돌을 막는 검사 없음 |
| 12 | mini-react | 2026-11-09 | `08bbe4a` | "새 세션 리뷰를 반영해 ADR 0005의 인용을 바로잡고 검사가 형식 오류와 ID 없는 테스트도 알리도록 고칩니다" | 예, 검사 강화 (`check-decision-links.mjs`; 형식 오류는 ✓, ID 없는 테스트는 출력만) |
| 13 | mini-react | 2026-11-11 | `2f5b2ef` | "요구사항 표의 낡은 문장과 검사의 빈틈을 고치고, 같은 문장이 세 번 반복된 ADR 둘을 바로잡습니다" | 예, 검사 변경 (`check-decision-links.mjs` 25줄) |
| 14 | mini-react | 2026-11-11 | `dc14ea4` | "Biome이 실제로 잡는 범위에 맞춰 이름 규칙과 README와 요구사항 표를 고칩니다" | 문서를 도구에 맞춤. 새 검사는 없음 |
| 15 | mini-react | 2026-11-11 | `56fda9d` | "Biome useHookAtTopLevel로 Hook 호출 위치를 검사하도록 Root Component를 PascalCase로 바꾸고" | 예, 4 → 2 (부분 ✓) |
| 16 | mini-react | 2026-11-07 | PR #15 댓글 | "오너의 예외 허용으로, PR #3이 병합되기 전에 쌓인 초안 PR을 올렸습니다 … PR #3이 병합되면 base를 main으로 바꾸고" | 예, 2일 뒤 `5107a22` `retarget-stacked-prs.yml` (2 ✓) |
| 17 | mini-react | 2026-11-09 | PR #27, #28, #29 댓글 | "승인 없이 병합했습니다. owner가 ruleset main-protection에 admin bypass(PR 병합만)를 잠시 넣고, 병합 직후에 뺐습니다" | 설정. 지금 ruleset (수정 2026-11-11 04:24)에는 관리자 `pull_request` 우회가 있음. PR #54, #55, #56은 승인 없이 병합 |
| 18 | mini-react | 2026-11-12 | `b70673a`, `7180116` | "새 세션 리뷰를 반영해 자식 Component 결정의 F67, F68 인용을 되돌리고" | 아니오 |
| 19 | mini-react | 2026-11-06 | `a652342`, `0bba7fb` | "PR 템플릿을 손으로도 쓸 수 있는 형식으로 줄입니다" | 템플릿에서 71줄을 지우고 7줄을 더함 (4). CI를 코드 검사로 줄임 (2) |
| 20 | mini-dbms | 2026-11-16 | PR #2 댓글, `8702815` | "환경 PR #3(DA의 C 빌드 환경 + macOS CI + 용어 정합)에 맞춰 이 PR을 고쳤습니다. 병합 순서는 #3, 그다음 이 PR입니다." | 아니오 |
| 21 | mini-dbms | 2026-11-16 | `2d35f9c`, `7681e4f` | "README의 Phase 표 상태와 파일 트리를 티켓 01 이전으로 되돌려, Phase 1이 끝날 때 따로 고치게 합니다" | 아니오 |
| 22 | mini-dbms | 2026-11-17 | `27ee0da` | "함수의 마지막 return 위에 3줄 이상 이어진 줄이 있는 61곳에 빈 줄을 넣어" | 아니오. 함수 규칙 3은 4 ✗ 그대로 ("clang-format은 … 강제하지도 않으므로 리뷰에서 봅니다") |
| 23 | mini-dbms | 2026-11-17 | `b0b3078` | "모든 테스트 ID가 문서에서 인용됩니다" | 아니오. `check-ids.py`는 인용된 ID가 있는지만 보고, 인용 안 된 ID는 보지 않음 |
| 24 | pintos-userprog | 2026-10-20 | `899bb3c` | "struct file_descriptor -> struct fd_entry (C4: fd 개념에 file_descriptor 금지)" | 이 저장소에서는 아니오 (C 규칙은 리뷰만). mini-redis에서 개념 표의 `fd` 행과 `clang-tidy` `fd` 예외로 이어짐 |
| 25 | pintos-userprog | 2026-10-15 | `3016cb2` | "make reports a failed recipe as exit 2, so the documented code was wrong." | 문서를 고침. 새 검사 없음 |

넣지 않은 후보: Pintos VM 10-26 이력 재작성 (`05af662`, 이유가 메시지에 없음), pintos-userprog `4a50cae` (PR 템플릿 테스트 줄), mini-redis `3c87926`, `0307017` (측정 기록의 숫자와 문장 수정), mini-dbms `40828fb` (두 티켓의 오류 종류를 `error_reason` 하나로 합침), `6b7c2be` (용어집의 커서와 겹치는 이름 변경).

## E. 확인 못 한 것

- Pintos VM의 ruleset, branch protection, 규칙 조회가 모두 403입니다 (플랜 기능 메시지). `README.md`가 적은 "main·develop의 강제 push와 삭제 차단"이 실제 설정인지 확인하지 못했습니다.
- pintos-userprog는 private 사용자 저장소이고 ruleset `[]`입니다. 플랜 때문에 ruleset을 만들 수 없는 상태인지는 확인하지 않았습니다.
- Pintos 두 저장소의 `security_and_analysis`가 `null`이라 secret scanning 상태를 알 수 없습니다.
- Pintos VM PR 번호가 #4에서 #153으로 건너뛴 이유, pintos-userprog PR이 #104부터 시작하는 이유를 확인하지 않았습니다 (이전 저장소에서 옮겨 온 이슈 번호일 수 있으나 근거 없음).
- Pintos VM 10-26 이력 재작성의 이유와, 재작성 전 이력은 보지 않았습니다.
- Pintos 로컬 `CLAUDE.md`, `GLOSSARY.md`가 처음 생긴 날은 git에 없어서, 파일 시각(수정 시각)만 적었습니다. 생성 시각은 아닙니다.
- Copilot 리뷰 요청이 저장소 설정인지 계정 설정인지 확인하지 않았습니다.
- 모든 저장소에서 테스트, `make lint`, `make verify`를 로컬로 실행하지 않았습니다.
- R3 `.gitattributes`가 R2, R5와 md5가 다른 줄은 열어 보지 않았습니다.
- `compile_flags.txt`는 R4와 R5 사이에서 비교하지 않았습니다.
- 팀원이 커밋 규칙, PR 전 merge 규칙을 실제로 지켰는지는 이력 전체를 세지 않았습니다.
- 커밋 메시지와 PR 댓글만 찾았습니다. Slack, 회의록, GitHub Project 카드에 남은 바로잡기는 보지 않았습니다. PR 본문 안의 문장도 검색하지 않았습니다 (댓글과 리뷰 본문만 검색).
- git 작성자 이름 "안다빈"과 "DavinAn6"이 같은 사람인지는 이 문서에서 판정하지 않았습니다. 로그에 보이는 이름 그대로 적었습니다.
