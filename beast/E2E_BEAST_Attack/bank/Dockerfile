#docker build -t server_image .
#docker run --rm -t --name server_container --network=host server_image
# Use Ubuntu 16.04 as the base image
FROM ubuntu:16.04

# Install necessary dependencies for building Python
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libdb5.3-dev \
    libbz2-dev \
    libexpat1-dev \
    liblzma-dev \
    tk-dev \
    wget \
    curl

# Download and install Python 3.9 from the source
RUN wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz && \
    tar -xf Python-3.9.0.tgz && \
    cd Python-3.9.0 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall

# Verify Python 3.9 installation
RUN python3.9 --version

# Install pip for Python 3.9
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3.9 get-pip.py

# Install dependencies (including pyopenssl)
RUN pip3.9 install pyopenssl cryptography


# Set working directory
WORKDIR /app

# Copy the server script and certificate files into the container
COPY server.py /app
COPY server.crt /app
COPY server.key /app

# Expose port 
EXPOSE 443

# Run the server script
CMD ["python3.9", "server.py"]
