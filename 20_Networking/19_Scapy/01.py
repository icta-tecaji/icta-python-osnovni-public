# sudo -E env PATH=$PATH PYTHONPATH=$PYTHONPATH python3 01.py
#from scapy.all import *
from scapy.all import sr1, IP, ICMP

print(sr1(IP(dst="8.8.8.8")/ICMP()).summary())