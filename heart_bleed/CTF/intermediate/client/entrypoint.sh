#!/bin/bash

# Ensure the server address is passed as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <server-address>"
    exit 1
fi

SERVER_ADDRESS=$1

# Run heartbleed_test.py
python3 heartbleed_test.py "$SERVER_ADDRESS"
