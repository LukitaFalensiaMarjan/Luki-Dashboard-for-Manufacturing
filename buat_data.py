import pandas as pd
import numpy as np

# Determines the amount of data to be created
jumlah_data = 1000
# Determine the maximum machine life in hours as a starting point.
max_umur_mesin_jam = 5000

# Generate random sensor data within realistic ranges
suhu = np.random.uniform(30, 100, jumlah_data)
rotasi = np.random.uniform(1000, 2500, jumlah_data)
vibrasi = np.random.uniform(0, 5, jumlah_data) # Vibrasi dalam mm/s
jam_operasional = np.random.uniform(0, max_umur_mesin_jam, jumlah_data)

# New formula to calculate remaining useful life (RUL) of the machine
pengurangan_umur = (
    (suhu - 30) * 15 +             # temperature impact
    (rotasi - 1000) * 0.8 +        # Impact of rotation speed
    (vibrasi * 150) +              # Impact of vibration
    jam_operasional                # Operational hours impact
)

# Add some random noise to simulate real-world variability
noise = np.random.normal(0, 100, jumlah_data)
# Calculate remaining useful life
sisa_umur_pakai_jam = max_umur_mesin_jam - pengurangan_umur + noise
# Ensure that there is no negative remaining life value or one that exceeds the maximum life.
sisa_umur_pakai_jam = np.clip(sisa_umur_pakai_jam, 0, max_umur_mesin_jam)

# Create DataFrame
df = pd.DataFrame({
    'suhu': suhu,
    'rotasi': rotasi,
    'vibrasi': vibrasi,
    'jam_operasional': jam_operasional,
    'sisa_umur_pakai_jam': sisa_umur_pakai_jam
})

# Save to CSV
df.to_csv('data_mesin.csv', index=False)
print("The file 'data_mesin.csv' was successfully created.")