"""Accept one connection and never call read().

Lesson L2: the bytes the client sends wait in the kernel receive buffer of
this socket. Watch it with: ss -tan 'sport = :8080' (Recv-Q)

    python3 tools/no_read.py [port]
"""

import socket
import sys
import time

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

listen_sock = socket.socket()
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_sock.bind(("127.0.0.1", port))
listen_sock.listen(1)
print(f"listen on 127.0.0.1:{port}, accept once, no read. Ctrl-C to stop.")
conn_sock, addr = listen_sock.accept()
print(f"accepted {addr[0]}:{addr[1]}; not reading.")
try:
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    pass
