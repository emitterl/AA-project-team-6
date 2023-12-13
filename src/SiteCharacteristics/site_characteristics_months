import sys
import os
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_preparation import merged_df



df_site1 = merged_df[merged_df['siteID'] == '1']
df_site2 = merged_df[merged_df['siteID'] == '2']

# Funktion zur Berechnung der Varianz der Verbindungen pro Monat
def calculate_monthly_variance(df):
    monthly_counts = df['connectionTime'].dt.month.value_counts().sort_index()
    variance = monthly_counts.var()
    return variance

connection_counts__month_site1 = df_site1['connectionTime'].dt.month.value_counts().sort_index()
connection_counts__month_site2 = df_site2['connectionTime'].dt.month.value_counts().sort_index()

variance_site1 = calculate_monthly_variance(df_site1)
variance_site2 = calculate_monthly_variance(df_site2)

# Plotten der Daten
fig, axs = plt.subplots(1, 2, figsize=(15, 6))

# Site 1
monthly_counts_site1 = df_site1['connectionTime'].dt.month.value_counts().sort_index()
axs[0].bar(monthly_counts_site1.index, monthly_counts_site1.values)
axs[0].set_title('Monthly Connection Counts for Site 1')
axs[0].set_xlabel('Month')
axs[0].set_ylabel('Number of Connections')
axs[0].set_xticks(range(1, 13))
axs[0].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
axs[0].text(0.5, -0.1, f'Varianz: {variance_site1:.2f}', horizontalalignment='center', verticalalignment='center', transform=axs[0].transAxes)

# Site 2
monthly_counts_site2 = df_site2['connectionTime'].dt.month.value_counts().sort_index()
axs[1].bar(monthly_counts_site2.index, monthly_counts_site2.values)
axs[1].set_title('Monthly Connection Counts for Site 2')
axs[1].set_xlabel('Month')
axs[1].set_ylabel('Number of Connections')
axs[1].set_xticks(range(1, 13))
axs[1].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
axs[1].text(0.5, -0.1, f'Varianz: {variance_site2:.2f}', horizontalalignment='center', verticalalignment='center', transform=axs[1].transAxes)

plt.tight_layout()
plt.show()
