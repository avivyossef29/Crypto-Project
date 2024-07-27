# Use Ubuntu 20.04 as a base image
FROM ubuntu:20.04

# Set environment variables to non-interactive to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update and install required packages
RUN apt-get update && \
    apt-get install -y build-essential wget python3 python3-pip

# Install vulnerable OpenSSL version
RUN wget https://www.openssl.org/source/old/1.0.1/openssl-1.0.1f.tar.gz && \
    tar -xzf openssl-1.0.1f.tar.gz && \
    cd openssl-1.0.1f && \
    ./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl shared zlib && \
    make && \
    make install_sw

# Ensure the locally built OpenSSL is used
ENV PATH="/usr/local/ssl/bin:${PATH}"
RUN openssl version

# Install Flask and other dependencies
RUN pip3 install flask flask_sqlalchemy flask_login

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Generate self-signed certificate using the vulnerable OpenSSL version
RUN /usr/local/ssl/bin/openssl req -x509 -newkey rsa:2048 -keyout /app/key.pem -out /app/cert.pem -days 365 -nodes -subj "/C=US/ST=NC/L=Chapel Hill/O=Acme/CN=www.example.com"

# Ensure any existing database is removed
RUN rm -f /app/db.sqlite
RUN rm -rf /app/instance

# Expose ports 80 for HTTP and 443 for HTTPS
EXPOSE 80 443

# Run the Flask app with SSL
CMD ["python3", "app.py"]
