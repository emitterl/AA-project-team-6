import pandas as pd
from data_preparation import merged_df
from holiday_data import holiday_df
from weather_data import hourly_dataframe

df = merged_df.head(1000)

# Zeitbereich definieren
start_time = pd.to_datetime("2018-04-25 04:00:00").tz_localize('America/Los_Angeles')
end_time = pd.to_datetime("2021-09-14 07:00:00").tz_localize('America/Los_Angeles')
print(start_time, end_time)
time_range = pd.date_range(start=start_time, end=end_time, freq='H', tz='America/Los_Angeles')

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

# Vereinigen der DataFrames
# Angenommen, 'time' ist der gemeinsame Schlüssel
model_df = model_df.merge(hourly_dataframe, on='time', how='left')

# Zerlegen des 'time'-Objekts in Jahr, Monat, Tag und Stunde
# model_df['Year'] = model_df['time'].dt.year
# model_df['Month'] = model_df['time'].dt.month
# model_df['Day'] = model_df['time'].dt.day
# model_df['Hour'] = model_df['time'].dt.hour
model_df['Weekday'] = model_df['time'].dt.dayofweek 

# Umwandlung der Wochentag-Integer in Wochentag-Namen
weekday_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
model_df['Weekday'] = model_df['Weekday'].map(weekday_map)

# Entfernen der ursprünglichen 'time'-Spalte
# model_df.drop('time', axis=1, inplace=True)

# Erste Zeilen anzeigen
print(model_df.head())