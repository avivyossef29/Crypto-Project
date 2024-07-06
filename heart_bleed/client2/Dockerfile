# Use an official Ubuntu stable as a parent image
FROM ubuntu:20.04

# Set environment variables to non-interactive to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update and install required packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev build-essential wget

# Install vulnerable OpenSSL version
RUN wget https://www.openssl.org/source/old/1.0.1/openssl-1.0.1f.tar.gz && \
    tar -xzf openssl-1.0.1f.tar.gz && \
    cd openssl-1.0.1f && \
    ./config no-threads shared no-zlib no-asm no-hw no-engine && \
    make && \
    make install_sw && \
    cd .. && \
    rm -rf openssl-1.0.1f.tar.gz openssl-1.0.1f

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Command to keep the container running
CMD ["tail", "-f", "/dev/null"]
