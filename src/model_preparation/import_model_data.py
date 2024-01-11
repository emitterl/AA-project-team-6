import pandas as pd

# Importieren des DataFrames aus der CSV-Datei
model_df = pd.read_csv('model_data.csv')

# Typen der Spalten deklarieren
model_df['time'] = pd.to_datetime(model_df['time'])  # Annahme: Zeitformat ist 'YYYY-MM-DD HH:MM:SS'
model_df['siteID'] = model_df['siteID'].astype(str)
model_df['occupied_count'] = model_df['occupied_count'].astype(float)
model_df['is_holiday'] = model_df['is_holiday'].astype(bool)
model_df['temperature'] = model_df['temperature'].astype(float)
model_df['weather_description'] = model_df['weather_description'].astype(str)
model_df['Weekday'] = model_df['Weekday'].astype(str)

# Überprüfen des importierten DataFrames
print(model_df.head())
