import pandas as pd
import ast

csv_file_path = 'charging_sessions.csv'

df = pd.read_csv(csv_file_path, delimiter=',', quotechar='"')


# Hilfsfunktion zum Erstellen der userInput Tabelle
def parse_user_inputs(row):
    
    user_inputs = row['userInputs']
    id = row['id']

    if isinstance(user_inputs, str):
        try:
            # Konvertieren des Strings in ein Python-Dictionary
            user_inputs_data = ast.literal_eval(user_inputs)

            for entry in user_inputs_data:
                entry['reference_id'] = id
            
            return user_inputs_data
        except Exception as e:
            print(f"Fehler beim Parsen von userInputs für ID {id}: {e}")
            return []
    else:
        return []
    

# Funktion zur Umwandlung der Zeitzone
def convert_timezone(time):
    if pd.notna(time):
        return time.tz_convert('America/Los_Angeles')
    return time


# Konvertieren der Datentypen in charging_sessions
df['id'] = df['id'].astype(str)
df['connectionTime'] = pd.to_datetime(df['connectionTime'], utc=True, errors='coerce').apply(convert_timezone)
df['disconnectTime'] = pd.to_datetime(df['disconnectTime'], utc=True, errors='coerce').apply(convert_timezone)
df['doneChargingTime'] = pd.to_datetime(df['doneChargingTime'], utc=True, errors='coerce').apply(convert_timezone)
df['kWhDelivered'] = df['kWhDelivered'].astype(float)
df['sessionID'] = df['sessionID'].astype(str)
df['siteID'] = df['siteID'].astype(str)
df['spaceID'] = df['spaceID'].astype(str)
df['stationID'] = df['stationID'].astype(str)
df['timezone'] = df['timezone'].astype(str)
df['userID'] = df['userID'].astype(str)

    

# Löscht Spalten Unnamed, stationID, sessionID   
df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
df.drop(['sessionID', 'stationID', 'timezone'], axis=1, inplace=True)

# Löscht alle Duplikate
df = df.drop_duplicates()

# Setzt überall, wo die doneChargingTime später als die disconnectTime ist, die doneChargingTime auf die disconnectTime
df.loc[df['doneChargingTime'] > df['disconnectTime'], 'doneChargingTime'] = df['disconnectTime']


# Lösche doneChargingTime überall, wo es vor connectionTime ist
df.loc[df['doneChargingTime'] < df['connectionTime'], 'doneChargingTime'] = pd.NaT

# Erstelle DataFrame user_inputs_df
user_inputs_list = df.apply(parse_user_inputs, axis=1)
user_inputs_df = pd.DataFrame([item for sublist in user_inputs_list for item in sublist])


# löscht userInputs, da in eigener Tabelle
df = df.drop('userInputs', axis=1)

# löscht paymentRequired, da immer true
user_inputs_df = user_inputs_df.drop('paymentRequired', axis=1)

# Konvertieren der Datentypen in user_inputs_df
user_inputs_df['WhPerMile'] = user_inputs_df['WhPerMile'].astype(float)
user_inputs_df['kWhRequested'] = user_inputs_df['kWhRequested'].astype(float)
user_inputs_df['milesRequested'] = user_inputs_df['milesRequested'].astype(float)
user_inputs_df['minutesAvailable'] = user_inputs_df['minutesAvailable'].astype(float)
user_inputs_df['modifiedAt'] = pd.to_datetime(user_inputs_df['modifiedAt'], utc=True).apply(convert_timezone)
user_inputs_df['requestedDeparture'] = pd.to_datetime(user_inputs_df['requestedDeparture'], utc=True).apply(convert_timezone)

# Handle missing values (in progress)
dfNan = df[df.isna().any(axis=1)]

# Erste Zeilen der importierten Daten anzeigen von charging_sessions und user_inputs
print(df.head())
print(user_inputs_df.head())

user_inputs_df = user_inputs_df.drop('userID', axis=1, errors='ignore')

# Sortieren des user_inputs_df nach 'reference_id' und 'modifiedAt', um den neuesten Eintrag für jede ID zu erhalten
user_inputs_df_sorted = user_inputs_df.sort_values(by=['reference_id', 'modifiedAt'], ascending=[True, False])

# Behalten nur des neuesten Eintrags für jede reference_id
user_inputs_df_latest = user_inputs_df_sorted.drop_duplicates(subset=['reference_id'])

# Merge des df mit user_inputs_df_latest
# left join, um sicherzustellen, dass alle Zeilen aus df beibehalten werden
merged_df = pd.merge(df, user_inputs_df_latest, how='left', left_on='id', right_on='reference_id')

# Entfernen der Spalte 'reference_id', da sie identisch mit 'id' ist
merged_df.drop('reference_id', axis=1, inplace=True)

# Entfernen von Ausreißern
merged_df.loc[merged_df.kWhDelivered > 123, "kWhDelivered"] = 123 # https://ev-database.org --> max 123 kwh
merged_df.loc[merged_df.WhPerMile > 474.8, "WhPerMile"] = 474.8 # https://ev-database.org --> max 474.8 wh/mile
merged_df.loc[merged_df.WhPerMile < 223.7, "WhPerMile"] = 223.7 # https://ev-database.org --> min 223.7 wh/mile
merged_df.loc[merged_df.kWhRequested > 123, "kWhRequested"] = 123 # https://ev-database.org --> max 123 kwh
merged_df = merged_df.drop(merged_df[merged_df.kWhRequested == 0].index, axis=0) #--> 0 not possible --> Del
merged_df = merged_df.drop(merged_df[merged_df.milesRequested == 0].index, axis=0) #--> 0 not possible --> Del
merged_df.loc[merged_df.milesRequested > 425.6, "milesRequested"] = 425.6  #--> # https://ev-database.org --> max 425,6 miles
merged_df = merged_df.drop(merged_df[merged_df.minutesAvailable == merged_df.minutesAvailable.max()].index, axis=0) # Outlier --> Del




# Anzeigen der ersten Zeilen des gemergten DataFrames
print(merged_df)
