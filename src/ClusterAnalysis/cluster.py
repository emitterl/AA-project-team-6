import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_preparation import merged_df
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.cluster.hierarchy as sc
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

## Data preparation - drop IDs and not needed columns, and convert time values into hours
dropped_df = merged_df.copy()

dropped_df.drop('id', axis=1, inplace=True)
dropped_df.drop('siteID', axis=1, inplace=True)
dropped_df.drop('spaceID', axis=1, inplace=True)
dropped_df.drop('userID', axis=1, inplace=True)
dropped_df.drop('modifiedAt', axis=1, inplace=True)
dropped_df.drop('requestedDeparture', axis=1, inplace=True)
dropped_df.drop('WhPerMile', axis=1, inplace=True)
dropped_df['connectionTime'] =  dropped_df['connectionTime'].dt.hour
dropped_df['disconnectTime'] =  dropped_df['disconnectTime'].dt.hour
dropped_df['doneChargingTime'] =  dropped_df['doneChargingTime'].dt.hour
dropped_df = dropped_df.dropna()

# Create sample from dataset as original dataset is too big
dropped_df = dropped_df.sample(n=3_000, random_state=42)

## Scale data
scaler = MinMaxScaler()
scaled = scaler.fit_transform(dropped_df)
scaled_df = pd.DataFrame(scaled, columns=dropped_df.columns, index=dropped_df.index)

sns.pairplot(data=scaled_df)

# How many clusters should we use?
# 1. Plot residual loss for different number of clusters, find 'elbow' and select corresponding number of clusters
# 2. Use hierarchical clustering to detect suitable braching and corresponding number of clusters

## Residual loss plot -> number of clusters between 2 and 5
k_max = 15
clusters = []
losses = []

for k in range(k_max):
    model = KMeans(n_clusters=k+1, n_init='auto')
    model.fit(scaled)
    clusters.append(k+1)
    losses.append(model.inertia_)

plt.figure(figsize=(10, 5))  
plt.plot(clusters, losses)
plt.ylabel("Loss")
plt.xlabel("Number of clusters")
plt.show()

## Hierarchal Clustering -> number of clusters = 3
# Plot dendrogram
plt.figure(figsize=(20, 7))  
plt.title("Dendrograms")  
plt.title('Dendrogram')
plt.xlabel('Sample index')
plt.ylabel('Euclidean distance')
sc.dendrogram(sc.linkage(scaled, method='ward'))

## K Means with 3 clusters
numbers = ["one", "two", "three"]
three_means = KMeans(n_clusters=3, n_init='auto')
three_means.fit(scaled)

# match records to clusters by calling predict
three_means.predict(scaled)
scaled_df["three"] = three_means.predict(scaled)
scaled_df["three"] = scaled_df["three"].apply(lambda x: numbers[x])

sns.pairplot(data=scaled_df, hue="three")