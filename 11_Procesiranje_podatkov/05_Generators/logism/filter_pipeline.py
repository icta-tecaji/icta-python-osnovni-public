import re
import sys
from re import Pattern

from follow import follow


def grep(pattern: Pattern, lines_gen):
    for line in lines_gen:
        if pattern.search(line):
            yield line


if __name__ == "__main__":
    with open("access-log") as logfile:
        pattern = sys.argv[1]
        pattern = re.compile(pattern)
        loglines = follow(logfile)
        filtered_lines = grep(pattern, loglines)

        for line in filtered_lines:
            print(line, end="")
