#docker build -t attacker_image .
#docker run --rm -t --name attacker_container --network=host attacker_image

# Use Ubuntu 20.04 as the base image (or any preferred version)
FROM ubuntu:20.04

# Set environment variables to prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libpcap-dev \
    net-tools \
    iputils-ping \
    tcpdump \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Scapy and other Python libraries required for the attacker script
RUN pip3 install scapy

# Copy the attacker script into the container
COPY attacker.py /usr/src/attacker.py

# Set the working directory
WORKDIR /usr/src

# Expose port 1337 for listening to client connections
EXPOSE 1337

# Run the attacker script
CMD ["python3", "attacker.py"]
