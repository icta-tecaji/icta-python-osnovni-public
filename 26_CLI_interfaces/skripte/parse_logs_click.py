import click
import csv
import sys
import os
from tqdm import tqdm

def parse_web_logs(input_file, mode='all', header=True):
    ips = {}
    statuses = {}
    with open(input_file, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        line_count = 0
        for key in tqdm(range(100)):
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


@click.command()
@click.argument('file_path')
@click.option('-m', '--mode', help="select the mode of the parser [all, ip, status]", default='all',  metavar='MODE', type=click.Choice(['all', 'ip', 'status']))
@click.option('--header/--no-header', help='add this if there is no header in log file', default=True)
def parse(file_path, mode, header):
    if os.path.exists(file_path):
        parse_web_logs(file_path, mode=mode, header=header)
    else:
        click.echo('The path specified does not exist!')
        sys.exit()
        

if __name__ == '__main__':
    parse()