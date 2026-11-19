# 규칙별 층 표 (mini-react, mini-redis, mini-dbms)

조사일 2026-11-18. 읽기만 했고, 저장소에는 아무것도 바꾸지 않았습니다.

층: 1 코드베이스 · 2 정적 (lint, typecheck, 컴파일러, 테스트, CI, ID 검사) · 3 검증 (실제 실행, sanitizer, 시연) · 4 문서 · 5 사람.
강제되나: ✓ 아무도 고르지 않아도 도구가 실패시키거나 막음 · △ 누가 실행할 때만 · ✗ 문서뿐 · ? 확인 못 함.
GitHub 설정은 그 설정이 막는 층에 넣고 "어디에 있나" 칸에 적었습니다.

## 읽은 상태

| 저장소 | 브랜치 | 작업 트리 | 기준 |
|---|---|---|---|
| mini-react | `CJG` | 깨끗함 | `CJG`의 내용이 `origin/main`(`a6df9f7`)과 같음 (`git diff --stat HEAD origin/main`이 비어 있음). 로컬 `main`은 `c466e2b`에 멈춰 있어 `git diff --stat main`은 71개 파일을 보여 주지만, 이는 로컬 `main`이 낡은 탓이라 `origin/main`과 비교했습니다 |
| mini-redis | detached HEAD `9e1812d` | 깨끗함 | `origin/main`과 같은 커밋. 로컬 `main`은 첫 커밋 `444ee75` |
| mini-dbms | `CJG` `921223e` | 깨끗함 | `origin/main`과 같은 커밋. 로컬 `main`은 첫 커밋 `fe69033` |

`origin/main`의 세 커밋은 `gh run list`가 보여 준 최신 `main` CI 커밋과 같습니다.

GitHub 설정 요약:

| 저장소 | ruleset | branch protection | 필수 check | 관리자 우회 |
|---|---|---|---|---|
| mini-react | `main-protection` (active): deletion, non_fast_forward, pull_request (승인 1, stale 승인 무효, merge만), required check `code` (`strict: false`) | 없음 (404) | `code` | 관리자 역할, `pull_request` 모드 (PR 병합 때만) |
| mini-redis | `Ruleset` (active, 2026-11-18 생성): deletion, non_fast_forward, pull_request (승인 0, merge, squash, rebase 허용) | 없음 (404) | 없음 | 관리자 역할, `always` |
| mini-dbms | 없음 (`[]`) | 없음 (404) | 없음 | 해당 없음 |

세 저장소 모두 secret scanning과 push protection이 `disabled`입니다. 로컬 git hook은 mini-react에만 있고(`post-commit`, `post-merge`), 둘 다 code-map을 다시 만드는 hook이라 커밋을 막지 않습니다.

## mini-react

| 규칙 | 지금 층 | 어디에 있나 | 강제되나 | 사람이 읽어야 하나 |
|---|---|---|---|---|
| `main`은 PR로만 바꿉니다 | 2 정적 + 4 문서 | `CONVENTION.md` 1; ruleset `main-protection`의 `pull_request` 규칙 | ✓ 직접 push는 관리자도 막힘 (bypass_mode `pull_request`) | 아니오 |
| `main` 삭제와 force push 금지 | 2 정적 | ruleset `main-protection`의 `deletion`, `non_fast_forward` | ✓ | 아니오 |
| 승인 1건을 받은 뒤 병합합니다 | 2 정적 + 4 문서 + 5 사람 | `CONVENTION.md` 3; ruleset `required_approving_review_count: 1`; bypass actor = 저장소 관리자 역할, `bypass_mode: pull_request` | ✓ 단, 관리자는 PR 병합 때 우회 가능. PR #54, #55, #56은 `reviewDecision: REVIEW_REQUIRED` 상태로 병합됨 | 사람 |
| 승인 뒤 diff가 바뀌면 다시 승인받습니다 | 2 정적 + 4 문서 | `CONVENTION.md` 3; ruleset `dismiss_stale_reviews_on_push: true` | ✓ (관리자 우회는 위와 같음) | 사람 |
| merge commit으로만 병합합니다 | 2 정적 + 4 문서 | `CONVENTION.md` 3; ruleset `allowed_merge_methods: [merge]` (저장소 설정은 merge, squash, rebase 모두 허용) | ✓ | 아니오 |
| CI `code`가 통과해야 병합합니다 (typecheck → check → test → build) | 2 정적 | `.github/workflows/ci.yml` job `code`; ruleset `required_status_checks: code`, `strict: false` | ✓ | 아니오 |
| PR 전에 `origin/main`을 개인 브랜치에 병합합니다 | 4 문서 | `CONVENTION.md` 2 (required check가 `strict: false`라 최신 반영을 요구하지 않음) | ✗ | 에이전트, 사람 |
| 개인 브랜치는 이니셜로 만들고 병합 뒤에도 남깁니다. 포크는 쓰지 않습니다 | 4 문서 | `CONVENTION.md` 1; `docs/adr/team/personal-branches-no-forks.md`; 저장소 설정 `delete_branch_on_merge: false` | ✗ (설정은 자동 삭제를 하지 않을 뿐, 이름 규칙이나 포크를 막지 않음) | 에이전트, 사람 |
| 쌓은 PR의 아래쪽이 병합되면 위쪽 PR의 base를 옮깁니다 | 2 정적 | `.github/workflows/retarget-stacked-prs.yml` | ✓ | 아니오 |
| `main` CI가 실패하면 본 사람이 먼저 되돌리거나 고칩니다 | 5 사람 | `CONVENTION.md` 4 | ✗ | 사람 |
| 커밋 첫 줄은 목적과 결과를 적은 한국어 문장이고, 매일 커밋합니다 | 4 문서 | `CONVENTION.md` 5 | ✗ | 에이전트, 사람 |
| PR 전에 작성자가 본문과 diff를 읽고 생성 파일과 비밀 정보가 없는지 확인합니다 | 4 문서 + 5 사람 | `CONVENTION.md` 6; `.gitignore`; secret scanning과 push protection은 `disabled` | ✗ | 사람 |
| 병합된 코드의 원리를 말로 설명할 수 있어야 합니다 | 5 사람 | `CONVENTION.md` 6 | ✗ | 사람 |
| 규칙 파일과 ADR도 PR과 승인 1건으로 바꿉니다. GitHub 설정은 승인 뒤 오너가 반영합니다 | 2 정적 + 5 사람 | `CONVENTION.md` 8; 파일 변경은 위 ruleset이 덮음 | 파일 ✓ (관리자 우회 가능) / 설정 반영 ✗ | 사람 |
| 기록 위치: 할 일은 이슈와 보드, 회의 안건은 회의록, 확정 규칙은 `CONVENTION.md`와 ADR | 4 문서 | `CONVENTION.md` 7 | ✗ | 에이전트, 사람 |
| 타입 검사는 TS 7 `strict`, `noUncheckedIndexedAccess`로 판정합니다 | 2 정적 | `tsconfig.json`; `package.json` `typecheck`; CI | ✓ 단, `include`가 `src`와 `vitest.config.ts`뿐이라 `examples/`, `scripts/`는 타입 검사 밖 | 아니오 |
| 포맷과 린트 (Biome `recommended`), Markdown은 Biome 대상 아님 | 2 정적 | `biome.json`; `npm run check`; CI | ✓ | 아니오 |
| 이름 형식, 파일 이름 형식, `src/`의 default export 금지, 매개변수 재할당 금지 | 2 정적 | `biome.json`: `useNamingConvention`, `useFilenamingConvention`, `noDefaultExport`(`src/**`), `noParameterAssign` | ✓ | 아니오 |
| 모듈 의존 방향 표를 지킵니다 | 2 정적 + 5 사람 | `CONVENTION.md` 모듈 구조; `biome.json` `noImportCycles` | 양쪽 값 import 순환만 ✓ / 방향과 `import type` 순환은 ✗ (리뷰) | 사람 |
| 코어는 폴더 없이 `src/`에 기능당 파일 하나, `index.ts` 없음 | 4 문서 + 5 사람 | `CONVENTION.md` 모듈 구조; `docs/adr/team/one-file-per-feature-no-folders.md` | ✗ | 에이전트, 사람 |
| `Patch` 타입은 `patch.ts`에 두고 `diff.ts`는 `import type`으로 가져옵니다 | 4 문서 + 5 사람 | `docs/adr/team/patch-type-lives-in-patch-ts.md` | ✗ (Biome가 이 import를 판정하는지 확인 안 함) | 사람 |
| 테스트는 소스 옆 `*.test.ts`에 둡니다 | 4 문서 | `CONVENTION.md` 테스트; `docs/adr/team/tests-sit-next-to-source.md` | ✗ (`examples/examples.test.ts`는 `src/` 밖에 있고 vitest가 실행함) | 에이전트 |
| 테스트 이름은 ID로 시작하고 ID는 저장소 전체에서 하나입니다 | 2 정적 | `scripts/check-decision-links.mjs` (`npm run check`, CI) | 중복 ID ✓ / ID 없는 이름은 `[확인]` 출력만 / `src/`만 읽어 `examples/`의 E1–E10은 검사 밖 | 아니오 |
| ADR이 인용한 테스트 ID가 있고, 인용 형식이 `(테스트: T9, T26)`입니다 | 2 정적 | `scripts/check-decision-links.mjs`; CI | ✓ | 아니오 |
| `docs/requirements/` 표의 근거 칸에 적은 ADR 파일이 있습니다 | 2 정적 | `scripts/check-decision-links.mjs`; CI | ✓ | 아니오 |
| ADR 문장과 테스트 기대값의 뜻이 같습니다 | 4 문서 + 5 사람 | `docs/adr/team/decisions-and-tests-linked-by-id.md`; PR 템플릿 `새 세션 리뷰` | ✗ | 에이전트, 사람 |
| 결정을 바꾸면 새 ADR을 쓰고 옛 ADR을 `superseded by`로 바꿉니다 | 4 문서 | `CONVENTION.md` 결정과 테스트 잇기 | ✗ (대체된 ADR만 인용하는 테스트는 CI 로그에 `[확인]`으로만 나옴) | 에이전트 |
| 새로 생겼고 어느 ADR도 인용하지 않은 테스트를 보여 줍니다 | 2 정적 | `scripts/check-decision-links.mjs` (`origin/main`과 비교) | ✗ 출력만 하고, CI에서는 `origin/main`이 없어 `[건너뜀]` (2026-11-12 PR CI 로그 확인) | 에이전트 |
| ADR 형식: 번호 없는 파일 하나, 결정 한 문장, CAUTION 한 줄, 인용 두 줄, 폴더는 모듈 단계, 파일 이름은 폴더가 달라도 유일 | 2 정적 + 4 문서 | `CONVENTION.md` ADR 쓰기; `docs/adr/README.md`; `docs/adr/team/adr-is-one-decision-and-one-caution.md` | 인용 줄 형식만 ✓ / 나머지 ✗ (스크립트가 ADR 이름을 Set에 넣어 이름 중복을 알리지 않음) | 에이전트 |
| `it.todo`는 곧 쓸 테스트에만 씁니다 | 4 문서 | `CONVENTION.md` 테스트 | ✗ (todo 테스트를 인용하면 `[확인]` 출력만) | 에이전트 |
| 테스트는 내보낸 함수로 확인하고, 테스트만을 위해 내보내지 않으며, 기대값은 직접 적습니다 | 4 문서 + 5 사람 | `CONVENTION.md` 테스트 | ✗ | 사람 |
| 동사 표, `create<결과>From<입력>`, 숫자 상수 이름, 주석은 이유만, 함수 나누기 세 질문 | 4 문서 + 5 사람 | `CONVENTION.md` 이름과 함수; `docs/adr/team/names-and-functions-for-human-tracing.md` | ✗ | 사람 |
| `GLOSSARY.md`의 이름을 쓰고, 새 개념은 같은 PR에 정의합니다 | 4 문서 | `GLOSSARY.md`; `CONVENTION.md` 에이전트, 용어 가이드 | ✗ | 에이전트 |
| 에이전트는 생성 전에 기능, 인터페이스, 위치를 말하고 같은 일을 하는 함수를 검색합니다 | 4 문서 | `CONVENTION.md` 에이전트 | ✗ | 에이전트 |
| 에이전트가 쓴 PR 본문에 테스트 수 표, 데모 동작, 필요하면 mermaid와 함수 이름 트리, 새 세션 리뷰를 적습니다 | 4 문서 | `AGENTS.md`; `.github/pull_request_template.md`; `CONVENTION.md` 9 | ✗ | 에이전트 |
| 앱의 런타임 의존성은 0개입니다 | 4 문서 | `docs/adr/team/zero-runtime-dependencies.md` (`package.json`에 지금 `dependencies` 없음) | ✗ | 사람 |
| 코어가 내놓는 변환, 비교, 반영 함수는 넷이고 `createVNodeFromDom`은 요소만 받습니다 | 1 코드베이스 + 2 정적 | `src/*.ts`의 export; `createVNodeFromDom(element: Element)`; `docs/adr/team/core-public-function-names.md` (T1, T22, D1, P1) | ✓ (tsc, 테스트) | 아니오 |
| Hook은 Root Component가 렌더링하는 동안에만 부릅니다 | 1 코드베이스 + 2 정적 | `src/function-component.ts:225`의 `throw`; 렌더링 커서는 export하지 않는 모듈 변수; `docs/adr/render/hook-outside-render-throws-error.md`; `docs/adr/team/hooks-share-one-file-with-function-component.md` | ✓ (실행 시 `Error`, CI 테스트) | 아니오 |
| 렌더링 중에는 setter를 부르지 않습니다 | 1 코드베이스 + 2 정적 | `src/function-component.ts:147`의 `throw`; `docs/adr/setter/setter-during-render-throws-error.md` | ✓ (실행 시 `Error`) | 아니오 |
| `mount()`는 한 번만, `update()`는 `mount()` 뒤에만 | 1 코드베이스 + 2 정적 | `src/function-component.ts:49`, `:72`의 `throw`; `docs/adr/instance/` | ✓ (실행 시 `Error`) | 아니오 |
| Hook은 Root Component 본문 최상위에서 매번 같은 순서로 부릅니다 | 2 정적 + 4 문서 + 5 사람 | `biome.json` `useHookAtTopLevel`; `docs/adr/render/hook-rule-kept-by-convention.md`; `docs/adr/team/hook-position-checked-by-lint.md`; `examples/README.md` | 부분 ✓ (Biome은 대문자 Component와 소문자 `function` 선언만 봄. 소문자 화살표 함수 안은 못 봄) | 사람 |
| Root Component는 PascalCase, 자식 Component는 `function create<이름>` 선언이고 Hook을 쓰지 않습니다 | 2 정적 + 4 문서 + 5 사람 | `CONVENTION.md` 이름; `examples/README.md` 표 (알려 주는 곳: 리뷰, Biome) | 부분 ✓ (자식이 `function` 선언일 때 Hook만 Biome) / PascalCase는 ✗ | 사람 |
| Component 본문에서 DOM을 직접 고치지 않습니다 | 4 문서 + 5 사람 | `docs/adr/instance/component-returns-view-and-function-component-draws.md`; `examples/README.md` (알려 주는 곳: 리뷰). F144는 어긴 결과를 보여 줄 뿐 막지 않음 | ✗ | 사람 |
| 동작 결정 ADR (click, setter, instance, render, diff, patch, effect, history, vnode, verification-page, demo-page) | 2 정적 + 4 문서 | `docs/adr/<폴더>/` 94개; 89개가 `(테스트: …)`로 테스트를 인용; `npm test` (CI) | 인용한 89개 ✓ / 인용 없는 5개 ✗ (아래 목록) | 인용한 것 아니오, 나머지 에이전트 |
| 예제 페이지 7개가 설명대로 동작합니다 (E1–E10) | 3 검증 | `examples/examples.test.ts` (vitest + jsdom, `npm test`, CI) | ✓ | 아니오 |
| `main`의 검증 페이지를 GitHub Pages에 올립니다 | 3 검증 + 5 사람 | `.github/workflows/deploy-pages.yml` | 배포 ✓ / 화면 확인 ✗ | 사람 |
| Node 26을 씁니다 | 2 정적 | `.nvmrc`; CI `setup-node`의 `node-version-file` | ✓ (CI) | 아니오 |
| 모든 텍스트 파일은 LF | 2 정적 | `.gitattributes` | ✓ | 아니오 |

인용 없는 동작 ADR 5개: `demo-page/demo-splits-view-into-child-components`, `instance/failed-mount-instance-is-not-reusable` (superseded), `verification-page/verification-patch-reads-test-area-through-template`, `vnode/leading-newline-in-pre-and-textarea-is-not-handled`, `vnode/textarea-select-svg-template-are-not-covered`. `team/` ADR 11개 중에서는 `core-public-function-names` 하나만 테스트를 인용합니다.

로컬 `npm run check` 결과 (2026-11-18): 테스트 367개, ADR이 인용한 테스트 343개, 인용 안 된 테스트 24개, 실패 없음.

## mini-redis

| 규칙 | 지금 층 | 어디에 있나 | 강제되나 | 사람이 읽어야 하나 |
|---|---|---|---|---|
| `main`은 PR로만 바꿉니다 | 2 정적 + 4 문서 | `CONVENTION.md` 1; ruleset `Ruleset` (2026-11-18 생성)의 `pull_request` 규칙; bypass actor = 저장소 관리자 역할, `bypass_mode: always` | ✓ 단, 관리자는 언제나 우회 가능 | 아니오 |
| `main` 삭제와 force push 금지 | 2 정적 | ruleset `Ruleset`의 `deletion`, `non_fast_forward` | ✓ (관리자 우회 가능) | 아니오 |
| 승인 1건을 받은 뒤 병합합니다. 오너가 PR에 밝히면 승인 없이 병합합니다 | 4 문서 + 5 사람 | `CONVENTION.md` 3; ruleset `required_approving_review_count: 0` | ✗ | 사람 |
| 승인 뒤 diff가 바뀌면 다시 승인받습니다 | 4 문서 + 5 사람 | `CONVENTION.md` 3; ruleset `dismiss_stale_reviews_on_push: false` | ✗ | 사람 |
| merge commit으로 병합합니다 | 4 문서 | `CONVENTION.md` 3; ruleset `allowed_merge_methods: [merge, squash, rebase]` | ✗ | 사람 |
| CI에서 `make verify`가 통과합니다 | 2 정적 + 3 검증 | `.github/workflows/ci.yml` job `verify`; ruleset에 `required_status_checks` 없음 | ✓ 실패는 표시되지만 병합을 막지 않음 | 사람 (병합 전 결과 확인) |
| 실험 브랜치는 `<이니셜>-<주제>`이고 `main`으로 PR을 올리지 않습니다 | 4 문서 | `CONVENTION.md` 1 | ✗ | 사람 |
| PR 전에 `origin/main`을 개인 브랜치에 병합합니다 | 4 문서 | `CONVENTION.md` 2 | ✗ | 에이전트, 사람 |
| `main` CI가 실패하면 본 사람이 먼저 되돌리거나 고칩니다 | 5 사람 | `CONVENTION.md` 4 | ✗ | 사람 |
| 커밋 첫 줄은 한국어 문장이고, 매일 커밋합니다 | 4 문서 | `CONVENTION.md` 5 | ✗ | 에이전트, 사람 |
| PR 전에 생성 파일과 비밀 정보가 없는지 확인하고, 병합 코드의 원리를 설명할 수 있어야 합니다 | 4 문서 + 5 사람 | `CONVENTION.md` 6; `.gitignore` (`build/`); secret scanning `disabled` | ✗ | 사람 |
| `CONVENTION.md`도 PR과 승인 1건으로 바꿉니다. GitHub 설정은 승인 뒤 오너가 반영합니다 | 4 문서 + 5 사람 | `CONVENTION.md` 8 | ✗ (PR은 ✓, 승인 1건은 설정 0건) | 사람 |
| 기록 위치와 보드 카드 규칙 (마일스톤당 draft 카드 하나, 6단계 체크리스트, `Status`, `레포` 필드) | 4 문서 + 5 사람 | `CONVENTION.md` 7 | ✗ | 사람 |
| C11, 경고를 오류로 보는 빌드 | 2 정적 | `Makefile` `CFLAGS` (`-std=c11 -Wall -Wextra -Werror`); CI | ✓ | 아니오 |
| AddressSanitizer와 UBSan을 켠 단위 테스트 | 2 정적 + 3 검증 | `Makefile` `test`, `-fsanitize=address,undefined -fno-sanitize-recover=all`; `tests/*_test.c`; CI | ✓ | 아니오 |
| 실제 서버와 캐시 데모를 띄운 기능 테스트 | 3 검증 | `Makefile` `functional`, `cache-functional`; `tests/functional/*.py`; CI | ✓ (PostgreSQL 기능 테스트는 `make cache-functional-postgres`로만 △) | 아니오 |
| HTTP 계약 (요청, 응답, 오류 이유, 상한) | 3 검증 + 4 문서 | `docs/api.md`; `tests/functional/api_test.py`, `concurrency_test.py`, `expire_test.py` | ? 기능 테스트는 CI에서 ✓. 계약의 어느 줄까지 테스트가 덮는지는 대조하지 않음 | 에이전트 |
| 코드 모양은 `.clang-format` (Linux 스타일, 4칸, 중괄호, 80열) | 2 정적 | `.clang-format`; `scripts/convention.py lint` (`make verify`, CI) | ✓ | 아니오 |
| 이름 형식 (snake_case, 상수 대문자), 이름 3글자 이상, 중괄호 | 2 정적 | `.clang-tidy`; `scripts/convention.py lint`; CI | ✓ | 아니오 |
| Markdown의 물결표(`~`)는 `\~`로 씁니다 | 2 정적 | `scripts/convention.py` `check_tildes`; CI | ✓ | 아니오 |
| CI와 같은 clang-format 21.1.8, clang-tidy 21.1.6을 씁니다 | 2 정적 + 4 문서 | `ci.yml`의 `pip install`; `CONVENTION.md` 코드 | CI ✓ / 로컬 ✗ | 에이전트, 사람 |
| 3글자 이상 줄임말 금지, `모듈_동사`, 동사 표, 개념 이름 표, 구조체 `typedef` 금지, 숫자 상수 이름 | 4 문서 + 5 사람 | `CONVENTION.md` 이름 1–5 | ✗ | 사람 |
| 함수는 단계의 나열, 파일은 위에서 아래로, 마지막 `return` 앞 빈 줄 | 4 문서 + 5 사람 | `CONVENTION.md` 함수 1–3 | ✗ | 사람 |
| 가져온 코드 (Pintos `hash`, `list`, acutest, mongoose, siphash)는 원래 모양을 지킵니다 | 2 정적 + 4 문서 | `.clang-format-ignore`; `Makefile` 주석의 upstream commit | lint 제외 ✓ / 원본과 같은지 대조하는 도구 없음 ✗ | 사람 |
| 처음 전체 포맷 커밋을 blame에서 건너뜁니다 | 4 문서 | `.git-blame-ignore-revs`; `CONVENTION.md` 코드 | △ (각자 `git config`를 한 번 실행해야 함) | 사람 |
| 테스트 ID는 이름 문자열 맨 앞 `[T1]`이고 저장소 전체에서 하나입니다 | 2 정적 | `scripts/check-ids.py`; CI | ✓ (중복 검사. 지금 ID 21개) | 아니오 |
| ADR `결정` 행과 `docs/requirements.md` `근거` 칸이 인용한 ID가 실제로 있습니다 | 2 정적 | `scripts/check-ids.py`; CI | ✓ (지금 ADR 9개의 `결정` 행에는 ID 인용이 0개. 인용은 `requirements.md`에만 있음) | 아니오 |
| `근거` 칸의 ADR 이름에 해당하는 파일이 있습니다 | 2 정적 | `scripts/check-ids.py`; CI | ✓ | 아니오 |
| ADR 본문은 `항목`, `내용` 두 칸 표 하나, 행 순서 맥락→결정→이유→버린 대안→결과 | 2 정적 + 4 문서 | `scripts/check-ids.py` `ADR_PARAGRAPH_LABEL`; `CONVENTION.md` ADR | 문단 형식 라벨(`결정:` 등)만 ✓ / 행 순서 ✗ | 에이전트 |
| ADR은 `docs/adr/`에 평평하게, 번호 없는 이름, frontmatter `status`와 `milestone` | 4 문서 | `CONVENTION.md` ADR; `docs/agents/domain.md` (지금 9개 모두 두 칸이 있음) | ✗ | 에이전트 |
| ADR이 되는 두 기준, 이유 칸은 2단계에서 팀원이 말한 문장만 | 4 문서 + 5 사람 | `CONVENTION.md` ADR | ✗ | 사람 |
| 결정을 바꾸면 새 ADR과 `superseded by` | 4 문서 | `CONVENTION.md` ADR; `docs/agents/domain.md` | ✗ | 에이전트 |
| 마일스톤 하나는 6단계를 돕니다 | 4 문서 + 5 사람 | `CONVENTION.md` 마일스톤 | ✗ | 사람 |
| `overview.md`에 Redis의 실제 방식을 적지 않고, 아직 답을 다루지 않은 마일스톤을 문서 이름이나 예시로 쓰지 않습니다 | 4 문서 + 5 사람 | `CONVENTION.md` 마일스톤; `docs/agents/issue-tracker.md` | ✗ | 사람, 에이전트 |
| `spec.md`에 `## Redis와 대조` 절을 우리 생각→Redis 방식→고른 것 순서로 둡니다 | 4 문서 | `CONVENTION.md` 마일스톤; `docs/agents/issue-tracker.md` | ✗ | 에이전트 |
| 끝난 마일스톤 폴더는 고치지 않습니다 | 4 문서 | `CONVENTION.md` 마일스톤; `docs/agents/issue-tracker.md` | ✗ | 에이전트, 사람 |
| 티켓은 한 파일에 하나, `NN-` 번호, 위쪽에 `Status:` 줄, 아래에 `## Comments` | 4 문서 | `docs/agents/issue-tracker.md`; `docs/agents/triage-labels.md` | ✗ (spec과 티켓 38개 중 15개는 `Status:`, 23개는 `**Status:**`) | 에이전트 |
| 측정 기록: 파일 이름 `<번호>-<이니셜>-<주제>.md`, 한 파일 한 측정, frontmatter 칸, 고치지 않음, 머신이 다른 숫자는 비교하지 않음 | 4 문서 | `CONVENTION.md` 측정 기록 | ✗ | 에이전트, 사람 |
| cache-demo 기록용 측정은 3회 이상 | 2 정적 | `scripts/bench/cache_bench.py` `RECORD_RUNS_MIN = 3` | △ (`--output`을 준 실행에서만 실패) | 아니오 |
| 커밋하지 않은 변경이 있는 측정은 기록하지 않습니다 | 4 문서 + 5 사람 | `CONVENTION.md` 측정 기록; `cache_bench.py`는 `(커밋하지 않은 변경 있음)`을 출력만 함 | ✗ | 사람 |
| 시간 수치 측정은 `make verify`와 CI에 넣지 않습니다 | 1 코드베이스 | `Makefile` (`bench`, `cache-bench`, `rehash-micro`가 `verify` 의존에 없음) | ✓ | 아니오 |
| 테스트 파일 하나는 마일스톤 하나, 이름은 한국어 문장, 도구는 acutest | 1 코드베이스 + 4 문서 | `CONVENTION.md` 테스트; `Makefile` `TEST_SRCS := tests/*_test.c` | 파일 위치는 ✓ (패턴 밖 파일은 빌드되지 않음) / 나머지 ✗ | 에이전트 |
| 테스트는 공개 함수를 부르고 기대값은 직접 적습니다 | 4 문서 + 5 사람 | `CONVENTION.md` 테스트 | ✗ | 사람 |
| store의 내부는 `store.c`만 만지고, `store_get`이 돌려준 value는 읽기 전용입니다 | 1 코드베이스 | `src/store.h`의 `struct store;` (불완전 타입), `const void **value`; `docs/adr/get-lends-value-until-next-change.md` | ✓ (컴파일러) | 아니오 |
| mongoose를 읽는 모든 파일이 같은 `MG_MAX_HTTP_HEADERS`로 컴파일되고, mongoose는 서버에만 링크합니다 | 1 코드베이스 | `Makefile` `CPPFLAGS`, `$(SERVER)` 규칙 | ✓ | 아니오 |
| 서버는 프로세스 1개, 스레드 1개로 요청을 처리합니다 | 4 문서 | `docs/adr/single-thread-event-loop.md` | ✗ (스레드 생성을 막는 검사 없음) | 사람 |
| 변경 전에 `CONVENTION.md`, `GLOSSARY.md`를 읽고 용어를 그대로 쓰며, ADR과 어긋나면 밝힙니다 | 4 문서 | `AGENTS.md`; `docs/agents/domain.md` | ✗ | 에이전트 |

로컬 `python3 scripts/check-ids.py` 결과: 통과, 테스트 ID 21개.

## mini-dbms

| 규칙 | 지금 층 | 어디에 있나 | 강제되나 | 사람이 읽어야 하나 |
|---|---|---|---|---|
| `main`은 PR로만 바꿉니다 | 4 문서 | `CONVENTION.md` 1; ruleset 없음 (`[]`), branch protection 없음 (404) | ✗ | 사람 |
| 승인 1건, 승인 뒤 diff가 바뀌면 재승인, merge commit, 오너가 밝히면 승인 없이 병합 | 4 문서 + 5 사람 | `CONVENTION.md` 3; ruleset 없음 | ✗ | 사람 |
| CI에서 `make verify`와 `make tsan`이 통과합니다 | 2 정적 + 3 검증 | `.github/workflows/ci.yml` job `verify (ubuntu-latest)`, `verify (macos-latest)`; required check 없음 | ✓ 실패는 표시되지만 병합을 막지 않음 | 사람 (병합 전 결과 확인) |
| macOS와 Linux에서 같은 테스트가 같은 결과를 내고, glibc 전용 기능을 쓰지 않습니다 | 2 정적 + 4 문서 | `ci.yml` OS matrix; `docs/prd/final.md` 공통 | ✓ (두 OS CI) | 아니오 |
| 실험 브랜치는 `main`으로 PR을 올리지 않고, PR 전에 `origin/main`을 병합합니다 | 4 문서 | `CONVENTION.md` 1, 2 | ✗ | 에이전트, 사람 |
| `main` CI 실패 수습, 커밋 메시지는 한국어 문장과 매일 커밋 | 4 문서 + 5 사람 | `CONVENTION.md` 4, 5 | ✗ | 사람 |
| PR 전에 생성 파일과 비밀 정보 확인, 병합 코드 원리 설명 | 4 문서 + 5 사람 | `CONVENTION.md` 6; `.gitignore` (`build/`, `data/`, `__pycache__/`); secret scanning `disabled` | ✗ | 사람 |
| `CONVENTION.md`도 PR과 승인 1건으로 바꿉니다 | 4 문서 + 5 사람 | `CONVENTION.md` 8 | ✗ | 사람 |
| C11, 경고를 오류로 보는 빌드 | 2 정적 | `Makefile` `CFLAGS`; CI | ✓ | 아니오 |
| AddressSanitizer와 UBSan을 켠 단위 테스트 | 2 정적 + 3 검증 | `Makefile` `test`; `tests/*_test.c`; CI | ✓ | 아니오 |
| CLI와 서버를 실제로 실행하는 기능 테스트, 서버 출력에 sanitizer 경고가 있으면 실패 | 3 검증 | `Makefile` `functional`, `functional-server`; `tests/functional/*.py`; `server_test.py`의 `SANITIZER_MARKS`; CI | ✓ | 아니오 |
| 잠금, 작업 대기열, 여러 스레드가 엔진을 부르는 테스트와 서버 기능 테스트를 ThreadSanitizer로 다시 돌립니다 | 3 검증 | `Makefile` `tsan`, `tsan-server` (`TSAN_ENGINE_TESTS := T123 T124 T125 T126 T241`); CI | ✓ | 아니오 |
| 측정 절차가 작은 record 수로 끝까지 돕니다 | 3 검증 | `Makefile` `bench-smoke` (`verify`에 포함); 100만 건 `make bench`, `make bench-cursor`는 수동 | smoke ✓ / 전체 측정 △ | 아니오 |
| 코드 모양 `.clang-format`, 이름 형식과 길이, 중괄호, Markdown 물결표 | 2 정적 | `.clang-format`; `.clang-tidy`; `scripts/convention.py lint`; CI | ✓ (git이 아는 파일만. 새 파일은 `git add` 뒤부터) | 아니오 |
| CI와 같은 clang 도구 버전 | 2 정적 + 4 문서 | `ci.yml`; `CONVENTION.md` 코드; `README.md` 설치 | CI ✓ / 로컬 ✗ | 에이전트, 사람 |
| 모든 텍스트 파일은 LF | 2 정적 | `.gitattributes` | ✓ | 아니오 |
| 이름 규칙 (줄임말, `모듈_동사`, 동사 표, 개념 이름 표, `typedef` 금지, 숫자 상수)과 함수 규칙 (단계 나열, 순서가 중요한 쓰기와 되돌리기는 호출부에, 위에서 아래로, `return` 앞 빈 줄) | 4 문서 + 5 사람 | `CONVENTION.md` 이름, 함수 | ✗ | 사람 |
| 가져온 코드 (acutest, mongoose)는 원래 모양을 지킵니다 | 2 정적 + 4 문서 | `.clang-format-ignore`; `Makefile` 주석 | lint 제외 ✓ / 원본 대조 ✗ | 사람 |
| 테스트 ID는 `[T1]` 형식이고 저장소 전체에서 하나, 인용한 ID가 있습니다 | 2 정적 | `scripts/check-ids.py` (mini-redis와 같은 파일); CI | ✓ (지금 ID 95개) | 아니오 |
| `requirements.md` `근거` 칸의 ADR 이름에 파일이 있습니다 | 2 정적 | `scripts/check-ids.py`; CI | ✓ (지금 ADR 0개라 검사할 이름도 없음) | 아니오 |
| ADR 규칙: 평평한 폴더, 번호 없음, frontmatter `status`와 `phase`, 표 형식, 두 기준, 이유 칸은 회의에서 팀원이 말한 문장만 | 2 정적 + 4 문서 + 5 사람 | `CONVENTION.md` ADR; `scripts/check-ids.py`는 문단 라벨만 검사; `docs/adr/`에는 `.gitkeep`만 있음; `docs/prd/final.md`의 ADR 후보 넷은 팀원 확인 뒤에 씀 | 문단 라벨만 ✓ / 나머지 ✗ | 사람 |
| 작업 흐름 4단계, PRD 초안은 최종 PRD 뒤에 고치지 않습니다 | 4 문서 + 5 사람 | `CONVENTION.md` 작업 흐름; `docs/agents/issue-tracker.md` | ✗ | 사람, 에이전트 |
| PRD와 티켓 위쪽에 `Status:` 줄 | 4 문서 | `docs/agents/issue-tracker.md`; `docs/agents/triage-labels.md` | ✗ (티켓 13개는 `**Status:** done`, `final.md`는 `Status: ready-for-agent`, 초안 3개는 없음) | 에이전트 |
| 측정 기록: 파일 이름, 한 파일 한 측정, frontmatter (`records` 포함), 고치지 않음 | 4 문서 | `CONVENTION.md` 측정 기록 | ✗ | 에이전트, 사람 |
| 단위 테스트 파일 하나는 모듈 하나, 기능 테스트는 `tests/functional/<이름>_test.py`, 서버 테스트에는 서버 경로를 넘깁니다 | 1 코드베이스 + 4 문서 | `CONVENTION.md` 테스트; `Makefile` `FUNCTIONAL_TESTS`, `SERVER_FUNCTIONAL_TESTS` | 경로 넘기기 ✓ (Makefile) / 파일 나누기 ✗ | 에이전트 |
| 테스트는 테이블 파일을 임시 폴더에 만들고 지우며, 고정 입력은 `tests/` 아래에 커밋합니다 | 4 문서 | `CONVENTION.md` 테스트; `.gitignore` `data/` | ✗ | 사람 |
| 테스트는 공개 함수를 부르고 기대값은 직접 적습니다 | 4 문서 + 5 사람 | `CONVENTION.md` 테스트; `docs/prd/final.md` Testing Decisions | ✗ | 사람 |
| 엔진 바깥은 `engine.h`의 함수로만 엔진을 씁니다 | 1 코드베이스 | `src/engine.h`의 `struct engine;` (불완전 타입). PRD는 함수 넷이라 적고, 헤더에는 `engine_execute_from`까지 다섯이 있음 | ✓ (컴파일러) | 아니오 |
| 테스트가 파일 쓰기, 자르기, 할당 실패를 만들 수 있게 함수 포인터 표로 부릅니다 | 1 코드베이스 | `src/table.h:36-38`; `docs/prd/final.md` Testing Decisions | ✓ | 아니오 |
| B+ 트리 불변식 (리프 깊이, 키 순서, 키 수) | 2 정적 | `tests/bptree_test.c` (예: T42); CI | ✓ | 아니오 |
| PRD의 엔진 동작 결정 (데이터 폴더 독점, 깨진 파일 시작 거부, INSERT 실패 되돌리기, ID 발급, 상태 코드 등) | 2 정적 + 3 검증 + 4 문서 | `docs/prd/final.md` Implementation Decisions; `tests/engine_test.c`, `tests/functional/*.py`; 판정과 테스트 ID는 `docs/requirements.md` `근거` | ? 테스트는 CI에서 ✓. PRD 항목마다 테스트가 있는지는 대조하지 않음 | 에이전트 |
| 변경 전에 `CONVENTION.md`, `GLOSSARY.md`를 읽고 용어를 그대로 쓰며, ADR과 어긋나면 밝힙니다 | 4 문서 | `AGENTS.md`; `docs/agents/domain.md` | ✗ | 에이전트 |

로컬 `python3 scripts/check-ids.py` 결과: 통과, 테스트 ID 95개.

## 여러 저장소에 있는데 층이 다른 규칙

| 규칙 | mini-react | mini-redis | mini-dbms |
|---|---|---|---|
| `main`은 PR로만 | 2 ruleset ✓ (관리자도 직접 push 불가) | 2 ruleset ✓ (관리자는 언제나 우회) | 4 문서 ✗ (삭제와 force push 금지도 설정 없음) |
| 승인 1건 뒤 병합 | 2 ruleset ✓ (관리자 PR 병합 우회. #54–#56이 승인 없이 병합됨) | 4 문서 ✗ (ruleset 승인 0) + 오너 예외 | 4 문서 ✗ + 오너 예외 |
| 승인 뒤 diff가 바뀌면 재승인 | 2 ruleset ✓ | 4 ✗ | 4 ✗ |
| merge commit만 | 2 ruleset ✓ | 4 ✗ (ruleset이 셋 다 허용) | 4 ✗ |
| CI 통과 후 병합 | 2 required check `code` ✓ | 2 CI는 돌지만 필수 아님 | 2 CI (Linux, macOS)는 돌지만 필수 아님 |
| 결정과 테스트를 ID로 잇기 | 2 ADR 94개 중 89개가 인용, 끊긴 ID는 CI 실패 | 2 도구는 ADR `결정` 행을 읽지만 지금 인용 0개. 인용은 `requirements.md` `근거` 칸에만 | 2 ADR 0개. 인용은 `requirements.md` `근거` 칸에만 |
| ADR 형식 | 2 인용 줄 형식만 검사 | 2 문단 라벨만 검사 | 2 문단 라벨만 검사 (ADR 없음) |
| 이름 규칙 | 2 Biome 이름 형식 + 4·5 동사 표 | 2 clang-tidy 대소문자, 길이 + 4·5 줄임말, 동사 표 | mini-redis와 같음 |
| 모듈 경계 | 1 렌더링 커서 비공개 + 2 Biome 값 순환 + 5 방향 표 | 1 `struct store` 불완전 타입 | 1 `struct engine` 불완전 타입, 파일 함수 포인터 표 |
| 실행 중 검사 | 1 Hook, setter, mount의 `throw` | 3 ASan, UBSan | 3 ASan, UBSan, TSan |
| 실제로 실행하는 테스트 | 3 예제 jsdom (E1–E10) | 3 서버와 캐시 데모 기능 테스트 | 3 CLI와 서버 기능 테스트, TSan 서버 |
| 같은 도구 버전 | 2 `.nvmrc` (CI) | 2 CI의 clang 21 고정, 로컬 ✗ | mini-redis와 같음 |
| LF 줄바꿈 | 2 `.gitattributes` | 규칙 없음 | 2 `.gitattributes` |
| PR 본문 형식 | 4 PR 템플릿, `AGENTS.md` | 템플릿 없음 | 템플릿 없음 |
| 측정 기록 규칙 | 규칙 없음 | 4 문서 + 2 3회 이상만 △ | 4 문서 |
| 생성 파일과 비밀 정보 확인 | 5 사람 | 5 사람 | 5 사람 |

## 층별 개수

### mini-react

- 행 48개. 층별 (한 행이 두 층이면 두 층에 모두 셈): 1 코드베이스 4 · 2 정적 26 · 3 검증 2 · 4 문서 26 · 5 사람 15
- 강제 칸이 ✗로 시작하는 행: 21개. 일부만 ✗인 행 (예: `CI ✓ / 로컬 ✗`): 6개

### mini-redis

- 행 47개. 층별 (한 행이 두 층이면 두 층에 모두 셈): 1 코드베이스 4 · 2 정적 15 · 3 검증 4 · 4 문서 31 · 5 사람 13
- 강제 칸이 ✗로 시작하는 행: 25개. 일부만 ✗인 행 (예: `CI ✓ / 로컬 ✗`): 4개

### mini-dbms

- 행 32개. 층별 (한 행이 두 층이면 두 층에 모두 셈): 1 코드베이스 3 · 2 정적 13 · 3 검증 6 · 4 문서 19 · 5 사람 8
- 강제 칸이 ✗로 시작하는 행: 13개. 일부만 ✗인 행 (예: `CI ✓ / 로컬 ✗`): 4개

## 확인 못 한 것

- GitHub Project 보드(`projects/7`)의 카드가 mini-redis `CONVENTION.md` 7의 카드 규칙을 지키는지는 보지 않았습니다.
- 저장소 관리자 역할(bypass actor id 5)을 가진 사람이 누구인지, 팀원의 저장소 권한은 조회하지 않았습니다.
- `week11-12/CLAUDE.md`와 GitHub 설정이 다릅니다. CLAUDE.md는 mini-redis에 ruleset이 없다고 적지만 지금은 `Ruleset`이 있고(2026-11-18 03:09 생성), mini-react에서 admin bypass를 PR #29 뒤에 지웠다고 적지만 지금 ruleset에는 관리자 `pull_request` 우회가 있습니다(ruleset 수정 2026-11-11). 누가 왜 바꿨는지는 확인하지 않았습니다.
- `make verify`, `make tsan`, `npm run typecheck`, `npm test`는 로컬에서 실행하지 않았습니다(`build/`와 산출물을 만들지 않으려고). CI 결과만 봤습니다: 세 저장소 모두 최신 `main` CI가 success입니다.
- Biome `recommended`가 `import type` 사용(`useImportType`)을 판정하는지 확인하지 않았습니다. 그래서 `Patch` 타입 행은 문서의 "리뷰에서 봅니다"를 따랐습니다.
- mini-redis `docs/api.md`와 mini-dbms `docs/prd/final.md`의 각 항목을 테스트가 덮는지는 줄 단위로 대조하지 않았습니다(표의 `?` 두 행).
- `vendor/`와 Pintos에서 가져온 파일이 upstream 원본과 같은지는 대조하지 않았습니다.
- 커밋 메시지 규칙, 매일 커밋, PR 전 `origin/main` 병합을 실제 이력이 지키는지는 조사하지 않았습니다.
- `github-pages` environment의 보호 규칙과 Actions 권한 설정은 조회하지 않았습니다.
- 팀원 clone의 로컬 git hook은 볼 수 없습니다. 이 clone의 hook만 봤습니다.
