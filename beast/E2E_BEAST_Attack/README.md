# BEAST Attack Demonstration

This project demonstrates the BEAST Attack (CVE-2011-3389)
by setting up an TLS bank server, malicious website server, client and an attacker.
First the client accesses to the malicious server, which inject him Java Applet that make him open connections to the bank server, and send cookie bearing requests.
Meanwhile, the attacker perfom MITM attack, capures those requests,then he perform the
cryptographic part of the attack, and decide what will be the next path of the following
request, according to the byte he just discovered.
When the attack ends, the attacker prints the client's cookie.

## Overview

### Bank server

The server is configured with a vulnerable version of TLS (TLS 1.0 with AES-128-CBC). It is designed to receive SSL/TLS connections and handle POST and GET requests.

### Client

The client establishes a connection to malicious website, controled by the attacker.

### Malicious server

When client accesses the web, it injects him Java Applet, which make the client open connections to his Bank server and make requests that include the client’s cookies.

### Attacker

The attacker perform MITM attack. He eavesdrop the communication between the victim (the ’Client’) and the Bank, captures the cookie bearing requests.
Then he perform the cryptographic part of the attack, and decide what will be the next path of the following request.

## Prerequisites

- Docker must be installed on your system.

## Setup
- use 4 different terminals for the bank server, malicious server, client and attacker.
### Build and Run the Bank server

1. Navigate to the bank directory:
   ```sh
   cd bank
   ```

2. Build the Docker image for the bank server:
   ```sh
   docker build -t server_image .
   ```

3. Run the bank server container:
   ```sh
   docker run --rm -t --network=host server_image
   ```

### Build and Run the Malicious server

1. Navigate to the malicious server directory:
   ```sh
   cd malicious_web
   ```

2. Build the Docker image for the malicious server:
   ```sh
   docker build -t mal_server_image .
   ```

3. Run the malicious server container:
   ```sh
   docker run --rm -t --network=host mal_server_image
   ```

### Build and Run the Attacker

1. Navigate to the attacker directory:
   ```sh
   cd attacker
   ```

2. Build the Docker image for the attacker:
   ```sh
   docker build -t attacker_image .
   ```

3. Run the attacker container:
   ```sh
   docker run --rm -t --network=host attacker_image
   ```

### Build and Run the Client

1. Navigate to the client directory:
   ```sh
   cd client
   ```

2. Build the Docker image for the client:
   ```sh
   docker build -t client_image .
   ```

3. Run the client container:
   ```sh
   docker run --rm -t --network=host client_image

## Output
- Now you can see the attacker print the client's cookie byte after byte.
