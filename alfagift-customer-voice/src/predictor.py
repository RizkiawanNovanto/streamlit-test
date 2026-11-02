"""Prediksi sentimen satu ulasan untuk halaman "Coba Prediksi".

Mesin dipilih otomatis (yang pertama tersedia):
1. IndoBERT hasil fine-tuning  -> simpan modelnya ke salah satu folder pada MODEL_DIR_NAMES
                                  (lihat petunjuk di halaman "Coba Prediksi" atau README di bawah).
2. SVM + TF-IDF yang dilatih dari data ulasan di dashboard (mode cadangan).
3. Aturan kata sederhana (mode cadangan terakhir, tanpa library tambahan).

Cara menyimpan IndoBERT dari notebook:
    trainer.save_model("models/indobert")
    tokenizer.save_pretrained("models/indobert")
Urutan kelas model harus 0 = Negatif, 1 = Netral, 2 = Positif (atau isi id2label pada config).
"""
import os
import re
from pathlib import Path

import numpy as np

LABELS = ["Negatif", "Netral", "Positif"]
MODEL_DIR_NAMES = ["indobert", "indobert_best", "indobert-sentiment", "indobert_sentiment"]

SLANG = {"gk": "tidak", "gx": "tidak", "gak": "tidak", "nggak": "tidak", "ngga": "tidak", "yg": "yang", "dgn": "dengan",
         "bgt": "banget", "aja": "saja", "udah": "sudah", "blm": "belum", "krn": "karena"}

NEG_WORDS = ["jelek", "kecewa", "lama", "lambat", "lemot", "gagal", "error", "parah", "buruk", "rugi", "penipu", "tidak bisa",
             "tidak bisa", "tidak ada", "tidak masuk", "tidak sampai", "belum sampai", "telat", "terlambat", "kacau", "ribet",
             "susah", "sulit", "crash", "hilang", "batal", "mengecewakan", "tidak sesuai", "tidak puas", "kesal", "bohong"]
POS_WORDS = ["bagus", "mantap", "puas", "cepat", "mudah", "membantu", "rekomen", "suka", "keren", "murah", "hemat", "lengkap",
             "ramah", "praktis", "terbaik", "memuaskan", "senang", "oke", "recommended", "top", "sesuai"]


def clean_text(text):
    """Pembersihan ringan yang sama dengan tahap preprocessing penelitian (tanpa stemming)."""
    t = str(text).lower()
    t = re.sub(r"http\S+|www\.\S+", " ", t)
    t = re.sub(r"[@#]\w+", " ", t)
    t = re.sub(r"[^a-zA-Z\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return " ".join(SLANG.get(w, w) for w in t.split())


def _softmax(x):
    x = np.asarray(x, dtype=float)
    e = np.exp(x - x.max())
    return e / e.sum()


def _as_dict(order, probs):
    d = {k: 0.0 for k in LABELS}
    for k, v in zip(order, probs):
        d[k] = float(v)
    return d


# ---------------------------------------------------------------- mesin 3: aturan kata
class RulePredictor:
    name = "Aturan kata sederhana (mode cadangan)"
    kind = "rule"
    note = "Model belum tersedia, jadi prediksi memakai aturan kata sederhana. Hasilnya hanya gambaran kasar."

    def predict(self, text):
        t = clean_text(text)
        neg = sum(1 for w in set(NEG_WORDS) if re.search(r"\b" + re.escape(w), t))
        pos = sum(1 for w in set(POS_WORDS) if re.search(r"\b" + re.escape(w), t))
        logits = [1.3 * neg, 0.9 if (neg + pos) == 0 else 0.2, 1.3 * pos]
        p = _softmax(logits)
        return {"label": LABELS[int(np.argmax(p))], "probs": _as_dict(LABELS, p)}


# ---------------------------------------------------------------- mesin 2: SVM + TF-IDF
class SvmPredictor:
    name = "SVM + TF-IDF (mode cadangan)"
    kind = "svm"
    note = ("Model IndoBERT belum ditemukan, jadi prediksi memakai SVM + TF-IDF yang dilatih dari data ulasan di dashboard. "
            "Skor keyakinan berupa perkiraan.")

    def __init__(self, texts, labels):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.pipeline import make_pipeline
        from sklearn.svm import LinearSVC
        cleaned = [clean_text(t) for t in texts]
        self.pipe = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, max_features=60000),
                                  LinearSVC(class_weight="balanced"))
        self.pipe.fit(cleaned, labels)
        self.classes = list(self.pipe.classes_)

    def predict(self, text):
        dec = self.pipe.decision_function([clean_text(text)])[0]
        dec = np.atleast_1d(dec)
        if len(self.classes) == 2:
            dec = np.array([-dec[0], dec[0]])
        p = _softmax(dec * 3.0)
        d = _as_dict(self.classes, p)
        return {"label": max(d, key=d.get), "probs": d}


# ---------------------------------------------------------------- mesin 1: IndoBERT
_MAP = {"negative": "Negatif", "neg": "Negatif", "negatif": "Negatif", "neutral": "Netral", "netral": "Netral",
        "positive": "Positif", "pos": "Positif", "positif": "Positif"}


def _norm_label(name, i):
    k = str(name).strip().lower()
    if k in _MAP:
        return _MAP[k]
    return LABELS[i] if i < len(LABELS) else str(name)


class BertPredictor:
    kind = "bert"
    note = "Prediksi memakai model IndoBERT hasil fine-tuning pada penelitian."

    def __init__(self, path):
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer
        self.torch = torch
        self.tok = AutoTokenizer.from_pretrained(path)
        self.model = AutoModelForSequenceClassification.from_pretrained(path)
        self.model.eval()
        id2 = getattr(self.model.config, "id2label", {}) or {}
        n = self.model.config.num_labels
        self.order = [_norm_label(id2.get(i, f"LABEL_{i}"), i) for i in range(n)]
        self.name = "IndoBERT (fine-tuned)"

    def predict(self, text):
        enc = self.tok(clean_text(text), truncation=True, max_length=128, return_tensors="pt")
        with self.torch.no_grad():
            logits = self.model(**enc).logits[0]
        p = self.torch.softmax(logits, dim=-1).cpu().numpy()
        d = _as_dict(self.order, p)
        return {"label": max(d, key=d.get), "probs": d}


# ---------------------------------------------------------------- pemilih mesin
def find_model_dir(*roots):
    env = os.environ.get("ALFAGIFT_MODEL_DIR")
    cands = [Path(env)] if env else []
    for r in roots:
        for n in MODEL_DIR_NAMES:
            cands.append(Path(r) / "models" / n)
    for c in cands:
        if c.exists() and (c / "config.json").exists():
            return c
    return None


def load_predictor(root, texts=None, labels=None, app_dir=None):
    """Kembalikan mesin prediksi pertama yang tersedia."""
    mdir = find_model_dir(root, app_dir or root)
    if mdir is not None:
        try:
            return BertPredictor(str(mdir))
        except Exception:
            pass
    if texts is not None and labels is not None and len(texts) >= 50:
        try:
            return SvmPredictor(texts, labels)
        except Exception:
            pass
    return RulePredictor()


# ---------------------------------------------------------------- penilaian bintang vs teks
def rating_label(star):
    return "Negatif" if star <= 2 else ("Netral" if star == 3 else "Positif")


def assess(sent, star):
    """Gabungkan sentimen teks dan bintang menjadi kesimpulan singkat."""
    rl = rating_label(star)
    agree = sent == rl
    base = {"rating_label": rl, "agree": agree}
    if sent == "Negatif" and rl == "Negatif":
        return {**base, "urgency": "Tinggi", "tone": "red", "icon": "🚨", "headline": "Keluhan jelas: teks dan bintang sama-sama negatif",
                "explanation": "Pengguna kecewa dan menunjukkannya lewat tulisan maupun bintang. Sebaiknya segera ditindaklanjuti."}
    if sent == "Negatif" and rl == "Positif":
        return {**base, "urgency": "Sedang", "tone": "yellow", "icon": "🕵️", "headline": "Keluhan tersembunyi: bintang tinggi, tetapi teks mengeluh",
                "explanation": "Bintang tinggi bisa menutupi masalah yang sebenarnya. Penelitian ini melabeli sentimen dari rating, sehingga kasus seperti ini mudah terlewat. Tetap telaah isi teksnya."}
    if sent == "Negatif":
        return {**base, "urgency": "Sedang", "tone": "yellow", "icon": "⚠️", "headline": "Teks mengeluh, bintang netral",
                "explanation": "Ada keluhan pada teks meski bintang tidak terlalu rendah. Layak ditindaklanjuti sebelum berubah menjadi bintang rendah."}
    if sent == "Positif" and rl == "Negatif":
        return {**base, "urgency": "Rendah", "tone": "yellow", "icon": "🤔", "headline": "Teks positif, tetapi bintang rendah",
                "explanation": "Kemungkinan pengguna keliru memberi bintang. Tidak perlu perbaikan layanan, tetapi bisa diverifikasi."}
    if sent == "Positif":
        return {**base, "urgency": "Rendah", "tone": "green", "icon": "💚", "headline": "Pengalaman positif",
                "explanation": "Teks dan bintang menunjukkan pengguna puas. Pertahankan hal yang membuat mereka puas."}
    if rl == "Negatif":
        return {**base, "urgency": "Sedang", "tone": "yellow", "icon": "❓", "headline": "Bintang rendah, tetapi teks tidak jelas mengeluh",
                "explanation": "Bintang rendah belum disertai alasan yang jelas pada teks. Minta pengguna menjelaskan kendalanya."}
    return {**base, "urgency": "Rendah", "tone": "yellow" if rl == "Netral" else "green", "icon": "😐", "headline": "Sentimen netral",
            "explanation": "Belum ada keluhan atau pujian yang menonjol pada ulasan ini."}
