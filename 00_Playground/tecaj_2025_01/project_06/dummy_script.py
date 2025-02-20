import sys
import time

RUN_FAST = False
TOTAL_RUNS = 1


def flush_then_wait():
    sys.stdout.flush()
    sys.stderr.flush()
    time.sleep(0.1) if RUN_FAST else time.sleep(0.5)


print(f"Arguments: {sys.argv}")

if "--run-fast" in sys.argv:
    RUN_FAST = True

is_total_runs = any("--total-runs=" in arg for arg in sys.argv)
if is_total_runs:
    total_runs = next(arg for arg in sys.argv if "--total-runs=" in arg)
    TOTAL_RUNS = int(total_runs.split("=")[1])
    print(f"Total runs: {TOTAL_RUNS}")


for i in range(TOTAL_RUNS):
    print("Script stdout 1\n", file=sys.stdout, flush=True, end="")
    sys.stdout.write("Script stdout 2\n")
    sys.stdout.write("Script stdout 3\n")
    sys.stderr.write("Total time: 00:05:00\n")
    print("Total complete: 10%\n", file=sys.stderr, flush=True, end="")
    flush_then_wait()

    sys.stdout.write("name=Martin\n")
    sys.stdout.write("Script stdout 4\n")
    sys.stdout.write("Script stdout 5\n")
    sys.stderr.write("Total complete: 30%\n")
    flush_then_wait()

    sys.stderr.write("Elapsed time: 00:00:10\n")
    sys.stderr.write("Elapsed time: 00:00:50\n")
    sys.stderr.write("Total complete: 50%\n")
    sys.stdout.write("country=Nederland\n")
    flush_then_wait()

    sys.stderr.write("Elapsed time: 00:01:10\n")
    sys.stderr.write("Total complete: 100%\n")
    sys.stdout.write("Script stdout 6\n")
    sys.stdout.write("Script stdout 7\n")
    sys.stdout.write("website=www.mfitzp.com\n")
    flush_then_wait()
