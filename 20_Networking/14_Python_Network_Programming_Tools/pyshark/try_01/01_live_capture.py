import pyshark

capture = pyshark.LiveCapture(interface='wlp4s0') # Poglej da daš ta prav interface kle..
'''
$ ip r | grep default
> default via 10.1.1.1 dev wlp4s0 proto dhcp metric 600 

default interface je wlp4s0
'''
for packet in capture.sniff_continuously(packet_count=5):
    print(packet)
    print(40*"=")
