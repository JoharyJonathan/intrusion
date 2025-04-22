from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib

def train_intrusion_model():
    # Charger les données
    data = pd.read_csv('../data/processed_data.csv')
    
    # Vérifier les colonnes non numériques
    non_numeric = data.drop('label', axis=1).select_dtypes(include=['object']).columns
    if len(non_numeric) > 0:
        raise ValueError(f"Colonnes non numériques détectées : {non_numeric.tolist()}")
    
    # Séparer les features et la target
    # On ne garde que les colonnes numériques et on exclut 'label'
    X = data.drop(['label'], axis=1)
    
    # Convertir la target en binaire (0 = normal, 1 = anomalie)
    y = data['label'].apply(lambda x: 0 if x == 'normal' else 1)
    
    # Séparation train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Création et entraînement du modèle
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1  # Utiliser tous les cœurs disponibles
    )
    model.fit(X_train, y_train)
    
    # Évaluation
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy:.4f}")
    
    # Sauvegarde du modèle
    joblib.dump(model, 'intrusion_detection.joblib')
    print("Modèle sauvegardé avec succès.")

if __name__ == '__main__':
    train_intrusion_model()