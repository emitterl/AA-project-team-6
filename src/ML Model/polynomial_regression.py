import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from model_preparation.import_model_data import model_df



model_df['Year'] = model_df['time'].dt.year
model_df['Month'] = model_df['time'].dt.month
model_df['Day'] = model_df['time'].dt.day
model_df['Hour'] = model_df['time'].dt.hour

model_df.drop('time', axis=1, inplace=True)


model_df['siteIDIsOne'] = model_df['siteID'] == '1'
model_df.drop('siteID', axis=1, inplace=True)

# Umwandlung kategorialer Variablen in Dummy-Variablen
model_df = pd.get_dummies(model_df, columns=['Weekday', 'weather_description'])

# Zielvariable und Merkmale trennen
X = model_df.drop('occupied_count', axis=1)  
y = model_df['occupied_count']               

# Aufteilen in Trainings- und Testdaten
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Definieren der Pipeline
pipeline = Pipeline([
    ('poly', PolynomialFeatures()),
    ('scaling', StandardScaler()),
    ('ridge', Ridge())
])

# Hyperparameter für die Grid-Suche
param_grid = {
    'poly__degree': [2, 3, 4],
    'poly__interaction_only': [True, False],
    'poly__include_bias': [True, False],
    'ridge__alpha': [0.001, 0.01, 0.1, 1, 10, 100], 
}

# GridSearchCV auf den Trainingsdaten
grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)

# Beste Parameter und Modell
best_params = grid_search.best_params_
best_model = grid_search.best_estimator_

# Bewertung auf den Testdaten
y_pred = best_model.predict(X_test)
test_mse = mean_squared_error(y_test, y_pred)

print("Beste Parameter:", best_params)
print("Test MSE:", test_mse)