import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
from model_data import model_df



model_df['Year'] = model_df['time'].dt.year
model_df['Month'] = model_df['time'].dt.month
model_df['Day'] = model_df['time'].dt.day
model_df['Hour'] = model_df['time'].dt.hour

model_df.drop('time', axis=1, inplace=True)


model_df['siteIDIsOne'] = model_df['siteID'] == '1'
model_df.drop('siteID', axis=1, inplace=True)

# Umwandlung kategorialer Variablen in Dummy-Variablen
model_df = pd.get_dummies(model_df, columns=['Weekday'])

# Zielvariable und Merkmale trennen
X = model_df.drop('occupied_count', axis=1)  # Merkmale
y = model_df['occupied_count']               # Zielvariable

# Aufteilung in Trainings- und Testdaten
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Erstellen polynomialer Features (Grad einstellen)
poly_degree = 5 # Grad der polynomiale Erweiterung
poly = PolynomialFeatures(degree=poly_degree)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# Skalieren der polynomialen Features
scaler = StandardScaler()
X_train_poly_scaled = scaler.fit_transform(X_train_poly)
X_test_poly_scaled = scaler.transform(X_test_poly)

# Erstellen und Trainieren des Ridge-Modells
ridge_reg = Ridge(alpha=1)
ridge_reg.fit(X_train_poly_scaled, y_train)

# Vorhersagen auf den Testdaten
y_pred = ridge_reg.predict(X_test_poly_scaled)

# Bewertung des Modells
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")
