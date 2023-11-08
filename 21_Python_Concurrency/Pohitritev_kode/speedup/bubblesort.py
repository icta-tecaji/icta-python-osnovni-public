import time
import numpy as np

original = np.arange(0.0, 30.0, 0.01, dtype="f4")
shuffled = original.copy()
np.random.shuffle(shuffled)

start_time = time.time()


def bubblesort(X):
    N = len(X)
    for end in range(N, 1, -1):
        for i in range(end - 1):
            cur = X[i]
            if cur > X[i + 1]:
                tmp = X[i]
                X[i] = X[i + 1]
                X[i + 1] = tmp


bubblesort(shuffled)

end_time = time.time()
print(f"It took {end_time-start_time:.10f} seconds to compute")
