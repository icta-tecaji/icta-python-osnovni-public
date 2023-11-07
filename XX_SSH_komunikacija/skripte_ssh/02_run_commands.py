import paramiko

def execute_command(client, command):
    """Execute command in succession."""
    stdin, stdout, stderr = client.exec_command(command)
    status = stdout.channel.recv_exit_status()
    if status != 0:
        print(f'Status: {status}, message: {stderr.readlines()}')
    response = stdout.readlines()
    client.close()
    print(response)

ssh_client =paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname='ssh-telnet-test', port=22, username='testuser', password='test')
command = "uname -a"

execute_command(ssh_client, command)