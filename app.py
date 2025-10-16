from flask import Flask, request, render_template, url_for
import joblib
import numpy as np
import pandas as pd
import mysql.connector
import datetime
from scipy.stats import norm
from math import sqrt
import tflite_runtime.interpreter as tflite
from PIL import Image
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

UPLOAD_FOLDER = 'static/uploads'
upload_path_abs = f"/home/lukifm17/mysite/{UPLOAD_FOLDER}" # Change according to your path
os.makedirs(upload_path_abs, exist_ok=True)

path_ke_file = "Change according to your path/"

# Load model
model_maintenance = joblib.load(path_ke_file + 'model_prediksi_kerusakan.joblib')
model_demand = joblib.load(path_ke_file + 'model_peramalan_permintaan.joblib')
interpreter_defect = tflite.Interpreter(model_path=path_ke_file + 'model_deteksi_cacat.tflite')
interpreter_defect.allocate_tensors()
input_details = interpreter_defect.get_input_details()
output_details = interpreter_defect.get_output_details()

# Variabel and data
db_config = { 
    'host': 'Change according to your host', 
    'user': 'Change according to your username',
    'password': 'Change according to your password',                        
    'database': 'Change according to your database name' 
}
df_supplier = pd.read_csv(path_ke_file + 'data_supplier.csv')
df_penjualan = pd.read_csv(path_ke_file + 'data_penjualan.csv', parse_dates=['tanggal'])
daftar_mesin = ["Mesin Bubut A-01", "Mesin CNC B-02", "Pompa Air C-03"]
defect_class_names = ['Kucing (Produk Bagus)', 'Anjing (Produk Cacat)']

# --- Function init_db() ---
def init_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INT AUTO_INCREMENT PRIMARY KEY, timestamp DATETIME NOT NULL, suhu FLOAT NOT NULL,
            rotasi FLOAT NOT NULL, vibrasi FLOAT NOT NULL, jam_operasional FLOAT NOT NULL,
            prediksi_rul INT NOT NULL, id_mesin VARCHAR(100)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html', daftar_mesin=daftar_mesin, active_tab='maintenance')

@app.route('/predict_maintenance', methods=['POST'])
def predict_maintenance():
    hasil_dict = {}; history_data = {}; id_mesin_terpilih = ""
    try:
        id_mesin_terpilih = request.form['id_mesin']; suhu = float(request.form['suhu']); rotasi = float(request.form['rotasi']); vibrasi = float(request.form['vibrasi']); jam_operasional = float(request.form['jam_operasional'])
        fitur = np.array([[suhu, rotasi, vibrasi, jam_operasional]]); prediksi_rul = model_maintenance.predict(fitur); sisa_jam = int(round(prediksi_rul[0], 0))
        timestamp = datetime.datetime.now(); conn = mysql.connector.connect(**db_config); cursor = conn.cursor()
        sql = 'INSERT INTO history (timestamp, suhu, rotasi, vibrasi, jam_operasional, prediksi_rul, id_mesin) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        val = (timestamp, suhu, rotasi, vibrasi, jam_operasional, sisa_jam, id_mesin_terpilih); cursor.execute(sql, val); conn.commit()
        sql_select = "SELECT * FROM history WHERE id_mesin = %s ORDER BY timestamp"; history_df = pd.read_sql_query(sql_select, conn, params=(id_mesin_terpilih,)); conn.close()
        if sisa_jam > 500:
            hasil_dict['urgensi'] = "Normal"; hasil_dict['rekomendasi'] = "Lanjutkan operasi..."; hasil_dict['warna_alert'] = "success"
        else:
            if 50 < sisa_jam <= 500:
                hasil_dict['urgensi'] = "Periksa Segera"; hasil_dict['rekomendasi'] = "Jadwalkan perawatan..."; hasil_dict['warna_alert'] = "warning"
            else:
                hasil_dict['urgensi'] = "Kritis"; hasil_dict['rekomendasi'] = "Segera Hentikan Mesin!"; hasil_dict['warna_alert'] = "danger"
            feature_names = ['Suhu', 'Rotasi', 'Vibrasi', 'Jam Operasional']; importances = model_maintenance.feature_importances_
            feature_importance_map = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)
            penjelasan = "Pemicu Utama: " + ", ".join([f"{n} ({i:.0%})" for n, i in feature_importance_map[:2]])
            hasil_dict['penyebab'] = penjelasan
        hasil_dict['sisa_jam'] = sisa_jam
        history_data['labels_riwayat'] = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in history_df['timestamp']]; history_data['data_riwayat'] = list(history_df['prediksi_rul'])
    except Exception as e:
        hasil_dict['urgensi'] = str(e); hasil_dict['warna_alert'] = "secondary"
    return render_template('index.html', daftar_mesin=daftar_mesin, hasil_maintenance=hasil_dict, riwayat_maintenance=history_data, id_mesin_terpilih=id_mesin_terpilih, active_tab='maintenance')

@app.route('/show_history', methods=['POST'])
def show_history():
    history_data = {}; id_mesin_terpilih = ""
    try:
        id_mesin_terpilih = request.form['id_mesin_history']; conn = mysql.connector.connect(**db_config)
        sql_select = "SELECT * FROM history WHERE id_mesin = %s ORDER BY timestamp"; history_df = pd.read_sql_query(sql_select, conn, params=(id_mesin_terpilih,)); conn.close()
        history_data['labels_riwayat'] = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in history_df['timestamp']]; history_data['data_riwayat'] = list(history_df['prediksi_rul'])
    except Exception as e:
        print(f"Error fetching history: {e}")
    return render_template('index.html', daftar_mesin=daftar_mesin, riwayat_maintenance=history_data, id_mesin_terpilih=id_mesin_terpilih, active_tab='maintenance')

@app.route('/predict_demand', methods=['POST'])
def predict_demand():
    data_historis = df_penjualan.tail(180); labels_historis = [d.strftime('%Y-%m-%d') for d in data_historis['tanggal']]; data_historis_list = list(data_historis['jumlah_penjualan'])
    keyakinan_persen = int(request.form['keyakinan']); ada_promosi_di_masa_depan = 1 if 'promosi' in request.form else 0
    future_dates = pd.date_range(start=df_penjualan['tanggal'].iloc[-1], periods=90, freq='D'); future_df = pd.DataFrame({'tanggal': future_dates})
    future_df['tahun'] = future_df['tanggal'].dt.year; future_df['bulan'] = future_df['tanggal'].dt.month; future_df['hari'] = future_df['tanggal'].dt.day; future_df['hari_dalam_seminggu'] = future_df['tanggal'].dt.dayofweek; future_df['hari_dalam_tahun'] = future_df['tanggal'].dt.dayofyear
    future_df['ada_promosi'] = ada_promosi_di_masa_depan; X_future = future_df[['tahun', 'bulan', 'hari', 'hari_dalam_seminggu', 'hari_dalam_tahun', 'ada_promosi']]
    prediksi_per_pohon = np.array([tree.predict(X_future) for tree in model_demand.estimators_]); std_dev_per_prediksi = np.std(prediksi_per_pohon, axis=0); prediksi_utama = model_demand.predict(X_future)
    alpha = 1 - (keyakinan_persen / 100.0); faktor_keyakinan = norm.ppf(1 - alpha / 2)
    batas_atas = prediksi_utama + faktor_keyakinan * std_dev_per_prediksi; batas_bawah = prediksi_utama - faktor_keyakinan * std_dev_per_prediksi
    data_ramalan = [int(x) for x in prediksi_utama]; data_batas_atas = [int(x) for x in batas_atas]; data_batas_bawah = [int(x) for x in batas_bawah]; labels_ramalan = [d.strftime('%Y-%m-%d') for d in future_dates]
    return render_template('index.html', daftar_mesin=daftar_mesin, labels_ramalan=labels_ramalan, data_ramalan=data_ramalan,data_batas_atas=data_batas_atas,data_batas_bawah=data_batas_bawah,labels_historis=labels_historis,data_historis=data_historis_list,keyakinan_persen=keyakinan_persen, active_tab='planning')

@app.route('/predict_supply_chain', methods=['POST'])
def predict_supply_chain():
    bobot_biaya = int(request.form['bobot_biaya']); bobot_waktu = int(request.form['bobot_waktu']); bobot_kualitas = int(request.form['bobot_kualitas'])
    df_ranked = df_supplier.copy(); df_norm = df_supplier.copy()
    for column in ['biaya_per_unit', 'waktu_pengiriman_hari', 'rating_kualitas']:
        min_val = df_norm[column].min(); max_val = df_norm[column].max()
        if (max_val - min_val) != 0: df_norm[column] = (df_norm[column] - min_val) / (max_val - min_val)
        else: df_norm[column] = 0
    skor = (bobot_biaya * (1 - df_norm['biaya_per_unit'])) + (bobot_waktu * (1 - df_norm['waktu_pengiriman_hari'])) + (bobot_kualitas * df_norm['rating_kualitas'])
    df_ranked['skor_rekomendasi'] = skor; df_ranked = df_ranked.sort_values(by='skor_rekomendasi', ascending=False).reset_index(drop=True)
    peringkat_supplier = df_ranked.to_dict('records')
    return render_template('index.html', daftar_mesin=daftar_mesin, peringkat_supplier=peringkat_supplier, active_tab='planning')

@app.route('/optimize_inventory', methods=['POST'])
def optimize_inventory():
    try:
        biaya_pesan = float(request.form['biaya_pesan']); biaya_simpan = float(request.form['biaya_simpan']); lead_time = int(request.form['lead_time']); safety_stock = int(request.form['safety_stock'])
        future_dates = pd.date_range(start=df_penjualan['tanggal'].iloc[-1], periods=365, freq='D'); future_df = pd.DataFrame({'tanggal': future_dates})
        future_df['tahun'] = future_df['tanggal'].dt.year; future_df['bulan'] = future_df['tanggal'].dt.month; future_df['hari'] = future_df['tanggal'].dt.day; future_df['hari_dalam_seminggu'] = future_df['tanggal'].dt.dayofweek; future_df['hari_dalam_tahun'] = future_df['tanggal'].dt.dayofyear
        future_df['ada_promosi'] = 0; X_future = future_df[['tahun', 'bulan', 'hari', 'hari_dalam_seminggu', 'hari_dalam_tahun', 'ada_promosi']]
        prediksi_setahun = model_demand.predict(X_future); permintaan_total_tahunan = sum(prediksi_setahun); permintaan_harian_rata2 = permintaan_total_tahunan / 365
        eoq = sqrt((2 * permintaan_total_tahunan * biaya_pesan) / biaya_simpan); rop = (permintaan_harian_rata2 * lead_time) + safety_stock
        hasil_eoq = int(round(eoq, 0)); hasil_rop = int(round(rop, 0))
    except Exception as e:
        hasil_eoq = f"Error: {e}"; hasil_rop = ""
    return render_template('index.html', daftar_mesin=daftar_mesin, hasil_eoq=hasil_eoq, hasil_rop=hasil_rop, active_tab='planning')

@app.route('/predict_defect', methods=['POST'])
def predict_defect():
    if 'file' not in request.files:
        return render_template('index.html', daftar_mesin=daftar_mesin, hasil_prediksi_defect="Tidak ada file yang diunggah.", active_tab='quality')
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', daftar_mesin=daftar_mesin, hasil_prediksi_defect="File belum dipilih.", active_tab='quality')
    if file:
        filepath = os.path.join(upload_path_abs, file.filename)
        file.save(filepath)
        img = Image.open(filepath).convert('RGB').resize((180, 180))
        img_array = np.array(img, dtype=np.float32)
        img_array = np.expand_dims(img_array, 0)
        img_array = img_array / 255.0
        interpreter_defect.set_tensor(input_details[0]['index'], img_array)
        interpreter_defect.invoke()
        predictions = interpreter_defect.get_tensor(output_details[0]['index'])
        score_exp = np.exp(predictions[0])
        score = score_exp / np.sum(score_exp)
        hasil = f"Prediksi: {defect_class_names[np.argmax(score)]} ({100 * np.max(score):.2f}%)"
        gambar_url = url_for('static', filename='uploads/' + file.filename)
        return render_template('index.html', daftar_mesin=daftar_mesin, hasil_prediksi_defect=hasil, gambar_hasil_defect=gambar_url, active_tab='quality')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)