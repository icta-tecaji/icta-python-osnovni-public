import paramiko

def execute_command(client, command):
    """Execute command in succession."""
    stdin, stdout, stderr = client.exec_command(command)
    #dodatek
    stdin.write('blu8z3\n')
    status = stdout.channel.recv_exit_status()
    if status != 0:
        print(f'Status: {status}, message: {stderr.readlines()}')
    response = stdout.readlines()
    client.close()
    print(response)

ssh_client =paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname='192.168.56.101', port=2022, username='testuser', password='test')
command = "sudo ls"

execute_command(ssh_client, command)