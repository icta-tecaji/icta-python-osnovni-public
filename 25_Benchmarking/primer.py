import sys
import csv

with open(sys.argv[1]) as f:
    for row in csv.reader(f):
        # Some kind of processing
        pass

# somescript.py
import sys
import csv


def main(filename):
    with open(filename) as f:
        for row in csv.reader(f):
            # Some kind of processing
            pass


main(sys.argv[1])
