# 10-client-hello — TLS가 시작되기 전에 손님을 본다

TLS 연결의 첫 메시지인 ClientHello는 아직 암호화되지 않은 평문이다. `rproxy`는 OpenSSL에 소켓을 넘기기 전에 이 바이트를 `recv(..., MSG_PEEK)`로 엿보고, 거기서 JA4를 만든다. 이 probe는 그 "엿보기"만 떼어 낸 서버다. 인증서도 OpenSSL도 없다. ClientHello를 읽어 필드를 찍고, 연결을 닫는다.

관련 코드: `../mini-webserver/src/rproxy/client_hello.c` (같은 일을 테스트와 함께 하는 parser), `main.c`의 `hello_peek`.

## 실행할 명령

`week13/lab/`에서 빌드하고 서버를 띄운다.

```bash
make 10-client-hello/peek_server && ./10-client-hello/peek_server
```

다른 터미널에서 손님을 바꿔 가며 접속한다. 서버가 handshake를 이어가지 않으므로 curl은 실패하는 게 정상이다.

```bash
curl -k https://localhost:18444/
curl -k https://127.0.0.1:18444/
curl -k --http1.1 https://localhost:18444/
openssl s_client -connect 127.0.0.1:18444 -servername example.com -alpn h2,http/1.1 </dev/null
printf 'GET / HTTP/1.1\r\n\r\n' | nc 127.0.0.1 18444
```

Windows 브라우저로 `https://localhost:18444/`도 열어 본다 (WSL이 localhost를 넘겨 주는 경우).

## 볼 것

- **`localhost`와 `127.0.0.1`.** 같은 curl인데 `server_name` 줄이 한쪽에만 있다. curl은 IP 주소에는 SNI를 보내지 않는다. JA4의 네 번째 글자 `d`/`i`가 이 차이다.
- **`--http1.1`.** ALPN의 첫 이름이 `h2`에서 `http/1.1`로 바뀐다. JA4의 ALPN 두 글자 `h2`/`h1`이 이 차이다.
- **curl과 `openssl s_client`.** 둘 다 OpenSSL 3.5.5를 쓴다. cipher 목록과 extension 순서가 같은지 본다. 같다면 둘의 JA4도 거의 같다 — "TLS 라이브러리가 같으면 지문이 같다"는 GLOSSARY의 JA4 정의 그대로다.
- **브라우저.** `GREASE` 표시가 cipher와 extension에 섞여 나온다. 브라우저는 매번 다른 GREASE 값을 넣는다. JA4가 GREASE를 빼는 이유다.
- **`key_share` 1258 bytes.** 양자 내성 키 교환(X25519MLKEM768) 때문에 ClientHello가 1.5 KB를 넘는다. 그래서 `peek_record`는 5바이트 header를 먼저 엿보고, 거기 적힌 길이만큼 다시 엿본다.
- **`recv() after the peek`.** 엿본 바이트가 소켓에 그대로 남아 있어서, 보통 `recv()`가 같은 수의 바이트를 다시 받는다. `rproxy`에서는 이 자리에서 OpenSSL이 같은 바이트를 처음부터 읽는다.
- **`nc`로 보낸 평문 HTTP.** 첫 바이트가 `0x16`이 아니라 `'G'`다. `rproxy`가 평문 HTTP를 받으면 응답 없이 닫는 근거가 이 한 바이트다.

## 혼자 하는 변경 과제

`supported_versions`(0x002b) 줄 뒤에 그 extension이 담은 버전 값들을 찍고, GREASE를 뺀 가장 큰 값을 `highest 0x0304`처럼 표시한다. 브라우저와 curl에서 `legacy_version`(0x0303)과 이 값이 왜 다른지 본다.

## 확인 질문

`rproxy`는 왜 ClientHello를 `recv()`로 읽지 않고 `MSG_PEEK`로 엿보는가? 그냥 `recv()`로 읽어 버리면 그다음 OpenSSL handshake에 무슨 일이 생기는가?
