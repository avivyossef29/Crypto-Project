# Use an older Ubuntu base image
FROM ubuntu:20.04

# Install necessary packages for building OpenSSL and Python dependencies
RUN apt-get update && \
    apt-get install -y build-essential checkinstall zlib1g-dev wget \
    python3-pip

# Install Flask
RUN pip3 install flask

# Download OpenSSL 1.0.2u (the last release of the 1.0.2 branch)
RUN wget https://www.openssl.org/source/openssl-1.0.2u.tar.gz && \
    tar -xvf openssl-1.0.2u.tar.gz && \
    cd openssl-1.0.2u && \
    ./config enable-ssl3 enable-ssl3-method no-shared && \
    make && \
    make install

# Update the OpenSSL paths
ENV PATH="/usr/local/ssl/bin:$PATH"
ENV LD_LIBRARY_PATH="/usr/local/ssl/lib"

# Set working directory
WORKDIR /server

# Copy the Flask server into the container
COPY ./server.py /server/server.py

# Copy the SSL certificates
COPY ./server.crt /server/server.crt
COPY ./server.key /server/server.key

# Expose port 443 for HTTPS
EXPOSE 443

ENTRYPOINT [ "python3" ]

# Run the Flask server
CMD ["server.py"]