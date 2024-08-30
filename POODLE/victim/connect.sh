#!/bin/bash

# Connect to the Flask server using OpenSSL
#echo "Connecting to server using OpenSSL..."
#openssl s_client -connect demo-server:443 -ssl3 -cipher AES128-SHA

# Connect to the Flask server using Curl
echo "Connecting to server using Curl..."
curl --sslv3 --ciphers AES128-SHA https://demo-server/ --insecure