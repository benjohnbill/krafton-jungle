# Notes

## 시작

이 workspace에서 `/teach`를 입력하면 첫 세션이 시작된다. 첫 일은 MISSION.md 초안 확인, 그다음 L1 lesson이다. 틀은 2026-11-24 세션에서 정했다 (user said "1, 2, 3번 전부 수용").

## 그가 정한 규칙 (2026-11-24)

- **노트는 지식, lesson은 연습.** 지식 본문은 `rproxy 요구분석` 노트(`week13/notes/rproxy-requirements.html`, 사이트 `study/week13/mini-webserver/rproxy-requirements.html`)의 단계 카드와, 배경 노트 00~03이 맡는다. lesson이 노트가 이미 설명한 개념을 다시 설명하면, 그 문장을 노트 앵커 링크로 바꾼다. 퀴즈는 링크된 카드나 절을 읽어야 풀리게 낸다. 따로 reference 문서를 만들기 전에 노트로 충분한지 먼저 본다.
- **흐름: lesson → 따라치기 → 질문.** lesson의 마지막 절은 따라칠 함수의 파일과 줄이다.
- **lesson 6개, 단계 순서.** 아래 표. lesson 이름은 단계 이름이다 (user said 2026-11-24).
- 용어는 `mini-webserver/GLOSSARY.md`를 따른다. 별도 glossary를 만들지 않는다.

## lesson 한 장의 틀

1. 먼저 읽기: 노트 앵커 링크 2~4개. 설명은 쓰지 않는다.
2. 예측: Scene 결과 하나를 숫자로 예측한다 (답은 `20261124-arena-layers.md`).
3. 퀴즈: 노트 절을 읽어야 풀리는 문제. 보기는 같은 길이로, 정답 위치를 바꾼다.
4. 우리 코드: 따라칠 함수와 읽을 곳의 위치 표만 둔다 (위치, 무엇).
5. 예측의 답: 접힌 칸. 그 아래 다음 lesson 링크와 후속 질문 안내.

답안 칸(`assets/quiz.js`)은 퀴즈 아래에 붙는다. 그가 붙이면 `learning-records/`에 기록한다. lesson은 간결하게 쓴다: 4절에 질문 callout, 읽는 법 문단, 혼자 하는 과제를 쓰지 않고, 답안 복사 안내 절과 주 자료 절을 따로 두지 않는다. 주 자료는 1절 링크가 맡는다 (user said 2026-11-24).

## 커리큘럼

순서는 연결 하나가 지나는 단계 순서다: TCP → ClientHello → TLS → HTTP → Cache → Origin (user said 2026-11-24, grilling 1라운드). 각 lesson은 그 단계의 카드(보이는 신호, 거르는 기준, 구분하는 사용자, 서버 비용, 고려할 점)를 연습한다. 군비 경쟁 이야기는 카드의 "고려할 점"으로 옮겼다. HTTP 단계는 규칙이 몰려서 세 장으로 나눈다.

| lesson | 단계 카드 | 승리 하나 | 예측할 Scene 결과 | 따라칠 코드 |
|---|---|---|---|---|
| L1 TCP, ClientHello: 규칙 표 (완료) | `#s-tcp`, `#s-hello`, `#s-tls` | handshake 전에 서버가 무엇을 볼 수 있고, drop이 왜 싼지 말한다 | `spread` 000=5120 | `connection_decide` (`src/rproxy/connection_verdict.c:24`) |
| L2 ClientHello: 지문 | `#s-hello`, 03 `#m-tls`, `#m-ua` | JA4가 ClientHello의 어느 칸에서 나오고, 왜 라이브러리의 지문인지 말한다 | `disguised` (UA Chrome, JA4 curl) | `ja4_format` (`src/rproxy/ja4.c:35`) |
| L3 HTTP ①: 양 | `#s-http`, 03 `#m-rate` | 59 = 10 + 5 × 10을 token bucket으로 설명한다 | `repeat` 200=59 | `rate_limit_take` (`src/rproxy/rate_limit.c:60`) |
| L4 HTTP ②: 시험과 비용 비대칭 | `#s-http`, `#cost`, 03 `#m-pow`, `#m-tarpit` | "방어 비용 < crawler가 피해 가는 비용"을 Proof of work와 tarpit 실패로 말한다 | `solver` 200=55, `disguised` 때 `human.py` 0 | `pow_is_solved` (`src/rproxy/pow.c:36`), `tarpit_start` (`src/rproxy/event_loop.c:642`) |
| L5 HTTP ③: 신원, 거래, 규칙 순서 | `#s-http`, `#rules`, 03 `#m-honey`, `#m-pay`, `#m-wba` | 착한 bot을 통과시키는 법과 `verdict_decide`의 규칙 8개 순서를 말한다 | `signed` 대 `named`, `trapped` 6860 | `verdict_decide` (`src/rproxy/verdict.c:52`) |
| L6 Cache, Origin: 통과한 요청의 비용 | `#s-cache`, `#s-origin`, `#arena` | cache가 crawler 비용을 줄이지 못하는 이유와 304를 말한다 | `revalidate` 304=55, `repeat` MiB | `cache_find` (`src/rproxy/event_loop.c:996` 호출부) |

줄 번호는 `CJG` commit `a1e0984`(Event loop) 기준이다. lesson을 만들 때 다시 확인한다.

## 주의

- `mini-webserver/`는 Event loop 재작성(SPEC §11 step 13)이 push될 때까지 읽기만 한다. `event_loop.c`의 `tarpit_start`는 `a1e0984`에서 642줄이다. push 전이라 GitHub 링크는 걸 수 없다.
- 알려진 버그: Origin이 query string이 붙은 정적 경로에 404를 준다. lesson 문제에 query string을 쓰지 않는다.
- 사이트 게시는 `../teach/publish/build.py`의 방식을 따른다: 원본 lesson → `publish/` 사본 → 사이트 `study/week13/mini-webserver/lessons/` (노트는 `study/week13/mini-webserver/notes/`, 2026-11-24 user said). 사이트에 올리기 전에 `benjohnbill.github.io/AGENTS.md`의 "Site rules"를 읽는다. `assets/`는 `../teach/assets/`에서 복사했다 (`flow-lanes.js`는 요청 흐름 전용이라 빼고).

## 진행

- 2026-11-24: Mission 확정. 그는 성공 기준이 "조금 빡세다"고 했다 (user said). 다섯 lesson이 끝난 뒤 기준을 다시 본다.
- 2026-11-24: L1 `lessons/0001-map-and-cost.html` 작성. 코드 위치는 `CJG` `a1e0984` 기준 (Event loop 재작성 포함, push 전).
- 2026-11-24: L1 따라치기 끝 (`type/connection_verdict.c`, 기록 0003). 함수 포인터에서 막혔고, 메모리 그림 한 장과 질문 하나로 풀렸다.
- 2026-11-24: L2 `lessons/0002-clienthello-fingerprint.html` 작성. 코드 위치는 `CJG` `48bf7a0` 기준. 예측 답은 `20261124-arena-disguised-v3.md`. 따라칠 것은 `ja4_format`(35-58줄)뿐이고, helper는 뼈대 파일에 미리 넣는다.
- 노트 링크는 lesson 안에서 해당 절의 앵커로 건다: "먼저 읽기" 표와 퀴즈 해설 끝 (user said "노트의 해당 부분을 내부적으로 링크 걸어서").
- 예측 문제에 쓰는 낱말(Scene, preset, `000` 등)은 그 절 안에서 먼저 정의한다. L1에서 정의 없이 내서 그가 막혔다 (2026-11-24).
- 낱말 "경기장"은 쓰지 않는다. `bench/arena/`의 한 번 실행은 GLOSSARY 용어 Scene으로 부른다 (user said 2026-11-24: "경기장이라는 표현 제발 쓰지 말아주라").
