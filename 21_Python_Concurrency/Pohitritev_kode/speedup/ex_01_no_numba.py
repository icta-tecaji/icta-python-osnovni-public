import time

import numpy as np

start_time = time.time()
x = np.arange(10000).reshape(100, 100)


def go_fast(a):
    trace = 0.0
    for i in range(a.shape[0]):
        trace += np.tanh(a[i, i])
    return a + trace


for _ in range(10000):
    go_fast(x)

end_time = time.time()
print(f"It took {end_time-start_time:.10f} seconds to compute")
