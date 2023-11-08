from scapy.all import *

# rdpcap comes from scapy and loads in our pcap file
packets = rdpcap('mycapture.cap')
# Let's iterate through every packet
for packet in packets:
    print(packet.summary())
    wrpcap("moj_capture.pcap", packet, append=True)

print("Pregled")
packets = rdpcap('moj_capture.pcap')

# Let's iterate through every packet
for packet in packets:
    print(packet.summary())
