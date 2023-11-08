from scapy.all import ARP, Ether, srp

target_ip = "10.1.8.1/24" #"192.168.8.1/24"
arp = ARP(pdst=target_ip)

ether = Ether(dst="ff:ff:ff:ff:ff:ff") # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
packet = ether/arp
result = srp(packet, timeout=3)[0] # index 0 are answeres, index 1 are unanswerd packets

print(result)

print("Devices on the network:")
print("IP \t\t\t\t MAC")
for sent, received in result:
    print(f"{received.psrc} \t\t\t {received.hwsrc}")