import json
from pathlib import Path
from colorama import Fore, Style
import os
from sshclient.remote_client import RemoteClient


def get_absolute_file_path(relative_path: str) -> str:
    return str(Path(__file__).parent.joinpath(relative_path))


def load_hosts_data():
    with open(get_absolute_file_path("hosts.json")) as fp:
        remote_hosts_data = json.load(fp)
        return remote_hosts_data["hosts"]


if __name__ == "__main__":
    REMOTE_HOSTS = load_hosts_data()

    for remote_host in REMOTE_HOSTS:
        client = RemoteClient(
            host=remote_host["ip"],
            port=remote_host["port"],
            user=remote_host["username"],
            authentication_mode="password",
            allow_all_host_keys=True,
        )
        print(f"{Fore.YELLOW}**************************************************")
        print(f"Connecting to host: {remote_host['name']}, IP: {remote_host['ip']}")
        print(f"**************************************************{Style.RESET_ALL}")
        print()
        local_folder = get_absolute_file_path(f"hosts_logs/{remote_host['name']}")
        os.makedirs(local_folder, exist_ok=True)
        client.execute_command(
            "echo test | sudo -S chown -R testuser:testuser /var/log", verbose=True
        )

        client.download_folder("/var/log", local_folder)

    client.disconnect()
