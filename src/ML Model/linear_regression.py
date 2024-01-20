import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from model_preparation.import_model_data import model_df
import pandas as pd


model_df['Year'] = model_df['time'].dt.year
model_df['Month'] = model_df['time'].dt.month
model_df['Day'] = model_df['time'].dt.day
model_df['Hour'] = model_df['time'].dt.hour

model_df.drop('time', axis=1, inplace=True)

# Umwandlung kategorialer Variablen in Dummy-Variablen
model_df = pd.get_dummies(model_df, columns=['Weekday', 'weather_description'])

model_df['siteIDIsOne'] = model_df['siteID'] == '1'
model_df.drop('siteID', axis=1, inplace=True)

# Zielvariable und Merkmale trennen
X = model_df.drop('occupied_count', axis=1)  # Merkmale
y = model_df['occupied_count']               # Zielvariable

pipeline = Pipeline([
    ('scaling', StandardScaler()),
    ('lin_reg', LinearRegression())
])

# Einstellen der Parameter für die Kreuzvalidierung
kfold = KFold(n_splits=5, shuffle=True, random_state=42)

# Durchführen der Kreuzvalidierung
scores = cross_val_score(pipeline, X, y, cv=kfold, scoring='neg_mean_squared_error')

# Berechnen des durchschnittlichen MSE
average_mse = -scores.mean()

print(f"Durchschnittlicher Mean Squared Error: {average_mse}")