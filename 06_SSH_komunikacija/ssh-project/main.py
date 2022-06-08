from sshclient.remote_client import RemoteClient, RemoteCommandExecutionErrorCode


if __name__ == "__main__":
    client = RemoteClient(
        host="212.101.140.9",
        port=2022,
        user="testuser",
        password="test",
        authentication_mode="password",
    )
    try:
        results = client.execute_command("ls /", verbose=False)
        print(results)
        results = client.execute_commands("uname -a", "pwd", "ls /", verbose=False)
        print(results)
        results = client.execute_commands(["uname -a", "pwd", "ls /"], verbose=False)
        print(results)
        client.execute_command("nekei")
    except RemoteCommandExecutionErrorCode as err:
        print(err)

    client.disconnect()
