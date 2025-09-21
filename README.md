# Dashboard AI Manufaktur

Aplikasi web full-stack yang berfungsi sebagai pusat komando cerdas (Intelligent Command Center) untuk operasi manufaktur, menyediakan analisis dan rekomendasi berbasis AI secara real-time.

## Latar Belakang & Tujuan Proyek
Tujuan proyek ini adalah untuk membangun sebuah platform terintegrasi yang menerapkan berbagai teknik Machine Learning dan Deep Learning untuk memecahkan masalah umum di dunia industri, mulai dari perawatan mesin hingga perencanaan bisnis. Aplikasi ini dirancang untuk menjadi portofolio yang menunjukkan kemampuan end-to-end dalam pengembangan produk AI, dari ide hingga deployment.

## Fitur Utama
- **Perawatan Prediktif (Predictive Maintenance)**
  - Memantau beberapa mesin secara terpisah.
  - Menyimpan riwayat kesehatan mesin ke database MySQL.
  - Memprediksi Sisa Umur Pakai (Remaining Useful Life - RUL) dalam jam.
  - Memberikan klasifikasi urgensi (Normal, Waspada, Kritis) dan rekomendasi tindakan.
  - Menampilkan faktor pemicu utama kerusakan menggunakan **Explainable AI (XAI)**.

- **Peramalan Permintaan (Demand Forecasting)**
  - Menampilkan data penjualan historis berdampingan dengan peramalan masa depan.
  - Mempertimbangkan input faktor eksternal seperti kampanye marketing.
  - Menyajikan hasil dengan **Rentang Keyakinan (Confidence Interval)** yang dapat diatur (50%-99%).

- **Optimasi Rantai Pasok (Supply Chain Optimization)**
  - Menerima input preferensi pengguna (sliders) untuk biaya, waktu, dan kualitas.
  - Menampilkan **tabel peringkat lengkap** semua supplier, diurutkan berdasarkan skor rekomendasi.

- **Optimasi Inventaris (Inventory Optimization)**
  - Menghitung **Economic Order Quantity (EOQ)** untuk menentukan jumlah pesanan paling efisien.
  - Menghitung **Reorder Point (ROP)** untuk menentukan waktu pemesanan ulang.

- **Kontrol Kualitas (Quality Control)**
  - Menggunakan model **Computer Vision (Deep Learning)** untuk klasifikasi gambar.
  - Memungkinkan pengguna mengunggah gambar produk untuk dianalisis secara real-time.
  - Diimplementasikan menggunakan **TensorFlow Lite** untuk efisiensi di lingkungan server.

## Tumpukan Teknologi (Tech Stack)
- **Backend**: Python, Flask
- **Database**: MySQL
- **AI/ML**: Scikit-learn, Pandas, NumPy, TensorFlow Lite, SciPy
- **Frontend**: HTML, CSS, JavaScript, Bootstrap, Chart.js
- **Deployment**: PythonAnywhere, Git

## Sorotan Proyek (Project Highlights)
- **Integrasi 5 Model AI Berbeda**: Menunjukkan keluasan pemahaman dalam berbagai paradigma AI (Regresi, Klasifikasi, Optimasi, Deep Learning).
- **Implementasi Fitur Lanjutan**: Menerapkan konsep canggih seperti XAI dan Confidence Interval.
- **Arsitektur Full-Stack**: Menggabungkan backend, frontend, dan database menjadi satu aplikasi yang kohesif.
- **Efisiensi Deployment**: Berhasil mengkonversi dan men-deploy model TensorFlow yang besar di lingkungan server dengan sumber daya terbatas menggunakan TFLite.