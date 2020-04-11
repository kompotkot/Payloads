"""
> python3 com_nmap-row.py -i 10.11.1.1

TODO:
- Add try to except closed ports
- Add check Host is up
"""
import os
import time
import argparse
import subprocess
from collections import ChainMap, Counter


defaults = {'ip': '10.11.1.250'}

parser = argparse.ArgumentParser(description='Nmap row')
parser.add_argument('-i', '--ip', help='Target (default: 10.11.1.250)')

args = parser.parse_args()
new_dict = {key: value for key, value in vars(args).items() if value}
settings = ChainMap(new_dict, defaults)


def light_scan(ip):
	command = ["nmap", ip, "--top-ports", "100"]
	result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	
	# Output result
	print('Output for Light Scan:')
	result_lines = result.stdout.splitlines()
	
	for line in result_lines:
		print(line)


def heavy_scan(ip):
	target_ports = []
	
	command = ["nmap", ip, "-p-", "-sT", "--reason", "--open"]
	result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	
	# Output result
	print('Output for Heavy Scan:')
	result_lines = result.stdout.splitlines()
	
	for line in result_lines:
		print(line)

	result_out = result.stdout.split('\n')  # Convert output to list

	# Find and clear out ports
	for i, char in enumerate(result_out):
		if 'open' in char:
			port = char.split('/')[0]
			target_ports.append(port)

	return target_ports


def deep_heavy_scan(ip, target_ports):
	target_ports = ','.join(map(str, target_ports))		# Convert list to string

	command = ["nmap", ip, "-p", target_ports, "-sV", "--reason"]
	result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	
	# Output result
	print('Output for Deep Heavy Scan:')
	result_lines = result.stdout.splitlines()
	
	for line in result_lines:
		print(line)


def main():
	startTime = time.time()

	print('\nLight Scan started!#################\n')
	light_scan(settings['ip'])

	print('\nHeavy Scan started!#################\n')
	target_ports = heavy_scan(settings['ip'])

	print('\nDeep Heavy Scan started!############\n')
	deep_heavy_scan(settings['ip'], target_ports)

	print(f'\nRequired time: {time.time() - startTime}')


if __name__ == '__main__':
	main()
