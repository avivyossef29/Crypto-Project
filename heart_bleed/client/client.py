import socket
import ssl

def perform_handshake(host, port):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)  # Use TLSv1 for compatibility with OpenSSL 1.0.1f
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            print(f"SSL established. Peer: {ssock.getpeercert()}")
            print(f"Cipher used: {ssock.cipher()}")
            print(f"SSL version: {ssock.version()}")

if __name__ == "__main__":
    host = "172.17.0.2"  # Replace with your server's IP or hostname
    port = 5000  # Default port for your Flask app
    perform_handshake(host, port)
