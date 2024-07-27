
# Heartbleed Vulnerability Demonstration

This project demonstrates the Heartbleed vulnerability (CVE-2014-0160)
by setting up an SSL server and using two clients to interact with it. 
The first client sends passeward.txt to the server.
Later,the second client sends a malicious heartbeat request to exploit the vulnerability,
and print thr first 100 lines of the server response.
You can check that the server response contain sensitive data from the passeward.txt file  

## Overview

### Server

The server is configured with a vulnerable version of OpenSSL (1.0.1f). It is designed to receive SSL/TLS connections and handle heartbeat requests, demonstrating the Heartbleed vulnerability.

### Client

The first client connects and sends data to the server:

1. Sends a Client Hello message to establish an SSL/TLS connection.
2. Sends sensitive data to the server to be stored in its memory.
3. Adds a delay to ensure OpenSSL completes the process.

The second client connects and sends a malicious heartbeat request to the server:

1. Runs the heartbleed_test.py script to exploit the Heartbleed vulnerability.
2. Saves the server's response to heartbeat_response.txt.
3. Prints the first 100 lines of the server's response, showing that it contains sensitive data from the password.txt file.

## Prerequisites

- Docker must be installed on your system.

## Setup
- use 2 different terminals for client and server
### Build and Run the Server

1. Navigate to the server directory:
   ```sh
   cd server
   ```

2. Build the Docker image for the server:
   ```sh
   docker build -t openssl-heartbleed-server .
   ```

3. Run the server container:
   ```sh
   docker run --rm -it -p 443:443 openssl-heartbleed-server
   ```

### Build and Run the Client

1. Navigate to the client directory:
   ```sh
   cd client
   ```

2. Build the Docker image for the client:
   ```sh
   docker build -t vulnerable-ssl-client .
   ```

3. Run the client container:
   ```sh
   docker run --rm vulnerable-ssl-client 172.17.0.2
   
## Output
- Now you can see the server response to the heartblead attack in the client side, and the server logs in the server side.  
   ```
