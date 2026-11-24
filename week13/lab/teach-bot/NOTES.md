# Notes

## 시작

이 workspace에서 `/teach`를 입력하면 첫 세션이 시작된다. 첫 일은 MISSION.md 초안 확인, 그다음 L1 lesson이다. 틀은 2026-11-24 세션에서 정했다 (user said "1, 2, 3번 전부 수용").

## 그가 정한 규칙 (2026-11-24)

- **노트는 지식, lesson은 연습.** 지식 본문은 crawler 노트 00~04가 맡는다. lesson이 노트가 이미 설명한 개념을 다시 설명하면, 그 문장을 노트 앵커 링크로 바꾼다. 퀴즈는 링크된 절을 읽어야 풀리게 낸다. 그래야 노트도 읽힌다. 노트 00~04는 이 workspace의 reference 역할도 한다. 따로 reference 문서를 만들기 전에 노트로 충분한지 먼저 본다.
- **흐름: lesson → 따라치기 → 질문.** lesson의 마지막 절은 따라칠 함수의 파일과 줄이다.
- **lesson 5개.** 아래 표.
- 용어는 `mini-webserver/GLOSSARY.md`를 따른다. 별도 glossary를 만들지 않는다.

## lesson 한 장의 틀

1. 먼저 읽기: 노트 앵커 링크 2~4개. 설명은 쓰지 않는다.
2. 예측: arena 결과 하나를 숫자로 예측한다 (답은 `20261124-arena-layers.md`).
3. 퀴즈: 노트 절을 읽어야 풀리는 문제. 보기는 같은 길이로, 정답 위치를 바꾼다.
4. 우리 코드: 따라칠 함수의 위치와, 그 함수가 답하는 질문 한 줄 (SPEC §11 "Code the owner types").
5. 답안 복사 블록 (`assets/quiz.js`). 그가 붙이면 `learning-records/`에 기록한다.
6. 후속 질문은 agent에게 하라는 안내.

## 커리큘럼

순서는 군비 경쟁 순서다. lesson마다 "crawler는 어떻게 피해 가나"의 답이 다음 lesson이 생긴 이유가 된다. 노트 02 `#rounds`가 같은 순서다.

| lesson | 승리 하나 | 먼저 읽기 | 예측할 arena 결과 | 따라칠 코드 |
|---|---|---|---|---|
| L1 지도와 비용 | handshake 전에 서버가 무엇을 볼 수 있고, drop이 왜 싼지 말한다 | 00 `#layers`, 01 `#paths`, 02 `#rounds`, 04 `#flow` | `spread`의 000 (drop) 수 | `connection_decide` (`src/rproxy/connection_verdict.c:24`) |
| L2 신원 묻기 | User-Agent는 거짓말할 수 있고 JA4는 어렵다는 것을 `disguised`로 말한다 | 03 `#m-robots`, `#m-ua`, `#m-tls`, `#m-ip`, 04 `#map` | `named` 402, `disguised`, `polite` 10 | `ja4_format` (`src/rproxy/ja4.c:35`) |
| L3 양 제한하기 | 59 = 10 + 5 × 10을 token bucket으로 설명하고, Honeypot이 Block table로 이어지는 길을 말한다 | 03 `#m-rate`, `#m-honey`, 04 `#rules` | `repeat` 59, `trapped` 9와 6860 | `rate_limit_take` (`src/rproxy/rate_limit.c:60`) |
| L4 시험과 비용 비대칭 | "방어는 서버가 crawler보다 싸게 치러야 한다"를 tarpit 실패로 말한다 | 03 `#m-pow`, `#m-tarpit`, 04 `#cost` | `solver` 200=55, `disguised` 때 `human.py` 0 | `pow_is_solved` (`src/rproxy/pow.c:36`), `tarpit_start` (`src/rproxy/event_loop.c:624`) |
| L5 거래와 규칙 순서 | 착한 bot을 통과시키는 법과, `verdict_decide`의 규칙 8개 순서를 말한다 | 03 `#l0`, `#m-304`, `#m-pay`, `#m-wba`, 04 `#rules`, `#arena` | `signed` 대 `named`, `revalidate` 304=55 | `verdict_decide` (`src/rproxy/verdict.c:52`) |

줄 번호는 `CJG`의 2026-11-24 작업 트리 기준이다. lesson을 만들 때 다시 확인한다.

## 주의

- `mini-webserver/`는 Event loop 재작성(SPEC §11 step 13)이 push될 때까지 읽기만 한다. `event_loop.c`의 `tarpit_start`는 그 작업 안에 있어서, L4의 코드 위치는 push 뒤에 확정한다.
- 알려진 버그: Origin이 query string이 붙은 정적 경로에 404를 준다. lesson 문제에 query string을 쓰지 않는다.
- 사이트 게시는 `../teach/publish/build.py`의 방식을 따른다: 원본 lesson → `publish/` 사본 → 사이트 `study/week13/mini-webserver/lessons/` (노트는 `study/week13/mini-webserver/notes/`, 2026-11-24 user said). 사이트에 올리기 전에 `benjohnbill.github.io/AGENTS.md`의 "Site rules"를 읽는다. `assets/`는 `../teach/assets/`에서 복사했다 (`flow-lanes.js`는 요청 흐름 전용이라 빼고).

## 진행

- 2026-11-24: Mission 확정. 그는 성공 기준이 "조금 빡세다"고 했다 (user said). 다섯 lesson이 끝난 뒤 기준을 다시 본다.
- 2026-11-24: L1 `lessons/0001-map-and-cost.html` 작성. 코드 위치는 `CJG` `a1e0984` 기준 (Event loop 재작성 포함, push 전).
- 노트 링크는 lesson 안에서 해당 절의 앵커로 건다: "먼저 읽기" 표와 퀴즈 해설 끝 (user said "노트의 해당 부분을 내부적으로 링크 걸어서").
