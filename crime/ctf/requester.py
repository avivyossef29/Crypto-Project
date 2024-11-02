import requests
import string
from requests.adapters import HTTPAdapter, Retry
from urllib3.util.retry import Retry
from functools import lru_cache
import urllib.parse
from enum import Enum
import time

class DifficultyLevel(Enum):
    NORMAL = "normal"
    HARD = "hard"


class CRIMERequester:
    def __init__(self, base_url, max_retries=3, pool_connections=10, pool_maxsize=100):
        self.session = requests.Session()

        # Configure connection pooling
        adapter = HTTPAdapter(
            pool_connections=pool_connections,  # Number of connection pools
            pool_maxsize=pool_maxsize,  # Max connections per pool
            max_retries=Retry(
                total=max_retries,
                backoff_factor=0.1,  # Exponential backoff
                status_forcelist=[500, 502, 503, 504],
            ),
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self.base_url = base_url.rstrip("/")

    @lru_cache(maxsize=1024)
    def get_response_length(self, payload, difficulty):
        try:
            # URL encode parameters properly
            params = {
                "payload": payload,
                "difficulty": (
                    difficulty.value if hasattr(difficulty, "value") else difficulty
                ),
            }

            # Make request using existing session
            response = self.session.get(
                self.base_url,
                params=params,
                timeout=5,  # Add timeout to prevent hanging
            )

            # Raise for bad status codes
            response.raise_for_status()

            data = response.json()
            return data.get("length")

        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return None
        except ValueError as e:
            print(f"JSON parsing error: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None