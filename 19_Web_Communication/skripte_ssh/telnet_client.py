import getpass
import telnetlib

HOST = "ssh-telnet-test"

user = 'testuser' 
#user = input("Enter your remote account: ")

password = 'test' 
#password = getpass.getpass()


with telnetlib.Telnet(HOST) as tn:
    tn.read_until(b"login: ")
    tn.write(user.encode('ascii') + b"\n")

    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

    tn.write(b"ls\n")
    tn.write(b"mkdir /home/testuser/telnet-test \n")

    tn.write(b"exit\n")

    print(tn.read_all().decode('ascii'))