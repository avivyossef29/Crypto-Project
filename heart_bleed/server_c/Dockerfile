# Use Ubuntu 20.04 as a base image
FROM ubuntu:20.04

# Set environment variables to non-interactive to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update and install required packages
RUN apt-get update && \
    apt-get install -y build-essential wget zlib1g-dev libssl-dev

# Install vulnerable OpenSSL version and modify the source code
RUN wget https://www.openssl.org/source/old/1.0.1/openssl-1.0.1f.tar.gz && \
    tar -xzf openssl-1.0.1f.tar.gz && \
    cd openssl-1.0.1f && \
    sed -i '1i #include <stdio.h>\n#include <stdlib.h>\nvoid load_passwords_into_memory() {\nFILE *password_file;\nchar *passwords;\nlong length;\npassword_file = fopen("/app/passwords.txt", "r");\nif (password_file) {\nfseek(password_file, 0, SEEK_END);\nlength = ftell(password_file);\nfseek(password_file, 0, SEEK_SET);\npasswords = malloc(length + 1);\nif (passwords) {\nif (fread(passwords, 1, length, password_file) == length) {\npasswords[length] = '\\0';\nprintf("Passwords loaded into memory:\\n%s\\n", passwords);\nprintf("First 10 chars: %.10s\\n", passwords);\n}\n}\nfclose(password_file);\n}\n}' ssl/t1_lib.c && \
    sed -i '/if (hbtype == TLS1_HB_REQUEST) {/a setbuf(stdout, NULL);\nprintf("Heartbeat request received in openssl proccess\\n");\nload_passwords_into_memory();\nfflush(stdout);' ssl/t1_lib.c && \
    sed -i '/int ret = 0;/a printf("Message received, processing in OpenSSL\\n");' ssl/s3_pkt.c && \
    ./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl shared zlib && \
    make && \
    make install_sw && \
    ln -sf /usr/local/ssl/bin/openssl /usr/bin/openssl && \
    ln -sf /usr/local/ssl/include/openssl /usr/include/openssl && \
    ln -sf /usr/local/ssl/lib/libssl.so /usr/lib/libssl.so && \
    ln -sf /usr/local/ssl/lib/libcrypto.so /usr/lib/libcrypto.so

# Ensure the locally built OpenSSL is used
ENV PATH="/usr/local/ssl/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/ssl/lib"

# Verify the OpenSSL version
RUN openssl version

# Create the /app directory
RUN mkdir -p /app

# Copy the server.c and Makefile files into the /app directory
COPY server.c /app/server.c
COPY Makefile /app/Makefile
COPY passwords.txt /app/passwords.txt

# Set the working directory
WORKDIR /app

# Compile the server.c file using the Makefile with the correct OpenSSL
RUN make CFLAGS="-I/usr/local/ssl/include" LDFLAGS="-L/usr/local/ssl/lib -lssl -lcrypto"

# Generate self-signed certificate using the vulnerable OpenSSL version
RUN /usr/local/ssl/bin/openssl req -x509 -newkey rsa:2048 -keyout /app/key.pem -out /app/cert.pem -days 365 -nodes -subj "/C=US/ST=NC/L=Chapel Hill/O=Acme/CN=www.example.com"

# Expose port 443 for HTTPS
EXPOSE 443

# Run the compiled server
CMD ["./server"]
