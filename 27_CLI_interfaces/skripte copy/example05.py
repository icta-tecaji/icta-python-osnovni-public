import subprocess

try:
    out_bytes = subprocess.check_output(['ls','-lah', '/'])
except subprocess.CalledProcessError as e:
    out_bytes = e.output # Output generated before error
    code = e.returncode # Return code

#print(out_bytes, type(out_bytes))
out_text = out_bytes.decode('utf-8')
print(out_text)
