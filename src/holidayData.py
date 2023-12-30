import pandas as pd


# Jahre, für die Sie Daten haben
years = ['2018', '2019', '2020', '2021', '2022', '2023', '2024']

# Leere Liste, um alle DataFrames zu sammeln
dataframes = []

for year in years:
    # Pfad zur CSV-Datei
    file_path = f'HolidayData/holidays_{year}.csv'
    # Lesen der CSV-Datei
    df = pd.read_csv(file_path)

    # Nur internationale Feiertage oder Feiertage in Kalifornien
    df = df[(pd.isna(df['region'])) | (df['region'] == 'CA')]
    
    # Hinzufügen des DataFrame zur Liste
    dataframes.append(df)

# Kombinieren aller DataFrames in einen
holiday_df = pd.concat(dataframes)

# Entfernen der Spalten 'locale', 'types', 'notes' und 'region'
holiday_df.drop(['locale', 'type', 'notes', 'region'], axis=1, inplace=True)

print(holiday_df.head)