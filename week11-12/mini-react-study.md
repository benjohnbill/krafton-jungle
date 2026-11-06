---
role: mini-react study plan for the learner and the agent. Teammates do not read this file
truth: Decisions and levels are from the 2026-11-06 session. Step contents are a draft from two critics (Claude, Codex) and the agent
status: Trial. The learner changes the level of any step at any time
progress: memory/progress.md holds the current step. This file does not
---

# mini-react study plan

## Goal

세 질문에 mini-react를 근거로 자기 말로 답합니다. 오늘 전부 끝내는 것보다, 단계를 따라가며 이해하는 것을 우선합니다.

1. Why that framework? Why do people use it?
2. What problems does the framework solve?
3. Why are those functionalities in that framework?

## Decisions

학습자가 2026-11-06에 정한 내용입니다.

- **App order:** Vanilla → 실제 React → mini-react. 사다리 전체를 한 번 지나갑니다. 개념마다 세 번 치지 않습니다.
- **Language:** Vanilla와 실제 React는 JS, mini-react부터 TS입니다.
- **Reader:** 학습자와 에이전트입니다. 팀원과 그들의 에이전트는 고려하지 않습니다.
- **Reading:** 단계마다 에이전트가 위치를 찍어 준 짧은 구절만 읽습니다.
- **Page:** 버튼과 측정 화면은 에이전트가 만들고, `diff`와 `patch`는 학습자가 친 함수를 불러 씁니다.
- **Levels:** 모든 세부 단계에 Min, Mid, Best를 적어 둡니다. 학습자가 진행하면서 단계별로 수준을 바꿉니다.
- **Time:** 분 단위로 계획하지 않습니다. 순서와 비중만 봅니다. 4a~4c가 오늘 작업의 절반 정도입니다.

## One block

첫 묶음에서 시험하고, 과하면 학습자가 줄입니다.

1. 에이전트가 코드 5~12줄과 새 개념 하나를 줍니다. 익숙해지면 20줄 이하로 늘립니다.
2. 학습자가 칩니다. 뜻을 모르는 줄은 바로 묻습니다.
3. 실행 전에 결과를 한 줄로 예측합니다.
4. 예측이 틀리면 왜 틀렸는지 묻습니다.
5. 힌트 없는 변경 과제를 합니다. 오래 막히면 에이전트가 힌트를 줍니다.
6. 짧은 구절을 읽습니다.
7. 자기 말로 한 문장을 쓰면, 에이전트가 빠진 부분을 짚고 질문 하나를 합니다.

- **Questions:** 문법, 함수, 오류는 바로 묻습니다. "왜 이렇게 만들었지?"는 한 줄로 적어 두었다가 묶음 끝에 묻습니다. 질문 개수는 목표가 아닙니다.
- **Pass signal:** 예측, 변경 과제, 한 문장입니다. 하나라도 막히면 그 자리에서 멈춥니다.
- **No sheet:** stage sheet는 쓰지 않습니다.

## Ladder: before the meeting

Mid가 에이전트의 기본값입니다. 시간이 모자라면 R, 학습 단계, 5단계 순서로 뺍니다.

| Step | Problem | Min | Mid | Best | Read |
|---|---|---|---|---|---|
| 0 | 입력한 글자는 어디에 있을까요? | 콘솔에서 `.value`와 `setAttribute` 비교 | + `document`, `window`, 입력칸 객체 살펴보기 | + `cloneNode`와 `innerHTML`에서 값이 어떻게 되는지 확인 | MDN input |
| 1~2 | 손으로 맞추면 어떤 곳을 빠뜨릴까요? | 목록, 합계, 삭제 | + 빈 목록 안내로 함수가 커지는 것을 체감 | + 함께 바꿔야 하는 곳을 전부 적기 | Reacting to Input |
| 3 | 전체를 다시 그리면 무엇이 교체될까요? | `innerHTML` 다시 그리기 | + 키를 누를 때마다 다시 그리기 | + 글자를 상태에 저장해도 노드는 새것임을 확인 | MDN `innerHTML` |
| R | React에서는 무엇이 그대로 남을까요? | 짧은 React 목록을 실행해서 관찰 | 같은 목록과 같은 과제를 직접 치기 | + DOM 노드가 같은지 3단계와 비교 | Render and Commit |
| 4a | 왜 화면 설명을 객체로 둘까요? | `VNode` 타입과 노드 생성 | + 중첩 목록 | + DOM을 Virtual DOM으로 변환 | Virtual DOM FAQ |
| 4b | 다른 곳만 어떻게 고칠까요? | 글자 `diff`, `patch` | + 속성, 입력칸의 `.value` | + 속성 삭제, 변경 없음, 단위 테스트 | WHATWG input의 해당 구절 |
| 4c | 구조가 바뀌면 어떻게 할까요? | 노드 추가, 삭제 | + 교체, 떨어진 두 행 삭제, 학습자의 함수로 페이지 실행 | + 경우별 단위 테스트, 빈 자식 | Reconciliation |
| 5 | 맨 앞에 넣으면 값은 어디로 갈까요? | 페이지에서 예측하고 관찰 | + 직접 치기, React에서 index와 id 비교 | + `key` 기반 Diff 구현 | Rendering Lists |
| 학습 | DOM 변경의 비용은 어디에서 생길까요? | Reflow, `MutationObserver` 구절 읽기 | + 학습자의 페이지에서 Paint flashing 관찰 | + 스타일 쓰기와 `offsetWidth` 읽기 실험 | MDN, Chrome DevTools |

## Ladder: after the meeting

순서만 정했고, 세부 내용은 도착했을 때 다시 정합니다.

| Step | Problem | Min | Mid | Best |
|---|---|---|---|---|
| 6 | 강의 페이지와 History를 어떻게 만들까요? | 실제 영역, 테스트 영역, 3개 버튼 | + DOM 변환, 복사본이 필요한 이유 확인 | + 기능 테스트, 뒤로 간 뒤에 새 변경 |
| 7 | 함수를 다시 실행하면 상태는 어디에 있을까요? | 클로저, hooks 배열, `useState` | + React로 카운터 2개 비교 | + `if` 안의 `useState`를 일부러 깨 보기 |
| 8 | `useEffect`와 `useMemo`는 왜 있을까요? | 각 Hook의 짧은 구현 | + 렌더링 중 타이머, 재계산 횟수 실험 | + 정리 함수, 의존성 엣지 케이스 |

## Meeting and reading levels

| Item | Min | Mid | Best |
|---|---|---|---|
| 2026-11-07 meeting | PR 없이 공부한 내용을 말로 공유 | PR 없이, 직접 친 코드와 페이지를 보여 주며 설명 | 직접 친 `diff`, `patch`로 `CJG`에서 부분 구현 PR. 단위 테스트 포함, 설명할 수 있는 코드만 포함 |
| Framework reading (after step 8) | 하지 않음. 체감한 이유만 답하고 나머지는 "확인하지 못했다"로 구분 | Svelte의 "Virtual DOM is pure overhead" 읽기 | + Vue 렌더링 문서, 기술적 이유와 채택 이유 구분 |

공지의 필수 범위는 "Phase 1에 대한 개념 파악 및 자료조사"이고, 구현과 PR은 권장입니다.

## Keep these straight

- 입력값이 사라지는 것이 Virtual DOM의 이유는 아닙니다. 교체되는 것은 노드입니다. React의 목적은 선언적 UI이고, Virtual DOM은 구현 방법의 하나입니다.
- 강의의 State History와 "루트에서만 Hook 사용"은 강의용 구조입니다. React의 규칙이 아닙니다. 구현할 때 "React에도 있나요?"를 함께 적습니다.
- "5가지 핵심 케이스"의 목록은 강의 페이지에 없습니다. 글자, 속성, 추가, 삭제, 교체는 에이전트의 해석입니다. 회의에서 확인합니다.
- 입력칸에 글자를 친 뒤에는 `setAttribute("value", x)`로 화면의 글자가 바뀌지 않습니다. Patch는 `.value`에 씁니다.

## Environment

- Vanilla and real React practice code: `week11-12/lab/`. This path is in `.git/info/exclude` of the `krafton-jungle` repository. `week11-12` has no repository of its own.
- From step 4a (his choice 2026-11-07): he types in `mini-react` on the study branch `CJG-study`, which is pushed and never merged as a whole. The agent gives only TS code that passes `npm run typecheck` and `npm run check` in `mini-react`. For a PR, take only code that he can explain into `CJG`.
- Tools: Vite and npm, set up by the agent. Node version from `mini-react/.nvmrc`.
- Real React stays in the lab. It does not enter `mini-react` dependencies.

## Record

한 사이클을 마치면 `../docs/ai-together-mode.md`에 날짜가 있는 관찰로 남깁니다. 틀린 예측 수, 질문 수, 다음 날 아침에도 그 문장을 말할 수 있는지를 적습니다. 규칙으로 올리지 않습니다.
