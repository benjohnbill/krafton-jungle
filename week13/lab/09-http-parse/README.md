# 09-http-parse — 요청이 어디서 끝나는지 알아보는 서버

08의 `tick_server.c`를 복사해서 HTTP 요청을 읽는 서버로 바꾼다. 1단계에서는 빈 줄이 나올 때까지 읽고 고정 응답을 보낸다. 2단계에서는 요청 줄을 나누고, 깨진 요청에 400이나 405를 돌려준다. T1의 03(telnet)과 04(nc)에서 nginx와 브라우저로 본 사실을 이번에는 내 서버로 확인한다.

## 실행할 명령

`week13/lab/`에서 복사한다.

```bash
cp 08-sigpipe/tick_server.c 09-http-parse/parse_server.c
```

### 1단계: 빈 줄까지 읽기

`#include <stdlib.h>` 아래에 한 줄을 더한다.

```c
#include <string.h>
```

`#define`을 고친다. `BUFFER_SIZE`는 8192로 바꾸고, `TICK_COUNT` 줄은 지운다.

```c
#define BUFFER_SIZE 8192
```

선언 `static void tick(int conn_fd);`를 이 네 줄로 바꾼다.

```c
static void serve(int conn_fd);
static ssize_t read_request(int conn_fd, char *buffer, size_t size);
static char *find_header_end(char *buffer);
static void send_response(int conn_fd, int status, const char *reason,
                          const char *body);
```

`tick` 함수 전체를 아래 네 함수로 바꾼다.

`serve`: 요청 하나를 읽고 응답 하나를 보낸다.

```c
static void serve(int conn_fd)
{
    char buffer[BUFFER_SIZE];
    ssize_t length = read_request(conn_fd, buffer, sizeof(buffer));
    if (length == 0) {
        return;
    }
    if (length < 0) {
        send_response(conn_fd, 400, "Bad Request", "header too long\n");
        return;
    }
    printf("%s", buffer);
    send_response(conn_fd, 200, "OK", "hello\n");
}
```

`read_request`: 빈 줄이 보일 때까지 `read`를 되풀이해서 `buffer` 뒤에 이어 붙인다.

```c
static ssize_t read_request(int conn_fd, char *buffer, size_t size)
{
    size_t used = 0;

    while (used < size - 1) {
        ssize_t length = read(conn_fd, buffer + used, size - 1 - used);
        if (length <= 0) {
            return 0;
        }
        printf("read %zd bytes\n", length);
        used += length;
        buffer[used] = '\0';
        if (find_header_end(buffer) != NULL) {
            return used;
        }
    }
    return -1;
}
```

`find_header_end`: 빈 줄을 찾는다. 빈 줄은 줄 끝 바로 뒤에 또 줄 끝이 오는 곳이다.

```c
static char *find_header_end(char *buffer)
{
    for (char *p = strchr(buffer, '\n'); p != NULL; p = strchr(p + 1, '\n')) {
        if (p[1] == '\n') {
            return p + 2;
        }
        if (p[1] == '\r' && p[2] == '\n') {
            return p + 3;
        }
    }
    return NULL;
}
```

`send_response`: 상태 줄, 헤더, 빈 줄, body 순서로 보낸다.

```c
static void send_response(int conn_fd, int status, const char *reason,
                          const char *body)
{
    char header[BUFFER_SIZE];
    int length = snprintf(header, sizeof(header),
                          "HTTP/1.1 %d %s\r\n"
                          "Content-Type: text/plain\r\n"
                          "Content-Length: %zu\r\n"
                          "Connection: close\r\n"
                          "%s"
                          "\r\n",
                          status, reason, strlen(body),
                          status == 405 ? "Allow: GET\r\n" : "");

    if (write(conn_fd, header, length) < 0 ||
        write(conn_fd, body, strlen(body)) < 0) {
        perror("write");
        return;
    }
    printf("-> %d %s\n", status, reason);
}
```

`main`의 `tick(conn_fd);`를 `serve(conn_fd);`로 바꾸고 빌드한다.

```bash
make 09-http-parse/parse_server
```

터미널 1: 서버

```bash
./09-http-parse/parse_server
```

터미널 2: telnet으로 한 줄씩 친다. 줄마다 터미널 1을 본다. 마지막에는 아무것도 치지 않고 Enter만 친다.

```bash
telnet localhost 8080
```

```text
GET /hello HTTP/1.1
Host: localhost

```

그다음 curl과 브라우저(`http://localhost:8080/abc`)로 한 번씩 요청한다.

```bash
curl -v localhost:8080/hello
```

### 2단계: 요청 줄 나누기

`#include <signal.h>` 아래에 한 줄을 더한다.

```c
#include <stdbool.h>
```

`#define` 블록 아래에 구조체를 더한다.

```c
struct request {
    char *method;
    char *target;
    char *version;
};
```

선언 목록 끝에 한 줄을 더한다.

```c
static bool parse_request_line(char *buffer, struct request *request);
```

`find_header_end` 아래에 함수를 더한다. 첫 줄의 공백 두 개를 `'\0'`으로 바꿔서, 문자열 하나를 셋으로 자른다.

```c
static bool parse_request_line(char *buffer, struct request *request)
{
    char *line_end = strchr(buffer, '\n');
    *line_end = '\0';
    if (line_end > buffer && line_end[-1] == '\r') {
        line_end[-1] = '\0';
    }

    char *first_space = strchr(buffer, ' ');
    if (first_space == NULL) {
        return false;
    }
    char *second_space = strchr(first_space + 1, ' ');
    if (second_space == NULL) {
        return false;
    }
    *first_space = '\0';
    *second_space = '\0';

    request->method = buffer;
    request->target = first_space + 1;
    request->version = second_space + 1;

    if (request->method[0] == '\0' || request->target[0] == '\0') {
        return false;
    }
    return strcmp(request->version, "HTTP/1.0") == 0 ||
           strcmp(request->version, "HTTP/1.1") == 0;
}
```

`serve`의 마지막 줄 `send_response(conn_fd, 200, "OK", "hello\n");`를 이 덩어리로 바꾼다.

```c
    struct request request;
    if (!parse_request_line(buffer, &request)) {
        send_response(conn_fd, 400, "Bad Request", "bad request line\n");
        return;
    }
    if (strcmp(request.method, "GET") != 0) {
        send_response(conn_fd, 405, "Method Not Allowed", "GET only\n");
        return;
    }

    char body[BUFFER_SIZE];
    snprintf(body, sizeof(body), "method: %s\ntarget: %s\nversion: %s\n",
             request.method, request.target, request.version);
    send_response(conn_fd, 200, "OK", body);
```

다시 빌드하고 서버를 띄운 뒤, 터미널 2에서 하나씩 보낸다.

```bash
printf 'GET /hello HTTP/1.1\r\nHost: x\r\n\r\n' | nc localhost 8080
printf ' GET / HTTP/1.1\r\n\r\n' | nc localhost 8080
printf 'GET / HTTP1.1\r\n\r\n' | nc localhost 8080
printf 'GOT / HTTP/1.1\r\n\r\n' | nc localhost 8080
printf 'GET / HTTP/1.1\nHost: x\n\n' | nc localhost 8080
```

## 볼 것

실행 전 예측. 단계마다 실행 전에 묻고, 실행 뒤 실제를 옆에 적는다. 4번까지는 T1 03, 04에서 nginx와 브라우저로 본 사실이 근거다.

| # | 예측 | 실제 |
|---|---|---|
| 1 | telnet에서 요청 줄만 치고 Enter를 치면 응답이 올까. 예측 (2026-11-21): 안 온다, Host를 안 쳤으니까 | 응답은 안 왔다. 그런데 `Host: localhost`(17 bytes)를 치고 `a`, `s`, `d` 같은 줄(3 bytes씩)을 여섯 개 더 쳐도 안 왔다. Enter만 친 순간 `-> 200 OK`, `closed` |
| 2 | 요청 줄, Host 줄, 빈 줄을 따로 치면 `read N bytes`가 몇 번 찍힐까. 예측 (2026-11-21): 칠 때마다 찍혀서 3번 | 맞다. Enter마다 `read`가 한 번 돌아왔다: 21 (요청 줄 19 + `\r\n`), 17 (Host 줄), 줄을 더 칠 때마다 3 |
| 3 | 2단계: 앞 공백, `HTTP1.1`, `GOT`에 각각 몇 번이 올까 | |
| 4 | 2단계: `\n`만 쓴 요청에 이 서버는 몇 번을 돌려줄까 | |
| 5 | 브라우저로 한 번 열면 서버에 요청이 몇 개 올까. 예측 (2026-11-21): 모름. 상식으로는 1개, 아니면 0개? | 2개. `GET /abc` (698 bytes) 다음에 브라우저가 스스로 `GET /favicon.ico` (598 bytes, 탭 아이콘)를 보냈다. 둘 다 `read` 한 번, 둘 다 `Connection: keep-alive`를 달았지만 이 서버는 응답 뒤 닫는다 |

함께 볼 것:

- 1단계에서 curl의 `read N bytes`는 몇 번인가. telnet과 왜 다른가.
  결과 (2026-11-21): curl은 83 bytes를 `read` 한 번에 받았다. curl은 요청 전체를 `write` 한 번으로 보내고, telnet은 Enter마다 그 줄을 보낸다. `read`는 그때까지 도착한 만큼만 꺼낸다.
- 브라우저 요청의 헤더 줄 수. T1 04에서 nc로 본 것과 같은가.
- 이 서버는 GET이 아닌 메서드에 모두 405를 준다. RFC 9110은 서버가 아예 모르는 메서드(`GOT`)에는 501, 알지만 허용하지 않는 메서드(`POST`)에는 405를 쓰라고 한다. T1에서 nginx는 `GOT`에 405를 줬다.

## 혼자 하는 변경 과제

HTTP/1.1 요청에 `Host` 헤더가 없으면 400을 돌려주게 바꾼다. HTTP/1.0 요청은 `Host`가 없어도 통과한다. 아래 두 요청으로 확인한다.

```bash
printf 'GET / HTTP/1.1\r\n\r\n' | nc localhost 8080
printf 'GET / HTTP/1.0\r\n\r\n' | nc localhost 8080
```

## 확인 질문

서버는 요청이 어디서 끝나는지 어떻게 알까. 그리고 왜 `read`를 한 번만 부르지 않고 되풀이할까.
