# # myls_argp.py
# # Import the argparse library
# import argparse

# import os
# import sys

# # Create the parser
# my_parser = argparse.ArgumentParser(prog='myls',
#                                     description='List the content of a folder')

# # Add the arguments
# my_parser.add_argument('Path',
#                        metavar='path',
#                        type=str,
#                        help='the path to list')

# # Execute the parse_args() method
# args = my_parser.parse_args()

# input_path = args.Path

# if not os.path.isdir(input_path):
#     print('The path specified does not exist')
#     sys.exit()

# print('\n'.join(os.listdir(input_path)))

# myls.py
# Import the argparse library
import argparse

import os
import sys

# Create the parser
my_parser = argparse.ArgumentParser(description='List the content of a folder')

# Add the arguments
my_parser.add_argument('Path',
                       metavar='path',
                       type=str,
                       help='the path to list')
my_parser.add_argument('-l',
                       '--long',
                       action='store_true',
                       help='enable the long listing format')

# Execute parse_args()
args = my_parser.parse_args()

input_path = args.Path

if not os.path.isdir(input_path):
    print('The path specified does not exist')
    sys.exit()

for line in os.listdir(input_path):
    if args.long:  # Simplified long listing
        size = os.stat(os.path.join(input_path, line)).st_size
        line = f'{size:10d}  {line}'
    print(line)