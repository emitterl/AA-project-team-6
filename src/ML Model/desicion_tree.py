import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_squared_error
from model_preparation.import_model_data import model_df

# Aufteilen der 'time'-Spalte in Jahr, Monat, Tag und Stunde
model_df['Year'] = model_df['time'].dt.year
model_df['Month'] = model_df['time'].dt.month
model_df['Day'] = model_df['time'].dt.day
model_df['Hour'] = model_df['time'].dt.hour
model_df.drop('time', axis=1, inplace=True)

# Ich halte mögliche Vergleiche wie Weekday >= 5 sinnvoll, um Wochentag und Wochenende unterscheiden zu können
weekday_map = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
model_df['Weekday'] = model_df['Weekday'].map(weekday_map)

# Umwandlung kategorialer Variablen in Dummy-Variablen
model_df = pd.get_dummies(model_df, columns=['weather_description'])

# Zielvariable und Merkmale trennen
X = model_df.drop('occupied_count', axis=1)
y = model_df['occupied_count']

# Aufteilen in Trainings- und Testdaten
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Parameter für GridSearchCV
param_grid = {
    'max_depth': [5, 7, 10],
    'min_samples_leaf': [50, 100, 500, 1000, 1500],
    'max_features': ['sqrt', 'log2', None]
}

# GridSearchCV auf den Trainingsdaten
grid_search = GridSearchCV(DecisionTreeRegressor(random_state=42, ccp_alpha=0.1), param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)

# Beste Parameter und Modell
best_params = grid_search.best_params_
best_tree = grid_search.best_estimator_

plt.figure(figsize=(30, 15))
plot_tree(best_tree, feature_names=X.columns, filled=True)
plt.savefig('decision_tree.svg', format='svg')
plt.close() 

# Bewertung auf den Testdaten
y_pred = best_tree.predict(X_test)
test_mse = mean_squared_error(y_test, y_pred)

print("Beste Parameter:", best_params)
print("Test MSE:", test_mse)