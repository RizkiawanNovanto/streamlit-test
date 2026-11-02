"""Kategori masalah & keyword mapping (edit di sini untuk menambah/ubah kategori)."""
import re

ISSUES = {
    "Pembayaran": {"icon": "💳",
        "keywords": ["bayar","pembayaran","payment","transaksi","qris","ovo","gopay","dana","saldo","transfer","virtual account","gagal bayar"],
        "description": "Review yang membahas kendala pembayaran, transaksi gagal, pembayaran tertahan, atau metode pembayaran yang tidak berjalan sesuai harapan.",
        "recommendation": "Perjelas status transaksi, perbaiki penanganan transaksi gagal atau tertahan, dan tampilkan pesan error yang mudah dipahami pengguna."},
    "Kurir & Pengiriman": {"icon": "🛵",
        "keywords": ["kurir","pengiriman","antar","diantar","delivery","terlambat","telat","paket","tracking","lacak","driver","pickup","same day","instant","ongkir"],
        "description": "Review mengenai kecepatan pengiriman, pengalaman dengan kurir, tracking, ongkir, dan ketepatan status pesanan.",
        "recommendation": "Perbaiki akurasi tracking, notifikasi perubahan status, serta monitoring keterlambatan pada proses pengiriman."},
    "Performa Aplikasi": {"icon": "⚡",
        "keywords": ["lemot","lambat","loading","ngelag","lag","hang","crash","force close","blank","freeze","error","bug","tidak bisa dibuka","respons","respon"],
        "description": "Review yang mengeluhkan aplikasi lambat, error, crash, halaman kosong, atau interaksi yang tidak responsif.",
        "recommendation": "Prioritaskan stabilitas aplikasi dan waktu respons pada alur yang paling sering digunakan, serta pantau crash dan error berdasarkan versi aplikasi."},
    "Promo & Harga": {"icon": "🏷️",
        "keywords": ["promo","diskon","voucher","kupon","cashback","harga","potongan","tebus murah","gratis ongkir","kode promo"],
        "description": "Review tentang promo, voucher, diskon, harga, dan program penawaran yang digunakan pelanggan.",
        "recommendation": "Tampilkan syarat promo secara lebih jelas, validasi voucher sebelum checkout, dan jelaskan harga akhir sebelum pembayaran."},
    "Produk & Stok": {"icon": "📦",
        "keywords": ["stok","stock","barang","produk","habis","kosong","tidak tersedia","tidak ada","katalog","catalog","varian"],
        "description": "Review terkait ketersediaan produk, akurasi stok, katalog, dan perbedaan informasi produk.",
        "recommendation": "Tingkatkan sinkronisasi stok dan tampilkan ketersediaan produk yang lebih akurat sebelum pengguna melakukan checkout."},
    "Pesanan & Checkout": {"icon": "🛒",
        "keywords": ["checkout","pesan","pesanan","order","keranjang","cart","batal","cancel","pesanan hilang","pesanan gagal","tambah keranjang"],
        "description": "Review mengenai keranjang, checkout, pembuatan pesanan, pembatalan, dan status order.",
        "recommendation": "Perjelas ringkasan order, sederhanakan checkout, dan tampilkan status pesanan yang konsisten sejak dibuat sampai selesai."},
    "Customer Service": {"icon": "🎧",
        "keywords": ["cs","customer service","admin","komplain","complaint","bantuan","help","lapor","keluhan","dibalas","jawaban"],
        "description": "Review yang membahas respons customer service, penanganan komplain, dan kemudahan mendapatkan bantuan.",
        "recommendation": "Percepat respons, berikan status penyelesaian komplain yang jelas, dan sediakan akses bantuan yang mudah ditemukan."},
    "Akun & Membership": {"icon": "👤",
        "keywords": ["akun","login","masuk","otp","password","member","membership","poin","point","stamp","registrasi","daftar","nomor hp"],
        "description": "Review terkait login, OTP, akun pengguna, membership, poin, dan registrasi.",
        "recommendation": "Tingkatkan reliabilitas login dan OTP serta berikan feedback yang jelas saat akun atau benefit membership mengalami kendala."},
}


def normalize(text):
    text = re.sub(r"[^a-zA-ZÀ-ÿ0-9\s]", " ", str(text).lower())
    return re.sub(r"\s+", " ", text).strip()


# \b di awal kata mencegah salah cocok (mis. "cs" di tengah kata)
PATTERNS = {n: [re.compile(r"\b" + re.escape(normalize(k))) for k in i["keywords"]] for n, i in ISSUES.items()}


def issue_for(text):
    text = normalize(text)
    scores = {n: sum(1 for p in pats if p.search(text)) for n, pats in PATTERNS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] else "Lainnya"


# ----------------------------------------------------------------------------
# Untuk halaman "Coba Prediksi": deteksi topik, tindak lanjut, dan contoh balasan
# ----------------------------------------------------------------------------
def rank_issues(text):
    """Kategori masalah yang cocok dengan teks, diurutkan dari kecocokan terbanyak."""
    t = normalize(text)
    scores = {n: sum(1 for p in pats if p.search(t)) for n, pats in PATTERNS.items()}
    return sorted([(n, s) for n, s in scores.items() if s > 0], key=lambda x: -x[1])


def matched_keywords(text, cat):
    """Kata kunci pada teks yang membuat kategori tersebut terdeteksi."""
    if cat not in ISSUES:
        return []
    t = normalize(text)
    return [k for k, p in zip(ISSUES[cat]["keywords"], PATTERNS[cat]) if p.search(t)]


ACTIONS = {
    "Pembayaran": {"owner": "Tim Payment & Engineering",
        "steps": ["Periksa log transaksi gagal atau tertahan pada metode pembayaran yang disebut pengguna.",
                  "Tampilkan status transaksi dan pesan error yang mudah dipahami di aplikasi.",
                  "Siapkan jalur pengembalian dana otomatis atau notifikasi saat dana tertahan."],
        "reply": "Mohon maaf atas kendala pembayaran yang Anda alami. Kami sedang memeriksa transaksi tersebut. Mohon kirimkan nomor pesanan dan metode pembayaran melalui fitur bantuan agar dapat segera kami tindak lanjuti."},
    "Kurir & Pengiriman": {"owner": "Tim Operasional & Logistik",
        "steps": ["Cek status dan estimasi pengiriman pesanan yang dikeluhkan.",
                  "Perbaiki akurasi tracking dan kirim notifikasi saat status berubah atau terjadi keterlambatan.",
                  "Pantau keterlambatan per area atau kurir, lalu beri kabar proaktif atau kompensasi bila perlu."],
        "reply": "Mohon maaf atas keterlambatan pengiriman pesanan Anda. Kami telah meneruskan kendala ini ke tim terkait. Mohon kirimkan nomor pesanan melalui fitur bantuan agar status pengirimannya dapat segera kami cek."},
    "Performa Aplikasi": {"owner": "Tim Engineering & QA",
        "steps": ["Reproduksi masalah pada versi aplikasi dan perangkat yang sama dengan pengguna.",
                  "Periksa catatan crash dan error berdasarkan versi aplikasi.",
                  "Prioritaskan perbaikan pada alur yang paling sering dipakai dan jalankan regression testing sebelum rilis."],
        "reply": "Mohon maaf aplikasi terasa lambat atau bermasalah. Mohon perbarui aplikasi ke versi terbaru dan sampaikan tipe perangkat serta langkah saat kendala muncul agar tim kami dapat menelusurinya."},
    "Promo & Harga": {"owner": "Tim Marketing & Produk",
        "steps": ["Periksa syarat dan periode promo atau voucher yang disebut pengguna.",
                  "Validasi voucher sebelum checkout dan tampilkan alasan jika tidak dapat dipakai.",
                  "Tampilkan harga akhir sebelum pembayaran agar tidak ada selisih yang mengejutkan."],
        "reply": "Mohon maaf promo atau voucher belum dapat Anda gunakan. Kami akan memeriksa syarat dan periodenya. Mohon kirimkan kode promo dan nomor pesanan melalui fitur bantuan."},
    "Produk & Stok": {"owner": "Tim Merchandising & Inventory",
        "steps": ["Cek sinkronisasi stok antara aplikasi dan toko atau gudang.",
                  "Tampilkan ketersediaan produk yang akurat sebelum pengguna melakukan checkout.",
                  "Tawarkan produk pengganti atau pemberitahuan saat barang kembali tersedia."],
        "reply": "Mohon maaf produk yang Anda cari belum tersedia atau tidak sesuai. Kami akan meneruskan informasi ini ke tim terkait. Mohon kirimkan nama produk dan lokasi toko Anda melalui fitur bantuan."},
    "Pesanan & Checkout": {"owner": "Tim Produk & Operasional",
        "steps": ["Telusuri status pesanan yang dikeluhkan sejak dibuat sampai saat ini.",
                  "Sederhanakan alur checkout dan perjelas ringkasan pesanan sebelum dibayar.",
                  "Pastikan status pesanan konsisten dan informasi pembatalan mudah ditemukan."],
        "reply": "Mohon maaf atas kendala pada pesanan Anda. Kami akan memeriksa statusnya. Mohon kirimkan nomor pesanan melalui fitur bantuan agar dapat segera kami tindak lanjuti."},
    "Customer Service": {"owner": "Tim Customer Care",
        "steps": ["Balas keluhan dan berikan status penyelesaian secara proaktif.",
                  "Sediakan akses bantuan yang mudah ditemukan di dalam aplikasi.",
                  "Tetapkan target waktu respons dan eskalasi keluhan yang berulang."],
        "reply": "Mohon maaf respons kami belum memuaskan. Keluhan Anda sudah kami catat dan akan segera dibalas oleh tim Customer Care. Terima kasih atas kesabaran Anda."},
    "Akun & Membership": {"owner": "Tim Engineering & CRM",
        "steps": ["Periksa pengiriman OTP dan status akun pengguna yang bermasalah.",
                  "Beri umpan balik yang jelas saat login atau OTP gagal, lengkap dengan langkah pemulihan.",
                  "Pastikan poin dan benefit membership tercatat dengan benar."],
        "reply": "Mohon maaf Anda mengalami kendala pada akun atau OTP. Mohon pastikan nomor ponsel Anda aktif dan coba kembali beberapa saat lagi. Jika masih bermasalah, kirimkan nomor ponsel terdaftar melalui fitur bantuan."},
    "Lainnya": {"owner": "Tim Produk",
        "steps": ["Baca konteks keluhan secara langsung untuk memahami masalahnya.",
                  "Kelompokkan secara manual dan tambahkan kata kunci baru jika topiknya baru.",
                  "Pantau apakah keluhan serupa muncul berulang."],
        "reply": "Mohon maaf atas ketidaknyamanan yang Anda alami. Masukan Anda sangat berarti bagi kami dan telah kami teruskan ke tim terkait."},
}
