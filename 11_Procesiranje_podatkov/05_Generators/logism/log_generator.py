import random
import time
from data import ips, docs

with open("access-log", "w") as f:
    while True:
        time.sleep(random.random())
        ip_n = random.randint(0, len(ips) - 1)
        docs_n = random.randint(0, len(docs) - 1)
        t = time.time()
        date = time.strftime("[%d/%b/%Y:%H:%M:%S]", time.localtime(t))
        f.write(f"{ips[ip_n]} -- {date} {docs[docs_n]}\n")
        f.flush()
