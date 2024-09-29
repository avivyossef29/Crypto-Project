from scapy.all import *
import sys
import os
import time

victim_ip = "192.168.10.4"
victim_mac = "02:42:ac:11:00:01"
server_ip = "192.168.10.2"
server_mac = "02:42:ac:11:00:00"

# def run_script(cookie):
#     for i in range(16):
#         load = create_load()
#         pkt = IP(src=victim_ip, dst=server_ip) / TCP(sport= '10000', dport='443', seq=0, ack=0, flags="PA") / Raw(load=load)

# def create_load():
#     return "POST /aaaaaaa HTTP/1.1\r\nHost: server_container\r\nsessioncookie: \r\naaaaaaaaaaa"

# def find_byte():


def parse_packet(packet):
    if packet.haslayer(Raw) and packet.haslayer(IP):
        print("-----------------------------------------")
        print('-=-=-=-=-' + str(len(packet[Raw].load)) + '-=-=-=-=-')
        if len(packet[Raw].load) == 394:
            print_packet(packet)
            #forge_packet(packet, 0)
        else:
            packet.show()
        print("-----------------------------------------")


def print_packet(packet):
    packet = packet[Raw].load
    print([hex(i) for i in packet])

def forge_packet(packet, i):
    new_packet = packet[Raw].load
    #new_packet = new_packet[:-16] + new_packet[16 * i : 16 * (i + 1) - 1] + new_packet[-1]   
    #new_packet = new_packet[:-16] + new_packet[16 * i : 16 * (i + 1)]
    #packet[Raw].load = new_packet
    time.sleep(10)
    print('scapy sending packet')
    send(packet)


print('sniff started')
conf.L3socket = L3RawSocket

sniff(iface="eth0", prn=parse_packet)
