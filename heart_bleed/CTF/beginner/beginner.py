import struct
import argparse

# 18 - heartbeat , 03 02 - TLS 1.1 , 00 03 - length , 01 - message type ,40 00 - payload
# The server will return the payload in the heartbeat response without checking payload == length
HEARTBEAT_REQUEST_HEX = (
    "18 03 02 00 03"  # Heartbeat request type, SSL/TLS version, payload length (3 bytes)
    "01 40 00"        # Heartbeat request body with actual payload of 2 bytes
)

# Flag to be revealed after successful exploitation
FLAG = "CTF_FLAG{The bug that broke the internet}"

# Hint to help participants understand the exploit
HINT = """
Hint: The Heartbleed vulnerability happens when the payload length is greater than the actual payload size.
Try increasing the payload length to request more data from the server than is present in the actual payload.
"""

# Function to convert hex string to bytes
def hex_to_bytes(hex_str):
    return bytes.fromhex(hex_str.replace(" ", ""))

def check_heartbeat_exploit(request, show_hint):
    """
    Check if the Heartbeat request is malicious by comparing the payload length with the actual payload size.
    """
    # Extract the payload length from the request (bytes 3 and 4)
    payload_length = int.from_bytes(request[3:5], byteorder='big')

    # Calculate the actual payload size (subtract the 5-byte header)
    actual_payload_size = len(request) - 6

    # Compare payload length and actual payload size
    if payload_length > actual_payload_size:
        print(f"Success! Exploit worked. Payload length ({payload_length}) is greater than actual payload size ({actual_payload_size}).")
        print(f"Here is your flag: {FLAG}")
    else:
        print(f"Failure! Payload length ({payload_length}) is not greater than actual payload size ({actual_payload_size}).")
        if show_hint:
            print(f"{HINT}")

if __name__ == "__main__":
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description="Exploit the Heartbleed vulnerability.")
    parser.add_argument('--hint', action='store_true', help="Show hint even if exploit fails")
    args = parser.parse_args()

    # Check if the exploit is successful and show hint if requested
    check_heartbeat_exploit(hex_to_bytes(HEARTBEAT_REQUEST_HEX), args.hint)
