import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_preparation import df


df_site1 = df[df['siteID'] == '1']
df_site2 = df[df['siteID'] == '2']

print(f"Anzahl verschiedene App-Nutzer site 1: {df_site1['userID'].nunique()}")
print(f"Anzahl verschiedene App-Nutzer site 2: {df_site2['userID'].nunique()}")


print(f"Anzahl verschiedene spaceIDs site 1: {df_site1['spaceID'].nunique()}")
print(f"Anzahl verschiedene spaceIDs site 2: {df_site2['spaceID'].nunique()}")

print(f"Alle spaceIDs site 1: {df_site1['spaceID'].unique()}")
print(f"Alle spaceIDs site 2: {df_site2['spaceID'].unique()}")

print(f"Anzahl Aufladungen Insgesamt site 1: {len(df_site1)}")
print(f"Anzahl Aufladungen Insgesamt site 2: {len(df_site2)}")

print(f"Komische spaceID: {df[df['spaceID'] == '11900388']}")
print(f"Frühster Wert: {df[df['spaceID'] == '11900388']['connectionTime'].min()}")
print(f"Spätester Wert: {df[df['spaceID'] == '11900388']['connectionTime'].max()}")

print(f"Insgesamt frühster Wert: {df_site2['connectionTime'].min()}")
print(f"Insgesamt spätester Wert: {df_site2['connectionTime'].max()}")