import ssl
import socket

def create_client():
    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Wrap the socket with SSL
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)  # Use TLS 1.0

    # Set cipher list to include only AES128-SHA
    context.set_ciphers('AES128-SHA')

    # Connect to server
    wrapped_socket = context.wrap_socket(sock, server_hostname='localhost')
    wrapped_socket.connect(('localhost', 10001))

    # Send request
    wrapped_socket.sendall(b'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n')
    
    # Receive response
    response = wrapped_socket.recv(4096)
    print(response.decode())
    
    # Close the connection
    wrapped_socket.close()

if __name__ == "__main__":
    create_client()
