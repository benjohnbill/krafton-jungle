#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>

#define PORT 8080
#define BACKLOG 8
#define BUFFER_SIZE 8192

static int open_listen_fd(void);
static struct sockaddr_in create_socket_addr(void);
static void bind_and_listen_by_fd(int listen_fd);

static void serve(int conn_fd);
static ssize_t read_request(int conn_fd, char *buffer, size_t size);
static char *find_header_end(char *buffer);
static void send_response(int conn_fd, int status, const char *reason,
                          const char *body);

static int open_listen_fd(void)
{
    int listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (listen_fd < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    bind_and_listen_by_fd(listen_fd);
    printf("listening on port %d\n", PORT);
    return listen_fd;
}

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

/* =================== Helper Functions ====================== */

static void bind_and_listen_by_fd(int listen_fd)
{
    int reuse = 1;
    if (setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse)) <
        0) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }

    struct sockaddr_in addr = create_socket_addr();
    if (bind(listen_fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("bind");
        exit(EXIT_FAILURE);
    }

    if (listen(listen_fd, BACKLOG) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }
}

static struct sockaddr_in create_socket_addr(void)
{
    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    addr.sin_port = htons(PORT);
    return addr;
}

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

/* =================== Helper Functions ====================== */

int main(void)

{
    signal(SIGPIPE, SIG_IGN);
    int listen_fd = open_listen_fd();

    for (;;) {
        struct sockaddr_in addr;
        socklen_t addr_len = sizeof(addr);

        int conn_fd = accept(listen_fd, (struct sockaddr *)&addr, &addr_len);
        if (conn_fd < 0) {
            perror("accept");
            continue;
        }
        printf("accepted %s:%d\n", inet_ntoa(addr.sin_addr),
               ntohs(addr.sin_port));
        serve(conn_fd);
        close(conn_fd);
        printf("closed\n");
    }
}
