import time

start_time = time.time()

for i in range(100):
    print(i)

end_time = time.time()
print(f"It took {end_time-start_time:.10f} seconds to compute")
