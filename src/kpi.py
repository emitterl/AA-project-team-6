from data_preparation import merged_df
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# KPI - Difference of doneChargingTime and DisconnectionTime in hours
# Car is connected but is fully charged

# Calculcate difference of disconnect and doneCharging times
conDiff = merged_df['disconnectTime'] - merged_df['doneChargingTime']
conDiff = conDiff.dropna()
# Filter negative values
conDiffPos = conDiff.sort_values(ascending=True)

max = conDiffPos.max()
min = conDiffPos.min()
# Group by hour and count values
diffCounts = conDiffPos.apply(lambda x : (x/np.timedelta64(1, 'h'))).astype(int).value_counts().sort_index()
diffCountsZoom = diffCounts[diffCounts.values > 50]

## Plot
plt.figure(figsize=(8, 6))

plt.plot(diffCounts.index, diffCounts.values)

plt.xlabel('Total hours (rounded)')
plt.ylabel('Sum of Charging Sessions')
plt.title('Difference of doneChargingTime and disconnectionTime')
plt.text(80, 0, f'Max: {max}\n Min: {min}', horizontalalignment='center', verticalalignment='center')
plt.show()

plt.figure(figsize=(8, 6))

plt.plot(diffCountsZoom.index, diffCountsZoom.values)

plt.xlabel('Total hours (rounded)')
plt.ylabel('Sum of Charging Sessions')
plt.title('Difference of doneChargingTime and disconnectionTime (zoom -> sum > 50)')
plt.show()

# KPI - recurring users

dfUsers = merged_df.loc[:, ('userID', 'connectionTime')] 
dfUsers['connectionTime'] = dfUsers['connectionTime'].dt.date
# recurringUsers = dfUsers[dfUsers.groupby('userID').userID.transform(len) > 1]
recurringUsers = dfUsers['userID'].value_counts().sort_values()


# KPI - Difference of kWhRequested and kWhDelivered

rows_with_userInputs = merged_df[merged_df['kWhRequested'].notna() & (merged_df['kWhRequested'] != '')]
rows_with_userInputs['kwhDiff'] = rows_with_userInputs['kWhDelivered'] - rows_with_userInputs['kWhRequested']

kwhDiffCounts = rows_with_userInputs['kwhDiff'].value_counts().sort_index()

## Plot
plt.figure(figsize=(8, 6))

plt.plot(kwhDiffCounts.index, kwhDiffCounts.values)

plt.xlabel('Difference of delivered and requested kWh')
plt.ylabel('Total amount')
plt.title('Difference of delivered and requested kWh')
plt.show()