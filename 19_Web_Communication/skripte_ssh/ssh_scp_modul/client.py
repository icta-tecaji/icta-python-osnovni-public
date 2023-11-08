"""Remote host object to handle connections and actions."""
import sys
from loguru import logger
from os import system
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient, SCPException

logger.add(sys.stderr, format="{time} {message}", filter="client", level="INFO")

logger.add(
    "logs/log_{time:YYYY-MM-DD}.log",
    format="{time} {level} {message}",
    filter="client",
    level="INFO",
)


class RemoteClient:
    """Client to interact with a remote host via SSH & SCP."""

    def __init__(
        self, host, user, password=None, passphrase=None, remote_path="~/", port=22
    ):
        self.host = host
        self.user = user
        self.password = password
        self.passphrase = passphrase
        self.remote_path = remote_path
        self.port = port
        self.client = None
        self.scp = None

    # Open and close remote SSH and SCP connections.
    # ------------------------------------------------------
    def __connect(self):
        """Open connection to remote host."""
        self.client = SSHClient()
        # self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(
            self.host,
            username=self.user,
            timeout=5000,
            port=self.port,
            passphrase=self.passphrase,
            password=self.password,
        )
        self.scp = SCPClient(self.client.get_transport())
        return self.client

    def disconnect(self):
        """Close ssh connection."""
        self.client.close()
        self.scp.close()

    # Execute commands on your remote host.
    # ------------------------------------------------------
    def execute_commands(self, commands):
        """Execute multiple commands in succession."""
        if self.client is None:
            self.client = self.__connect()
        for cmd in commands:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            status = stdout.channel.recv_exit_status()
            if status != 0:
                logger.error(f"Status: {status}, message: {stderr.readlines()}")
            response = stdout.readlines()
            for line in response:
                logger.info(f"INPUT: {cmd} | OUTPUT: {line}")
            logger.info(f"------------------------------")

    # Upload or download files from host.
    # ------------------------------------------------------
    def download_file(self, file):
        """Download file from remote host."""
        if self.client is None:
            self.client = self.__connect()
        self.scp.get(file)

    def bulk_upload(self, files):
        """Upload multiple files to a remote directory."""
        if self.client is None:
            self.client = self.__connect()
        uploads = [self.__upload_single_file(file) for file in files]
        logger.info(
            f"Finished uploading {len(uploads)} files to {self.remote_path} on {self.host}"
        )

    def __upload_single_file(self, file):
        """Upload a single file to a remote directory."""
        try:
            self.scp.put(file, recursive=True, remote_path=self.remote_path)
        except SCPException as error:
            logger.error(error)
            raise error
        finally:
            logger.info(f"Uploaded {file} to {self.remote_path}")
