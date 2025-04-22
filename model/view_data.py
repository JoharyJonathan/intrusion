import pandas as pd

def inspect_csv():
    data = pd.read_csv('../data/processed_data.csv')
    print("Colonnes disponibles :")
    print(data.columns.tolist())
    print("\n5 premières lignes :")
    print(data.head())

if __name__ == '__main__':
    inspect_csv()