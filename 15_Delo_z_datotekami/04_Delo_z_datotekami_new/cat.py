import fileinput

with fileinput.input() as files:
    for line in files:
        if fileinput.isfirstline():
            print(f"\n--- Reading {fileinput.filename()} ---")
        print(" -> " + line, end="")
    print()
