# rproxy 방어 layer Resources

## Knowledge

### 우리 자료 (lesson이 먼저 링크하는 곳)

- [노트 00: crawler 트래픽과 서버의 방어](https://benjohnbill.github.io/study/week13/mini-webserver/notes/00-overview.html)
  layer 그림과 출처 등급. Use for: L1의 전체 지도 (`#layers`).
- [노트 01: crawler 트래픽의 비용](https://benjohnbill.github.io/study/week13/mini-webserver/notes/01-cost.html)
  사람의 요청과 crawler의 요청 비교, 운영자들의 청구서. Use for: L1의 "왜 막나" (`#paths`). 나머지 절은 배경 자료다.
- [노트 02: crawler 방어와 우회의 역사](https://benjohnbill.github.io/study/week13/mini-webserver/notes/02-history.html)
  방어와 우회의 11 라운드. Use for: L1의 군비 경쟁 순서 (`#rounds`).
- [노트 03: crawler 방어 layer와 우회 방식](https://benjohnbill.github.io/study/week13/mini-webserver/notes/03-layers.html)
  layer 0~5와 방법마다 우회 방식. Use for: L2~L5의 지식 본문 (`#m-*` 앵커).
- [rproxy 요구분석: 단계마다 무엇을 보고 누구를 거르나](https://benjohnbill.github.io/study/week13/mini-webserver/rproxy-requirements.html)
  목표, 사용자 셋, 단계 카드 ①~⑥, Not-Goal, Scene, 대가와 한계. 2026-11-24에 노트 04를 이 형태로 다시 썼다. Use for: 모든 lesson의 지식 본문과 "우리 코드" 쪽 (`#s-*` 카드 앵커).
- `mini-webserver/docs/spec-cjg.md` §11, "Defaults taken from practice"
  generator가 고른 값마다 출처(nginx, fail2ban, Cloudflare, Anubis, RFC). Use for: 퀴즈의 "왜 이 값인가".
- `mini-webserver/docs/measurements/20261124-arena-layers.md`
  `layers` preset에서 Crawler script 10개의 결과. Use for: 모든 lesson의 예측 문제와 정답.
- `mini-webserver/docs/adr/reverse-proxy-runs-one-event-loop-per-core.md`
  tarpit 실패 뒤 Event loop로 바꾼 결정. Use for: L4.

### 1차 출처 (외부)

- [nginx `ngx_http_access_module`](https://nginx.org/en/docs/http/ngx_http_access_module.html)
  "첫 매치가 이긴다" 규칙 순서. Use for: L1 `connection_decide`, L5 `verdict_decide`.
- [nginx `ngx_http_limit_req_module`](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html)
  rate와 burst, 표가 찼을 때의 처리. Use for: L3 token bucket.
- [FoxIO JA4](https://github.com/FoxIO-LLC/ja4)
  JA4 규칙(`technical_details/JA4.md`). Use for: L2 `ja4_format`.
- [Cloudflare: JA4 signals](https://blog.cloudflare.com/ja4-signals/)
  실제 bot 관리에서 JA4를 쓰는 법. Use for: L2 User-Agent 대 JA4.
- [RFC 9309: Robots Exclusion Protocol](https://datatracker.ietf.org/doc/rfc9309/)
  `robots.txt` 규칙과 경로 접두사 매치. Use for: L2 부탁하기, L3 Honeypot.
- [fail2ban](https://github.com/fail2ban/fail2ban)
  `jail.conf`의 `maxretry`, `findtime`, `bantime`. Use for: L3 scanner 규칙과 Block table.
- [Xe Iaso: Anubis](https://xeiaso.net/blog/2025/anubis/)
  Proof of work를 쓰는 이유와 난이도. Use for: L4.
- [RFC 6585 §4: 429 Too Many Requests](https://datatracker.ietf.org/doc/rfc6585/)
  slow(429)와 Retry-After. Use for: L3.
- [Cloudflare: Introducing pay per crawl](https://blog.cloudflare.com/introducing-pay-per-crawl/)
  402와 `crawler-price`. Use for: L5.
- [Cloudflare: Web Bot Auth](https://blog.cloudflare.com/web-bot-auth/)
  bot이 서명으로 자기 이름을 증명하는 구조. Use for: L5.
- [RFC 9421: HTTP Message Signatures](https://datatracker.ietf.org/doc/rfc9421/)
  서명 형식. Use for: L5에서 그가 물을 때만.

## Wisdom (Communities)

- 크래프톤 정글 week13 팀. Use for: 각 layer 결정을 서로 설명하고 검증.

## Gaps

- bot 방어를 다루는 외부 커뮤니티는 아직 정하지 않았다. 그가 원할 때 찾는다.
