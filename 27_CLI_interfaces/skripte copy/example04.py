# include standard modules
import getopt, sys

# read commandline arguments, first
fullCmdArguments = sys.argv

# - further arguments
argumentList = fullCmdArguments[1:]

print(argumentList)

unixOptions = "ho:v"
gnuOptions = ["help", "output=", "verbose"]

try:
    arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
except getopt.error as err:
    # output error, and return with an error code
    print(str(err))
    sys.exit(2)

# evaluate given options
for currentArgument, currentValue in arguments:
    if currentArgument in ("-v", "--verbose"):
        print("enabling verbose mode")
    elif currentArgument in ("-h", "--help"):
        print("displaying help")
    elif currentArgument in ("-o", "--output"):
        print(f"enabling special output mode {currentValue}")