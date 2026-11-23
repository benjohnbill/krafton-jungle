#include <netinet/in.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>

#define PORT 18444
#define BACKLOG 8
#define RECORD_HEADER_SIZE 5
#define RECORD_MAX (RECORD_HEADER_SIZE + 16384)

static int open_listen_fd(void);
static size_t peek_record(int conn_fd, unsigned char *bytes);
static void print_hello(const unsigned char *bytes, size_t length);
static void print_extensions(const unsigned char *at, const unsigned char *end);
static const char *extension_name(unsigned type);
static unsigned read_u16(const unsigned char *at);
static bool is_grease(unsigned value);

int main(void)
{
    int listen_fd = open_listen_fd();
    printf("listening on %d\n", PORT);

    while (true) {
        int conn_fd = accept(listen_fd, NULL, NULL);
        if (conn_fd < 0) {
            perror("accept");
            continue;
        }
        static unsigned char bytes[RECORD_MAX];
        size_t length = peek_record(conn_fd, bytes);
        if (length > 0) {
            print_hello(bytes, length);
        }
        /* MSG_PEEK left the bytes in the socket: recv() gets them again. */
        ssize_t again = recv(conn_fd, bytes, sizeof(bytes), 0);
        printf("recv() after the peek got %zd bytes again\n\n", again);
        close(conn_fd);
    }
}

static int open_listen_fd(void)
{
    int listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (listen_fd < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }
    int reuse = 1;
    setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse));

    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    addr.sin_port = htons(PORT);
    if (bind(listen_fd, (struct sockaddr *)&addr, sizeof(addr)) < 0 ||
        listen(listen_fd, BACKLOG) < 0) {
        perror("bind or listen");
        exit(EXIT_FAILURE);
    }

    return listen_fd;
}

/* Peeks until one whole TLS record is in the socket. Returns its length,
   or 0 if the bytes are not a TLS handshake record. */
static size_t peek_record(int conn_fd, unsigned char *bytes)
{
    size_t want = RECORD_HEADER_SIZE;
    while (true) {
        ssize_t got = recv(conn_fd, bytes, want, MSG_PEEK | MSG_WAITALL);
        if (got < (ssize_t)want) {
            printf("the client closed after %zd bytes\n", got);
            return 0;
        }
        if (bytes[0] != 0x16) {
            printf("not TLS: the first byte is 0x%02x ('%c')\n", bytes[0],
                   bytes[0]);
            return 0;
        }
        size_t record_length = RECORD_HEADER_SIZE + read_u16(bytes + 3);
        if (want == record_length) {
            return record_length;
        }
        want = record_length;
    }
}

static void print_hello(const unsigned char *bytes, size_t length)
{
    const unsigned char *end = bytes + length;
    printf("record: type 0x%02x, version 0x%04x, length %u\n", bytes[0],
           read_u16(bytes + 1), read_u16(bytes + 3));

    const unsigned char *at = bytes + RECORD_HEADER_SIZE;
    printf("handshake type %u (1 = ClientHello)\n", at[0]);
    at += 4; /* type, 3-byte length */
    printf("legacy_version 0x%04x\n", read_u16(at));
    at += 2 + 32; /* version, random */
    at += 1 + at[0]; /* session id */

    unsigned cipher_bytes = read_u16(at);
    at += 2;
    printf("ciphers (%u):", cipher_bytes / 2);
    for (unsigned i = 0; i < cipher_bytes; i += 2) {
        unsigned cipher = read_u16(at + i);
        printf(" %04x%s", cipher, is_grease(cipher) ? "(GREASE)" : "");
    }
    printf("\n");
    at += cipher_bytes;
    at += 1 + at[0]; /* compression methods */

    if (at + 2 <= end) {
        unsigned extension_bytes = read_u16(at);
        at += 2;
        print_extensions(at, at + extension_bytes);
    }
}

static void print_extensions(const unsigned char *at, const unsigned char *end)
{
    printf("extensions, in wire order:\n");
    while (at + 4 <= end) {
        unsigned type = read_u16(at);
        unsigned data_length = read_u16(at + 2);
        const unsigned char *data = at + 4;
        printf("  %04x %-24s %4u bytes", type,
               is_grease(type) ? "GREASE" : extension_name(type), data_length);
        if (type == 0x0000 && data_length > 5) { /* server_name */
            printf("  host \"%.*s\"", read_u16(data + 3), data + 5);
        }
        if (type == 0x0010 && data_length > 3) { /* ALPN: first name */
            printf("  first \"%.*s\"", data[2], data + 3);
        }
        printf("\n");
        at = data + data_length;
    }
}

static const char *extension_name(unsigned type)
{
    switch (type) {
    case 0x0000:
        return "server_name";
    case 0x000a:
        return "supported_groups";
    case 0x000b:
        return "ec_point_formats";
    case 0x000d:
        return "signature_algorithms";
    case 0x0010:
        return "alpn";
    case 0x0017:
        return "extended_master_secret";
    case 0x002b:
        return "supported_versions";
    case 0x002d:
        return "psk_key_exchange_modes";
    case 0x0033:
        return "key_share";
    default:
        return "?";
    }
}

static unsigned read_u16(const unsigned char *at)
{
    return (unsigned)at[0] << 8 | at[1];
}

/* RFC 8701: 0x0a0a, 0x1a1a, ... 0xfafa. */
static bool is_grease(unsigned value)
{
    return (value & 0x0f0f) == 0x0a0a && (value >> 8) == (value & 0xff);
}
