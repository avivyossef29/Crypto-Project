#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define PORT 443
#define MAX_BUFFER_SIZE 1024

// Function to handle the Heartbeat request
void handle_heartbeat_request(int client_socket, const char *buffer, int len)
{
    if (len < 6)
    {
        // Invalid heartbeat request, length too short
        printf("Invalid Heartbeat request: too short\n");
        return;
    }

    // Extract the payload length from the heartbeat message (3rd and 4th bytes)
    unsigned short payload_length = (buffer[3] << 8) | buffer[4];
    unsigned short actual_payload_length = len - 6; // Header is 6 bytes long

    // Send back the data as a simulated heartbeat response
    printf("Sending Heartbeat response\n");
    send(client_socket, buffer, payload_length + 6, 0);
}

void handle_client(int client_socket)
{
    char buffer[MAX_BUFFER_SIZE];
    printf("Connection established with client\n");
    fflush(stdout); // Flush stdout

    while (1)
    {
        int len = recv(client_socket, buffer, MAX_BUFFER_SIZE, 0);
        if (len <= 0)
        {
            break; // Connection closed or error
        }

        // Check if it's a Heartbeat request
        if (buffer[0] == 0x18) // Heartbeat request type
        {
            printf("Received Heartbeat request\n");
            handle_heartbeat_request(client_socket, buffer, len);
        }
        else
        {
            buffer[len] = '\0';
            printf("Received message: %s\n", buffer);
            fflush(stdout); // Flush stdout
        }
    }

    close(client_socket);
}

int main()
{
    int sock;
    struct sockaddr_in addr;

    // Create socket
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0)
    {
        perror("Unable to create socket");
        return 1;
    }

    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    addr.sin_addr.s_addr = htonl(INADDR_ANY);

    // Bind the socket to the port
    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
        perror("Unable to bind");
        return 1;
    }

    // Listen for incoming connections
    if (listen(sock, 1) < 0)
    {
        perror("Unable to listen");
        return 1;
    }

    printf("Server is listening on port %d\n", PORT);

    while (1)
    {
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);

        // Accept incoming connection
        int client_socket = accept(sock, (struct sockaddr *)&client_addr, &client_len);
        if (client_socket < 0)
        {
            perror("Unable to accept connection");
            continue;
        }

        printf("New client connected\n");
        handle_client(client_socket);
    }

    // Close the listening socket
    close(sock);

    return 0;
}
