import paramiko

def execute_command(client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    status = stdout.channel.recv_exit_status()
    if status != 0:
        print(f'Status: {status}, message: {stderr.readlines()}')
    respose = stdout.readlines()
    for line in respose:
        print(line)

ssh_client = paramiko.SSHClient()
ssh_client.load_system_host_keys()
ssh_client.connect(hostname='ssh-telnet-test', port=22, username='testuser', password='test', passphrase='plume')
print('Connected...')
execute_command(ssh_client, 'mkdir -v test_01')
ssh_client.close()
print('Connection closed...')

 
