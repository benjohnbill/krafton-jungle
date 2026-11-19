---
scope: mini-react Phase 1 테스트·구현에서 에이전트가 정한 결정과 그 근거
authority: 결정 요약. 팀 규칙의 원문은 mini-react의 docs/adr/0005~0008, CONVENTION.md, GLOSSARY.md
decided: 2026-11-09
status: 오라버니 검토 대기 (팀 공유 전)
---

# mini-react Phase 1 — 결정 요약

오라버니가 [결정 필요]를 "기존 관례와 안정성 위주로 자율 결정"하라고 맡긴 결과예요. 모든 코드는 `CJG`에 단위별로 커밋하고 push했어요. `main` PR과 Lark 공유는 아직 안 했어요.

## 한눈에

| 단위 | 커밋 | 테스트 파일 | 결과 |
|---|---|---|---|
| Patch 형식 + `applyPatchesToDom` | `190175d` | `patch.test.ts` | 38 passed |
| `diffViews` | `13648f9` | `diff.test.ts` | 39 passed |
| `StateHistory` | `94b0e59` | `history.test.ts` | 17 passed, 1 todo |
| 변환 보강 + 왕복 | `269fc30` | `vnode.test.ts`, `round-trip.test.ts` | 48 + 9 passed |
| Diff → Patch 통합 | `6f8b14a` | `diff-patch.test.ts` | 12 passed |
| 검증 페이지 + History 복원 | `7a007ed` | `test-pages/*.test.ts` | 35 + 15 passed, 1 todo |
| 리뷰 반영 | `89bdc1a`, `a261c83` | (위 파일들) | 아래 "독립 리뷰" |

합계 214 passed, 2 todo. `npm run typecheck`, `npm run check`, `npm test`, `npm run build` 모두 통과.

todo 2개는 Lark에서 **선택** 표시된 행이에요: 69행 `hist-max-size`(이력 최대 개수), 92행 `verify-highlight`(바뀐 곳 강조).

## 결정 목록

DEC 번호는 Aside 설계 문서(`aside-handoff/phase1-test-design.md` §5)의 번호예요.

### Patch와 Diff — ADR 0006

| 항목 | 결정 | 근거 |
|---|---|---|
| Patch 종류 | `TEXT`, `REPLACE`, `PROPS{set, remove}`, `INSERT`, `REMOVE` | Lark 24~50행의 형식 그대로. `CREATE`만 `INSERT`로 바꿈 |
| `CREATE` → `INSERT` | 이름 변경 | CONVENTION 동사 표의 `create`는 "새로 만들어 돌려줍니다". DOM에 끼워 넣는 일과 뜻이 섞임 |
| path 기준 (DEC-05) | 앞의 Patch를 적용한 뒤의 트리 | Lark 32·36·37·45행이 이미 "뒤에서부터 REMOVE"를 기대. 반대안(변경 전 트리)은 INSERT 위치 표현이 따로 필요 |
| 순서 책임 | `diffViews`: 같은 번호끼리 → INSERT 앞부터 → REMOVE 뒤부터, 한 요소의 PROPS가 자식보다 먼저 | key 없는 비교에서는 지우는 자식이 늘 끝 번호라 앞 번호와 부딪히지 않음 |
| `path: []` | View 자신. container는 그대로 | Lark 46행 |
| TEXT의 path | 글자 노드 자체 | Lark 25·33·34행의 `[0]`, `[1, 0]`, `[0, 1, 0]` |
| 번호 세는 법 (DEC-04) | 글자와 요소만, 주석 제외, 공백·빈 글자 포함 | ADR 0005의 `children` 규칙과 같게 |
| 실패 | path 앞 Error(메시지에 path), 되돌리지 않음 | Lark 49행. 되돌리기는 요구사항에 없음 |
| `diffViews` 인자 검사 | 두 인자가 `null`·`undefined`일 때만 TypeError | Lark 39행. 자식 안까지는 검사 안 함 |
| 빈 PROPS | DOM을 바꾸지 않음 | 현재 동작 유지 (DEC-13) |
| 같은 Patch 재적용(멱등성) | 요구하지 않음 | DEC-13: 계약 없음 |
| 입력칸 value 삭제 PROPS | 정하지 않음, 지금은 속성만 지움 | ADR 0005가 입력칸 value를 항상 넣으므로 DOM에서 읽은 View끼리는 생기지 않음 |
| 글자 비교 | 다듬지 않고 그대로 | ADR 0005의 공백 유지와 같은 규칙 |

### 변환 — ADR 0005 (기존)

| 항목 | 결정 | 근거 |
|---|---|---|
| 공백 (DEC-01) | 공백만 있는 글자 노드도 유지 | ADR 0005. Lark 9행을 `fromdom-keep-whitespace`로 고침 |
| 루트 입력 (DEC-02) | `createVNodeFromDom(element: Element)` 유지 | ADR 0004가 시그니처를 확정. Lark 3·12행(루트가 글자·주석)은 자식 사례로 검사 |
| 입력칸 (DEC-03) | `.value`를 읽고, 빈 값도 넣음. `checkbox`, `radio`, `file`은 입력칸이 아님 | ADR 0005. `file`은 리뷰에서 추가: `.value`에 글자를 쓰면 `InvalidStateError` |

### StateHistory — ADR 0007 (신규)

| 항목 | 결정 | 근거 |
|---|---|---|
| API (DEC-06) | `push`, `current`, `back`, `forward`, `canBack`, `canForward`, `size` | Lark 60~69행과 브라우저 History의 이름. 동사 표에 `can`, `push`, `back`·`forward` 추가 |
| 빈 이력·경계 이동 | `null`을 돌려주고 현재 위치 유지 | Lark 64·65행을 빈 이력까지 넓힘 |
| 같은 내용 저장 (DEC-07) | `push`는 늘 저장. 거르는 일은 페이지가 `diffViews` 결과로 | 비교는 `diffViews`의 일. 역할이 겹치지 않게 |
| 격리 (DEC-08) | 저장·반환 모두 `structuredClone` 사본 | Lark 67·68행. View가 작아서 사본이 단순 |
| 최대 개수 | 구현 안 함 (`it.todo`) | Lark 69행이 "선택" |

### 검증 페이지

| 항목 | 결정 | 근거 |
|---|---|---|
| 테스트 영역 | HTML 원문을 쓰는 `textarea` | Lark 71행 "테스트 영역의 HTML", 85·86·87행이 HTML 입력을 전제 |
| 입력 읽기 (DEC-12) | `<template>`로 읽고 `script`, `iframe`, `object`, `embed`, `meta`, `base`, `link`, `on*` 속성, `srcdoc`, 값 어디에든 든 `javascript:`를 지움. 주석도 지우고 인접 글자를 합침 | Lark 88행은 script·onerror만 요구. 다른 문서를 열거나 URL로 실행되는 경로까지 막음 (보안은 최소주의 예외) |
| 최상위 노드 | 요소 정확히 하나. 공백 글자·주석은 세지 않음 | Lark 85·86행 |
| 바뀐 것 없는 Patch | 아무것도 안 함, 이력도 안 쌓음 | Lark 80행 |
| 과거 위치의 바뀐 것 없는 Patch (DEC-09) | 앞쪽 기록(redo) 유지 | 바뀐 게 없으면 이력을 건드릴 이유가 없음 |
| 저장 안 한 편집 후 이동 (DEC-10) | 편집을 버리고 이력의 View를 보여 줌 | 경고창·자동 저장 같은 새 UI를 만들지 않는 쪽 |
| 뒤로·앞으로 | 실제 영역을 다시 읽어 `diffViews` + `applyPatchesToDom` | 선택 사항인 Lark 90행(바뀐 곳만 고침)도 같이 충족 |
| Patch의 비교 기준 (DEC-15, 리뷰 후) | 실제 영역을 다시 읽어 비교·적용하고, 이력에는 현재 View와 다를 때만 쌓음 | 뒤로·앞으로와 기준을 맞춤. 실제 영역 입력칸에 직접 친 값도 테스트 영역 값으로 맞춰지고, 그 차이만으로는 이력이 쌓이지 않음 |
| 적용 중 오류 (리뷰 후) | 보여야 할 View로 실제 영역을 다시 그리고 `#message`에 오류 표시. Patch면 이력에 안 쌓음 | ADR 0006은 되돌리지 않으므로, 반쯤 바뀐 화면을 페이지가 수습 |
| Patch 로그 | 마지막으로 적용한 Patch(이동 포함)의 종류와 path를 표시 | Lark 91행(선택), 구현이 간단해서 포함 |
| 실제 영역 | 루트 요소 하나만 둠 (`index.html`은 들여쓰지 않음) | 앞에 공백 글자가 있으면 path `[]`가 그 공백을 가리킴 |
| 입구 함수 | `startVerificationPage(document)` | 동사 표에 `start` 추가 |
| 기능 테스트 (DEC-14) | jsdom으로 페이지 코드를 직접 조작 + Aside 브라우저로 실제 확인 | 오라버니 결정. 새 브라우저 러너 의존성을 들이지 않음 |

## 바뀐 팀 문서

- **ADR 0006 (신규)**: Patch 형식, path, 순서, 실패, 빈 PROPS, `diffViews` 인자 검사.
- **ADR 0007 (신규)**: StateHistory 동작과 이름.
- **ADR 0008 (신규)**: 검증 페이지. 입력 읽기와 지우는 범위, 실제 영역 기준 비교(DEC-15), 이동 때 편집 버리기, 적용 오류 수습, 기능 테스트 방법.
- **ADR 0005**: `file` 입력칸 제외, `createVNodeFromDom`은 요소만 받음(DEC-02). **ADR 0006**: container에는 View 하나, 같은 Patch 재적용은 약속하지 않음(DEC-13).
- **ADR 0004**: ADR 0006으로 가는 한 줄. `Patch = unknown` 단계 종료.
- **GLOSSARY.md**: `path`, `StateHistory`, 검증 페이지, 실제 영역, 테스트 영역 추가.
- **CONVENTION.md**:
  - "형식이 정해지기 전에는 Patch 내용을 읽지 않는다" 삭제.
  - 동사 `get`, `can`, `push`, `back`·`forward`, `start` 추가.
  - StateHistory 메서드 이름 규칙 한 줄.

ADR 0005~0008은 모두 `status: proposed`예요. 팀 승인은 PR에서 받아요: #21 문서 → #22 테스트 → #23 구현 순서로 머지해요.

## 실제 브라우저 확인 (Aside, 2026-11-09)

`npm run dev`로 띄운 페이지에서 실제 키 입력과 마우스 클릭으로 확인했어요. 콘솔 오류는 0건이에요.

- **처음 상태**: 두 영역이 같고, 뒤로가기와 앞으로가기가 꺼져 있음 (70~72행).
- **글자 하나 고치고 Patch**: 변경 기록은 그 글자 노드의 `characterData` 1건뿐이고, `li` 세 개는 같은 객체로 남음 (74·75행). 로그에 `TEXT [5, 3, 0]`.
- **바뀐 것 없이 Patch**: 변경 0건 (80행).
- **뒤로가기와 앞으로가기**: 두 영역이 함께 바뀌고 버튼 상태가 맞음 (81·82행).
- **빈 입력**: 거절하고 "최상위 노드가 하나 필요합니다"를 표시 (85행).
- **`onerror`, `javascript:`, `<script>` 입력**: 아무것도 실행되지 않고 실제 영역에서 지워짐 (88행).

확인하지 못한 것은 실제 한글 IME 조합 중 Patch, 그리고 포커스와 커서 유지예요. 자동화로는 OS IME를 재현할 수 없어서 오라버니가 직접 쳐 봐야 해요.

## 독립 리뷰 (코드를 쓰지 않은 리뷰어, 2026-11-09)

14건 중 결함 3건은 재현한 뒤 고쳤고, 나머지는 문서와 이름을 고쳤어요.

| 지적 | 등급 | 처리 |
|---|---|---|
| 뒤로간 뒤 바뀐 것 없는 Patch가 이력을 쌓고 앞쪽 기록을 지움 (`<p>a<!--x-->b</p>`의 글자 두 개가 HTML을 거치면 하나로 합쳐짐) | 높음 | 입력과 실제 영역에서 주석을 지우고 인접 글자를 합침. HR-N07, HR-N08 |
| `type="file"` 입력칸에 `.value`를 써서 오류 | 중간 | `isTextInput`에서 `file` 제외, ADR 0005. T52, P38 |
| 적용 중 오류가 나면 이력·화면·버튼이 어긋남 | 중간 | 다시 그리고 안내. V93, V94 |
| ADR 0006에 "container에는 View 하나" 전제가 없음 | 낮음 | ADR 0006에 추가 |
| Patch와 이동의 비교 기준이 다름 | 낮음 | DEC-15. V95, V95a |
| `meta`·`base`가 살아남음 | 낮음 | 지움. V88a, 값 중간 `javascript:`는 V88b |
| 이름·주석·테스트 도우미·문서 표 | 낮음 | 이름 변경, 주석은 이유만, CONVENTION 모듈 표, GLOSSARY 용어 3개 |

남은 위험:
- `<pre>`, `<textarea>`는 여는 태그 바로 뒤 줄바꿈을 HTML 파서가 버려요. 그래서 그 줄바꿈으로 시작하는 글자는 왕복이 정확하지 않고, 뒤로간 뒤 바뀐 것 없는 Patch가 이력을 쌓을 수 있어요. 드문 입력이라 남겼어요.

## 관찰 (결정은 아님)

리뷰 전에는 Patch가 실제 영역 입력칸에 직접 친 값을 보지 않았어요. DEC-15로 바뀌어서, 지금은 Patch를 누르면 그 값이 테스트 영역의 값으로 맞춰져요. 과제는 사용자가 실제 영역을 편집한다고 가정하지 않아요.

## Lark

Lark 시트는 다빈님 개인 파일로 쓰기로 해서 고치지 않았어요(2026-11-09 결정). 이 문서와 테스트 지도 HTML이 팀 공유 자료예요. 시트와 다른 점은 아래와 같아요.

- `CREATE` → `INSERT` (31, 33, 37, 44, 101행). 44행 ID는 코드 쪽에서 `patch-insert`로 불러요.
- 9행 `fromdom-skip-whitespace`: 코드는 공백을 유지해요(ADR 0005).
- 3행 `fromdom-text`, 12행 `fromdom-comment-node`: 루트가 아니라 자식 사례로 검사해요(DEC-02).
- 8행 `fromdom-bool-attr`: `<input disabled>`의 기대값은 `{ disabled: '', value: '' }`이에요(ADR 0005).
- 51행 `int-render-roundtrip`: 입력 View는 정규형이어야 해요(입력칸에 value가 있고 주석이 없음).

## 상태

- 독립 리뷰: 완료, 반영 (`89bdc1a`, `a261c83`)
- Lark: 고치지 않음 (다빈님 개인 파일)
- HTML: `test-map.html`(대상 13개, 갈래 57개), `decisions.html`
