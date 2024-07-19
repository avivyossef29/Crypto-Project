# Use an Ubuntu base image
FROM ubuntu:14.04

# Install Curl and OpenSSL
RUN apt-get update && \
    apt-get install -y curl openssl

# Create a script to connect to the server
COPY ./connect.sh /connect.sh

# Make the script executable
RUN chmod +x /connect.sh

# Run the connection script
CMD ["/connect.sh"]