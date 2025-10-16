import pandas as pd
import numpy as np

# Create a date range of 3 years (2022-2024)
dates = pd.date_range(start='2022-01-01', end='2024-12-31', freq='D')

# Create an increasing sales trend
trend = np.linspace(start=100, stop=300, num=len(dates))

# Add weekly seasonality (higher sales on weekends)
seasonality = 1 + (dates.dayofweek // 5) * 0.5

# Add promotional events (randomly scattered)
np.random.seed(42) # For reproducibility
ada_promosi = np.random.choice([0, 1], size=len(dates), p=[0.95, 0.05])
# Promotional effect: increase sales by 150 units on promo days
efek_promosi = ada_promosi * 150 

# Add random noise
noise = np.random.normal(loc=0, scale=20, size=len(dates))

# Calculate final sales numbers
jumlah_penjualan = trend * seasonality + efek_promosi + noise
jumlah_penjualan = np.maximum(jumlah_penjualan, 20).astype(int)

# create DataFrame and save to CSV
df = pd.DataFrame({
    'tanggal': dates,
    'ada_promosi': ada_promosi, # Kolom baru
    'jumlah_penjualan': jumlah_penjualan
})

df.to_csv('data_penjualan.csv', index=False)
print(f"The file 'data_penjualan.csv' was successfully created.")