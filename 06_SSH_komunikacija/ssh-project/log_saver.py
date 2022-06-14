import json
from pathlib import Path
from colorama import Fore, Style

from sshclient.remote_client import RemoteClient


def get_absolute_file_path(relative_path: str) -> str:
    return str(Path(__file__).parent.joinpath(relative_path))


def load_hosts_data():
    with open(get_absolute_file_path("hosts.json")) as fp:
        remote_hosts_data = json.load(fp)
        return remote_hosts_data["hosts"]


if __name__ == "__main__":
    REMOTE_HOSTS = load_hosts_data()
    print(REMOTE_HOSTS)

    for remote_host in REMOTE_HOSTS:
        client = RemoteClient(
            host=remote_host["ip"],
            port=remote_host["port"],
            user=remote_host["username"],
            authentication_mode="password",
        )
        print(f"{Fore.YELLOW}**************************************************")
        print(f"Connecting to host: {remote_host['name']}, IP: {remote_host['ip']}")
        print(f"**************************************************{Style.RESET_ALL}")
        print()

    # client.execute_command("ls ~", verbose=True)
    # client.disconnect()
