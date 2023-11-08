https://linuxhint.com/building-your-own-network-monitor-with-pyshark/

inštaliraš še TShark - https://lindevs.com/install-tshark-on-ubuntu/




Ko zalaufaš:
PermissionError: [Errno 13] Permission denied: '/usr/bin/dumpcap'
SOlution:
$ sudo chmod +x /usr/bin/dumpcap


PyShark uses tshark (so you are using wire sharks ability to capture packets and then you are parsing them in python)


https://github.com/KimiNewt/pyshark - ta model je spisu knjiznjico