import re


def grep(pattern, lines):
    RE_FILTER = re.compile(pattern)
    for line in lines:
        if RE_FILTER.search(line):
            yield line


if __name__ == "__main__":
    from follow import follow

    with open("access-log") as log_file:
        loglines = follow(log_file)
        filter_lines = grep(r"python", loglines)

        for line in filter_lines:
            print(line, end="")
