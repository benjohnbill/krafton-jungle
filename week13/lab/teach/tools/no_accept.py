"""Listen on a port and never call accept().

Lesson L1: the kernel finishes the handshake anyway, and each connection
waits in the accept queue. Watch it with: ss -tln 'sport = :8080'

    python3 tools/no_accept.py [port] [backlog]
"""

import socket
import sys
import time

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
backlog = int(sys.argv[2]) if len(sys.argv) > 2 else 2

listen_sock = socket.socket()
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_sock.bind(("127.0.0.1", port))
listen_sock.listen(backlog)
print(f"listen on 127.0.0.1:{port}, backlog {backlog}, no accept. Ctrl-C to stop.")
try:
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    pass
