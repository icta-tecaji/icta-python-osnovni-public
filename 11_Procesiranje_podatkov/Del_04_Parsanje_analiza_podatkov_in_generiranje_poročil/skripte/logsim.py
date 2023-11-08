# logsim.py
import time, random

from data import ips
from data import docs

with open("access-log","w") as f:
    while True:
        time.sleep(random.random())
        n = random.randint(0,len(ips)-1)
        m = random.randint(0,len(docs)-1)
        t = time.time()
        date = time.strftime("[%d/%b/%Y:%H:%M:%S -0600]",time.localtime(t))
        write_String = f'{ips[n]} - - {date} {docs[m]}\n'
        f.write(write_String)
        f.flush()