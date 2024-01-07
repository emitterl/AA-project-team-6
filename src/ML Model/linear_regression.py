import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from model_data import model_df
import pandas as pd

# Umwandlung kategorialer Variablen in Dummy-Variablen
model_df = pd.get_dummies(model_df, columns=['Weekday'])

model_df['siteIDIsOne'] = model_df['siteID'] == '1'
model_df.drop('siteID', axis=1, inplace=True)

# Zielvariable und Merkmale trennen
X = model_df.drop('occupied_count', axis=1)  # Merkmale
y = model_df['occupied_count']               # Zielvariable


# Aufteilung in Trainings- und Testdaten
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print(X_train.head())


# Initialisieren des StandardScaler
scaler = StandardScaler()

# Anpassen des Scalers nur auf die Trainingsdaten
scaler.fit(X_train)

# Skalieren der Trainings- und Testdaten
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Erstellen und Trainieren des linearen Regressionsmodells
lin_reg = LinearRegression()
lin_reg.fit(X_train_scaled, y_train)

# Vorhersagen auf den Testdaten
y_pred = lin_reg.predict(X_test_scaled)

# Bewertung des Modells
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")