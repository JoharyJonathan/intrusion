from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import pandas as pd
from datetime import datetime, timedelta
import sqlite3
import os
import subprocess
import traceback

import logging
logging.basicConfig(filename='api.log', level=logging.INFO)

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/model/intrusion_detection.joblib'))
model = joblib.load(MODEL_PATH)
blacklist = {}
request_count = 0
malicious_count = 0

def init_db():
    conn = sqlite3.connect('blacklist.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS blacklist
                 (ip TEXT, timestamp DATETIME, reason TEXT)''')
    conn.commit()
    conn.close()
    
@app.route('/blacklist', methods=['GET'])
def get_blacklist():
    conn = sqlite3.connect('blacklist.db')
    c = conn.cursor()
    c.execute("SELECT * FROM blacklist")
    results = c.fetchall()
    conn.close()

    blacklist_data = [{'ip': row[0], 'timestamp': row[1], 'reason': row[2]} for row in results]
    return jsonify(blacklist_data)

@app.route('/predict', methods=['POST'])
def predict():
    global request_count, malicious_count
    
    try:
        data = request.json
        request_count += 1
        
        # Vérifier que toutes les features nécessaires sont présentes
        expected_columns = model.feature_names_in_
        
        # Créer un dictionnaire avec toutes les features initialisées à 0
        complete_data = {feature: 0 for feature in expected_columns}
        
        # Mettre à jour avec les données reçues
        for key in data:
            if key in complete_data:
                complete_data[key] = data[key]
            else:
                print(f"Feature inattendue reçue: {key}")
        
        # Convertir en DataFrame
        features = pd.DataFrame([complete_data], columns=expected_columns)
        
        # Faire la prédiction
        prediction = model.predict(features)[0]
        
        # Utiliser l'IP du header X-Real-IP si disponible
        ip = request.headers.get('X-Real-IP', request.remote_addr)
        
        if prediction == 1:
            malicious_count += 1
            blacklist[ip] = blacklist.get(ip, 0) + 1
            print(f"⚠️ Activité suspecte détectée depuis {ip} (score: {blacklist[ip]}/3)")
            
            if blacklist[ip] >= 3:
                try:
                    subprocess.run(f"iptables -A INPUT -s {ip} -j DROP", shell=True, check=True)
                    conn = sqlite3.connect('blacklist.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO blacklist VALUES (?, ?, ?)", 
                            (ip, datetime.now(), "Multiple suspicious attempts"))
                    conn.commit()
                    conn.close()
                    print(f"🚨 IP bloquée: {ip}")
                except subprocess.CalledProcessError as e:
                    print(f"Erreur iptables: {e}")
        
        print(f"""
        [DEBUG] Requête de {ip}
        Prédiction: {'Malveillante' if prediction else 'Normale'}
        Compteur actuel: {blacklist.get(ip, 0)}/3
        """)
        
        return jsonify({
            'is_malicious': bool(prediction),
            'current_score': blacklist.get(ip, 0)
        })
    
    except Exception as e:
        error_message = traceback.format_exc()
        logging.error(f"Erreur dans /predict : {error_message}")
        print(f"Erreur dans /predict : {error_message}")
        return jsonify({'error': 'Erreur interne du serveur'}), 500

@app.route('/stats')
def stats():
    conn = sqlite3.connect('blacklist.db')
    c = conn.cursor()
    
    # IPs bloquées
    c.execute("SELECT COUNT(DISTINCT ip) FROM blacklist")
    blocked_count = c.fetchone()[0]
    
    # Dernières attaques
    c.execute("SELECT ip, timestamp, reason FROM blacklist ORDER BY timestamp DESC LIMIT 5")
    recent_attacks = [{'ip': row[0], 'time': row[1], 'reason': row[2]} for row in c.fetchall()]
    
    conn.close()
    
    return jsonify({
        'total_requests': request_count,
        'malicious_requests': malicious_count,
        'blocked_ips': blocked_count,
        'recent_attacks': recent_attacks
    })

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)