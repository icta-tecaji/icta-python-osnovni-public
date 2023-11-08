# import paramiko

# ssh_client=paramiko.SSHClient()
# ssh_client.connect(hostname='192.168.56.101', port=2022, username='testuser', password='test')

# - primer 2
import paramiko
ssh_client =paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname='ssh-telnet-test', port=22, username='testuser', password='test')
# neki delamo 
print('Working')
ssh_client.close()