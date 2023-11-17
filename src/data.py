import pandas as pd
import json
import traceback
import re
from datetime import datetime


csv_file_path = 'charging_sessions.csv'


df = pd.read_csv(csv_file_path, delimiter=',', quotechar='"')

# Umwandlung von datetime und boolean um in Tabelle richtig zu importieren
def correct_dates_and_bools(json_str):
    # Regulärer Ausdruck, um Datumsangaben zu finden
    date_pattern = r'\w{3}, \d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2} GMT'
    dates = re.findall(date_pattern, json_str)
    
    for date in dates:
        parsed_date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT')
        iso_date = parsed_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        json_str = json_str.replace(date, iso_date)

    # Ersetzen von Python-Booleschen Werten durch JSON-Boolesche Werte
    json_str = json_str.replace("True", "true").replace("False", "false")

    return json_str

# parst userInput-String in eine neue Tabelle (Um userINput Tabelle in charging_session tabelle zu verschachteln)
# def parse_user_inputs(json_str):
    if isinstance(json_str, str):
        try:
            corrected_str = json_str.replace("'", '"')
            corrected_str = correct_dates_and_bools(corrected_str)
            data = json.loads(corrected_str)
            user_inputs_df = pd.DataFrame(data)
            
            user_inputs_df['WhPerMile'] = user_inputs_df['WhPerMile'].astype(float)
            user_inputs_df['kWhRequested'] = user_inputs_df['kWhRequested'].astype(float)
            user_inputs_df['milesRequested'] = user_inputs_df['milesRequested'].astype(float)
            user_inputs_df['minutesAvailable'] = user_inputs_df['minutesAvailable'].astype(float)
            user_inputs_df['modifiedAt'] = pd.to_datetime(user_inputs_df['modifiedAt'], utc=True, format='%Y-%m-%dT%H:%M:%SZ')
            user_inputs_df['paymentRequired'] = user_inputs_df['paymentRequired'].astype(bool)
            user_inputs_df['requestedDeparture'] = pd.to_datetime(user_inputs_df['requestedDeparture'], utc=True, format='%Y-%m-%dT%H:%M:%SZ')

            return user_inputs_df
        except Exception as e:
            print("Fehler beim Parsen von userInputs:", str(e))
            traceback.print_exc()
            return pd.DataFrame()
    else:
        return pd.DataFrame()
    
# Erstellt neue Tupel in neuer user_inputs Tabelle mit Referenz auf eigentlichen Tupel
def parse_user_inputs(row):
    user_inputs = row['userInputs']
    id = row['id']  # id als Referenz-ID

    if isinstance(user_inputs, str):
        try:
            corrected_str = user_inputs.replace("'", '"')
            corrected_str = correct_dates_and_bools(corrected_str)
            data = json.loads(corrected_str)

            for d in data:
                d['reference_id'] = id  # Referenz-ID hinzufügen
            
            return data
        except Exception as e:
            print("Fehler beim Parsen von userInputs:", str(e))
            return []
    else:
        return []
    
user_inputs_list = df.apply(parse_user_inputs, axis=1)
user_inputs_df = pd.DataFrame([item for sublist in user_inputs_list for item in sublist])

# Konvertieren der Datentypen in user_inputs_df
user_inputs_df['WhPerMile'] = user_inputs_df['WhPerMile'].astype(float)
user_inputs_df['kWhRequested'] = user_inputs_df['kWhRequested'].astype(float)
user_inputs_df['milesRequested'] = user_inputs_df['milesRequested'].astype(float)
user_inputs_df['minutesAvailable'] = user_inputs_df['minutesAvailable'].astype(float)
user_inputs_df['modifiedAt'] = pd.to_datetime(user_inputs_df['modifiedAt'], utc=True, format='%Y-%m-%dT%H:%M:%SZ')
user_inputs_df['paymentRequired'] = user_inputs_df['paymentRequired'].astype(bool)
user_inputs_df['requestedDeparture'] = pd.to_datetime(user_inputs_df['requestedDeparture'], utc=True, format='%Y-%m-%dT%H:%M:%SZ')


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
# df['userInputs'] = df['userInputs'].apply(parse_user_inputs)

# löscht userInputs, da in eigener Tabelle
df = df.drop('userInputs', axis=1)


# Ersten Zeilen der importierten Daten anzeigen von charging_sessions und user_inputs
print(df.head())
print(user_inputs_df.head())