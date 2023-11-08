import fileinput

with fileinput.input() as files:
    for line in files:
        if fileinput.isfirstline():
            print(f"\n----- {fileinput.filename()} -----\n")
        print(line, end="")
