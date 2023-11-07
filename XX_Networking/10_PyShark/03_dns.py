import pyshark

cap = pyshark.LiveCapture("wlp4s0")

for packet in cap.sniff_continuously():
    if "dns" in packet:
        if packet.dns.qry_name:
            if "ip" in packet:
                print(f"DNS request from {packet.ip.src}: {packet.dns.qry_name}")
            elif "ipv6" in packet:
                print(f"DNS request from {packet.ipv6.src}: {packet.dns.qry_name}")