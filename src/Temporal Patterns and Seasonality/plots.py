import sys
import os
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_preparation import df

conditions = [
    (df['connectionTime'].dt.month == 1),
    (df['connectionTime'].dt.month == 2),
    (df['connectionTime'].dt.month == 3),
    (df['connectionTime'].dt.month == 4),
    (df['connectionTime'].dt.month == 5),
    (df['connectionTime'].dt.month == 6),
    (df['connectionTime'].dt.month == 7),
    (df['connectionTime'].dt.month == 8),
    (df['connectionTime'].dt.month == 9),
    (df['connectionTime'].dt.month == 10),
    (df['connectionTime'].dt.month == 11),
    (df['connectionTime'].dt.month == 12)
]

values = ['1_winter', '1_winter', '2_spring', '2_spring', '2_spring', '3_summer', '3_summer', '3_summer', '4_fall', '4_fall', '4_fall', '1_winter']

df['season'] = np.select(conditions, values)

df_site1 = df[df['siteID'] == '1']
df_site2 = df[df['siteID'] == '2']

#Plot for Temporal Patterns and Seasonality (Site 1 and Site 2)

diag, axes = plt.subplots(2, 4, figsize=(21, 7))

axes[0, 0].bar(df_site1['connectionTime'].dt.hour.value_counts().sort_index().index, df_site1['connectionTime'].dt.hour.value_counts().sort_index().values)
axes[0, 0].set_xlabel('hour')
axes[0, 0].set_ylabel('#chargingEvents')
axes[0, 0].set_title('Site 1: Number of charging events / hour')

axes[0, 1].bar(df_site1['connectionTime'].dt.weekday.value_counts().sort_index().index, df_site1['connectionTime'].dt.weekday.value_counts().sort_index().values)
axes[0, 1].set_xlabel('weekday')
axes[0, 1].set_ylabel('#chargingEvents')
axes[0, 1].set_title('Site 1: Number of charging events / weekday')
axes[0, 1].set_xticks(range(0, 7))
axes[0, 1].set_xticklabels(['Mon', 'Tues', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

axes[0, 2].bar(df_site1['connectionTime'].dt.month.value_counts().sort_index().index, df_site1['connectionTime'].dt.month.value_counts().sort_index().values)
axes[0, 2].set_xlabel('month')
axes[0, 2].set_ylabel('#chargingEvents')
axes[0, 2].set_title('Site 1: Number of charging events / month')
axes[0, 2].set_xticks(range(1, 13))
axes[0, 2].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

axes[0, 3].bar(df_site1['season'].value_counts().sort_index().index, df_site1['season'].value_counts().sort_index().values)
axes[0, 3].set_xlabel('season')
axes[0, 3].set_ylabel('#chargingEvents')
axes[0, 3].set_title('Site 1: Number of charging events / season')

axes[1, 0].bar(df_site2['connectionTime'].dt.hour.value_counts().sort_index().index, df_site2['connectionTime'].dt.hour.value_counts().sort_index().values)
axes[1, 0].set_xlabel('hour')
axes[1, 0].set_ylabel('#chargingEvents')
axes[1, 0].set_title('Site 2: Number of charging events / hour')

axes[1, 1].bar(df_site2['connectionTime'].dt.weekday.value_counts().sort_index().index, df_site2['connectionTime'].dt.weekday.value_counts().sort_index().values)
axes[1, 1].set_xlabel('weekday')
axes[1, 1].set_ylabel('#chargingEvents')
axes[1, 1].set_title('Site 2: Number of charging events / weekday')
axes[1, 1].set_xticks(range(0, 7))
axes[1, 1].set_xticklabels(['Mon', 'Tues', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

axes[1, 2].bar(df_site2['connectionTime'].dt.month.value_counts().sort_index().index, df_site2['connectionTime'].dt.month.value_counts().sort_index().values)
axes[1, 2].set_xlabel('month')
axes[1, 2].set_ylabel('#chargingEvents')
axes[1, 2].set_title('Site 2: Number of charging events / month')
axes[1, 2].set_xticks(range(1, 13))
axes[1, 2].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

axes[1, 3].bar(df_site2['season'].value_counts().sort_index().index, df_site2['season'].value_counts().sort_index().values)
axes[1, 3].set_xlabel('season')
axes[1, 3].set_ylabel('#chargingEvents')
axes[1, 3].set_title('Site 2: Number of charging events / season')

#Plot for Temporal Patterns and Seasonality (Site 1 and Site 2)

diag, axes = plt.subplots(1, 4, figsize=(21, 7))

axes[0].plot (df_site1['connectionTime'].dt.hour.value_counts().sort_index().index, df_site1['connectionTime'].dt.hour.value_counts().sort_index().values)
axes[0].plot (df_site2['connectionTime'].dt.hour.value_counts().sort_index().index, df_site2['connectionTime'].dt.hour.value_counts().sort_index().values)
axes[0].set_xlabel('hour')
axes[0].set_ylabel('#chargingEvents')
axes[0].set_title('Number of charging events / hour')

axes[1].plot(df_site1['connectionTime'].dt.weekday.value_counts().sort_index().index, df_site1['connectionTime'].dt.weekday.value_counts().sort_index().values)
axes[1].plot(df_site2['connectionTime'].dt.weekday.value_counts().sort_index().index, df_site2['connectionTime'].dt.weekday.value_counts().sort_index().values)
axes[1].set_xlabel('weekday')
axes[1].set_ylabel('#chargingEvents')
axes[1].set_title('Number of charging events / weekday')
axes[1].set_xticks(range(0, 7))
axes[1].set_xticklabels(['Mon', 'Tues', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

axes[2].plot(df_site1['connectionTime'].dt.month.value_counts().sort_index().index, df_site1['connectionTime'].dt.month.value_counts().sort_index().values)
axes[2].plot(df_site2['connectionTime'].dt.month.value_counts().sort_index().index, df_site2['connectionTime'].dt.month.value_counts().sort_index().values)
axes[2].set_xlabel('month')
axes[2].set_ylabel('#chargingEvents')
axes[2].set_title('Number of charging events / month')
axes[2].set_xticks(range(1, 13))
axes[2].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

axes[3].plot(df_site1['season'].value_counts().sort_index().index, df_site1['season'].value_counts().sort_index().values)
axes[3].plot(df_site2['season'].value_counts().sort_index().index, df_site2['season'].value_counts().sort_index().values)
axes[3].set_xlabel('season')
axes[3].set_ylabel('#chargingEvents')
axes[3].set_title('Number of charging events / season')

#Plot for Temporal Patterns and Seasonality

diag, axes = plt.subplots(1, 4, figsize=(21, 7))

axes[0].bar(df['connectionTime'].dt.hour.value_counts().sort_index().index, df['connectionTime'].dt.hour.value_counts().sort_index().values)
axes[0].set_xlabel('hour')
axes[0].set_ylabel('#chargingEvents')
axes[0].set_title('Number of charging events / hour')

axes[1].bar(df['connectionTime'].dt.weekday.value_counts().sort_index().index, df['connectionTime'].dt.weekday.value_counts().sort_index().values)
axes[1].set_xlabel('weekday')
axes[1].set_ylabel('#chargingEvents')
axes[1].set_title('Number of charging events / weekday')
axes[1].set_xticks(range(0, 7))
axes[1].set_xticklabels(['Mon', 'Tues', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

axes[2].bar(df['connectionTime'].dt.month.value_counts().sort_index().index, df['connectionTime'].dt.month.value_counts().sort_index().values)
axes[2].set_xlabel('month')
axes[2].set_ylabel('#chargingEvents')
axes[2].set_title('Number of charging events / month')
axes[2].set_xticks(range(1, 13))
axes[2].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

axes[3].bar(df['season'].value_counts().sort_index().index, df['season'].value_counts().sort_index().values)
axes[3].set_xlabel('season')
axes[3].set_ylabel('#chargingEvents')
axes[3].set_title('Number of charging events / season')

plt.tight_layout()
plt.show()
