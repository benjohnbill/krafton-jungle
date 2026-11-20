# 06-echo — 한 번에 한 손님만 상대하는 서버

`echo_server.c`를 직접 친다. 받은 바이트를 그대로 돌려보내는 서버다. HTTP는 없다. syscall 뼈대는 `socket → bind → listen → accept → read/write → close`이고, T4의 웹서버가 이 뼈대를 그대로 물려받는다.

앞선 lesson: [L1 연결 준비와 fd](../teach/lessons/0001-connection-setup-and-fd.html), [L2 수신 버퍼](../teach/lessons/0002-socket-lookup-and-receive-buffer.html).

## 실행할 명령

빌드 (`week13/lab/`에서):

```bash
make 06-echo/echo_server
```

터미널 1: 서버

```bash
./06-echo/echo_server
```

터미널 2: 클라이언트 A. `hi`를 치고 엔터, echo를 확인한 뒤 연결을 그대로 둔다.

```bash
nc localhost 8080
```

터미널 3: 클라이언트 B. A가 붙어 있는 동안 접속해서 `hello`를 치고 엔터.

```bash
nc localhost 8080
```

터미널 4: B가 `hello`를 친 뒤, 그리고 A를 `Ctrl-C`로 끊은 뒤 한 번씩.

```bash
ss -tan 'sport = :8080 or dport = :8080'
```

서버를 끄고 바로 다시 켜면 `bind: Address already in use`가 날 수 있다. 1분쯤 기다리면 된다. 이유는 T3에서 본다.

## 볼 것

실행 전 예측 (L1, L2 답안에서 옮김, 2026-11-20). 실행 전에 한 번 더 묻고, 실행 뒤 실제를 옆에 적는다.

| # | 예측 | 실제 |
|---|---|---|
| 1 | A가 붙어 있어도 B의 `connect`는 끝나는가. 그는 "서버 앱이 스레드를 쓰면 처리할 수 있다"는 쪽으로 생각했다 | |
| 2 | B가 `hello`를 치면 서버 쪽 B 줄의 Recv-Q는 6. 서버 커널에 들어왔지만 아무도 안 읽었다 | |
| 3 | A가 끊으면 B는 그제야 `accept`되고, 다시 치지 않아도 `hello`의 echo를 받는다. 바이트가 버퍼에 남아 있다 | |

함께 볼 것:

- 서버 출력의 `accepted`와 `closed`가 찍히는 순간. B의 `accepted`는 언제 찍히나.
- L1 퀴즈에서 틀린 것: SYN-ACK을 보내는 칸 (서버 커널). 다시 묻지 않는다.

## 혼자 하는 변경 과제

`BACKLOG`를 1로 바꾸고, A가 붙어 있는 동안 클라이언트를 3개 더 붙인다. 실행 전에 예측한다: 몇 번째 클라이언트부터 `connect`가 끝나지 않을까. `ss -tan`의 State 열로 확인하고, L1의 `no_accept.py` 결과와 비교해 한 문장으로 쓴다.

## 내 문장

- 
