import pyshark
import requests
import json
from collections import defaultdict
import time

# Dictionnaire pour stocker l'historique par ip
ip_history = defaultdict(lambda: {
    'count': 0,
    'failed_logins': 0,
    'srv_count': 0,
    'last_seen': time.time(),
    'service_ports': set(),
    'failed_attempts': []
})

def extract_features(packet):
    try:
        if not hasattr(packet, 'ip') or not hasattr(packet, 'tcp'):
            return None

        ip_src = packet.ip.src
        ip_dst = packet.ip.dst
        
        # Initialiser toutes les features requises par le modèle
        features = {
            'duration': 0,
            'protocol_type': 'tcp',
            'service': 'other',
            'flag': 'SF',
            'src_bytes': int(packet.length),
            'dst_bytes': 0,
            'land': 0,
            'wrong_fragment': 0,
            'urgent': 0,
            'hot': 0,
            'num_failed_logins': 0,
            'logged_in': 0,
            'num_compromised': 1 if 'attack' in str(packet).lower() else 0,
            'root_shell': 0,
            'su_attempted': 0,
            'num_root': 0,
            'num_file_creations': 0,
            'num_shells': 0,
            'num_access_files': 0,
            'num_outbound_cmds': 0,
            'is_host_login': 0,
            'is_guest_login': 0,
            'count': ip_history[ip_src]['count'] + 1,
            'srv_count': len(ip_history[ip_src]['service_ports']),
            'serror_rate': 0.5 if ip_history[ip_src]['failed_logins'] > 0 else 0,
            'srv_serror_rate': 0,
            'rerror_rate': 0,
            'srv_rerror_rate': 0,
            'same_srv_rate': 0,
            'diff_srv_rate': 0,
            'srv_diff_host_rate': 0,
            'dst_host_count': 0,
            'dst_host_srv_count': 0,
            'dst_host_same_srv_rate': 0,
            'dst_host_diff_srv_rate': 0,
            'dst_host_same_src_port_rate': 0,
            'dst_host_srv_diff_host_rate': 0,
            'dst_host_serror_rate': 0,
            'dst_host_srv_serror_rate': 0,
            'dst_host_rerror_rate': 0,
            'dst_host_srv_rerror_rate': 0
        }

        # Détection du service
        dst_port = str(getattr(packet.tcp, 'dstport', ''))
        if dst_port == '80':
            features['service'] = 'http'
        elif dst_port == '22':
            features['service'] = 'ssh'
            features['num_failed_logins'] = ip_history[ip_src]['failed_logins']

        # Mise à jour de l'historique
        ip_history[ip_src]['count'] += 1
        ip_history[ip_src]['service_ports'].add(dst_port)
        ip_history[ip_src]['last_seen'] = time.time()

        return features
    except Exception as e:
        print(f"Erreur extraction features: {str(e)}")
        return None

def analyze_packet(packet):
    time.sleep(0.1)
    try:
        features = extract_features(packet)
        if not features:
            return

        ip_src = packet.ip.src
        ip_dst = packet.ip.dst if hasattr(packet, 'ip') else 'N/A'
        dst_port = str(getattr(getattr(packet, 'tcp', None), 'dstport', '')) if hasattr(packet, 'tcp') else 'N/A'
        
        # Ajoutez cette ligne pour le logging
        print(f"[NETWORK] {ip_src}:{getattr(packet, 'tcp', {}).srcport or 'N/A'} -> {ip_dst}:{dst_port} Proto: {getattr(packet, 'transport_layer', 'N/A')}")
        
        try:
            response = requests.post(
                'http://172.18.0.2:5000/predict',
                json=features,
                headers={'X-Real-IP': ip_src},
                timeout=3
            )
            if response.status_code == 200 and response.json().get('is_malicious'):
                print(f"🚨 Attaque détectée depuis {ip_src}")
        except Exception as e:
            print(f"Erreur API: {str(e)}")

    except Exception as e:
        print(f"Erreur analyse paquet: {str(e)}")

# Capture en direct sur l'interface réseau eth0
capture = pyshark.LiveCapture(interface='eth0')

# Analyse continue des paquets capturés
for packet in capture.sniff_continuously():
    analyze_packet(packet)