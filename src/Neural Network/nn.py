import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model_preparation.import_model_data import model_df
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.environ["KERAS_BACKEND"] = "torch"
import keras
from keras import Sequential 
from keras.layers import Dense, Dropout

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

df = model_df
df['Year'] = model_df['time'].dt.year
df['Month'] = model_df['time'].dt.month
df['Day'] = model_df['time'].dt.day
df['Hour'] = model_df['time'].dt.hour
df.drop('time', axis=1, inplace=True)

df = pd.get_dummies(df, columns=['siteID', 'is_holiday', 'Weekday', 'weather_description'])
df.sample(5)

# Defining inputs and output
X = df.drop("occupied_count", axis=1)
y = df["occupied_count"]

# Splitting into train and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Normalizing training data
st_scaler = StandardScaler()
st_scaler.fit(X_train)
X_train_scaled = st_scaler.transform(X_train)

model = Sequential(
    [Dense(20, activation="relu", input_shape=[X_train.shape[1]]),
    Dense(20, activation="relu"),
     Dense(1)])

# Compiling the ANN
model.compile(loss='mse',
             optimizer="adam",
             metrics=["mae", "mse"])

model.summary()

epochs = 30

history = model.fit(X_train_scaled, y_train.values,
                   epochs=epochs, validation_split=0.2)

model.predict(X_train_scaled[:10])

history_df = pd.DataFrame(history.history)
history_df

root_metrics_df = history_df[["mse", "val_mse"]]
#root_metrics_df = history_df[["mse", "val_mse"]].apply(np.sqrt)
#root_metrics_df.rename({"mse":"rmse", "val_mse":"val_rmse"}, axis=1, inplace=True)
root_metrics_df

plt.Figure(figsize=(14,6), dpi=100)

plt.plot(root_metrics_df["mse"], label = 'Training error')
plt.plot(root_metrics_df["val_mse"], label = 'Validation error')

plt.xlabel("Epochs")
plt.ylabel("Mean Squared Error")

# plt.xlim([0, epochs])
plt.xticks(range(1,30))
plt.legend()

plt.show()

# Prediction on test set
X_test_scaled = st_scaler.transform(X_test)
y_pred = model.predict(X_test_scaled)

# Report regression performance on test set
print("MSE: ", mean_squared_error(y_test, y_pred))
print("MAE: ", mean_absolute_error(y_test, y_pred))
