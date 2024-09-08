import scapy.all as s

def parse_packet(packet):
    print(packet)

s.conf.L3socket = s.L3RawSocket

s.sniff(prn=parse_packet)