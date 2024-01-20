import pandas as pd

# Importieren des DataFrames aus der CSV-Datei
import_data = pd.read_csv('model_data.csv', parse_dates=['time'])
# Typen der Spalten deklarieren
import_data['time'] = pd.to_datetime(import_data['time'], errors='coerce').dt.tz_convert('America/Los_Angeles')
import_data['siteID'] = import_data['siteID'].astype(str)
import_data['occupied_count'] = import_data['occupied_count'].astype(float)
import_data['is_holiday'] = import_data['is_holiday'].astype(bool)
import_data['temperature'] = import_data['temperature'].astype(float)
import_data['weather_description'] = import_data['weather_description'].astype(str)
import_data['Weekday'] = import_data['Weekday'].astype(str)


model_df = import_data.copy()
print(import_data.head())
