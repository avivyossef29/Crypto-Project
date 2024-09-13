import scapy.all as s
import sys

attacker_ip = ""
attacker_mac = ""
victim_ip = ""
victim_mac = ""
server_ip = ""
server_mac = ""

def parse_packet(packet):
    print("=============== got packet ===============")
    print(repr(packet))

    if packet.haslayer(s.Raw):
        print("-----------------------------------------")
        print(packet[s.Raw].load)
        print("-----------------------------------------")
    print("==========================================")
    new_packet = ""
    #s.sendp()

def packet_filter(packet):
    return packet[s.IP].dst == '172.18.0.2'

#def arp_poison():
    #s.ARP(op=2, pdst= , hwdst=, psrc=, hwsrc=)

print('sniff started')
s.conf.L3socket = s.L3RawSocket

s.sniff(iface="eth0", prn=parse_packet)