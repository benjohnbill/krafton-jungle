---
scope: mini-react Phase 2 — LMS 문장 ↔ 기록(GLOSSARY, ADR) ↔ 코드 ↔ 테스트, 한 표
source: LMS learning/1307 (2026-11-11 Aside로 읽음), mini-react `CJG-phase2` (테스트 강화와 문서 지적 수정 이후)
status: 2026-11-11 최신. 이전의 phase2-extraction(에이전트 초안)과 phase2-audit(독립 점검)를 합쳤습니다
---

# Phase 2 표

- 파일 줄: `fc` = `src/function-component.ts`, `dp` = `src/test-pages/demo-page.ts`, `fct` = `src/function-component.test.ts`, `dpt` = `src/test-pages/demo-page.test.ts`.
- **테스트** 칸에는 코드를 일부러 깨뜨렸을 때(아래 변이 표의 M번호) 실패한 테스트만 적습니다. 깨뜨려도 통과하는 테스트는 근거로 세지 않습니다.
- **판정:** `완료` = 기록 + 코드 + 변이에서 실패하는 테스트 · `테스트 없음` = 기록과 코드는 있지만 그 결정만 깨는 변이를 만들 수 없음 · `기록 없음` = 코드만 있음 · `코드 없음` = 아직 구현 전 · `대상 아님` = 코드로 확인할 문장이 아님.
- **할 일** 칸: `용어` = GLOSSARY에 넣을 LMS의 추상적인 단어 · `ADR` = 코드가 이미 정했지만 ADR이 없는 결정 · `구현` = `useEffect`와 `useMemo` 작업에서 다룸.

## 1. 표

| # | LMS 문장 | 빈칸 | 코드의 답 | 기록 | 테스트 (변이) | 판정 | 할 일 |
|---|---|---|---|---|---|---|---|
| 1 | Component·State·Hooks를 직접 구현하고 동작하는 웹 페이지를 만든다 | 범위 전체를 묶는 문장 | `FunctionComponent`, `useState`, 데모 페이지 | GLOSSARY 절 "Component와 상태", "데모 페이지" | 하위 행 참조 | 테스트 없음 | 구현 (`useEffect`, `useMemo`) |
| 2 | Component는 UI를 나누는 작은 단위 | 나누는 기준, 자식을 어떻게 부르나 | 자식은 Root Component 본문에서 직접 부르는 함수. 데모는 나누지 않음 (dp:9-35) | GLOSSARY `Component`, ADR `root-only-function-component` | 행 67·68·69가 동작을 보이지만, 호출 방식이라 깨는 변이 없음 | 테스트 없음 | 용어 "자식 Component" |
| 3 | 각각의 Component는 자신만의 로직과 렌더링을 담당 | "로직"과 "렌더링"의 뜻 | 로직 = 본문에서 `useState`를 부르고 `on`으로 클릭 함수를 등록. 렌더링 = `VNode`를 돌려주기까지. DOM에 그리는 일은 `mount`와 `update` (fc:52-63) | GLOSSARY `Component`. "렌더링"은 정의 없이 여러 정의에 쓰임 | 행 67 (호출 횟수). 깨는 변이 없음 | 테스트 없음 | 용어 "렌더링", ADR "DOM 작업은 Component가 아니라 `FunctionComponent`" |
| 4 | 반드시 함수형 컴포넌트로 구현 | 프레임워크 내부 클래스는 허용되나 | `RootComponent = (props) => VNode` (fc:11). 클래스는 `FunctionComponent`뿐 | GLOSSARY `Component` | 타입 검사로만 보장 | 테스트 없음 | — |
| 5 | FunctionComponent 클래스가 함수형 컴포넌트를 감싼다 | 모두 감싸나, Root만 감싸나 | Root만 (fc:21-27) | GLOSSARY `FunctionComponent`, `Root Instance`, ADR `root-only-function-component` | 행 2·3 (M2), 9·13 (M3), 8 (M18) | 완료 | — |
| 6 | hooks 배열 (상태 저장용) | 칸의 모양, 칸을 찾는 규칙, 렌더링마다 초기화 | `{ value }` 칸, 렌더링마다 `hookIndex = 0`, 부른 순서대로 (fc:15, 55, 68-72) | GLOSSARY `hooks`. "칸", "Hook"은 정의 없음 | 행 8·17·20 (M1), 8·20·21 (M13) | 완료 | 용어 "Hook", "칸". ADR "칸은 호출 순서로 찾음" |
| 7 | mount(): 처음 렌더링 | 기존 자식, 두 번 mount, 이벤트 연결 시점 | `replaceChildren`, 컨테이너에 click 리스너 하나 (fc:29-38) | ADR `root-instance-keeps-container-and-current-view`, `click-wires-…`. 두 번 mount는 미결정 (`it.todo` 행 6) | 행 2·3 (M2) | 완료 | — |
| 8 | update(): 상태 변경 후 다시 렌더링 | 인자, 비교 대상, mount 전 호출 | 인자 없음, `currentView`와 비교, mount 전이면 `Error` (fc:41-49) | ADR `root-instance-keeps-container-and-current-view`, `update-before-mount-throws-error` | 행 8·22 (M18), 9·13 (M3), 10·12·13 (M12), 7 (M11) | 완료 | — |
| 9 | Hook은 최상위 컴포넌트에서만 사용 가능 | 코드가 막나, 약속인가 | 막지 않음. "렌더링 중인가"만 검사 (fc:101-106) | ADR `hook-rule-kept-by-convention` (의도적 이탈), GLOSSARY `Root Component` ("약속한") | 렌더링 밖: 행 15·43·44·45 (M9, M10). 한계: 행 70 | 완료 (LMS와 다르게 정한 것을 기록함) | — |
| 10 | State는 최상위 컴포넌트에서만 관리 | 강제 여부 | 저장소는 `hooks`뿐 (fc:22) | GLOSSARY `Root Component`, ADR `root-only-function-component` | 행 69. 깨는 변이 없음 | 테스트 없음 | — |
| 11 | 자식은 state 없이 부모가 준 props만 사용 (Lifting State Up) | 자식이 부모 상태를 바꾸는 경로 | 함수를 props로 넘기지 않음. 자식은 `data-action` 문자열만 그리고, 함수는 Root가 `on`으로 등록 | ADR `click-wires-…` (연결 방식만) | 행 69. 클릭 연결은 행 60 (M14), 62 (M15) | 테스트 없음 | 용어 "props". ADR "자식 → 부모는 `data-action` 문자열로" |
| 12 | 자식은 상태 없이 props만 받는 순수 함수 | "순수"의 뜻 | 강제하지 않음 | ADR `root-only-function-component` | 행 67. 깨는 변이 없음 | 테스트 없음 | — (코드가 좁힌 뜻이 없음) |
| 13 | State는 값이 변경될 수 있는 동적 데이터 | 무엇을 담을 수 있나 | `value: unknown`. 함수, 배열, NaN, -0 모두 받음 | 없음. "상태값"이 정의 없이 쓰임 | 행 22 (M4), 25 (M6), 28 (M5) | 기록 없음 | 용어 "State(상태)" |
| 14 | State가 바뀌면 화면이 자동으로 다시 그려진다 | "바뀌면"의 판정, 시점 | `Object.is`로 다를 때만, setter 안에서 바로 `update()` (fc:75-79) | ADR `setter-skips-same-value`, `setter-updates-without-batching` | 행 8·22 (M4), 24·27·28·32 (M5), 28·29·30 (M5b), 35·36·37 (M8) | 완료 | 용어 "setter" |
| 15 | Hooks: 상태와 생명주기를 쓰게 해 주는 기능 | "생명주기"의 범위 | 상태만. 생명주기 없음 | GLOSSARY `hooks`, `useState` | 상태 부분은 #16 | 코드 없음 (생명주기) | 구현 (`useEffect`와 함께 용어 "생명주기") |
| 16 | 최소 구현 대상: useState | 초깃값 함수, setter 함수, 같은 값, 렌더링 밖 | fc:66-106 | GLOSSARY `useState`, ADR 5개 (`initial-value-…`, `setter-accepts-…`, `setter-skips-…`, `setter-updates-…`, `hook-outside-render-…`) | 행 19 (M7, M7b), 23·25 (M6), 24·27·28·32 (M5), 8·17·20 (M1), 15·43·44·45 (M9, M10) | 완료 | — |
| 17 | 최소 구현 대상: useEffect | 실행 시점, deps, 정리 함수 | 없음 | 기본값 표만 (`mini-react-study.md`) | — | 코드 없음 | 구현 (#34, #36) |
| 18 | 최소 구현 대상: useMemo | 다시 계산하는 조건 | 없음 | 기본값 표만 | — | 코드 없음 | 구현 (#35) |
| 19 | "함수는 매번 새로 실행되는데, 상태는 어떻게 유지할까?" | 답의 형태 | 인스턴스의 `hooks`에 두고, 렌더링 중 `currentComponent`와 `hookIndex`로 순서대로 찾음 | GLOSSARY `Component`, `hooks` | 행 8·17·20 (M1), 8·20·21 (M13) | 완료 | ADR은 #6과 같음 |
| 20 | 다시 렌더링할 때 Phase 1의 Virtual DOM을 그대로 활용 | "그대로"의 범위, `StateHistory`도 쓰나 | `createDomFromVNode`, `diffViews`, `applyPatchesToDom`. `StateHistory`는 안 씀 | ADR `root-instance-keeps-container-and-current-view` (`StateHistory`에 맡기지 않는 이유 포함) | 행 9·13 (M3) | 완료 | — |
| 21 | 동작 흐름: Virtual DOM 생성 | 누가 언제 | `update()`마다 Root Component를 다시 불러 새 View | GLOSSARY `View`, `VNode` | 행 8·22 (M18) | 완료 | — |
| 22 | 이전 Virtual DOM과 비교 (Diff) | "이전"이 무엇인가 | 필드 `currentView` | ADR `root-instance-keeps-container-and-current-view` | 행 10·12·13 (M12) | 완료 | — |
| 23 | 바뀐 부분만 실제 DOM에 반영 (Patch) | — | `applyPatchesToDom` (fc:47) | 같은 ADR | 행 9·10·12·13·29·30 (M3) | 완료 | — |
| 24 | 목표: 전체를 다시 그리지 않고 필요한 부분만 | 측정 기준 | 노드 객체 유지, 같은 값이면 렌더링 건너뜀 | 같은 ADR, `setter-skips-same-value` | 행 9·10·12·13·29·30 (M3), 27 (M5) | 완료 | — |
| 25 | Phase 1과 2를 활용한 웹 페이지 | 한 페이지인가, 공존 | `index.html`의 `#demo`에 카운터. 검증 페이지와 같은 문서 | GLOSSARY `데모 페이지`, ADR `demo-page-is-one-counter`, 0008 | dpt 행 105·106·107·112 (M16), 104 처음 값 (M17) | 완료 (jsdom 기준) | — |
| 26 | 사용자의 입력/클릭 등에 따라 화면이 변경 | 어떤 이벤트 | click만. `dblclick`, `input`은 무시 | ADR `click-wires-…` (클릭만이라는 결정은 없음) | dpt 행 105–107 (M16), fct 행 60 (M14), 62·10 (M15), 66 | 완료 | ADR "입력 이벤트는 다루지 않음" |
| 27 | 중점: UI를 어떻게 Component로 나눌 것인가? | 질문만 | 나누지 않음 (카운터 하나) | ADR `root-only-…`, `demo-page-…` | 깨는 변이 없음 | 테스트 없음 | — |
| 28 | 중점: State는 어디에 두는 것이 좋은가? | 질문만 | Root Instance의 `hooks` | GLOSSARY `Root Component`, `Root Instance` | 행 69 | 테스트 없음 | — |
| 29 | 중점: setState는 상태 변경 외에 무엇을? | 질문만 | 같은 값 판정 뒤 `update()` | ADR `setter-skips-…`, `setter-updates-…` | 행 8·22 (M4), 27 (M5) | 완료 | 용어 "setter" (#14와 같음) |
| 30 | 중점: 여러 상태 변경을 한 번에? | 질문만 | 모으지 않음 | ADR `setter-updates-without-batching` | 행 35·36·37 (M8) | 완료 | — |
| 31 | Batching은 선택 과제 | 할지 말지 | 안 함 | 같은 ADR | 행 35·36·37 (M8) | 완료 | — |
| 32 | 실제 React와의 차이점 공부 | 산출물 형식 없음 | — | ADR 세 곳에 React 비교 | — | 대상 아님 | (발표 자료 몫) |
| 33 | 단위 테스트로 각 모듈 검증 | 충분 기준 | `useState`와 `FunctionComponent`는 `fct` | CONVENTION "테스트" 절 | #16의 변이들 | 완료 (`useState`) / 코드 없음 (`useEffect`, `useMemo`) | 구현 |
| 34 | 기능 테스트로 화면 동작 확인 | jsdom인가 실제 브라우저인가 | `dpt`가 jsdom에서 확인 | ADR 0008 § 테스트 (Phase 1용). 데모용은 테스트 파일 머리 주석뿐 | dpt 행 104–107·112 (M16, M17) | 완료 (jsdom) | 용어 "단위 테스트", "기능 테스트" |
| 35 | 테스트 영역에 다양한 태그를 추가해 확인 | Phase 2의 "테스트 영역" | 데모에는 테스트 영역이 없음. GLOSSARY `테스트 영역`은 Phase 1 | GLOSSARY `테스트 영역`, ADR 0008 | Phase 1 범위 (변이 안 함) | 테스트 없음 | — |
| 36 | 엣지 케이스를 최대한 고려 | "최대한"의 기준 | 같은 값, 초깃값 함수, 렌더링 중 Error, mount 전 update, 클릭 위임 경계 | 각 ADR의 CAUTION. "근거 없음" `it.todo` 14개 (fct 13, dpt 1) | 위 변이들 | 완료 (정한 것만) | 3단계 (ADR에서 테스트 펼치기) |
| 37 | 포트폴리오 수준의 완성도 | 측정 기준 없음 | — | — | — | 대상 아님 | — |

## 2. 요약

- **처리 (2026-11-11, `CJG-phase2` `ddf6ff8`):** 아래 용어 후보 9개를 `GLOSSARY.md`에 넣고(생명주기 제외), ADR 후보 4개를 썼습니다. Phase 2 ADR 15개 모두 새 형식(결정 한 문장 + CAUTION 한 줄 + 테스트 ID)입니다. 테스트 ID는 `F` + 이 표가 아닌 #30 표의 행 번호입니다. 인용되지 않은 테스트는 `it.todo`(근거 없음)와 F4, F5, F16, F40뿐입니다.

- **판정:** 완료 20, 테스트 없음 10, 기록 없음 1 (#13), 코드 없음 3 (#15 생명주기, #17, #18), 갈림 1 (#33), 대상 아님 2 (#32, #37).
- **모순:** 0건. 해결 기록: #8 `mount` 전 `update()` (ADR 추가, `it.todo` → 테스트), #9 Hook 규칙 (ADR `hook-rule-kept-by-convention`, 행 70을 "한계" 테스트로), GLOSSARY `Root Component`의 "유일한" (약속으로 고침), ADR `click-wires-…`의 "리스너 하나" (`mount`마다 하나, 두 번 mount는 미결정으로 적음).
- **용어 후보 (GLOSSARY):** 렌더링, State(상태), Hook, 칸, setter, props, 자식 Component, 단위 테스트와 기능 테스트. 생명주기는 `useEffect` 때.
- **ADR 후보 (코드가 이미 정함):** DOM 작업은 `FunctionComponent`가 함 (#3), 칸은 호출 순서로 찾음 (#6, #19), 자식 → 부모는 `data-action` 문자열 (#11), 입력 이벤트는 다루지 않음 (#26).
- **"테스트 없음" 10건의 공통 원인:** "자식은 상태 없는 함수"는 `src`의 장치가 아니라 부르는 방식이라, 그것만 깨는 변이를 만들 수 없습니다. 테스트를 더해도 풀리지 않는 종류입니다.

## 3. 변이와 결과 (테스트 강화 이후)

한 번에 하나씩 적용하고 `npx vitest run <파일> -t "<행 번호:>"`로 돌린 뒤 되돌렸습니다. 굵은 칸은 강화 전에 살아남았다가 이제 실패하는 테스트입니다.

| 변이 | 바꾼 곳 | 실패하는 테스트 |
|---|---|---|
| M1 | 렌더링마다 `hooks` 비우기 | 행 8, 17, 20 |
| M2 | mount의 `replaceChildren` → `append` | 행 2, 3 |
| M3 | Diff와 Patch 대신 전부 다시 그리기 | 행 9, 13, **10, 12, 29, 30** |
| M4 | setter에서 `update()` 제거 | 행 8, 22 |
| M5 | `Object.is` 건너뛰기 제거 | 행 24, 27, 28, 32 |
| M5b | `Object.is` → `===` | 행 28, **29, 30** |
| M6 | setter가 함수를 값으로 저장 | 행 23, 25 |
| M7, M7b | 초깃값 함수를 안 부름, 매번 부름 | 행 19 |
| M8 | `update()`를 microtask로 미룸 (Batching) | 행 35, 36, **37** |
| M9, M9b | `currentComponent` 비우기 제거, 성공 때만 비움 | 행 15, 44, 45 |
| M10 | 렌더링 밖 Hook의 명시 `throw` 제거 | **행 15, 43, 44, 45** |
| M11 | `update()`의 mount 전 검사 제거 | 행 7 |
| M12 | `currentView` 갱신 제거 | 행 12, 13, **10** |
| M13 | 렌더링마다 `hookIndex = 0` 제거 | 행 8, 20, 21 |
| M14 | 렌더링마다 `actions.clear()` 제거 | 행 60 |
| M15 | `update()`마다 리스너 추가 | 행 10, 62 |
| M16 | 데모 setter가 값을 안 늘림 | dpt 행 105, 106, 107, 112 |
| M17 | 데모가 7에서 시작 | **dpt 행 104 (처음 값)** |
| M18 | `update()`가 옛 View를 다시 씀 | 행 8, 22 |

## 4. 확인하지 못한 것

- 실제 브라우저에서의 데모 동작 (jsdom만).
- Phase 1 모듈과 검증 페이지 테스트의 강도 (#33, #35).
