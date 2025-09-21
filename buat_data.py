import pandas as pd
import numpy as np

# Menentukan jumlah data yang akan dibuat
jumlah_data = 1000
# Menentukan umur maksimal mesin dalam jam sebagai titik awal
max_umur_mesin_jam = 5000

# Membuat data acak untuk 4 fitur sensor
suhu = np.random.uniform(30, 100, jumlah_data)
rotasi = np.random.uniform(1000, 2500, jumlah_data)
vibrasi = np.random.uniform(0, 5, jumlah_data) # Vibrasi dalam mm/s
jam_operasional = np.random.uniform(0, max_umur_mesin_jam, jumlah_data)

# --- FORMULA YANG DISEIMBANGKAN ---
# Logika untuk menghitung pengurangan umur pakai mesin berdasarkan data sensor.
# Dampak vibrasi dikurangi, sementara dampak suhu & rotasi sedikit dinaikkan agar lebih realistis.
pengurangan_umur = (
    (suhu - 30) * 15 +             # Dampak suhu
    (rotasi - 1000) * 0.8 +        # Dampak rotasi
    (vibrasi * 150) +              # Dampak vibrasi
    jam_operasional
)

# Menambahkan sedikit noise/acak agar data tidak terlalu sempurna dan lebih realistis
noise = np.random.normal(0, 100, jumlah_data)
# Menghitung sisa umur pakai mesin
sisa_umur_pakai_jam = max_umur_mesin_jam - pengurangan_umur + noise
# Memastikan tidak ada nilai sisa umur yang negatif atau melebihi umur maksimal
sisa_umur_pakai_jam = np.clip(sisa_umur_pakai_jam, 0, max_umur_mesin_jam)

# Membuat DataFrame menggunakan library pandas
df = pd.DataFrame({
    'suhu': suhu,
    'rotasi': rotasi,
    'vibrasi': vibrasi,
    'jam_operasional': jam_operasional,
    'sisa_umur_pakai_jam': sisa_umur_pakai_jam
})

# Menyimpan DataFrame ke dalam file CSV
df.to_csv('data_mesin.csv', index=False)

print("File 'data_mesin.csv' dengan formula baru berhasil dibuat.")