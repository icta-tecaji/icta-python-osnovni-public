import pyshark

cap = pyshark.LiveCapture(interface="wlp4s0", output_file="moj_cap.cap")

cap.sniff(packet_count=5)
for packet in cap:
    print(packet)
    print(30*"=")

print("\n\n\nBRANJE IZ DATOTEKE")
cap = pyshark.FileCapture("./moj_cap.cap")
for packet in cap:
    print(packet)
    print(30*"=")