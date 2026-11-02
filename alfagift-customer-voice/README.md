# Alfagift Customer Voice Analytics

Dashboard Streamlit untuk menganalisis ulasan pengguna aplikasi **Alfagift** (Google Play):
sentimen, area masalah pengguna, tren, versi aplikasi, dan contoh review nyata.
Prediksi sentimen memakai hasil model **IndoBERT** dari penelitian skripsi
(dibandingkan dengan SVM + TF-IDF dan XLM-R).

## Fitur

| Menu | Isi |
|------|-----|
| Overview | Ringkasan sentimen, rating, dan area yang perlu perhatian |
| Coba Prediksi | Demo prediksi sentimen satu ulasan + saran tindak lanjut |
| Tentang Alfagift | Profil singkat layanan |
| Sentiment | Distribusi sentimen dan rating |
| Masalah Pengguna | Review negatif dikelompokkan per kategori masalah |
| Insights | Rekomendasi perbaikan per kategori |
| Tren | Perubahan review negatif per kategori dari waktu ke waktu |
| Kata Kunci | Kata/frasa yang paling sering muncul |
| Versi Aplikasi | Sentimen per versi aplikasi |
| Reviews | Pencarian dan unduh review |
| Performa Model | Metrik dan confusion matrix IndoBERT |

## Struktur Proyek

```
alfagift-customer-voice/
├── app.py                  # entry point: setup, sidebar, filter, routing
├── src/
│   ├── config.py           # konstanta, menu, contoh prediksi
│   ├── data.py             # load data, model prediksi, fungsi analisis
│   ├── context.py          # Ctx: data terfilter + helper tampilan
│   ├── components.py       # komponen UI & CSS
│   ├── issues.py           # kategori masalah + keyword mapping (edit di sini)
│   ├── predictor.py        # mesin prediksi (IndoBERT -> SVM -> aturan kata)
│   └── views/              # satu file per halaman (overview.py, predict.py, ...)
├── assets/                 # logo & favicon
├── data/
│   ├── final/              # data prediksi yang dibaca dashboard
│   └── results/            # metrik, uji McNemar, confusion matrix (referensi skripsi)
├── .streamlit/config.toml  # tema terang (base = "light") & konfigurasi server
├── requirements.txt
└── README.md
```

## Menambah Halaman Baru

1. Buat `src/views/nama.py` dengan fungsi `render(c)` (`c` = objek `Ctx`, berisi `c.fdf` data terfilter dll.).
2. Daftarkan di `src/views/__init__.py` (`PAGES`) dan `src/config.py` (`MENU`).

## Menjalankan Lokal

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy ke Streamlit Community Cloud

1. Push repo ini ke GitHub.
2. Buka [share.streamlit.io](https://share.streamlit.io) → **Create app**.
3. Pilih repo dan branch, isi **Main file path** dengan `app.py`.
4. Klik **Deploy**.

## Catatan Mesin Prediksi

Halaman *Coba Prediksi* memilih mesin secara otomatis:

1. **IndoBERT fine-tuned** — jika folder model ada di `models/indobert/`
   (atau path lain lewat variabel lingkungan `ALFAGIFT_MODEL_DIR`).
   Butuh `torch` dan `transformers`; model berukuran besar sehingga tidak disertakan di repo
   dan tidak cocok untuk paket gratis Streamlit Cloud.
2. **SVM + TF-IDF** — dilatih otomatis dari data review saat aplikasi dibuka (default saat deploy).
3. **Aturan kata sederhana** — cadangan terakhir.

Untuk memakai IndoBERT secara lokal, simpan model dari notebook:

```python
trainer.save_model("models/indobert")
tokenizer.save_pretrained("models/indobert")
```

Urutan kelas: `0 = Negatif`, `1 = Netral`, `2 = Positif`
(atau isi `id2label` pada config), lalu `pip install torch transformers`.

## Mengubah Kategori Masalah

Keyword tiap kategori ada di `src/issues.py` dan sengaja dibuat transparan.
Tambahkan atau ubah keyword sesuai hasil pembacaan review asli.

## Catatan Metodologis

Model hasil penelitian dipakai sebagai mesin klasifikasi. Insight bisnis adalah
interpretasi pola review negatif, bukan klaim bahwa setiap rekomendasi terbukti
memperbaiki operasional. Data berasal dari ulasan publik Google Play.
