---
scope: Step 3 of the Phase 2 reverse extraction — cases expanded from ADRs + GLOSSARY only, diffed against the F tests
authority: Snapshot of 2026-11-11 (`mini-react` `CJG-phase2` at `b6d3145`). Not the current truth after the next test or ADR change
---

# Phase 2 Step 3 — 코드를 보지 않은 에이전트의 케이스 표 대 기존 F 테스트

## Method

- Input: `GLOSSARY.md` + 32 Phase 2 ADRs, with the `결정:` / `CAUTION:` citation lines removed. No code, no tests.
- A fresh agent expanded them to a case table: **261 cases (C001–C261)** and **31 undecided questions (U01–U31)**.
- 에이전트(나)가 케이스를 F 테스트 112개와 **제목 수준**으로 대조했어요. 테스트 본문은 F87, F93만 읽었어요. 아래 "누락" 은 "제목에서 안 보임"이지, "본문에도 없음"의 증명이 아니에요.
- 전체 케이스 표 (`/tmp/step3/out/cases.md`) 는 WSL 종료 때 사라져요. 이 문서가 남기는 것은 판정이에요.

## 1. 문서 자체의 결함 (코드가 아니라 문장을 고쳐야 하는 것)

- **U01 모순.** `GLOSSARY.md:39`는 Root Instance가 "앱에 하나만" 있다고 해요. `root-instances-are-independent` ADR과 데모 두 개를 띄우는 테스트(F113, F14)는 여러 개를 전제해요. 문장을 고칠 곳은 GLOSSARY예요.
- **U02.** 검증 페이지가 Root Instance를 갖는지 GLOSSARY에 없는데, 위 ADR의 CAUTION이 "서로의 State를 읽을 수 없다"고 써요.
- **테스트는 결정했는데 ADR이 말하지 않는 곳** (테스트가 사실상 ADR 역할을 해요):
  - C044 / U07 — effect A의 setter 안 중첩 render 뒤 바깥 effect B (F91)
  - C191 / U14 — 클릭 대상 해석: 안쪽 요소, `data-action` 없음, 컨테이너 자신 (F50, F55, F56)
  - C193 / U16 — 다음 렌더링에서 등록하지 않은 이름 (F60)
  - C226 / U19 — 내용이 있는 컨테이너에 mount (F2)
  - C237 / U23 — 데모 표시 문구 (F114, F115)

## 2. 누락 케이스 — ADR이 결정을 말하는데 대응 테스트 제목이 없음

우선순위는 "ADR이 이미 결정을 적었는가"와 "실제로 빠질 만한 함정인가"로 매겼어요.

**높음 — 에러 경로 조합 (ADR 둘의 교차)**

- C157, C158 — effect가 `update()`에서, 그리고 setter가 시작한 update에서 Error (F93은 mount만)
- C159 — effect 3개 중 2번째가 던지면 3번째는 안 불림
- C163, C164 — render Error와 effect Error가 번갈아 나는 update 열
- C132, C141 — render Error면 effect도 cleanup도 안 불림
- C143 — effect가 던지기 전에 모든 cleanup은 이미 불림
- C045, C088 — 중첩 render Error와 갱신 함수 Error가 effect 안에서 나는 경우
- C212, C213 — setter로 render가 던지게 만든 뒤 셀 값 유지, 다음 성공 update가 직전에 그린 View와 비교됨
- C211 — 실패한 렌더링에서 `on`으로 등록한 이름은 남지 않음
- C214, C215 — setter가 시작한 update의 render Error, 자식 Component 본문의 Error
- C086, C087 — 한 클릭에서 `setA(ok)`, `setB(던짐)`, `setC` 가 안 불림, 그 뒤 setter 정상
- C061 — render Error 뒤 셀과 같은 값을 넘기면 건너뜀
- C033 — render 중 setter Error가 직전 화면과 클릭 함수를 남김

**중간 — 경계값과 함정**

- C103, C104, C106, C107 — memo 결과가 `null`/`0`/`false`/`""`, 함수 반환, 계산 함수의 Error, deps 누락 함정
- C114, C117, C121, C122, C123, C124 — deps 항목 하나만 다름, 매번 새 객체 literal, `[1]→[2]→[1]`, `[{}]`, `[[]]`, 같은 참조
- C050, C049 — `useEffect(fn, [setter])`는 한 번만 불림, 칸마다 setter가 다름
- C092, C096 — 거짓 같은 초깃값(`null`, `""`, `false`)이 다시 초기화되지 않음, `useState(() => myFn)`
- C065, C066, C074, C075, C076 — 갱신 함수가 `undefined`를 돌려줌, setter가 돌아오기 전에 갱신 함수가 끝남, 같은 값 setter 다음 새 값 setter는 렌더링 한 번, 두 setter와 effect deps, 렌더링 세 번
- C152 — `async` effect의 정리 함수는 불리지 않음
- C175, C176 — effect 안의 `on` 호출은 Error이고, Error 뒤에도 기존 버튼은 동작
- C028 — cleanup 안에서 `useState`
- C167 — 다른 컨테이너로 두 번째 `mount()`도 Error
- C187 — update 뒤에 처음 나타난 버튼도 클릭됨
- C189 — 함수 속성 View를 `StateHistory`에 저장하면 `DataCloneError` (`DataCloneError` 문자열이 `src` 어디에도 없음)
- C188 — `data-action` 문자열만 쓴 View는 `structuredClone`됨
- C081, C148, C206, C230 — 인스턴스 둘 사이: `B.update()`의 Error가 A에 안 닿음, cleanup, 같은 이름의 `on`, actions 표가 분리됨
- C135, C146 — 일부 effect만 다시 불리는 순서, 컨테이너를 문서에서 빼도 cleanup이 안 불림
- C021, C016 — Hook 중간에 던진 뒤 index가 0부터 다시 시작함, `hooks` 길이

**낮음 — 사소하거나 중복에 가까움**

C002, C003, C006, C202, C203, C204, C239, C243, C244, C245, C251, C252, C224

## 3. 이미 덮인 것 (제목 기준)

C004, C005, C008–C014, C018, C019, C022–C027, C029, C030, C032, C036–C041, C047, C048, C051–C060, C062–C064, C067–C069, C071–C073, C077–C080, C083–C085, C089–C091, C094, C095, C099–C102, C105, C108–C113, C115, C116, C118–C120, C125, C127–C130, C133, C134, C136–C139, C144, C145, C149–C151, C154, C156, C165, C166, C168, C171, C173, C174, C177, C179–C182, C184–C186, C194–C201, C205, C208–C210, C216, C220–C223, C225, C227–C229, C231, C232, C235, C236, C238, C240, C241, C246–C250, C253, C254.

Phase 1 범위(C255–C261: VNode, StateHistory, 검증 페이지)는 `vnode.test.ts`, `history.test.ts`, `verification-page.test.ts`에 있고 이번 대조에서 제외했어요.

## 4. 에이전트가 판단을 못 내린 질문 (U01–U31)

`UNDECIDED` 로 남긴 31개 중, 사용자가 정할 가치가 큰 것만 추리면:

- **U03** — 첫 `mount()`가 Error로 끝난 인스턴스의 상태 (다시 `mount()`할 수 있나, 리스너가 붙었나)
- **U09, U10** — 실패한 render가 이미 쓴 칸, 던진 effect의 deps와 cleanup 기록
- **U04, U05** — cleanup이 던질 때, cleanup 안에서 setter를 부를 때
- **U08** — render 중 setter를 자식 본문, `useMemo` 함수, 초깃값 함수, 갱신 함수에서 부를 때
- **U12** — 렌더링마다 Hook 개수나 종류가 달라질 때
- **U22** — `useMemo` 함수 안의 Hook은 "렌더링 안"인가

나머지(U11, U13–U21, U23–U31)는 `it.todo`가 아니라 범위 밖 한 줄로 처리할 후보예요 (`it.todo`는 쓸 테스트만).

## 5. 다음에 정할 것

- 누락 케이스를 어디까지 테스트로 쓸지 (높음만, 높음+중간, 전부)
- U01을 GLOSSARY에서 고칠지
- 판정할 질문을 ADR 한 줄로 만들지, 범위 밖으로 둘지

## 6. 진행 결과 (2026-11-11, 같은 세션)

사용자가 추천안 1·2·3을 수용했어요.

- **U01·U02:** `GLOSSARY.md` Root Instance 정의를 "앱에 여러 개 있을 수 있고 각 setter는 자기 인스턴스의 `update()`를 부릅니다"로 고쳤고, `root-instances-are-independent` CAUTION에서 검증 페이지를 뺐어요.
- **누락 케이스 (높음 19행 + CAUTION 계열 6행):** F117–F139 테스트 23개를 더했어요. 22개는 처음부터 통과했고, 변이 검사로 지키는 것을 확인했어요 (effect 오류 삼키기, `on` 등록 시점 앞당기기, setter가 렌더링 중 칸 쓰기, 정리 함수 일부만 부르기).
- **U03·U09·U10 (코드가 하는 일 확인):** 테스트 F140–F142.
  - **U09는 실제 버그였어요.** render가 Error를 던지기 전에 부른 `useEffect`가 deps를 먼저 기록해서, 다음에 성공한 렌더링에서 그 effect가 불리지 않았어요. `src/function-component.ts`에서 deps를 `runPendingEffects` 시작 때 기록하도록 고쳤어요 (ADR `render-error-does-not-record-effect-deps`).
  - U10: 던진 effect와 뒤의 effect는 deps가 같은 동안 다시 불리지 않아요 (ADR `effect-error-skips-later-effects-until-deps-change`). 코드는 그대로예요.
  - U03: 첫 `mount()`가 render Error로 끝나면 그 인스턴스는 다시 쓸 수 없어요 (ADR `failed-mount-instance-is-not-reusable`). 코드는 그대로예요.
- **U08:** 코드는 이미 어디서든 setter를 Error로 막고 칸을 쓰지 않아요. `setter-during-render-throws-error` 제목에 합쳐 F129, F130으로 지켜요.
- **범위 밖으로 둔 것:** U04, U05, U12, U22와 나머지 23개. `it.todo`로 남기지 않았어요.
- **검증:** `typecheck`, `check`, `test` (352개 통과, `it.todo` 2개), `build` 모두 통과.
- **남은 것 (대조 전용):** 중간 우선순위 중 CAUTION 계열이 아닌 케이스는 쓰지 않았어요.
