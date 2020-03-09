#!/bin/bash

# Simple zone transfer script, if no $1 arg - show info about script

if [ -z "$1" ]; then
	echo "[*] Simple Zone transfer scan"
	echo "[*] Usage: $0 <domain name>"
	exit 0
fi

for server in $(host -t ns $1 | cut -d " " -f4); do
	# For each of these servers, attempt a zone transfer
	host -l $1 $server | grep "has address"
done
