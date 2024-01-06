import pandas as pd
from sklearn.model_selection import train_test_split
from data_preparation import merged_df
from holiday_data import holiday_df

df = merged_df.head(7000)

# Zeitbereich definieren, in der Zeitzone "America/Los_Angeles"
start_time = df['connectionTime'].min()
end_time = df['disconnectTime'].max()
time_range = pd.date_range(start=start_time, end=end_time, freq='H')

# Vorbereiten einer leeren Liste für die Ergebnisse
results = []

# Durchgehen der Zeitpunkte und Berechnung der belegten Säulen
for time in time_range:
    for site_id in df['siteID'].unique():
        occupied_count = df[(df['connectionTime'] <= time) & (df['disconnectTime'] > time) & (df['siteID'] == site_id)].shape[0]
        results.append({'time': time, 'siteID': site_id, 'occupied_count': occupied_count})

# Ergebnisse in einem DataFrame speichern
model_df = pd.DataFrame(results)

# Hinzufügen der Feiertagsinformation
model_df['is_holiday'] = model_df['time'].dt.date.isin(holiday_df['date'])

# Erste Zeilen anzeigen
print(model_df.head())


# Zielvariable und Merkmale trennen
X = model_df.drop('occupied_count', axis=1)  # Merkmale
y = model_df['occupied_count']               # Zielvariable

# Aufteilung in Trainings- und Testdaten
# Angenommen, wir teilen die Daten in 80% Training und 20% Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ergebnisse überprüfen
print("Trainingsdaten:", X_train.shape, y_train.shape)
print("Testdaten:", X_test.shape, y_test.shape)