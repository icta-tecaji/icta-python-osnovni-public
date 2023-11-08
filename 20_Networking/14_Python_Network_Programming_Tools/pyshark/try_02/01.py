from modulefinder import packagePathMap
import pyshark

import pyshark
import time

# define interface
networkInterface = "wlp4s0"

# define capture object
capture = pyshark.LiveCapture(interface=networkInterface)

print("listening on %s" % networkInterface)

for packet in capture.sniff_continuously(packet_count=3):
    # get timestamp
    localtime = time.asctime(time.localtime(time.time()))

    print("New packet: ")
    print(f"Packet Layers: \t {packet.layers}")

    # Accessing specific layer
    eth_layer = packet["eth"] # or packet[0]  or  packet.eth
    print(eth_layer)

    print(100*"-")