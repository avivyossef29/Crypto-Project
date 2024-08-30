# Use an older Ubuntu base image
FROM ubuntu:20.04

# Install necessary packages
RUN apt-get update && \
    apt-get install -y curl openssl

# Copy the connection script
COPY ./connect.sh /connect.sh

# Make the script executable
RUN chmod +x /connect.sh

# Run the connection script
CMD ["curl", "--sslv3",  "--ciphers", "AES128-SHA", "https://server-demo/", " --insecure"]