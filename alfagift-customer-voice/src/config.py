"""Konstanta & konfigurasi dashboard."""
from pathlib import Path

from src.components import BRAND
from src.issues import ISSUES

ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / "assets" / "favicon.png"

# File data yang dibaca (yang pertama ada = default)
DATA_FILES = [ROOT / "data" / "final" / "model_predictions_common_test_set.csv",
              ROOT / "data" / "final" / "model_predictions_all.csv"]

NEG = {"negatif", "negative", "neg"}
ORDER = ["Positif", "Netral", "Negatif"]
RATINGS = [1, 2, 3, 4, 5]
PALETTE = [BRAND["red"], BRAND["navy"], BRAND["yellow"], "#1E9E5A", "#8B5CF6", "#F97316", "#06B6D4", "#64748B"]

INFO = {**ISSUES, "Lainnya": {
    "icon": "📝",
    "description": "Review negatif yang belum cocok dengan keyword kategori mana pun. Bisa berisi keluhan umum atau topik baru.",
    "recommendation": "Baca contoh review ini untuk menemukan topik baru, lalu tambahkan keyword-nya di src/issues.py."}}

STOP = set("""yang dan di ke dari ini itu untuk dengan saya aku tidak gak ga nggak tak ada pada juga sudah udah aja saja
bisa jadi kok sih nya lagi atau karena kalau kalo tapi tp banget sekali lebih mau akan dalam oleh sama yg dg dgn sy ya apa
mohon harus kenapa gimana sangat sudah masih belum mulai selalu setiap semua banyak cuma hanya kali pas dulu saat setelah
sebelum lalu terus pake pakai aplikasi alfagift alfamart app""".split())

# Urutan menu = urutan alur membaca: ringkasan -> analisis -> data -> info
MENU = {"Overview": "📊", "Coba Prediksi": "🧪", "Sentiment": "💬", "Masalah Pengguna": "🛠️",
        "Insights": "💡", "Tren": "📈", "Kata Kunci": "🔤", "Versi Aplikasi": "📱",
        "Reviews": "🔎", "Performa Model": "🤖", "Tentang Alfagift": "🎁"}

EXAMPLES = [
    ("🛵 Pengiriman lambat", "Pesanan sudah 4 jam belum sampai, status di aplikasi tidak berubah dan kurirnya susah dihubungi. Kecewa banget.", 1),
    ("🔐 OTP tidak masuk", "Udah coba berkali-kali tapi OTP gak pernah masuk, jadi gak bisa login sama sekali.", 2),
    ("💚 Puas belanja", "Belanja jadi gampang, promonya banyak dan barang sampai cepat. Mantap!", 5),
    ("🎭 Bintang tidak selaras", "Aplikasinya sering error dan lemot pas checkout, tapi yaudah deh.", 5),
]
