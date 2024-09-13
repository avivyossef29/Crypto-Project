# Use Ubuntu 20.04 as a base image
FROM ubuntu:20.04

# Set environment variables to non-interactive to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update and install required packages
RUN apt-get update && \
    apt-get install -y build-essential

# Create the /app directory
RUN mkdir -p /app

# Copy the server.c and Makefile files into the /app directory
COPY server.c /app/server.c
COPY Makefile /app/Makefile

# Set the working directory
WORKDIR /app

# Compile the server.c file using the Makefile
RUN make

# Expose port 443 for the TCP server
EXPOSE 443

# Run the compiled server
CMD ["./server"]
