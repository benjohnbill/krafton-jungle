# Mission: rproxy의 방어 layer를 내 말로 설명하기

> 확정 (2026-11-24, user said "일단, 확인했어"). 초안은 agent가 kickoff note와 세션에서 썼다. 그는 성공 기준이 "조금 빡세다"고 했다.

## Why
`mini-webserver`의 `rproxy` 방어 layer(SPEC §11 v2, step 7~13)는 generator가 만들었다. 코스는 "AI가 작성한 코드를 완벽히 내 것으로 소화해 그 원리를 설명할 수 있어야 합니다"라고 한다. PR의 핵심 결정 한 문단과 발표에서 각 layer를 내 말로 설명하려면, 각 layer의 결정을 우리 코드와 arena 숫자로 말할 수 있어야 한다.

## Success looks like
- 연결 하나의 길(ClientHello → Connection Verdict → TLS handshake → Request Verdict → cache → Origin)에서 각 단계가 보는 신호와 서버가 쓰는 비용을 말한다.
- layer마다 네 질문에 답한다: crawler는 무엇을 하나, 서버는 어떤 신호를 보나, 양쪽은 얼마를 쓰나, crawler는 어떻게 피해 가나.
- `20261124-arena-layers.md` 결과 표의 어느 행이든 그 숫자가 왜 나왔는지 말한다 (예: 59 = 10 + 5 × 10).
- row 1~4 함수(`ja4_format`, `rate_limit_take`, `verdict_decide`, `connection_decide`)를 따라친 뒤, 규칙 순서를 왜 그렇게 정했는지 말한다.
- tarpit이 `human.py`를 굶긴 이유와, Event loop의 timer가 그 비용을 어떻게 없애는지 말한다.

## Constraints
- 지식은 crawler 노트 00~04가 맡는다. lesson은 노트를 다시 설명하지 않고 링크한다. lesson이 맡는 것은 예측, 퀴즈, 코드 위치다.
- 흐름: lesson → 그 코드 따라치기 → 질문.
- lesson은 5개 (NOTES.md의 표).
- 한국어 본문. 용어는 `mini-webserver/GLOSSARY.md`가 쓰는 대로 쓴다 (Verdict, Block table, Crawler script …).

## Out of scope
- CAPTCHA, reverse DNS: SPEC §11 v2가 뺐다.
- TLS 암호 내부, Ed25519와 RFC 9421 서명 직렬화, distinct target의 linear counting 수학: 원리 한 줄만. 그가 물으면 답한다.
- 노트 01의 비용 통계와 02의 연표 63개 항목: 배경 자료다. lesson의 퀴즈 대상이 아니다.
