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
