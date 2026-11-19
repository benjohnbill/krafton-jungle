# 05-strace — 서버가 커널에 부탁하는 순서

## 실행할 명령

터미널 1:

```bash
strace -f -e trace=network nc -l 8080
```

터미널 2:

```bash
ss -tlnp | grep 8080
nc localhost 8080
```

터미널 2에서 글자를 몇 줄 치고, `Ctrl-C`로 끝낸다.

그다음 클라이언트 쪽을 본다.

```bash
strace -e trace=network curl -s http://example.com/ -o /dev/null
```

## 볼 것

- 서버(터미널 1): `socket`, `setsockopt`, `bind`, `listen`, `accept4`가 어떤 순서로 나오나. 터미널 2가 접속하기 전에 어디서 멈춰 있나.
- 각 호출이 돌려준 숫자. `socket`이 돌려준 숫자와 `accept4`가 돌려준 숫자는 같은가. 숫자가 두 개 필요한 이유는 무엇일까.
- `ss` 출력의 `LISTEN` 상태는 위 호출 중 어느 것 다음부터 생기나.
- 클라이언트(`curl`): `connect` 앞에 UDP 53번 포트로 무엇을 주고받나. 01의 DNS와 연결된다.

## 혼자 하는 변경 과제

`strace`를 켠 서버를 그대로 둔 채, 터미널 3에서 한 번 더 띄운다.

```bash
strace -e trace=network nc -l 8080
```

실행 전에 예측한다: 어느 호출이 실패하고, 에러 이름은 무엇일까. 그다음 실행해서 확인하고, 그 에러가 왜 필요한지 한 문장으로 쓴다.

## 내 문장

- 
