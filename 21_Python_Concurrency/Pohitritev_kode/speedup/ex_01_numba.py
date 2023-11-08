import time

import numpy as np
from numba import jit

start_time = time.time()
x = np.arange(10000).reshape(100, 100)


@jit(nopython=True)  # Set "nopython" mode for best performance, equivalent to @njit
def go_fast(a):  # Function is compiled to machine code when called the first time
    trace = 0.0
    for i in range(a.shape[0]):  # Numba likes loops
        trace += np.tanh(a[i, i])  # Numba likes NumPy functions
    return a + trace  # Numba likes NumPy broadcasting


for _ in range(10000):
    go_fast(x)

end_time = time.time()
print(f"It took {end_time-start_time:.10f} seconds to compute")
