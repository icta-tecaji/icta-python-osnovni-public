import argparse
import csv
import sys
import os

def parse_web_logs(input_file, mode='all', header=True):
    ips = {}
    statuses = {}
    with open(input_file, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if header and line_count == 0:
                line_count += 1
            else:
                if row[0].startswith('[') or row[0][0].isalpha():
                    continue
                ip = row[0]
                status = int(row[3])
                ips[ip] = ips.get(ip,0) + 1
                statuses[status] = statuses.get(status,0) + 1
                line_count += 1 
    
    if mode == 'all':
        print(f'IP: {ips}\nStatus codes: {statuses}')
    elif mode == 'ip':
        print(f'IP: {ips}')
    elif mode == 'status':
        print(f'Status codes: {statuses}')
    else:
        return None

#1-python3 parse_logs.py <IME_DATOTEKE> --count <ALL/IP/STATUS> --no-header
def parse():
    parser = argparse.ArgumentParser(prog='weblogpars',
                                     description='Pars the logs from the web server and sums IPs and status codes.')
    
    parser.add_argument('path',
                       metavar='FILE_PATH',
                       type=str,
                       help='the path to the file to parse')

    parser.add_argument('-m', '--mode', 
                        dest='mode', 
                        metavar='MODE', 
                        action='store', 
                        default='all',  
                        help="select the mode of the parser [all, ip, status]", 
                        choices=['all', 'ip', 'status'])

    parser.add_argument('-no', '--no-header', 
                        dest='no_header', 
                        action='store_false',
                        help='add this if there is no header in log file')
    
    args = parser.parse_args()

    file_path = args.path
    mode = args.mode
    header = args.no_header

    
    if os.path.exists(file_path):
        parse_web_logs(file_path, mode=mode, header=header)
    else:
        print('The path specified does not exist!')
        sys.exit()

if __name__ == '__main__':
    parse()
    