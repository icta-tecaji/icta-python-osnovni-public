from client import RemoteClient
from files import fetch_local_files

host = "ssh-telnet-test"
port = 22
# credentials
user = "testuser"
password = "test"
passphrase = "plume"
# file upload
local_file_directory = "/home/plume/vsebina/osnovni_tecaj/11_Interakcija_SSH_Telnet/skripte/ssh_scp_module/data"
remote_path = "/home/testuser"


def main():
    """Initialize remote host client and execute actions."""
    remote = RemoteClient(
        host,
        user,
        passphrase=passphrase,
        password=password,
        remote_path=remote_path,
        port=22,
    )
    # ODKOMENTIRAMO KAR RABIMO
    # execute_command_on_remote(remote)
    download_file_from_remote(remote)
    # upload_files_to_remote(remote)
    remote.disconnect()


def execute_command_on_remote(remote):
    """Execute UNIX command on the remote host."""
    remote.execute_commands(["unadddme -a", "ls", "touch test.txt"])


def upload_files_to_remote(remote):
    """Upload files to remote via SCP."""
    files = fetch_local_files(local_file_directory)
    remote.bulk_upload(files)


def download_file_from_remote(remote):
    remote.download_file("/home/testuser/some.txt")


main()
