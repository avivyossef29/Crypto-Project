# oracle_demo.py
# Demonstrates how the CRIME compression oracle works
import requests
import time
import statistics
from enum import Enum


class DifficultyLevel(Enum):
    NORMAL = "normal"
    HARD = "hard"


class CompressionOracle:
    def __init__(
        self, target_url="http://localhost:8443", difficulty=DifficultyLevel.NORMAL
    ):
        self.target_url = target_url
        self.difficulty = difficulty

    def get_response_length(self, payload):
        """Makes a request and returns the response length"""
        try:
            response = requests.get(
                f"{self.target_url}?payload={payload}&difficulty={self.difficulty.value}"
            )
            data = response.json()
            if "error" in data:
                print(f"Server error: {data['error']}")
                return None
            length = data["length"]
        except Exception as e:
            print(f"Error making request: {e}")
            return None
        time.sleep(0.1)  # Be nice to the server

        return length if length else None

    def demonstrate_compression_patterns(self):
        """Shows how different payloads affect compression"""
        print("\nDemonstrating compression patterns:")

        # Test 1: Repeated characters compress better
        test1a = "AAAAA"
        test1b = "ABCDE"
        if self.difficulty == DifficultyLevel.HARD:
            test1a += "A" * 16
            test1b += "FGHIJKLMNOPQRSTU"

        len1a = self.get_response_length(test1a)
        len1b = self.get_response_length(test1b)
        print("\nTest 1 - Repeated vs. Unique Characters:")
        print(f"Payload '{test1a}': length = {len1a}")
        print(f"Payload '{test1b}': length = {len1b}")
        print(f"Difference: {len1a - len1b}")
        print("Note: Repeated characters compress better!")

        # Test 2: Known prefix compression
        test2a = "secret_flag: CTF_FLAG{"
        test2b = "something_else: CTF_FLAG{"
        len2a = self.get_response_length(test2a)
        len2b = self.get_response_length(test2b)
        print("\nTest 2 - Known Text Matching:")
        print(f"Payload '{test2a}': length = {len2a}")
        print(f"Payload '{test2b}': length = {len2b}")
        print(f"Difference: {len2a - len2b}")
        print("Note: Matching existing text compresses better!")

        # Test 3: Partial matches
        test3a = "secret_flag: CTF_FLAG{C"
        test3b = "secret_flag: CTF_FLAG{b"
        len3a = self.get_response_length(test3a)
        len3b = self.get_response_length(test3b)
        print("\nTest 3 - Testing Different Endings:")
        print(f"Payload '{test3a}': length = {len3a}")
        print(f"Payload '{test3b}': length = {len3b}")
        print(f"Difference: {len3a - len3b}")
        print("Note: One might compress better if it matches the real flag!")

        # Test 4: Bonus points.
        test3a = "Cookie: session=www."
        test3b = "Cookie: session=aaa."
        len3a = self.get_response_length(test3a)
        len3b = self.get_response_length(test3b)
        print("\nTest 3 - Try extracting the session key too!:")
        print(f"Payload '{test3a}': length = {len3a}")
        print(f"Payload '{test3b}': length = {len3b}")
        print(f"Difference: {len3a - len3b}")


def main():
    print("CRIME Oracle Demonstration")
    print("=========================")
    print("\nThis demo shows how the CRIME attack works by leveraging")
    print("compression ratios to leak information.")

    print("\nChoose difficulty level:")
    print("1. Normal (Compression only)")
    print("2. Hard (Compression + Encryption)")
    choice = input("Enter choice (1/2): ")

    difficulty = DifficultyLevel.HARD if choice == "2" else DifficultyLevel.NORMAL
    oracle = CompressionOracle(difficulty=difficulty)

    print(f"\nRunning demonstrations in {difficulty.name} mode...")

    # Show basic compression patterns
    oracle.demonstrate_compression_patterns()

    print("\nKey Takeaways:")
    print("1. Repeated/matching text compresses better")
    print("2. We can use this to guess the flag character by character")
    print("3. The response length reveals information about matches")
    if difficulty == DifficultyLevel.HARD:
        print("4. CBC makes things a bit harder, find a solution!")

    print("\nNow you're ready to build your attack in exploit.py!")


if __name__ == "__main__":
    main()
