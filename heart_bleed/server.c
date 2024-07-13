#include <openssl/ssl.h>
#include <openssl/err.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <arpa/inet.h>  // Add this include for socket functions
#include <netinet/in.h> // Add this include for INADDR_ANY

#define PORT 443
#define CERT_FILE "/app/cert.pem"
#define KEY_FILE "/app/key.pem"

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

void configure_context(SSL_CTX *ctx)
{
    SSL_CTX_set_ecdh_auto(ctx, 1);

    if (SSL_CTX_use_certificate_file(ctx, CERT_FILE, SSL_FILETYPE_PEM) <= 0)
    {
        ERR_print_errors_fp(stderr);
        exit(EXIT_FAILURE);
    }

    if (SSL_CTX_use_PrivateKey_file(ctx, KEY_FILE, SSL_FILETYPE_PEM) <= 0)
    {
        ERR_print_errors_fp(stderr);
        exit(EXIT_FAILURE);
    }
}

int main(int argc, char **argv)
{
    int sock;
    struct sockaddr_in addr;

    printf("OpenSSL version: %s\n", OpenSSL_version(OPENSSL_VERSION));

    // Assert the correct OpenSSL version
    if (strcmp(OpenSSL_version(OPENSSL_VERSION), "OpenSSL 1.0.1f 6 Jan 2014") != 0)
    {
        fprintf(stderr, "Error: Incorrect OpenSSL version. Expected OpenSSL 1.0.1f 6 Jan 2014\n");
        exit(EXIT_FAILURE);
    }

    init_openssl();
    SSL_CTX *ctx = create_context();

    configure_context(ctx);

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0)
    {
        perror("Unable to create socket");
        exit(EXIT_FAILURE);
    }

    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    addr.sin_addr.s_addr = htonl(INADDR_ANY);

    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
        perror("Unable to bind");
        exit(EXIT_FAILURE);
    }

    if (listen(sock, 1) < 0)
    {
        perror("Unable to listen");
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
            exit(EXIT_FAILURE);
        }

        ssl = SSL_new(ctx);
        SSL_set_fd(ssl, client);

        if (SSL_accept(ssl) <= 0)
        {
            ERR_print_errors_fp(stderr);
        }
        else
        {
            const char reply[] = "Welcome to the vulnerable SSL server!\n";
            SSL_write(ssl, reply, strlen(reply));
        }

        SSL_shutdown(ssl);
        SSL_free(ssl);
        close(client);
    }

    close(sock);
    SSL_CTX_free(ctx);
    cleanup_openssl();
}
