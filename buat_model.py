import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv('data_mesin.csv')

# Separate Features (4 inputs) and Target (1 output)
X = df[['suhu', 'rotasi', 'vibrasi', 'jam_operasional']]
y = df['sisa_umur_pakai_jam']

# Train a Random Forest Regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the trained model using joblib
joblib.dump(model, 'model_prediksi_kerusakan.joblib')

print("Model AI Regresi berhasil dilatih dan disimpan kembali.")