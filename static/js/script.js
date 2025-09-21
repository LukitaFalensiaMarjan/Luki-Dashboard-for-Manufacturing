// Menunggu hingga seluruh halaman dimuat sebelum menjalankan script
document.addEventListener('DOMContentLoaded', function() {
    
    // Logika untuk slider Supply Chain
    const bobotBiayaSlider = document.getElementById('bobot_biaya');
    const valBiayaSpan = document.getElementById('val_biaya');
    if (bobotBiayaSlider && valBiayaSpan) {
        bobotBiayaSlider.addEventListener('input', function() {
            valBiayaSpan.innerText = this.value;
        });
    }

    const bobotWaktuSlider = document.getElementById('bobot_waktu');
    const valWaktuSpan = document.getElementById('val_waktu');
    if (bobotWaktuSlider && valWaktuSpan) {
        bobotWaktuSlider.addEventListener('input', function() {
            valWaktuSpan.innerText = this.value;
        });
    }

    const bobotKualitasSlider = document.getElementById('bobot_kualitas');
    const valKualitasSpan = document.getElementById('val_kualitas');
    if (bobotKualitasSlider && valKualitasSpan) {
        bobotKualitasSlider.addEventListener('input', function() {
            valKualitasSpan.innerText = this.value;
        });
    }

    // Logika untuk slider Demand Forecasting
    const keyakinanSlider = document.getElementById('keyakinan');
    const valKeyakinanSpan = document.getElementById('val_keyakinan');
    if (keyakinanSlider && valKeyakinanSpan) {
        keyakinanSlider.addEventListener('input', function() {
            valKeyakinanSpan.innerText = this.value;
        });
    }

});