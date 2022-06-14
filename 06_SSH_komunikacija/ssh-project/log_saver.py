from sshclient.remote_client import RemoteClient


if __name__ == "__main__":
    client = RemoteClient(
        host="212.101.140.9",
        port=2022,
        user="testuser",
        authentication_mode="passphrase",
    )
    client.execute_command("ls ~", verbose=True)
    client.disconnect()
