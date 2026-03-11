#!/usr/bin/env bash
set -euo pipefail

ROLE="${1:-}"

PROXY_IP="YOUR_IP_SERVER"
BACKEND_IP="YOUR_IP_SERVER"

if [[ -z "$ROLE" ]]; then
  echo "Usage: $0 proxy|backend"
  exit 1
fi

iptables -F
iptables -X
iptables -t nat -F

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

if [[ "$ROLE" == "proxy" ]]; then
  iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
  iptables -A INPUT -p tcp -s 127.0.0.1 --dport 6379 -j ACCEPT

elif [[ "$ROLE" == "backend" ]]; then
  iptables -A INPUT -p tcp -s "$PROXY_IP" --dport 8080 -j ACCEPT
  iptables -A INPUT -p tcp -s 127.0.0.1 --dport 5432 -j ACCEPT

else
  echo "Unknown role: $ROLE"
  exit 1
fi

echo "Rules applied for $ROLE"
iptables -S
