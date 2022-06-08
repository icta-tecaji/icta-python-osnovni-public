from sshclient.remote_client import RemoteClient


if __name__ == "__main__":
    client = RemoteClient(
        host="212.101.140.9", port=2022, user="testuser", password="test"
    )
    print("working")
    client.execute_command("nekei")
    client.disconnect()
