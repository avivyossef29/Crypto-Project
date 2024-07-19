#!/bin/bash

# Connect to the SSLv3 server using OpenSSL
echo "Connecting to server using OpenSSL..."
openssl s_client -connect server-demo:443 -ssl3

# Connect to the SSLv3 server using Curl
echo "Connecting to server using Curl..."
curl --sslv3 https://server-demo --insecure