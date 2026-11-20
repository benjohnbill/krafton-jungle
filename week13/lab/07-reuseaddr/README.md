# 07-reuseaddr — 서버를 끄고 바로 다시 켜기

06의 `echo_server.c`에 `SO_REUSEADDR` 한 덩어리를 더한다. 06에서 만난 `bind: Address already in use`를 없애는 probe다. 웹서버는 고치고 다시 켜는 일이 잦아서, 실제 서버는 거의 모두 이 옵션을 켠다.

앞선 lesson: [L3 close와 실패](../teach/lessons/0003-close-and-failure.html) §2, §3.

## 실행할 명령

준비: 06의 서버(BACKLOG 1로 띄운 것)가 아직 8080에서 돌고 있으면 먼저 끈다. 그다음 06 코드를 복사한다 (`week13/lab/`에서).

```bash
cp 06-echo/echo_server.c 07-reuseaddr/reuse_server.c
```

`reuse_server.c`의 `open_listen_fd`에서, `socket` 검사 바로 다음이자 `bind` 앞에 이 덩어리를 직접 친다.

```c
    int reuse = 1;
    if (setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse)) < 0) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
```

빌드:

```bash
make 07-reuseaddr/reuse_server
```

터미널 1: 서버

```bash
./07-reuseaddr/reuse_server
```

터미널 2: 손님. `hi`로 echo를 확인하고 그대로 둔다.

```bash
nc localhost 8080
```

터미널 1에서 서버를 `Ctrl-C`로 끄고, **바로** 다시 켠다. 그리고 터미널 3에서:

```bash
ss -tan 'sport = :8080 or dport = :8080'
```

마지막으로 터미널 2의 `nc`를 끝내고 새 손님을 붙여 `hi`가 돌아오는지 본다.

## 볼 것

실행 전 예측 (L3 답안에서 옮김, 2026-11-20). 실행 전에 한 번 더 묻고, 실행 뒤 실제를 옆에 적는다.

| # | 예측 | 실제 |
|---|---|---|
| 1 | 옵션을 넣은 서버는 손님이 붙은 채로 끄고 바로 켜도 `bind`에 성공한다 | |
| 2 | 새 서버가 `TIME-WAIT` 소켓에서 옛 연결을 다시 가져온다 | |

함께 볼 것:

- 다시 켠 뒤 `ss`에 옛 연결의 줄이 남아 있나. 새 LISTEN 줄과 함께 보이나.
- 새 손님의 클라 포트는 옛 손님의 포트와 같은가. L3 뒤에 나눈 질문("그럼 `TIME-WAIT`이 하던 두 일, 옛 바이트 버리기와 대답 다시 하기는 어떻게 되나")의 답이 여기 있다.

## 혼자 하는 변경 과제

`setsockopt` 덩어리를 `bind` **뒤로** 옮기고 같은 실험을 한다. 실행 전에 예측한다: 바로 다시 켠 서버는 어느 줄에서 멈출까. 결과를 한 문장으로 쓴다.

## 확인 질문

`SO_REUSEADDR`는 커널에게 정확히 무엇을 허락하는가. 옛 연결을 없애는가, 아니면 다른 무엇인가.
