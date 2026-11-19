# week13 lab — 직접 해 보는 웹 서버 기초

CSAPP 11장을 읽는 대신, 명령과 작은 C 코드로 직접 겪어 본다. 규칙은 `CLAUDE.md`, 질문은 `QUESTIONS.md`.

## Tracks

| Track | Probe | 겪어 볼 것 | 출처 |
|---|---|---|---|
| T1 CLI | `01-dns` | 이름 → IP | 11.3 |
| | `02-curl` | HTTP 요청·응답의 모양 | 11.5 |
| | `03-telnet-get` | HTTP는 손으로 칠 수 있는 글자 | 11.5 |
| | `04-browser-nc` | 브라우저가 보내는 날것의 요청, 손으로 쓴 응답 | 11.5 |
| | `05-strace` | socket → bind → listen → accept | 11.4 |
| T2 socket C | `06-echo` … | echo 서버 따라치기, 두 번째 클라이언트가 멈춤 | 11.4 |
| T3 TCP | … | SO_REUSEADDR, TIME_WAIT, handshake, SIGPIPE | 책 밖, 8장 |
| T4 HTTP | … | 정적 GET, MIME, 404, POST, keep-alive, CGI | 11.5–11.6, RFC 7230 |
| T5 concurrency | … | fork, pthread, epoll을 wrk로 비교 | 12장 |
| T6 proxy | … | nginx Reverse Proxy, socat 중계, C Forward Proxy | 1309 |

T2부터의 probe는 T1을 끝낸 뒤 만든다.

## Build

```bash
make 06-echo/echo_server
```
