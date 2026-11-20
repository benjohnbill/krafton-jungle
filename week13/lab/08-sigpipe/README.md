# 08-sigpipe — 손님이 응답 도중에 떠나면

07의 `reuse_server.c`를 복사해, 받은 것을 돌려주는 대신 1초마다 `tick N`을 10번 보내는 서버로 바꾼다. 긴 응답을 보내는 웹서버와 같은 모양이다. 손님이 중간에 끊으면 서버에 무슨 일이 생기는지 보고, 서버가 죽지 않게 막는다.

앞선 lesson: [L3 close와 실패](../teach/lessons/0003-close-and-failure.html) §5.

## 실행할 명령

`week13/lab/`에서 복사한다.

```bash
cp 07-reuseaddr/reuse_server.c 08-sigpipe/tick_server.c
```

### 1단계: 고치기 전

`tick_server.c`에서 세 곳을 바꾼다.

`#define BUFFER_SIZE 1024` 아래에 한 줄을 더한다.

```c
#define TICK_COUNT 10
```

선언 `static void echo(int conn_fd);`를 바꾼다.

```c
static void tick(int conn_fd);
```

`echo` 함수 전체를 이 함수로 바꾼다.

```c
static void tick(int conn_fd)
{
    char buffer[BUFFER_SIZE];

    for (int count = 1; count <= TICK_COUNT; count++) {
        int length = snprintf(buffer, sizeof(buffer), "tick %d\n", count);
        write(conn_fd, buffer, length);
        printf("wrote tick %d\n", count);
        sleep(1);
    }
}
```

`main`의 `echo(conn_fd);`를 `tick(conn_fd);`로 바꾼다. 그리고 빌드한다.

```bash
make 08-sigpipe/tick_server
```

터미널 1: 서버

```bash
./08-sigpipe/tick_server
```

터미널 2: 손님 1. `tick 2`까지 받으면 `Ctrl-C`로 끊는다.

```bash
nc localhost 8080
```

서버가 멈추면 터미널 1에서 종료 코드를 본다. 그다음 터미널 2에서 손님 2를 붙인다.

```bash
echo $?
```

### 2단계: 고친 뒤

`#include <unistd.h>` 위에 한 줄을 더한다.

```c
#include <signal.h>
```

`main`의 첫 줄, `int listen_fd = open_listen_fd();` 앞에 한 줄을 더한다.

```c
    signal(SIGPIPE, SIG_IGN);
```

`tick`의 `write(conn_fd, buffer, length);` 한 줄을 이 덩어리로 바꾼다.

```c
        if (write(conn_fd, buffer, length) < 0) {
            perror("write");
            return;
        }
```

다시 빌드하고 1단계와 같은 실험을 한다. 손님 1을 끊은 뒤 손님 2가 `tick`을 받는지 본다.

## 볼 것

실행 전 예측 (L3 답안에서 옮김, 2026-11-20). 실행 전에 한 번 더 묻고, 실행 뒤 실제를 옆에 적는다.

| # | 예측 | 실제 |
|---|---|---|
| 1 | 손님이 끊은 뒤 서버의 첫 `write`는 문제없고, 그다음 `write`에서 오류를 본다 | |
| 2 | 손님 쪽 커널에 `TIME-WAIT`이 남는다 | |
| 3 | 손님 쪽 커널이 "더 보내지 마"라는 신호를 줄지도 모른다 | |
| 4 | (아직 답 없음) 1단계에서 손님 2는 서비스를 받을까 | |

함께 볼 것:

- 1단계 서버 출력의 마지막 `wrote tick N`. 손님이 끊은 뒤 몇 번 더 썼나.
- 1단계의 `echo $?` 값. L3 §5의 141과 같은가.
- 손님 1을 끊고 몇 초 뒤의 `ss -tan 'sport = :8080 or dport = :8080'`. 그 연결의 줄이 남아 있나.

## 혼자 하는 변경 과제

2단계에서 `signal(SIGPIPE, SIG_IGN);` 한 줄만 지우고, `write` 검사는 그대로 둔다. 실행 전에 예측한다: 손님 1을 끊으면 서버 출력에 `write: Broken pipe`가 찍힐까. 결과를 한 문장으로 쓴다.

## 확인 질문

웹서버에서 이 두 줄(`signal`과 `write` 검사)은 각각 무엇을 막는가. 하나만 있으면 왜 부족한가.
