# Build one probe: make 06-echo/echo_server  (builds 06-echo/echo_server.c)
CC = cc
CFLAGS = -std=c17 -D_POSIX_C_SOURCE=200809L -Wall -Wextra -g -fsanitize=address,undefined
LDFLAGS = -fsanitize=address,undefined

%: %.c
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS)
