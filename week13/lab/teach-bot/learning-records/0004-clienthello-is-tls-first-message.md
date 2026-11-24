# 그는 ClientHello를 TCP handshake의 헤더로 보았고, 이제 TLS handshake의 첫 메시지로 본다

2026-11-24, L2. 그는 "TCP handshake를 커널이 수행할 때 맨 처음 받는 헤더의 느낌"이라고 했다. 바로잡은 것: TCP handshake는 데이터가 0 byte이고 kernel끼리 끝난다. ClientHello는 그 뒤 client가 연결에 처음 쓰는 데이터이고, TLS handshake의 첫 메시지라서 평문이다. 그는 `nc -l 9443 | xxd`와 `curl -k https://localhost:9443/`로 curl의 ClientHello 1569 byte를 직접 받았다. 그 안에서 `16`, `01`, cipher 30개(`003c`), SNI `localhost`, ALPN `h2`를 JA4 a 부분과 맞춰 보았다.

그는 카드 이름 "② ClientHello → ③ TLS"가 ClientHello를 TLS 밖에 두는 것처럼 읽힌다고 짚었다. 그래서 두 카드를 "TLS handshake: ClientHello"와 "TLS handshake: ServerHello부터"로 바꿨다. 단계는 프로토콜의 층이 아니라 rproxy가 판정하는 지점으로 나눈다.

Evidence: L2 퀴즈 5/6. 예측(`disguised`의 200)은 0으로 맞혔고, 이유도 "User-Agent는 Chrome인데 TLS가 curl이면 거짓말이 걸린다"로 맞다. 틀린 것: Chrome이 extension 순서를 섞을 때 JA3가 "모두 같은 값이 된다"고 골랐다. 실제로는 JA3가 받은 순서대로 hash해서 연결마다 값이 바뀌고, JA4는 정렬해서 이 문제를 고쳤다.

Implications: 순서와 정렬이 hash 값에 주는 영향이 아직 약하다. `ja4_format` 따라치기에서 `qsort` 줄(`extension_hash_format`)을 지날 때 이것을 다시 묻는다. TLS handshake의 ServerHello 이후 메시지는 그가 원한 대로 깊이 다루지 않는다 (user said "엄청나게 자세하게 적을 필요는 없어").
