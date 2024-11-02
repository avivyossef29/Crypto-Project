import http.server
import socketserver
import zlib
import random
import json
from urllib.parse import parse_qs, urlparse
from Crypto.Cipher import AES
import base64
from concurrent.futures import ThreadPoolExecutor
import threading
from typing import Dict, Optional
import time

# Configuration
PORT = 8443
SECRET_FLAG = "secret_flag: CTF_FLAG{C0mpr3ss1oN_1S_N0T_Y0uR_Fr13ND}"
SESSION_TOKEN = "www.youtube.com/watch?v=dQw4w9WgXcQ"

# Encryption configuration
ENCRYPTION_KEY = random.randbytes(AES.block_size)
IV = random.randbytes(AES.block_size)

# Connection and performance settings
MAX_WORKERS = 4
KEEP_ALIVE_TIMEOUT = 60
CONNECTION_CACHE_SIZE = 100


def pad(data: bytes, block_size: int = 16) -> bytes:
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length] * padding_length)
    return data + padding


class CacheEntry:
    def __init__(self, cipher):
        self.cipher = cipher
        self.last_used = time.time()


class CipherCache:
    def __init__(self, max_size: int = CONNECTION_CACHE_SIZE):
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self.lock = threading.Lock()

    def get_cipher(self, key: bytes, iv: bytes):
        cache_key = f"{key.hex()}:{iv.hex()}"
        with self.lock:
            if cache_key in self.cache:
                entry = self.cache[cache_key]
                entry.last_used = time.time()
                return entry.cipher

            if len(self.cache) >= self.max_size:
                # Remove oldest entry
                oldest_key = min(
                    self.cache.keys(), key=lambda k: self.cache[k].last_used
                )
                del self.cache[oldest_key]

            cipher = AES.new(key, AES.MODE_CBC, iv)
            self.cache[cache_key] = CacheEntry(cipher)
            return cipher


class DifficultyLevel:
    NORMAL = "normal"  # Only compression
    HARD = "hard"  # Compression + encryption


class OptimizedCRIMEHandler(http.server.SimpleHTTPRequestHandler):
    timeout = KEEP_ALIVE_TIMEOUT
    protocol_version = "HTTP/1.1"  # Enable keep-alive

    # Class-level cache for reuse
    response_template = """
    HTTP/1.1 200 OK
    Content-Type: text/plain
    Set-Cookie: session={session}
    {payload}
    """
    cipher_cache = CipherCache()

    def __init__(self, *args, **kwargs):
        self.thread_pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)
        super().__init__(*args, **kwargs)

    def generate_response_data(self, payload: str) -> str:
        """Generate the response data including the secret token"""
        response_data = self.response_template.format(
            session=SESSION_TOKEN, payload=payload
        )
        return f"Cookie: {SECRET_FLAG}\n{response_data}"

    def process_request(self, payload: str, difficulty: str) -> dict:
        """Process the request based on difficulty level"""
        response_with_secret = self.generate_response_data(payload)
        compressed = zlib.compress(response_with_secret.encode())

        if difficulty == DifficultyLevel.HARD:
            cipher = self.cipher_cache.get_cipher(ENCRYPTION_KEY, IV)
            encrypted = cipher.encrypt(pad(compressed))
            return {
                "length": len(encrypted),
                "data": base64.b64encode(encrypted).decode(),
                "mode": "encrypted+compressed",
            }

        return {
            "length": len(compressed),
            "data": base64.b64encode(compressed).decode(),
            "mode": "compressed",
        }

    def do_GET(self):
        # Parse URL and query parameters
        url = urlparse(self.path)
        query = parse_qs(url.query)

        if "payload" not in query:
            self.send_error(400, "Missing payload parameter")
            return

        payload = query["payload"][0]
        difficulty = query.get("difficulty", [DifficultyLevel.NORMAL])[0]

        try:
            # Process request in thread pool
            future = self.thread_pool.submit(self.process_request, payload, difficulty)
            response_data = future.result(timeout=30)  # 30 second timeout

            print (f"payload: {payload} \nresponding with: {response_data}")

            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Connection", "keep-alive")
            self.send_header("Keep-Alive", f"timeout={KEEP_ALIVE_TIMEOUT}")
            content = json.dumps(response_data).encode()
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")


class ThreadedTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def run_server():
    with ThreadedTCPServer(("", PORT), OptimizedCRIMEHandler) as httpd:
        print(f"Serving optimized CRIME challenge at port {PORT}")
        print(
            f"Difficulty modes available: {DifficultyLevel.NORMAL}, {DifficultyLevel.HARD}"
        )
        print(f"Using {MAX_WORKERS} worker threads")
        print(f"Keep-alive timeout: {KEEP_ALIVE_TIMEOUT} seconds")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
