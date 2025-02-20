import subprocess

from loguru import logger

# process = subprocess.run(["dir"], check=False, shell=True)
# print(f"Return code: {process.returncode}")

try:
    process1 = subprocess.run("powershell sleep 4", check=False, shell=True, capture_output=True, text=True, timeout=5)
    process2 = subprocess.run("powershell sleep 2", check=False, shell=True, capture_output=True, text=True, timeout=5)
    print("Waiting for the process to complete...")
except subprocess.TimeoutExpired as e:
    logger.error(f"Error: {e}")
except subprocess.CalledProcessError as e:
    logger.error(f"Error: {e}")
else:
    print(f"[1] Return code: {process1.returncode}")
    print(f"[1] STDOUT Output: {process1.stdout}")
    print(f"[1] STDERR Output: {process1.stderr}")
    print(f"[2] Return code: {process2.returncode}")
    print(f"[2] STDOUT Output: {process2.stdout}")
    print(f"[2] STDERR Output: {process2.stderr}")
