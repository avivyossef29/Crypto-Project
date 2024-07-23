from scapy.all import sniff, Raw, TCP
'''
def packet_callback(packet):
    if packet.haslayer(TCP):
        tcp_layer = packet.getlayer(TCP)
        if tcp_layer.sport == 1337 or tcp_layer.dport == 1337:
            print(f"Packet {packet.summary()}")
            if packet.haslayer(Raw):
                raw_data = packet.getlayer(Raw).load
                print(f"Data: {raw_data}")

# Sniff packets on the loopback interface
print("Starting packet sniffer on loopback interface...")
sniff(iface= '\\Device\\NPF_Loopback',filter='tcp', prn=packet_callback, store=0)
'''

stop_sniffing = False
captured_packet = None

def packet_callback(packet):
    global stop_sniffing,captured_packet
    # Check if the packet has a TCP layer and the port is 1337
    if TCP in packet and (packet[TCP].sport == 1337 or packet[TCP].dport == 1337):
        # Check if the packet has a Raw layer (data)
        if Raw in packet:
            captured_packet = packet
            print(f"Packet captured with data: {packet[Raw].load}")
            stop_sniffing = True

def stop_filter(packet):
    # Use the global variable to decide whether to stop sniffing
    return stop_sniffing

# Start sniffing packets with the custom stop filter
sniff(iface= '\\Device\\NPF_Loopback',filter='tcp',prn=packet_callback, stop_filter=stop_filter)

# The following code will execute after sniffing stops
print("Sniffing stopped. Processing captured packet data...")
