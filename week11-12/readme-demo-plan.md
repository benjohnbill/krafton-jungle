---
role: mini-react README의 Architecture와 Demo 절, 발표용 데모와 비교 페이지 계획. 개인 층이며 팀원은 읽지 않아요
truth: 2026-11-12 grilling 세션의 합의 (Q1~Q20)
status: 진행 중. 발표는 2026-11-12, 리허설 11:00. 아래 Work units의 체크가 현재 상태예요
---

# README + demo plan

## Revised (오라버니 결정 2026-11-12, 서사를 다시 정한 뒤)

아래 Decided와 부딪히면 이 절이 우선이에요.

- **Presentation**: README로 4분, 오라버니 혼자 발표해요.
- **Core**: 이 레포의 특징은 LMS 문장 → ADR → 테스트 → 코드의 top-down 구조와 그 연결의 자동 검사예요. README의 Architecture 절이 이것을 Phase, 단계, 문장 하나의 순서로 보여 줘요.
- **Honesty**: "모든 동작에 이유를 댈 수 있다"는 쓰지 않아요. ADR 초안은 AI가 썼고, Phase 2는 사람이 읽고 고쳤고, 전부 이해하지는 못했어요. 구조는 코드를 짠 뒤에 세웠어요. 발표에서 이것을 어떻게 말할지는 오라버니가 정해요. README에는 적지 않았어요.
- **Phase definitions**: Phase 1 = "두 `View`(Virtual DOM)의 차이를 찾아, 그 차이만 DOM에 반영합니다". Phase 2 = "State가 바뀌면 새 `View`를 만들어 Phase 1에 넘깁니다". 경계는 `View`예요. effect는 정의에서 빼고 단계 표에 둬요.
- **Stages**: Phase 1은 `vnode`, `diff`, `patch`, `history`. Phase 2는 `click`, `setter`, `instance`, `render`, `effect`. 단계마다 정의(폴더 `README.md`의 첫 줄), 대표 LMS 문장, 닿는 LMS 문장 수, ADR 수를 표로 둬요.
- **Chain example**: L16 "최소 구현 대상: useState"가 ADR 다섯 개로 퍼지는 표.
- **Dropped**: 세 레인 비교 페이지(`lab/`)와 다이어그램 PNG는 만들지 않아요. 비교는 README의 세 줄 표로 대신해요. Vanilla와 React의 줄은 재지 않았다고 적었어요.
- **Demo role**: 순위 페이지 GIF는 "사슬 예시의 결정이 화면에 보이는 장면"이에요. 쓰는 법은 팀원의 `docs/examples/`(PR #48)가 맡아요.
- **Open**: `View`가 청중에게 낯설 수 있다는 오라버니의 걱정. README는 첫 등장에 "LMS가 Virtual DOM이라 부르는 것"이라고 풀었어요.

## Decided

- **Budget**: 작업 시간 5~6시간. 에이전트가 만들고, 오라버니가 확인하고 Openscreen으로 녹화해요.
- **Spine**: ADR 단계 이름 일곱 개 `click → setter → instance → render → diff → patch → effect`를 다이어그램, 데모 패널, 비교 레인이 함께 써요. 번호 ①~⑤는 쓰지 않아요.
- **Data Flow**: Phase 1 입구는 `diff`에서 합류해요. 그림에는 단계 이름, 함수 이름, ADR 수만 둬요. 아래 표는 `단계 | 함수 | 대표 결정 1줄 | ADR 수`이고, 단계 이름은 그 폴더의 `README.md`로 링크해요.
- **Diagram format**: mermaid로 내용을 먼저 확정하고, 그다음 `diagram-design`으로 PNG를 만들어요. 원본 HTML도 `docs/images/` 옆에 커밋해요. 색은 Overview 담당의 대문이 정해지면 맞춰요.
- **Core Data**: 표 하나, 타입 코드 하나(`VNode`, `Patch`, `HookCell`), 클릭 한 번의 실제 값 하나. 오라버니가 결과물을 보고 피드백해요.
- **Chain example**: LMS 문장 → ADR → 테스트 → 코드를 실제 한 줄 예시와 숫자 세 개로 6줄 안쪽에 실어요. 예시는 `docs/requirements/`에서 확인해 골라요.
- **Main Demo**: 나만무 팀 판독기의 "동료 평가 → 익명 순위" 한 화면. 서버 없이 클릭만 쓰고 코어는 고치지 않아요. 한 프레임에 평가, 순위, Hook 패널을 둬요. 가짜 참가자 6명과 `Track`은 `product/shared/`의 것을 써요.
- **Hook cells**: `hooks[0]` `useState(scores)`, `hooks[1]` `useState(track)`, `hooks[2]` `useState(isAnonymous)`, `hooks[3]` `useMemo(ranking, [scores, track])`, `hooks[4]` `useEffect(제목에 1위 표시, [1위의 id])`.
- **Recording order**: 이름 가리기 토글(`useMemo`와 `useEffect` 건너뜀) → 점수 클릭 A(`useMemo` 실행) → 점수 클릭 B(1위가 바뀌어 셋 다 실행) → 트랙 탭(`REPLACE`).
- **Compare page**: 세 레인(Vanilla `innerHTML`, Mini, 실제 React)을 한 화면에 두고 클릭 두 번으로 갈라요. 클릭 A(순위 안 바뀜)는 Vanilla만 다르고, 클릭 B(순위 바뀜)는 Mini와 React가 갈려요. 축은 `MutationObserver`로 센 실제 DOM 변경 횟수와 포커스예요.
- **Message**: "State가 Root에만 있어서 key가 지킬 것이 DOM 상태뿐이다." 잃는 것은 순서가 바뀔 때의 DOM 변경 횟수와, 항목을 따라가지 않는 DOM 상태예요. 얻는 것은 `path`만으로 자리를 가리키는 `Patch`, key 오용 버그가 없다는 점, 83줄짜리 `diff.ts`예요.
- **Locations**: 데모는 `mini-react/src/test-pages/`의 세 번째 페이지(카운터 데모 페이지는 그대로). 비교 페이지는 `lab/`에 만들어 스터디 사이트 `study/week11/`에 올리고 README에서 링크해요. GIF 두 개는 `mini-react/docs/images/`에 10MB 이하로 넣어요.
- **Branch and PR**: `CJG` 위에 쌓은 `CJG-pr-8-demo-readme`. PR은 README의 `## Architecture`와 `## Demo` 절만 추가하고 `동작 흐름` 절을 대체해요. 병합은 오라버니가 admin bypass로 직접 해요 (오라버니 결정 2026-11-12).
- **Tickets**: 만들지 않아요. 이 파일의 Work units가 대신해요.

## Work units

- [ ] 1. mermaid 내용 확정 (노드와 화살표). 초안은 열어 보였고 오라버니 확인 대기 (2026-11-12 01:40)
- [ ] 2. 데모 페이지와 Hook 패널, 기능 테스트, `GLOSSARY.md` 용어. 오라버니 녹화
  - 만든 것 (브랜치 `CJG-pr-8-demo-readme`): `src/test-pages/ranking-page.ts`(`startRankingPage`), `hook-panel.ts`(`startHookPanel`), `ranking-page.test.ts`(K1~K9), `index.html`의 `#ranking-section`. 검증 명령 넷 통과, 테스트 367개
  - 남은 것: 오라버니의 브라우저 확인과 녹화. `CONVENTION.md`의 모듈 구조 목록에 두 파일 줄 추가는 오라버니 승인 뒤
  - 계획과 달라진 점: effect는 `document.title`이 아니라 container 밖의 `#ranking-notice`에 1위를 써요(카운터 데모 페이지와 제목이 겹쳐서). 트랙 탭의 Patch는 `REPLACE`가 아니라 `PROPS`, `TEXT`, `REMOVE`예요
- [x] 3. `lab/` 비교 페이지: 접었어요 (Revised)
- [ ] 4. README의 Architecture와 Demo 절 글, Core Data, 사슬 예시. 초안을 썼고 오라버니 검토 대기. GIF 줄은 주석으로 뒀어요
- [x] 5. 다이어그램 PNG: 접었어요 (Revised). mermaid는 Aside에서 렌더링을 확인했어요
- [x] 6. PR #49를 admin bypass로 `main`에 병합했어요 (2026-11-12, merge commit `774ab07`). PR #47의 커밋도 함께 들어가 PR #47이 병합됨으로 바뀌었어요. `main`의 CI와 Deploy Pages 통과. 새 세션 리뷰는 하지 않았고 PR 본문에 적었어요
- [ ] 7. 남은 것: GIF 녹화와 README의 GIF 줄 주석 풀기, 새 세션 리뷰, `CONVENTION.md` 모듈 구조 목록의 두 줄, 로컬 `CJG`에 `main` 반영 (`npm run typecheck && npm run check && npm test && npm run build`)

늦어지면 뒤에서부터 버려요: PNG는 mermaid로 남기고, React 레인은 표로 내려요.

## Unverified

- Mini 레인과 React 레인의 DOM 변경 횟수와 포커스 동작은 예측이에요. 비교 페이지를 돌려 실제 값으로 바꿔요.

## Open (오라버니가 확인)

- key를 팀이 논의해서 뺀 것인지. 확인 전에는 "의도적 결정"이라는 단어를 쓰지 않아요.
- 사슬 예시가 다른 팀원의 절과 겹치는지.
- Overview 담당의 대문 색.
- 스터디 사이트 push는 배포라서 그때 다시 승인받아요.
