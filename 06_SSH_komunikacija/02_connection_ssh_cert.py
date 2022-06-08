import os

import paramiko

SSH_USERNAME = os.environ.get("MY_SSH_USERNAME", "test")
SSH_PASS = os.environ.get("MY_SSH_PASS", "test")

print(f"Connecting to SSH with cert: {SSH_PASS}. Username: {SSH_USERNAME}")


def execute_command(client: paramiko.SSHClient, command: str):
    stdin, stdout, stderr = client.exec_command(command)
    status = stdout.channel.recv_exit_status()
    if status != 0:
        print(f"Status {status}, message: {stderr.readlines()}")
    response = stdout.read()
    print(response.decode())


if __name__ == "__main__":
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.connect(
        hostname="212.101.140.9", port=2022, username=SSH_USERNAME, passphrase=SSH_PASS
    )
    print("Working")
    execute_command(ssh_client, "ls /")
    execute_command(ssh_client, "uname -a")
    execute_command(ssh_client, "lscpu")

    ssh_client.close()
