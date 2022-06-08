import paramiko
import os

SSH_USERNAME = os.environ.get("MY_SSH_USERNAME", "test")
SSH_PASSWORD = os.environ.get("MY_SSH_PASSWORD", "test")
print(f"Connecting to SSH with username: {SSH_USERNAME} and password: {SSH_PASSWORD}.")

ssh_client = paramiko.SSHClient()
# ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.load_system_host_keys()
ssh_client.connect(
    hostname="212.101.140.9", port=2022, username=SSH_USERNAME, password=SSH_PASSWORD
)

print("Working")
ssh_client.close()
