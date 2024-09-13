# Use Ubuntu 20.04 as a base image
FROM ubuntu:20.04

# Set environment variables to non-interactive to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update and install required packages
RUN apt-get update && \
    apt-get install -y build-essential wget zlib1g-dev libssl-dev python3 python3-pip xxd

# Install vulnerable OpenSSL version
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

# Copy the entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY heartbleed_test.py ./heartbleed_test.py
RUN chmod +x /usr/local/bin/entrypoint.sh

# Copy the password file
COPY password.txt ./password.txt

# Set the entrypoint
ENTRYPOINT ["entrypoint.sh"]
