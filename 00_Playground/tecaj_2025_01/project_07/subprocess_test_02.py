import shlex
import subprocess

from loguru import logger

# process = subprocess.run(["dir"], check=False, shell=True)
# print(f"Return code: {process.returncode}")

try:
    process1 = subprocess.Popen(shlex.split("powershell sleep dsdsds4"), shell=True)
    print("[process1] Waiting for the process to complete...")
    process2 = subprocess.run("powershell sleep 2sdsdsd", check=False, shell=True, capture_output=True, text=True, timeout=5)
    print("[process2] Waiting for the process to complete...")
except subprocess.TimeoutExpired as e:
    logger.error(f"Error: {e}")
else:
    if process1.returncode == 1:
        logger.error("Process 1 failed!")
    elif process1.returncode == 0:
        logger.success("Process 1 completed successfully!")
    print(f"[2] Return code: {process2.returncode}")
    print(f"[2] STDOUT Output: {process2.stdout}")
    print(f"[2] STDERR Output: {process2.stderr}")
    process1.wait()
    print(f"[1] Return code: {process1.returncode}")
    print(f"[1] STDOUT Output: {process1.stdout}")
    print(f"[1] STDERR Output: {process1.stderr}")


# process = subprocess.Popen(shlex.split("powershell sleep 2"), shell=True)
# print("Waiting for the process to complete...")
# process.wait()
