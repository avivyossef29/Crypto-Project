from Crypto.Cipher import ARC4
import zlib


def compress_and_encrypt(data):
    return ARC4.new(KEY).encrypt(zlib.compress(data))


def decrypt_and_decompress(data):
    return ARC4.new(KEY).decrypt(zlib.decompress(data))


# TODO: Replace the oracle with a real vurnurable browser.
class EncryptionOracle:
    def __init__(self, key, headers):
        self.key = key
        self.headers = headers

    def process_request(self, request):
        modified_data = self.headers + request
        return compress_and_encrypt(modified_data)


def two_tries_recursive(oracle: EncryptionOracle, found):
    chars = range(33, 127)
    for i in chars:
        # TODO: Introduce varying sized randomness to reduce faiure rate.
        request1 = "cookie=" + "".join(found) + chr(i) + "~#:/[|/ç"
        request2 = "cookie=" + "".join(found) + "~#:/[|/ç" + chr(i)
        enc1 = oracle.process_request(request1.encode())
        enc2 = oracle.process_request(request2.encode())
        if len(enc1) < len(enc2):
            t = list(found)
            t.append(chr(i))
            t_text = "".join(t)
            print(f"\r[+] cookie={t_text}")
            two_tries_recursive(oracle, t)


if __name__ == "__main__":
    KEY = bytearray("AMAZINGKEY".encode())
    SECRET_HEADER = b"HEADERS = SOMETHING, cookie={super_duper_secret_token}"
    oracle = EncryptionOracle(KEY, SECRET_HEADER)
    two_tries_recursive(oracle, [])
