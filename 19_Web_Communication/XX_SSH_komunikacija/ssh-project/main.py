from sshclient.remote_client import RemoteClient


if __name__ == "__main__":
    client = RemoteClient(
        host="212.101.140.9",
        port=2022,
        user="testuser",
        password="test",
        authentication_mode="password",
    )
    # try:
    #     results = client.execute_command("ls /", verbose=False)
    #     print(results)
    #     results = client.execute_commands("uname -a", "pwd", "ls /", verbose=False)
    #     print(results)
    #     results = client.execute_commands(["uname -a", "pwd", "ls /"], verbose=False)
    #     print(results)
    #     client.execute_command("nekei")
    # except RemoteCommandExecutionErrorCode as err:
    #     print(err)

    # client.execute_command("touch ~/test.txt", verbose=True)
    # client.execute_command("touch ~/test2.txt", verbose=True)
    # client.execute_command("touch ~/test3.txt", verbose=True)

    # client.download_files(
    #     ["~/test.txt"],
    #     local_save_location="/home/administrator/izobrazevanje-python-osnovni-plume/data",
    # )
    # client.download_files(["~/test2.txt", "~/test3.txt"])

    # client.download_folder("/home/testuser/test")
    client.upload_files(
        ["remote_client.py", "main.py"], remote_save_location="~/nova_mapa"
    )
    client.upload_folder("sshclient")
    client.execute_command("ls ~", verbose=True)
    client.execute_command("ls ~/nova_mapa", verbose=True)
    client.disconnect()
