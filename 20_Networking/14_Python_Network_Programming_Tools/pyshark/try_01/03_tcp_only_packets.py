import pyshark

capture = pyshark.LiveCapture(interface='wlp4s0', bpf_filter='tcp port 80')
capture.sniff(packet_count=5) # zdej mamo .sniff , prej smo mel .sniff_continiously()
print(capture)
for packet in capture:
    print(packet.highest_layer)
