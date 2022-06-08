import os
from typing import Dict, List
from pathlib import Path
from paramiko import AutoAddPolicy, SSHClient
from scp import SCPClient, SCPException


class BadAuthenticationModeError(Exception):
    pass


class RemoteCommandExecutionErrorCode(Exception):
    pass


def get_default_path() -> str:
    return os.getcwd()


DEFAULT_PATH = get_default_path()


class RemoteClient:
    """Client to interact with remote host via SSH and SCP."""

    def __init__(
        self,
        host: str,
        user: str,
        port: int = 22,
        password: str = None,
        passphrase: str = None,
        allow_all_host_keys: bool = False,
        authentication_mode: str = "password",
    ):
        self.host: str = host
        self.user: str = user
        self.port: int = port
        self.password: str = password
        self.passphrase: str = passphrase
        self.allow_all_host_keys: bool = allow_all_host_keys
        self.authentication_mode: str = authentication_mode
        self.client: SSHClient = None
        self.scp: SCPClient = None

    def __connect(self):
        """Open connection to a remote host."""
        self.client = SSHClient()
        self.client.load_system_host_keys()
        if self.allow_all_host_keys:
            self.client.set_missing_host_key_policy(AutoAddPolicy())
        # set clinet mode
        # TODO June 08, 2022: dodaj error handling
        if self.authentication_mode == "password":
            # TODO June 08, 2022: dodaj nalaganje passworda iz zunanjih virov
            self.client.connect(
                self.host,
                username=self.user,
                timeout=5000,
                port=self.port,
                password=self.password,
            )
        elif self.authentication_mode == "passphrase":
            # TODO June 08, 2022: dodaj nalaganje passworda iz zunanjih virov
            self.client.connect(
                self.host,
                username=self.user,
                timeout=5000,
                port=self.port,
                passphrase=self.passphrase,
            )
        else:
            raise BadAuthenticationModeError(
                "Please use password or passphrase option for authentication_mode!"
            )
        self.scp = SCPClient(self.client.get_transport())
        return self.client

    def execute_command(self, command: str, verbose: bool = True) -> List[str]:
        """Execute a single command."""
        if not self.client:
            self.client = self.__connect()
        sdtin, sdtout, sdterr = self.client.exec_command(command)
        status_code: int = sdtout.channel.recv_exit_status()
        if status_code != 0:
            print(f"--> ERROR EXECUTING COMMAND: {command}")
            raise RemoteCommandExecutionErrorCode(
                f"\nCommand error ->\nStatus: {status_code}\nMessage:\n{sdterr.read().decode()}"
            )
        stdout_text = sdtout.read().decode()
        if verbose:
            print(f"--> EXECUTING COMMAND: {command}")
            print(stdout_text)
        return [result.strip() for result in stdout_text.split("\n") if result != ""]

    def execute_commands(self, *args, verbose: bool = True) -> Dict[str, List[str]]:
        """Execute multiple commands in succession."""
        if isinstance(args[0], list):
            commands = args[0]
        else:
            commands = args
        merged_results = dict()
        for command in commands:
            merged_results[command] = self.execute_command(command, verbose=verbose)
        return merged_results

    def _download_file(self, remote_path: str, local_path: str):
        """Download file from remote host."""
        if not self.client:
            self.client = self.__connect()
        try:
            self.scp.get(remote_path, local_path)
        except SCPException:
            print(f"  -> File missing. Skipping downloading file {remote_path}.")
            self.client = None

    def download_files(
        self, remote_paths: List[str], local_save_location: str = DEFAULT_PATH
    ) -> None:
        os.makedirs(local_save_location, exist_ok=True)
        for remote_path in remote_paths:
            remote_file_name = Path(remote_path).name
            local_path = os.path.join(local_save_location, remote_file_name)
            print(f"Downloading file: {remote_file_name} to local folder: {local_path}")
            self._download_file(remote_path, local_path)

    def download_folder(self):
        pass

    def _upload_file(self):
        pass

    def upload_files(self):
        pass

    def upload_folder(self):
        pass

    def disconnect(self):
        """Close SSH connection."""
        if self.client:
            self.client.close()
