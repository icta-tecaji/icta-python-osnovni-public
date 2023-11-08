import pyshark

cap = pyshark.LiveCapture(interface="wlp4s0")

for packet in cap.sniff_continuously():
    print(packet)
    print(50*"=")