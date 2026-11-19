# All Code Is Slop (Except Mine) — 시청 보고서

## 1. 발표자, 제목, 행사, 길이

- 발표자: Lauren Tan (닉네임 poteto, 자막에서는 "Potato"). 슬라이드 표기: Principal Engineer, SpaceX. SpaceXSI에서 Grok Bot을 만든다.
- 제목: "All Code Is Slop (Except Mine)". 마지막 슬라이드에는 "all code is slop (except yours)"로 바뀌어 있다.
- 행사: AI Engineer Code Summit (Google DeepMind 후원). YouTube 채널 AI Engineer, 업로드 2026-11-14.
- 길이: 17:31 (발표 본문은 약 0:12–17:10).

## 2. 논지 (3문장)

에이전트 덕분에 누구나 "coding machine"이 될 수 있으니, 이제 엔지니어의 일은 생산량을 크게 늘리면서 코드 품질을 유지하거나 높이는 것이다. 그 방법은 맹목적 신뢰가 아니라 에이전트의 환경(코드베이스, 정적 분석, 검증)에 투자해서 에이전트가 기본값으로 옳은 일을 하게 만드는 것이다. 에이전트를 고칠 때마다 그 교정을 prose 한 줄이 아니라 결정적 검사나 구조 변경으로 바꾸면, 결국 리뷰할 것이 남지 않고 에이전트가 자기 PR을 대부분 직접 머지할 수 있다.

## 3. 층별 예시와 조언

### Codebase
- [2:46] 에이전트는 입력으로 출력을 만들고, 코드베이스가 가장 큰 입력이다.
- [3:20–4:29] 정원 비유: 2024년엔 동료 PR 3개를 리뷰했는데 지금은 약 300개. 제약과 가드레일은 새 코드가 그 주위로 자라는 "콘크리트 기초". 슬라이드: "Organic Architecture", "software engineer is kind of becoming like gardening".
- [4:26] 우회책, 안티패턴, deprecated 코드, 기술 부채는 "확립된 패턴"처럼 보여서 다음 에이전트가 복사한다. 슬라이드 "each copy makes the next copy more likely"(one workaround → the pattern). 조언: 코드베이스를 최대한 깨끗하게 유지해서 에이전트가 좋은 것만 복사하게 하라.
- [4:59] Dune: Grok Bot용 클라이언트 프레임워크, "Electron 앱용 Next.js 비슷한 것". 기술적으로는 흥미롭지 않고, 데스크톱 앱 교훈을 제약과 lint 규칙으로 담은 점이 핵심. 슬라이드: app framework(navigation, rendering, IPC) + one folder per feature + strict import bans + no comments in code.
- [5:30] "nuance가 필요한 것은 slop으로 이어진다." 예: React `useEffect`. 제품 코드에서 금지하고 Dune API 내부 몇 곳에서만 허용. 결과: 문제가 "범주적으로 제거"되어 코드 리뷰에서 다시 잡을 필요가 없다. 슬라이드 부제: "just design better APIs".

### Static analysis
- [6:06–6:52] 디렉터리 구조와 import 금지 (5절 참고). 의존성 그래프 분석기와 lint 규칙으로 강제.
- [7:44–8:16] Cursor의 타이머 사례 (4절 참고).
- [8:49] Grok Bot과 Dune의 lint 규칙은 근본 원인을 고치라고 알려주는 "좋고 아주 도움이 되는 에러 메시지"를 낸다.
- [9:10 슬라이드] "whenever you correct your agent" 계단 그래프: 7월 1일 0개 → 7, 17, 38, 90, 139, 149, 157, 167개(11월 1일경). 아래 문구 "lint against it or categorically eliminate the problem". 숫자의 단위(lint 규칙 수로 보임)는 말로 설명되지 않았다.

### Verification
- [9:40] 코드 리뷰는 이제 "검증 산출물"(동영상, 스크린샷, 다이어그램, formal verification) 보기로 줄었다.
- [9:58] Runtime verification = 에이전트가 직접 코드를 실행하고 사람이 쓰는 디버깅 도구(Chrome DevTools Protocol)를 쓰게 하는 것.
- [10:15] Runtime verification skill 안의 "feature map": 사용자 관점의 기능 사이트맵. 에이전트가 "왼쪽 사이드바의 그거"를 추측하지 않게 하는 공유 어휘. 슬라이드: what features exist → how users reach it → what proves it works.
- [10:35] Skill 안에 custom CLI를 넣어 에이전트가 매번 같은 CLI와 driver를 재사용하게 함 → 토큰 절약. 슬라이드 예: `app aria-click --accessible-name "Settings"`, `app snapshot`, `app screenshot proof.png`, "drive the real app", "agent checks its own work".
- [10:50] Formal verification: TLA+로 여러 기기·플랫폼에 걸친 알림 같은 주요 사용자 흐름을 model checking. Lean으로 자체 virtualization 라이브러리에 깜빡임·떨림이 없음을 증명. 이미 버그를 꽤 찾았지만 "silver bullet은 아니고" 또 하나의 층으로 취급, 아직 실험 중.
- [11:33] UI property-based testing: 라이브러리 Bombadil (슬라이드 github.com/antithesishq/bombadil). UI 버그 몇 개를 찾음.
- [11:51–12:39] Cindy Sridharan 트윗: 6개월 전엔 미묘한 버그 때문에 에이전트를 못 믿었고, 빠진 것은 검증 과정이었다. 지금은 일일 토큰의 70%가 검증. 발표자도 토큰 대부분이 검증에 간다고 말함. 이 기법들은 새롭지 않고, 예전엔 비싸서 못 쓰던 것을 에이전트가 싸게 만들었다 → "testing과 verification의 황금기".
- [12:58] pstack의 `/statechart` skill: 사용자 관점 state machine을 시각화. 영상·스크린샷과 함께 리뷰하기 쉽다.

### Prose
- [2:46] rules, skills, AGENTS.md 등 "판단이 필요한 것". "약간" 얹는 층.
- [3:08] 교정할 때 rules나 AGENTS.md에 한 줄 더하는 대신 결정적 검사로 만들어라. 코드로 있으면 재현성이 높고 더 믿을 수 있다.
- [6:52–7:10] Markdown(문서, 코드 주석, rules, skills)은 에이전트가 옳은 일을 안 한 이유를 적는 장소가 되고, 작은 교정에 과잉 반응해 절대 규칙처럼 취급한다. 슬라이드: "stop agents from writing unsolicited markdown".

### Human review
- [9:21] 충분히 하면 리뷰할 것이 줄고, 결국 "리뷰할 것이 없다"는 걸 깨닫게 되며 에이전트가 PR 대부분을 직접 머지하게 할 수 있다.
- [16:47] 대부분의 제품 코드는 더 이상 깊은 사람 리뷰가 필요 없다.
- 슬라이드 [4:50] "yes, you should read the code sometimes" (말로는 언급 없음).

## 4. 실수를 상위 층 가드로 바꾸는 과정

- 일반 원칙 [8:49–9:21]: "에이전트를 교정할 때마다" (a) 결정적 검사로 바꾸거나 (b) 더 나은 API 설계·아키텍처로 문제를 범주적으로 제거할 방법을 생각한다.
- 순서 [15:11–15:22]: 교정은 먼저 코드베이스 개선으로. lint 규칙으로 새 안티패턴 발생을 막고, 그다음 옛 패턴을 정리한다. 그다음 검증을 튼튼하게.
- 사례 (Cursor 타이머) [7:22–8:49]: 슬라이드 타임라인 — 9월 9일 `// release later, in case it comes back` + `setTimeout(() => release(id), 0)`로 flicker 수정, 에이전트 변명 "it would be a larger change" → 10월 3일 공유 모듈로 복사 → 10월 17일 타이머 183개. 원인은 VS Code의 명령형 스타일과 React 선언형 스타일의 아키텍처 충돌을 타이머로 덮은 것. GC 증가와 jank. 대응(Grok Bot): 주석 99% 금지 + 근본 원인 수정을 요구하는 lint 메시지.
- 주석 금지 근거 [8:16]: 쉽게 낡고, 사람이 안 읽고, 에이전트에게 탈출구를 주고, 강제할 수 없다. 슬라이드 "comments are liabilities": 7월 31일 65,824개 → 현재 1,229개, pstack `/no-comments` 참조.
- prose나 사람 리뷰에서 멈추라는 명시적 판단 기준은 말하지 않았다. prose는 "판단이 필요한 것"이라는 정의 [2:46]와 "약간만" 얹으라는 말뿐이다.
- 자동화 순서 [15:22–15:55]: 내부 루프가 slop을 만들면 자동화는 slop을 더 만들고 토큰만 더 든다. 슬라이드 "don't automate a bad loop / improve your loop before automating": low trust(agent writes slop, human verifies) → high trust(agent writes good code, agent verifies) → "factory"(automated trigger, trust enables scale).

## 5. 디렉터리 구조, 모듈 경계, API 형태

- [6:06] "context through directory structure". Cursor에서 에이전트가 main thread 코드를 renderer thread로 import해 long task와 jank를 만들었다. Grok Bot과 Dune 앱에서는 최상위 디렉터리 `electron-renderer/`와 `electron-main/`을 두고, 둘 사이 import를 의존성 그래프 분석기와 lint로 금지한다.
- 슬라이드만 [6:10–6:55]: renderer 쪽 `features/`, `client/`, `primitives/`; main 쪽 `startup/`, `notifications/`, `update/`; `features/` ↔ main은 "not even types"; 둘 다 `shared/`(shared types)로만 연결. 사이드 프로젝트 tibo.dog의 `src/sim/tick.hot.ts`: 파일 이름이 "runs every tick", "no allocations"를 뜻함. Dune 슬라이드의 "one folder per feature".
- [5:30] API 형태: nuance가 필요한 API(`useEffect`)는 제품 코드에서 금지하고 프레임워크 API 안에 가둔다.

## 6. 에이전트 워크플로, skills, AGENTS.md

- 들어갈 것: 판단이 필요한 것 [2:46]. Runtime verification skill 안의 feature map과 custom CLI [10:15–10:35]. 공유 어휘 역할.
- 들어가면 안 될 것: 결정적 검사로 만들 수 있는 교정 [3:08]. 에이전트가 쓴 정당화와 작은 교정의 과잉 일반화 [6:52].
- pstack(potato stack, github.com/cursor/plugins/tree/main/pstack) 언급: `/statechart`(말로 언급), `/no-comments`, `/create-verification-skill`, `/create-formal-verification-skill`(슬라이드 각주만).
- 외부 루프 [15:55–16:47]: Grok Bot이 connectors, routines, projects로 Cursor cloud agent 수백~수천 개를 조율. 릴리스마다 Cursor project가 앱 전체를 실사용자처럼 fuzz하고, 버그마다 fix PR을 열고 auto-merge. 슬라이드 스레드: "sandcastle" 에이전트의 Linux fuzz 결과(NEW 3 bugs, PRE-EXISTING 47 bugs 등).

## 7. 슬라이드에만 있는 주장 vs 말한 주장

- 슬라이드만: "code is memory"(3:00), "yes, you should read the code sometimes"(4:50), "one folder per feature", "not even types", tibo.dog 예시, 주석 수 65,824→1,229, 교정 계단 그래프 수치, pstack skill 이름 대부분, 릴리스 간격 중앙값 44h→25h→28h, "there is a ceiling… (toying with the idea of a rust rewrite)".
- 숫자 불일치: 말로는 revert율이 "about half a percent"로 낮아졌다 [14:18]. 슬라이드는 6월 0.98% → 7월 0.61% → 8–10월 0.47–0.48%. 팀 PR은 말로 11,000 [13:42], 슬라이드는 10월 10,926. 개인 3,000 PR [0:45] 슬라이드 막대 최대 3,127. 기여자 227명(10월)은 말과 슬라이드 일치.
- 성능 [14:25–15:00]: 말로는 startup, typing, 채팅 열기·전환이 빨라졌다고만 한다. 슬라이드 표에는 cold launch −39% 등 수치와 함께 일부 항목 악화(idle memory +12%, idle cpu +100%, js+css at startup +285%)도 있다. 말로 언급되지 않았다.
- 피라미드 [2:00]: 슬라이드에는 맨 아래 "human review" 층과 "cost" 축이 있다. 말로는 앞의 네 층만 설명하고, human review는 층으로서 따로 설명하지 않았다.

## 8. 인용 (최대 10)

1. [1:08] "the meta of being a software engineer is figuring out how to maintain or even improve the quality of your code while massively increasing your productivity."
2. [1:30] "Not blind trust but investing in your agents environment so you can trust that your agents are going to do the right thing."
3. [3:08] "whenever you're correcting your agent, think about how you can make that a deterministic check instead of adding another line to your rules or your agents.md"
4. [4:30] "it's now likely to be just copied by the next agent since it looks like the established pattern in your codebase."
5. [5:30] "anything that requires nuance to use well often leads to slop."
6. [8:40] "the worst part about comments though is that they're not enforceable."
7. [9:10] "every time we correct our agents, it turns into one of these deterministic checks or we think about how to categorically eliminate that problem"
8. [9:30] "at some point you'll realize there's there's nothing left to review."
9. [12:39] "we are entering a golden age of software testing and verification"
10. [15:30] "if your inner coding loop produces slop, then automating that loop just produces more slop"

## 9. 확인하지 못한 것

- 자막은 YouTube 자동 생성 영어 자막(en-orig)만 있다. 수동 자막은 없다. "Graph Bot", "Growth Bot", "Gulp bot", "Grabot"은 Grok Bot의 오인식으로 보이고, "Dunanaps"는 "Dune apps"로 보인다. 인용은 이 자동 자막 기준이고 타임스탬프는 ±5초 정도 오차가 있을 수 있다.
- 슬라이드는 10초 간격 프레임으로 봤다. 그 사이에만 잠깐 나온 슬라이드나 애니메이션은 놓쳤을 수 있다. 11:33의 Bombadil 시연 영상은 빠르게 지나가서 내용을 읽지 못했다.
- 교정 계단 그래프(9:10)의 y축 단위, statechart 화면(12:50)의 세부 텍스트, Grok Bot 스레드 스크린샷(16:20)의 일부(가려진 부분)는 읽을 수 없거나 설명되지 않았다.
- "human review" 층을 언제 남기는지, prose에서 멈출 기준이 무엇인지는 영상에 없다.
