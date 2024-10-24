# CRIME Challenge Server - FOR CTF ORGANIZERS ONLY
# Enhanced version with both compression and encryption
import http.server
import socketserver
import zlib
import random
import string
import json
from urllib.parse import parse_qs, urlparse
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

# Configuration
PORT = 8443
SECRET_FLAG = (
    "secret_flag: CTF_FLAG{C0mpr3ss1on_1s_n0t_y0ur_fr13nd}"  # Hidden from challengers
)
SESSION_TOKEN = "www.youtube.com/watch?v=dQw4w9WgXcQ"

# Encryption configuration
ENCRYPTION_KEY = Fernet.generate_key()  # This should be kept secret
fernet = Fernet(ENCRYPTION_KEY)


class DifficultyLevel:
    NORMAL = "normal"  # Only compression
    HARD = "hard"  # Compression + encryption


class CRIMEChallengeHandler(http.server.SimpleHTTPRequestHandler):
    def generate_response_data(self, payload):
        """Generate the response data including the secret token"""
        response_data = f"""
        HTTP/1.1 200 OK
        Content-Type: text/plain
        Set-Cookie: session={SESSION_TOKEN}
        
        {payload}
        """
        return f"Cookie: {SECRET_FLAG}\n{response_data}"

    def process_request(self, payload, difficulty):
        """Process the request based on difficulty level"""
        response_with_secret = self.generate_response_data(payload)

        # First compress the data
        compressed = zlib.compress(response_with_secret.encode())

        if difficulty == DifficultyLevel.HARD:
            # For hard mode, encrypt after compression
            encrypted = fernet.encrypt(compressed)
            return {
                "length": len(encrypted),
                "data": base64.b64encode(encrypted).decode(),
                "mode": "encrypted+compressed",
            }
        else:
            # For normal mode, just return compression info
            return {
                "length": len(compressed),
                "data": base64.b64encode(compressed).decode(),
                "mode": "compressed",
            }

    def do_GET(self):
        url = urlparse(self.path)
        query = parse_qs(url.query)

        # Validate parameters
        if "payload" not in query:
            self.send_error(400, "Missing payload parameter")
            return

        payload = query["payload"][0]
        difficulty = query.get("difficulty", [DifficultyLevel.NORMAL])[0]

        # Process request based on difficulty
        response_data = self.process_request(payload, difficulty)

        # Send response
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())


def run_server():
    with socketserver.TCPServer(("", PORT), CRIMEChallengeHandler) as httpd:
        print(f"Serving CRIME challenge at port {PORT}")
        print(
            f"Difficulty modes available: {DifficultyLevel.NORMAL}, {DifficultyLevel.HARD}"
        )
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
