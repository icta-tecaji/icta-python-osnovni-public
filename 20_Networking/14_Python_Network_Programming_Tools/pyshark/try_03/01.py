import pyshark
import matplotlib.pyplot as plt
import numpy as np

# define interface
networkInterface = "wlp4s0"

# define capture object
capture = pyshark.LiveCapture(interface=networkInterface)

print("listening on %s" % networkInterface)

protocol_dict = {}
#for packet in capture.sniff_continuously(packet_count=100):
for packet in capture.sniff_continuously(): # mal drugačno kodo treba za posodabljanje matplotliba če že v tem primeru
   # print(packet)
   protocol = packet.transport_layer
   print(protocol, type(protocol))
   if protocol:
      if protocol in protocol_dict.keys():
         protocol_dict[protocol] += 1
      else:
         protocol_dict[protocol] = 1
   else:
      if "Other" in protocol_dict.keys():
         protocol_dict["Other"] += 1
      else:
         protocol_dict["Other"] = 1

print(protocol_dict)

plt.bar(range(len(protocol_dict)), list(protocol_dict.values()), align='center')
plt.xticks(range(len(protocol_dict)), list(protocol_dict.keys()))

plt.show()
