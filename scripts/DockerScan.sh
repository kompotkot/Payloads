#!/bin/bash

# COLORS
C_RESET='\033[0m'
C_RED='\033[1;31m'
C_GREEN='\033[1;32m'

# PROPS
HOST="172.17.0."
IP_START=1
IP_END=10
IP_PORT=22

# FUNCTIONS
function ip_scan {
  for i in $(seq $IP_START $IP_END); do
    ping -W 1 -c 1 ${HOST}${i} > /dev/null && 
    echo -e "${C_GREEN}Host Alive: ${HOST}${i}${C_RESET}" || 
    echo "Host Dead: ${HOST}${i}"
  done
}

function port_scan {
  for i in $(seq $IP_START $IP_END); do
    # Add 2>/dev/null before > /dev/tcp to hide errors
    echo "test" > /dev/tcp/${HOST}${i}/${IP_PORT} &&
    echo -e "${C_GREEN}PORT ${IP_PORT} Alive: ${HOST}${i}${C_RESET}" ||
    echo "PORT ${IP_PORT} Dead: ${HOST}${i}"
  done
}

# MAIN
if [[ $1 == "ip" ]]; then
  ip_scan
elif [[ $1 == "port" ]]; then
  port_scan
else
  echo -e "Use ${C_RED}ip${C_RESET} or ${C_RED}port${C_RESET} as second argument"
fi

