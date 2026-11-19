# 02-curl — HTTP 요청과 응답의 모양

## 실행할 명령

```bash
curl -sv http://example.com/ -o /dev/null 2>&1 | bat -l http
curl -sv http://example.com/nothing -o /dev/null 2>&1 | bat -l http
curl -sv http://localhost/ -o /dev/null 2>&1 | bat -l http
curl -sI http://localhost/ | bat -l http
```

`-v`의 상세 출력은 stderr로 나온다. 그래서 `2>&1`로 stdout에 합쳐서 `bat`에 보낸다.

`localhost`에는 nginx가 이미 80번 포트에서 돌고 있다(`ss -tln`으로 확인). 진짜 웹 서버를 내 컴퓨터에서 보는 셈이다.

## 볼 것

- `*`로 시작하는 줄: 어느 IP의 몇 번 포트에 연결했나. 이 연결은 HTTP를 보내기 전에 생긴다.
- `>`로 시작하는 줄: 내가 보낸 요청. 첫 줄의 세 칸(메서드, 경로, 버전)과 그 아래 헤더들.
- `<`로 시작하는 줄: 받은 응답. 첫 줄의 상태 코드, `Content-Type`, `Content-Length`.
- 헤더가 끝나는 자리는 어떻게 표시되나(빈 줄).
- `/nothing`의 상태 코드와 `Content-Length`.

## 혼자 하는 변경 과제

`Host` 헤더를 바꿔서 보낸다.

```bash
curl -sv -H 'Host: wrong.example' http://localhost/ -o /dev/null 2>&1 | bat -l http
```

실행 전에 예측한다: 연결하는 IP는 바뀔까, 응답은 바뀔까. 그다음 `example.com`에도 같은 일을 해 보고 nginx와 비교한다. `Host` 헤더가 왜 필요한지 한 문장으로 쓴다.

## 내 문장

- 
