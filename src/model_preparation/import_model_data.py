import pandas as pd

# Importieren des DataFrames aus der CSV-Datei
model_df = pd.read_csv('model_data.csv')

# Überprüfen des importierten DataFrames
print(model_df.head())
