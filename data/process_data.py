import pandas as pd
import os

columns = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins',
    'logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root',
    'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds',
    'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate',
    'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
    'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
    'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'label', 'difficulty'
]

def preprocess_data():
    # Chemin corrigé avec os.path.join
    train_path = os.path.join('KDDTrain+.txt')
    test_path = os.path.join('KDDTest+.txt')
    
    train = pd.read_csv(train_path, names=columns, usecols=columns[:-1])
    test = pd.read_csv(test_path, names=columns, usecols=columns[:-1])
    
    # Fusionner les données
    full_data = pd.concat([train, test])
    
    # Encodage des catégories avec drop_first=True pour éviter la colinéarité
    protocol_dummies = pd.get_dummies(full_data['protocol_type'], prefix='protocol', drop_first=True)
    service_dummies = pd.get_dummies(full_data['service'], prefix='service', drop_first=True)
    flag_dummies = pd.get_dummies(full_data['flag'], prefix='flag', drop_first=True)
    
    # Fusion et sauvegarde
    processed = pd.concat([
        full_data.drop(['protocol_type', 'service', 'flag'], axis=1),
        protocol_dummies,
        service_dummies,
        flag_dummies
    ], axis=1)
    
    # Sauvegarde dans le dossier courant ('data' si exécuté depuis le dossier parent)
    processed.to_csv('processed_data.csv', index=False)
    print(f"Fichier généré : {os.path.abspath('processed_data.csv')}")

if __name__ == '__main__':
    preprocess_data()