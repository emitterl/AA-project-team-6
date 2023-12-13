import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_preparation import merged_df
import matplotlib.pyplot as plt

from datetime import datetime, timedelta



# Filtern der Daten für jede Site
df_site1 = merged_df[merged_df['siteID'] == '1']
df_site2 = merged_df[merged_df['siteID'] == '2']


df_site1['weekday'] = df_site1['connectionTime'].dt.day_name()
df_site2['weekday'] = df_site2['connectionTime'].dt.day_name()


weekdays_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

connection_counts_site1 = df_site1['weekday'].value_counts().reindex(weekdays_order)
connection_counts_site2 = df_site2['weekday'].value_counts().reindex(weekdays_order)



fig, axs = plt.subplots(1, 2, figsize=(15, 10))

# Site 1 Connection
axs[0].bar(connection_counts_site1.index, connection_counts_site1.values)
axs[0].set_title('Connections per Weekday for Site 1')
axs[0].set_xlabel('Day of the week')
axs[0].set_ylabel('Number of Connections')

# Site 2 Connection
axs[1].bar(connection_counts_site2.index, connection_counts_site2.values)
axs[1].set_title('Connections per Weekday for Site 2')
axs[1].set_xlabel('Day of the weeky')
axs[1].set_ylabel('Number of Connections')

plt.tight_layout()
plt.show()
