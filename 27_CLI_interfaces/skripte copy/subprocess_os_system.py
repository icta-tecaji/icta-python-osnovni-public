#subprocess_os_system.py
import subprocess
completed = subprocess.run(['ls', '-l'])
print('returncode:', completed.returncode)
