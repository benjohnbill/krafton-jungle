#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>

#define PORT 8080
#define BACKLOG 8
#define BUFFER_SIZE 1024

static int open_listen_fd(void);
static void echo(int conn_fd);
static struct sockaddr_in create_socket_addr(void);

static int open_listen_fd(void)
{
    int listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (listen_fd < 0) {
        perror("socket");
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

    printf("listening on port %d\n", PORT);
    return listen_fd;
}

static void echo(int conn_fd)
{
    char buffer[BUFFER_SIZE];
    ssize_t length;

    while ((length = read(conn_fd, buffer, sizeof(buffer))) > 0) {
        write(conn_fd, buffer, length);
    }
}

/* =================== Helper Functions ====================== */

static struct sockaddr_in create_socket_addr(void)
{
    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    addr.sin_port = htons(PORT);
    return addr;
}

/* =================== Helper Functions ====================== */

int main(void)
{
    int listen_fd = open_listen_fd();

    for (;;) {
        struct sockaddr_in addr;
        socklen_t addr_len = sizeof(addr);

        int conn_fd = accept(listen_fd, (struct sockaddr *)&addr, &addr_len);
        if (conn_fd < 0) {
            perror("accept");
            continue;
        }
        printf("accepted %s:%d\n", inet_ntoa(addr.sin_addr), ntohs(addr.sin_port));
        echo(conn_fd);
        close(conn_fd);
        printf("closed\n");
    }
}
