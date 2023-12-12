from data_preparation import df, user_inputs_df
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# KPI - Difference of doneChargingTime and DisconnectionTime in hours
# Car is connected but is fully charged

# Calculcate difference of disconnect and doneCharging times
conDiff = df['disconnectTime'] - df['doneChargingTime']
# Filter negative values
conDiffPos = conDiff[conDiff.values > pd.Timedelta(0)].sort_values(ascending=True)

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

dfUsers = df.loc[:, ('userID', 'connectionTime')] 
dfUsers['connectionTime'] = dfUsers['connectionTime'].dt.date
# recurringUsers = dfUsers[dfUsers.groupby('userID').userID.transform(len) > 1]
recurringUsers = dfUsers['userID'].value_counts().sort_values()


# KPI - Difference of kWhRequested and kWhDelivered

# Find rows with latest modified time per ID
idx_max_values = user_inputs_df.groupby('id')['modifiedAt'].idxmax()
# Filter dataframe with latest modified times per ID
filtered_user_df = user_inputs_df.loc[idx_max_values]
# Merge dataframe and filtered user dataframe
merged_table = pd.merge(df.drop('userID', axis=1), filtered_user_df, on='id', how='inner')
# Calculate difference of delivered and requested kWh per session
merged_table['kwhDiff'] = merged_table['kWhDelivered'] - merged_table['kWhRequested']

kwhDiffCounts = merged_table['kwhDiff'].value_counts().sort_index()

## Plot
plt.figure(figsize=(8, 6))

plt.plot(kwhDiffCounts.index, kwhDiffCounts.values)

plt.xlabel('Difference of delivered and requested kWh')
plt.ylabel('Total amount')
plt.title('Difference of delivered and requested kWh')
plt.show()