import pyshark
import pandas as pd

def pcap_to_csv(pcap_file, csv_file):
    # Lire le fichier pcap
    capture = pyshark.FileCapture(pcap_file)
    
    # Extraire les données pertinentes
    data = []
    for packet in capture:
        try:
            row = {
                'timestamp': packet.sniff_time,
                'src_ip': packet.ip.src,
                'dst_ip': packet.ip.dst,
                'protocol': packet.transport_layer,
                'length': packet.length,
                'flags': packet.tcp.flags if hasattr(packet, 'tcp') else None
            }
            data.append(row)
        except AttributeError:
            continue
    
    # Convertir en DataFrame et sauvegarder en CSV
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)

if __name__ == '__main__':
    pcap_to_csv('capture.pcap', 'traffic.csv')