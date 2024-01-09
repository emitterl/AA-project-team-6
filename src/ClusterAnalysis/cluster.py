import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_preparation import merged_df
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram

dropped_df = merged_df.sample(n=3_000, random_state=42)
dropped_df.drop('id', axis=1, inplace=True)
dropped_df.drop('siteID', axis=1, inplace=True)
dropped_df.drop('spaceID', axis=1, inplace=True)
dropped_df.drop('userID', axis=1, inplace=True)
dropped_df.drop('connectionTime', axis=1, inplace=True)
dropped_df.drop('disconnectTime', axis=1, inplace=True)
dropped_df.drop('doneChargingTime', axis=1, inplace=True)
dropped_df.drop('modifiedAt', axis=1, inplace=True)
dropped_df.drop('requestedDeparture', axis=1, inplace=True)
dropped_df = dropped_df.dropna()

scaler = MinMaxScaler()
scaled = scaler.fit_transform(dropped_df)
scaled_df = pd.DataFrame(scaled, columns=dropped_df.columns, index=dropped_df.index)

# ergibt keinen Sinn (ändert nichts), aber führt sonst Fehler
scaled_reshape  = np.reshape(scaled, (-1, 5))
# print('x', scaled.ndim)
# print('reshape', scaled_reshape.ndim)

# Residual loss -> number of clusters between 3 and 5
k_max = 50  # We have c. 65_000 datapoints, more than 21_000 clusters are definitely not reasonable!

clusters = []
losses = []

for k in range(k_max):
    model = KMeans(n_clusters=k+1, n_init='auto')
    model.fit(scaled_reshape)
    clusters.append(k+1)
    losses.append(model.inertia_)

plt.plot(clusters, losses)
plt.ylabel("Loss")
plt.xlabel("Number of clusters")
plt.xlim([0,10])
plt.show()

## K Means
numbers = ["one", "two", "three", "four"]

# After deciding on number of clusters = 3
# refit algorithm
three_means = KMeans(n_clusters=3, n_init='auto')
three_means.fit(scaled_reshape)

# match records to clusters by calling predict
three_means.predict(scaled_reshape)

scaled_df["three"] = three_means.predict(scaled_reshape)
scaled_df["three"] = scaled_df["three"].apply(lambda x: numbers[x])

sns.pairplot(data=scaled_df, hue="three")

# 4 clusters
four_means = KMeans(n_clusters=4, n_init='auto')
four_means.fit(scaled_reshape)

# match records to clusters by calling predict
four_means.predict(scaled_reshape)

scaled_df["four"] = four_means.predict(scaled_reshape)
scaled_df["four"] = scaled_df["four"].apply(lambda x: numbers[x])

sns.pairplot(data=scaled_df, hue="four")


## Hierarchical clustering
def plot_dendrogram(model, **kwargs):

    # Children of hierarchical clustering
    children = model.children_

    # Distances between each pair of children
    # Since we don't have this information, we can use a uniform one for plotting
    distance = np.arange(children.shape[0])

    # The number of observations contained in each cluster level
    no_of_observations = np.arange(2, children.shape[0]+2)

    # Create linkage matrix and then plot the dendrogram
    linkage_matrix = np.column_stack([children, distance, no_of_observations]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)


agglo = AgglomerativeClustering(n_clusters=3) #The number of clusters to find
y_pred_agglo = agglo.fit_predict(scaled_reshape)

plt.figure(figsize=(40,15))
plt.title('Hierarchical Clustering Dendrogram')
plot_dendrogram(agglo, labels=agglo.labels_)
plt.ylabel("Distance")
plt.show()