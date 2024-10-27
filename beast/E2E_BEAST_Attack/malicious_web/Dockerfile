#docker build -t mal_server_image .
#docker run --rm -t --name mal_server_container --network=host mal_server_image

# Use Ubuntu 20.04 as the base image
FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget

# Install Flask (or other required libraries) via pip
RUN pip3 install flask

# Copy the malicious server script and html files
COPY mal_server.py /usr/src/mal_server.py
COPY index.html /usr/src/index.html
COPY sslApplet.class /usr/src/sslApplet.class

# Set the working directory
WORKDIR /usr/src

# Expose port 8080 to allow the client to connect
EXPOSE 8080

# Run the malicious server script
CMD ["python3", "mal_server.py"]
