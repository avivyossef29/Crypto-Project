#include <openssl/ssl.h>
#include <openssl/err.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define PORT 443
#define CERT_FILE "/app/cert.pem"
#define KEY_FILE "/app/key.pem"
#define PASSWORD_FILE "/app/passwords.txt"
#define MAX_BUFFER_SIZE 1024

char *passwords = NULL; // Global variable to hold passwords

void init_openssl()
{
    SSL_load_error_strings();
    OpenSSL_add_ssl_algorithms();
}

void cleanup_openssl()
{
    EVP_cleanup();
}

SSL_CTX *create_context()
{
    const SSL_METHOD *method;
    SSL_CTX *ctx;

    method = SSLv23_server_method();

    ctx = SSL_CTX_new(method);
    if (!ctx)
    {
        perror("Unable to create SSL context");
        ERR_print_errors_fp(stderr);
        exit(EXIT_FAILURE);
    }

    return ctx;
}

// Function to load passwords into memory
void load_passwords()
{
    FILE *file = fopen(PASSWORD_FILE, "r");
    if (!file)
    {
        perror("Unable to open password file");
        fflush(stderr); // Flush stderr
        exit(EXIT_FAILURE);
    }

    fseek(file, 0, SEEK_END);
    long fsize = ftell(file);
    fseek(file, 0, SEEK_SET);

    passwords = malloc(fsize + 1);
    if (!passwords)
    {
        perror("Unable to allocate memory");
        fflush(stderr); // Flush stderr
        exit(EXIT_FAILURE);
    }

    fread(passwords, 1, fsize, file);
    fclose(file);
    passwords[fsize] = '\0';
    printf("Passwords loaded into memory:\n%s\n", passwords);
    fflush(stdout); // Flush stdout
}

void configure_context(SSL_CTX *ctx)
{
    // Load server's certificate into the SSL context
    if (SSL_CTX_use_certificate_file(ctx, CERT_FILE, SSL_FILETYPE_PEM) <= 0)
    {
        ERR_print_errors_fp(stderr);
        fflush(stderr); // Flush stderr
        exit(EXIT_FAILURE);
    }

    // Load server's private key into the SSL context
    if (SSL_CTX_use_PrivateKey_file(ctx, KEY_FILE, SSL_FILETYPE_PEM) <= 0)
    {
        ERR_print_errors_fp(stderr);
        fflush(stderr); // Flush stderr
        exit(EXIT_FAILURE);
    }

    // Verify that the private key matches the certificate
    if (SSL_CTX_check_private_key(ctx) <= 0)
    {
        ERR_print_errors_fp(stderr);
        fflush(stderr); // Flush stderr
        exit(EXIT_FAILURE);
    }

    // Disable compression
    SSL_CTX_set_options(ctx, SSL_OP_NO_COMPRESSION);
}

void handle_client(SSL *ssl)
{
    char buffer[MAX_BUFFER_SIZE];
    printf("SSL connection established\n");
    fflush(stdout); // Flush stdout

    while (1)
    {
        int len = SSL_read(ssl, buffer, MAX_BUFFER_SIZE);
        if (len <= 0)
            break;

        // Check if it's a Heartbeat request
        if (buffer[0] == 0x18) // Heartbeat request type
        {
            printf("Received Heartbeat Request (c)\n");
            fflush(stdout); // Flush stdout
        }

        buffer[len] = '\0';
        printf("Received message(c): %s\n", buffer);
        fflush(stdout); // Flush stdout
    }
}

int main(int argc, char **argv)
{
    int sock;
    struct sockaddr_in addr;

    // Load passwords into memory
    // load_passwords();

    printf("OpenSSL version: %s\n", SSLeay_version(SSLEAY_VERSION));
    fflush(stdout); // Flush stdout
    init_openssl();
    SSL_CTX *ctx = create_context();

    configure_context(ctx);

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0)
    {
        perror("Unable to create socket");
        fflush(stderr); // Flush stderr
        exit(EXIT_FAILURE);
    }

    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    addr.sin_addr.s_addr = htonl(INADDR_ANY);

    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
        perror("Unable to bind");
        fflush(stderr); // Flush stderr
        exit(EXIT_FAILURE);
    }

    if (listen(sock, 1) < 0)
    {
        perror("Unable to listen");
        fflush(stderr); // Flush stderr
        exit(EXIT_FAILURE);
    }

    while (1)
    {
        struct sockaddr_in addr;
        uint len = sizeof(addr);
        SSL *ssl;

        int client = accept(sock, (struct sockaddr *)&addr, &len);
        if (client < 0)
        {
            perror("Unable to accept");
            fflush(stderr); // Flush stderr
            exit(EXIT_FAILURE);
        }

        ssl = SSL_new(ctx);
        SSL_set_fd(ssl, client);

        if (SSL_accept(ssl) <= 0)
        {
            ERR_print_errors_fp(stderr);
            fflush(stderr); // Flush stderr
        }
        else
        {
            handle_client(ssl);
        }

        SSL_shutdown(ssl);
        SSL_free(ssl);
        close(client);
    }

    close(sock);
    SSL_CTX_free(ctx);
    cleanup_openssl();
}
