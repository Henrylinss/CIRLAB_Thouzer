#include "../include/qt_cirlab_monitor/qsocket.hpp"

//int argc, char const* argv[]
int Send::Do(char* api, char* ip, int PORT)
{
    int sock = 0, valread, client_fd;
    struct sockaddr_in serv_addr;
    char* API = api;
    char buffer[1024] = { 0 };
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
//        printf("\n Socket creation error \n");
        return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    // Convert IPv4 and IPv6 addresses from text to binary
    // form
    if (inet_pton(AF_INET, ip, &serv_addr.sin_addr)
        <= 0) {
//        printf(
//            "\nInvalid address/ Address not supported \n");
        return -1;
    }

    if ((client_fd
         = connect(sock, (struct sockaddr*)&serv_addr,
                   sizeof(serv_addr)))
        < 0) {
//        printf("\nConnection Failed \n");
        return -1;
    }
    send(sock, API, strlen(API), 0);
//    printf("API message sent\n");
    valread = read(sock, buffer, 1024);
//    printf("%s\n", buffer);

    // closing the connected socket
    close(client_fd);
    return 0;
}
