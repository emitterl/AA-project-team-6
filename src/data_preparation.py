import pandas as pd
import ast
from datetime import datetime


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
    

# Konvertieren der Datentypen in charging_sessions
df['id'] = df['id'].astype(str)
df['connectionTime'] = pd.to_datetime(df['connectionTime'], utc=True)
df['disconnectTime'] = pd.to_datetime(df['disconnectTime'], utc=True)
df['doneChargingTime'] = pd.to_datetime(df['doneChargingTime'], utc=True)
df['kWhDelivered'] = df['kWhDelivered'].astype(float)
df['sessionID'] = df['sessionID'].astype(str)
df['siteID'] = df['siteID'].astype(str)
df['spaceID'] = df['spaceID'].astype(str)
df['stationID'] = df['stationID'].astype(str)
df['timezone'] = df['timezone'].astype(str)
df['userID'] = df['userID'].astype(str)
    

# Löscht Spalte Unnamed und anschließend alle Duplikate    
df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
df.drop(df.columns[df.columns.str.contains('timezone',case = False)],axis = 1, inplace = True)
df = df.drop_duplicates()


# Erstelle DataFrame user_inputs_df
user_inputs_list = df.apply(parse_user_inputs, axis=1)
user_inputs_df = pd.DataFrame([item for sublist in user_inputs_list for item in sublist])


# löscht userInputs, da in eigener Tabelle
df = df.drop('userInputs', axis=1)


# Konvertieren der Datentypen in user_inputs_df
user_inputs_df['WhPerMile'] = user_inputs_df['WhPerMile'].astype(float)
user_inputs_df['kWhRequested'] = user_inputs_df['kWhRequested'].astype(float)
user_inputs_df['milesRequested'] = user_inputs_df['milesRequested'].astype(float)
user_inputs_df['minutesAvailable'] = user_inputs_df['minutesAvailable'].astype(float)
user_inputs_df['modifiedAt'] = pd.to_datetime(user_inputs_df['modifiedAt'], utc=True)
user_inputs_df['paymentRequired'] = user_inputs_df['paymentRequired'].astype(bool)
user_inputs_df['requestedDeparture'] = pd.to_datetime(user_inputs_df['requestedDeparture'], utc=True)


# Duplikate in user_inputs_df löschen
duplikate_id_user = user_inputs_df[user_inputs_df.duplicated()]
user_inputs_df = user_inputs_df.drop_duplicates()

# Handle missing values (in progress)
dfNan = df[df.isna().any(axis=1)]

# Erste Zeilen der importierten Daten anzeigen von charging_sessions und user_inputs
print(df.head())
print(user_inputs_df.head())