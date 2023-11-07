import pyshark

cap = pyshark.FileCapture("./SSHv2.cap", only_summaries=True, display_filter="ssh") # https://www.wireshark.org/docs/man-pages/wireshark-filter.html

for packet in cap:
    print(packet)
    #print(30*"=")