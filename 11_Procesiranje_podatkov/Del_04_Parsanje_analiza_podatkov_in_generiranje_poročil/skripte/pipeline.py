# pipeline.py
#
# An example of setting up a processing pipeline with generators
import re

def grep(pattern,lines):
    patc = re.compile(pattern)
    for line in lines:
        if patc.search(line):
             yield line

if __name__ == '__main__':
    from follow import follow

    # Set up a processing pipe : tail -f | grep python
    with open("access-log") as logfile:
        loglines = follow(logfile)
        pylines  = grep(r"python", loglines)

        # Pull results out of the processing pipeline
        for line in pylines:
            print(line, end="")