import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv('data_penjualan.csv', parse_dates=['tanggal'])

# Feature Engineering
df['tahun'] = df['tanggal'].dt.year
df['bulan'] = df['tanggal'].dt.month
df['hari'] = df['tanggal'].dt.day
df['hari_dalam_seminggu'] = df['tanggal'].dt.dayofweek
df['hari_dalam_tahun'] = df['tanggal'].dt.dayofyear

# --- V2: Include Promotion Feature ---
X = df[['tahun', 'bulan', 'hari', 'hari_dalam_seminggu', 'hari_dalam_tahun', 'ada_promosi']]
y = df['jumlah_penjualan']

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the trained model
joblib.dump(model, 'model_peramalan_permintaan.joblib')
print("Demand Forecasting Model V2 was successfully trained.")