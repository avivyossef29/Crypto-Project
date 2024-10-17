from scapy.all import *
import sys
import os
import time

fake_packet = {}

# def run_script(cookie):
#     for i in range(16):
#         load = create_load()
#         pkt = IP(src=victim_ip, dst=server_ip) / TCP(sport= '10000', dport='443', seq=0, ack=0, flags="PA") / Raw(load=load)

# def create_load():
#     return "POST /aaaaaaa HTTP/1.1\r\nHost: server_container\r\nsessioncookie: \r\naaaaaaaaaaa"

# def find_byte():

def parse_packet(packet):
    global fake_packet
    if True:
        print("-----------------------------------------")
        packet.show()
        # if packet[IP].src == victim_ip and len(packet[Raw].load) == 394:
        #     fake_packet = packet
        #     print("updated packet")
        # if packet[IP].src == server_ip and len(packet[Raw].load) == 586:
        #     forge_packet(packet, 0)
        print("-----------------------------------------")


def print_packet(packet):
    packet = packet[Raw].load
    print([hex(i) for i in packet])

def forge_packet(packet, i):
    #new_packet = packet[Raw].load
    #new_packet = new_packet[:-16] + new_packet[16 * i : 16 * (i + 1) - 1] + new_packet[-1]   
    #new_packet = new_packet[:-16] + new_packet[16 * i : 16 * (i + 1)]
    #packet[Raw].load = new_packet
    fake_packet[TCP].ack = packet[TCP].seq + len(packet[Raw].load)
    fake_packet[TCP].seq = packet[TCP].ack
    print('scapy sending packet')
    fake_packet.show()
    send(fake_packet)


print('sniff started')
conf.L3socket = L3RawSocket

sniff(iface="eth0", prn=parse_packet)
