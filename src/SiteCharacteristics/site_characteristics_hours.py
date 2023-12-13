import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_preparation import merged_df
import matplotlib.pyplot as plt

from datetime import datetime, timedelta


def calculate_average_time(df_column):
    # Konvertierung Zeit in Sekunden seit Mitternacht
    seconds_since_midnight = df_column.dt.hour * 3600 + df_column.dt.minute * 60 + df_column.dt.second
    
    # Berechnung des Durchschnitts
    average_seconds = seconds_since_midnight.mean()
    
    # Konvertierung zurück in ein Zeitformat
    average_time = (datetime.min + timedelta(seconds=int(average_seconds))).time()
    
    # Formatierung
    return average_time.strftime("%H:%M:%S")

def calculate_variance_in_hours(df_column):
    # Konvertierung Zeit in Sekunden seit Mitternacht
    seconds_since_midnight = df_column.dt.hour * 3600 + df_column.dt.minute * 60 + df_column.dt.second
    
    # Berechnung der Varianz und Umwandlung in Stunden
    variance_seconds = seconds_since_midnight.var()
    variance_hours = variance_seconds / (3600 * 3600)  # Da Varianz in Sekunden^2 ist
    
    return variance_hours



# Filtern der Daten für jede Site
df_site1 = merged_df[merged_df['siteID'] == '1']
df_site2 = merged_df[merged_df['siteID'] == '2']

mean_conn_site1 = calculate_average_time(df_site1['connectionTime'])
mean_conn_site2 = calculate_average_time(df_site2['connectionTime'])

mean_disconn_site1 = calculate_average_time(df_site1['disconnectTime'])
mean_disconn_site2 = calculate_average_time(df_site2['disconnectTime'])

var_conn_site1 = calculate_variance_in_hours(df_site1['connectionTime'])
var_conn_site2 = calculate_variance_in_hours(df_site2['connectionTime'])

var_disconn_site1 = calculate_variance_in_hours(df_site1['disconnectTime'])
var_disconn_site2 = calculate_variance_in_hours(df_site2['disconnectTime'])



# Berechnen der Anzahl der Verbindungen pro Stunde für jede Site
connection_counts_site1 = df_site1['connectionTime'].dt.hour.value_counts().sort_index()
connection_counts_site2 = df_site2['connectionTime'].dt.hour.value_counts().sort_index()

# Berechnen der Anzahl der Trennungen pro Stunde für jede Site
disconnection_counts_site1 = df_site1['disconnectTime'].dt.hour.value_counts().sort_index()
disconnection_counts_site2 = df_site2['disconnectTime'].dt.hour.value_counts().sort_index()

fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# Site 1 Connection
axs[0, 0].bar(connection_counts_site1.index, connection_counts_site1.values)
axs[0, 0].set_title('Connection Time per Hour for Site 1')
axs[0, 0].set_xlabel('Hour of the Day')
axs[0, 0].set_ylabel('Number of Connections')
axs[0, 0].text(0.5, 0.9, f'Mean Time: {mean_conn_site1}\nVar (hours): {var_conn_site1:.2f}', 
               horizontalalignment='center', verticalalignment='center', transform=axs[0, 0].transAxes)

# Site 2 Connection
axs[0, 1].bar(connection_counts_site2.index, connection_counts_site2.values)
axs[0, 1].set_title('Connection Time per Hour for Site 2')
axs[0, 1].set_xlabel('Hour of the Day')
axs[0, 1].set_ylabel('Number of Connections')
axs[0, 1].text(0.5, 0.9, f'Mean Time: {mean_conn_site2}\nVar (hours): {var_conn_site2:.2f}', 
               horizontalalignment='center', verticalalignment='center', transform=axs[0, 1].transAxes)

# Site 1 Disconnection
axs[1, 0].bar(disconnection_counts_site1.index, disconnection_counts_site1.values)
axs[1, 0].set_title('Disconnection Time per Hour for Site 1')
axs[1, 0].set_xlabel('Hour of the Day')
axs[1, 0].set_ylabel('Number of Disconnections')
axs[1, 0].text(0.5, 0.9, f'Mean Time: {mean_disconn_site1}\nVar (hours): {var_disconn_site1:.2f}', 
               horizontalalignment='center', verticalalignment='center', transform=axs[1, 0].transAxes)

# Site 2 Disconnection
axs[1, 1].bar(disconnection_counts_site2.index, disconnection_counts_site2.values)
axs[1, 1].set_title('Disconnection Time per Hour for Site 2')
axs[1, 1].set_xlabel('Hour of the Day')
axs[1, 1].set_ylabel('Number of Disconnections')
axs[1, 1].text(0.5, 0.9, f'Mean Time: {mean_disconn_site2}\nVar (hours): {var_disconn_site2:.2f}', 
               horizontalalignment='center', verticalalignment='center', transform=axs[1, 1].transAxes)


plt.tight_layout()
plt.show()