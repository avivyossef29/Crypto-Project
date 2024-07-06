# Use an official Ubuntu stable as a parent image
FROM ubuntu:20.04

# Set environment variables to non-interactive to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/ssl/lib

# Update and install required packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev build-essential wget

# Install the vulnerable OpenSSL version
RUN wget https://www.openssl.org/source/old/1.0.1/openssl-1.0.1f.tar.gz && \
    tar -xzf openssl-1.0.1f.tar.gz && \
    cd openssl-1.0.1f && \
    ./config no-threads shared no-zlib no-asm no-hw no-engine && \
    make && \
    make install_sw && \
    cd .. && \
    rm -rf openssl-1.0.1f.tar.gz openssl-1.0.1f

# Ensure Python uses the newly installed OpenSSL
RUN apt-get install -y libssl-dev && \
    ln -sf /usr/local/ssl/bin/openssl /usr/bin/openssl && \
    ln -sf /usr/local/ssl/include/openssl /usr/include/openssl && \
    ln -sf /usr/local/ssl/lib/libssl.so.1.0.0 /usr/lib/libssl.so.1.0.0 && \
    ln -sf /usr/local/ssl/lib/libcrypto.so.1.0.0 /usr/lib/libcrypto.so.1.0.0 && \
    echo "/usr/local/ssl/lib" > /etc/ld.so.conf.d/openssl.conf && \
    ldconfig

# Install Python SSL dependencies
RUN pip3 install pyopenssl

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Run the client script
CMD ["python3", "client.py"]
