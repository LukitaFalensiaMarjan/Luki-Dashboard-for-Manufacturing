import pandas as pd

# Buat data fiktif untuk beberapa supplier
data = {
    'nama_supplier': [
        'Supplier Cepat Express',
        'Pabrik Murah Jaya',
        'Kualitas Utama Logistik',
        'Mitra Andal Sejahtera',
        'Sumber Berkah Nusantara'
    ],
    'biaya_per_unit': [120, 85, 150, 110, 95], # Semakin rendah semakin baik
    'waktu_pengiriman_hari': [2, 7, 3, 4, 6],   # Semakin rendah semakin baik
    'rating_kualitas': [4.5, 3.0, 5.0, 4.0, 3.5] # Semakin tinggi semakin baik (skala 1-5)
}

df = pd.DataFrame(data)
df.to_csv('data_supplier.csv', index=False)

print("File 'data_supplier.csv' berhasil dibuat.")