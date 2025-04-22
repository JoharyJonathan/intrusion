#!/bin/bash

# Démarrer SSH
service ssh start

# Réinitialiser iptables
iptables -F
iptables -X
iptables -P INPUT DROP
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 5000 -j ACCEPT

# Activer le forwarding
sysctl -w net.ipv4.ip_forward=1

# Initialiser la base de données
sqlite3 /app/db/blacklist.db "CREATE TABLE IF NOT EXISTS blacklist (ip TEXT, timestamp DATETIME, reason TEXT);"

# Démarrer les services
python3 /app/network_monitor.py 2>&1 | tee -a /var/log/ids.log &
tcpdump -i eth0 -w /capture.pcap -G 300 &
cd /app/api && python3 app.py &

# Garder le conteneur actif
tail -f /dev/null