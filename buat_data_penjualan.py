import pandas as pd
import numpy as np

# Buat rentang tanggal selama 3 tahun
dates = pd.date_range(start='2022-01-01', end='2024-12-31', freq='D')

# Buat tren penjualan yang meningkat
trend = np.linspace(start=100, stop=300, num=len(dates))

# Buat pola musiman (penjualan lebih tinggi di akhir pekan)
seasonality = 1 + (dates.dayofweek // 5) * 0.5

# --- BAGIAN BARU: Tambahkan faktor promosi ---
# Anggap ada promosi acak sekitar 5% dari total hari
np.random.seed(42) # Agar hasil acaknya selalu sama
ada_promosi = np.random.choice([0, 1], size=len(dates), p=[0.95, 0.05])
# Efek promosi: menaikkan penjualan sebanyak 150 unit
efek_promosi = ada_promosi * 150 

# Tambahkan noise/acak
noise = np.random.normal(loc=0, scale=20, size=len(dates))

# Gabungkan semua komponen
jumlah_penjualan = trend * seasonality + efek_promosi + noise
jumlah_penjualan = np.maximum(jumlah_penjualan, 20).astype(int)

# Buat DataFrame
df = pd.DataFrame({
    'tanggal': dates,
    'ada_promosi': ada_promosi, # Kolom baru
    'jumlah_penjualan': jumlah_penjualan
})

df.to_csv('data_penjualan.csv', index=False)
print(f"File 'data_penjualan.csv' versi upgrade (dengan promosi) berhasil dibuat.")