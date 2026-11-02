import streamlit as st

from src import components as ui
from src.components import BRAND, SENTIMENT_COLORS as SC
from src.config import EXAMPLES, INFO, ORDER
from src.data import get_predictor
from src.issues import ACTIONS, matched_keywords, rank_issues
from src.predictor import assess


def _use_example(text, star):
    st.session_state["pred_text"] = text
    st.session_state["pred_star"] = star


def render(c):
    ui.page_header("Coba Prediksi", "Tulis ulasan dan beri bintang, lalu lihat sentimen yang terbaca model beserta saran tindak lanjutnya.", "LIVE DEMO")
    engine = get_predictor(str(c.chosen) if c.chosen else "")
    st.session_state.setdefault("pred_text", "")
    st.session_state.setdefault("pred_star", 3)

    left, right = st.columns([1.4, 1], gap="large")
    with left:
        ui.section_label("TULIS ULASAN")
        st.caption("Belum punya ide? Coba salah satu contoh:")
        for i, (col, (label, text, star)) in enumerate(zip(st.columns(len(EXAMPLES)), EXAMPLES)):
            col.button(label, key=f"ex_{i}", on_click=_use_example, args=(text, star), use_container_width=True)
        with st.form("pred_form"):
            st.text_area("Ulasan", key="pred_text", height=130, max_chars=600,
                         placeholder="Contoh: pesanan sudah 4 jam belum sampai dan status di aplikasi tidak berubah…")
            st.radio("Berapa bintang yang kamu beri?", [1, 2, 3, 4, 5], key="pred_star", horizontal=True, format_func=ui.stars_text)
            submitted = st.form_submit_button("🔮 Prediksi Sekarang", type="primary", use_container_width=True)
    with right:
        ui.section_label("CARA KERJA")
        ui.info_card("1. Tulis dan beri bintang", "Ceritakan pengalamanmu seperti menulis ulasan di Play Store, lalu pilih jumlah bintang.")
        ui.info_card("2. Model membaca teksmu", "Model memperkirakan sentimen teks (negatif, netral, atau positif) lalu membandingkannya dengan bintangmu.", "yellow")
        ui.info_card("3. Dapatkan saran tindak lanjut", "Dashboard mengenali topik masalahnya dan menyarankan apa yang sebaiknya dilakukan.", "pink")
        st.markdown(f'<div class="owner">Mesin prediksi aktif: <b>{engine.name}</b></div>', unsafe_allow_html=True)

    if submitted:
        text_in = st.session_state.get("pred_text", "").strip()
        if len(text_in) < 5:
            st.warning("Tulis ulasan minimal beberapa kata agar model punya konteks.")
        else:
            st.session_state["pred_result"] = {"text": text_in, "star": int(st.session_state["pred_star"]),
                                               "pred": engine.predict(text_in)}
    res = st.session_state.get("pred_result")
    st.write("")
    if res is None:
        return ui.empty_state("Belum ada prediksi. Pilih salah satu contoh di atas atau tulis ulasanmu sendiri, lalu klik “Prediksi Sekarang”.")

    text, star, pred = res["text"], res["star"], res["pred"]
    sent, probs = pred["label"], pred["probs"]
    a = assess(sent, star)
    tone = {"Tinggi": BRAND["red"], "Sedang": BRAND["yellow"], "Rendah": SC["Positif"]}

    ui.section_label("HASIL PREDIKSI")
    ui.banner(a["headline"], a["explanation"], a["tone"], a["icon"])
    m1, m2, m3 = st.columns(3)
    ui.metric_card(m1, "Sentimen Teks", sent, f"Keyakinan model {probs[sent] * 100:.0f}%", SC[sent])
    ui.metric_card(m2, "Bintang Kamu", ui.stars_text(star), f"Setara sentimen {a['rating_label']}", SC[a["rating_label"]])
    ui.metric_card(m3, "Kesesuaian", "Selaras" if a["agree"] else "Tidak selaras", f"Prioritas tindak lanjut: {a['urgency']}", tone[a["urgency"]])
    st.write("")
    pa, pb = st.columns(2, gap="large")
    with pa:
        ui.section_label("KEYAKINAN MODEL")
        ui.prob_bars({k: probs[k] for k in ORDER}, SC, best=sent)
    with pb:
        ui.section_label("ULASAN YANG DIANALISIS")
        ui.quote(text, f"{ui.stars_text(star)} • {len(text.split())} kata")
    st.caption(f"Mesin prediksi: {engine.name}. {engine.note}")

    ui.section_label("INSIGHT & TINDAK LANJUT")
    ranked = rank_issues(text)
    if a["urgency"] != "Rendah":
        cat = ranked[0][0] if ranked else "Lainnya"
        info, act = INFO[cat], ACTIONS[cat]
        kws = matched_keywords(text, cat)
        cl, cr = st.columns([1.3, 1], gap="large")
        with cl:
            ui.action_card(info["icon"], cat, "Topik utama yang terdeteksi dari teks", ui.chips(kws, "red") if kws else "", act["steps"], act["owner"])
        with cr:
            if c.has_detail and not c.iss_all.empty and cat in set(c.iss_all["kategori"]):
                row = c.iss_all[c.iss_all["kategori"] == cat].iloc[0]
                rank = list(c.iss_all["kategori"]).index(cat) + 1
                ui.section_label("SEBERAPA UMUM?")
                ui.rank_card(rank, cat, int(row["jumlah"]), float(row["persentase"]), c.tag_all(cat))
                st.caption(f"Peringkat {rank} dari {len(c.iss_all)} kategori masalah pada data review.")
            elif c.has_detail:
                ui.info_card("Seberapa umum?", "Topik ini belum muncul pada kategori masalah di data review.")
            if len(ranked) > 1:
                st.markdown("<div class='owner'>Topik lain yang juga disebut:</div>" + ui.chips([n for n, _ in ranked[1:3]], "yellow"),
                            unsafe_allow_html=True)
            with st.expander("✉️ Contoh balasan untuk pengguna"):
                st.code(act["reply"], language=None)
            if c.has_detail and not c.neg_all.empty:
                with st.expander("📚 Review negatif serupa"):
                    sim = c.pick_examples(c.neg_all[c.neg_all["kategori"] == cat], 3, "Terbaru")
                    if sim.empty:
                        st.caption("Belum ada contoh pada kategori ini.")
                    else:
                        c.render_quotes(sim)
        return

    topics = [n for n, _ in ranked[:3]]
    if sent == "Positif" and a["rating_label"] == "Negatif":
        ui.action_card("🤔", "Verifikasi ketidaksesuaian", "Teks positif tetapi bintang rendah", "",
                       ["Hubungi pengguna untuk memastikan apakah bintang rendah disengaja atau keliru.",
                        "Jika keliru, sarankan pengguna memperbarui bintangnya.",
                        "Catat sebagai potensi ketidaksesuaian label bila ulasan dipakai sebagai data pelatihan."],
                       "Tim Customer Care", soft=True)
    elif sent == "Positif":
        ui.action_card("💚", "Pertahankan yang sudah baik", "Tidak ada masalah yang perlu ditindaklanjuti",
                       ui.chips(topics, "green") if topics else "",
                       ["Pertahankan kualitas layanan pada hal yang dipuji pengguna.",
                        "Pertimbangkan membalas ulasan sebagai bentuk apresiasi.",
                        "Gunakan ulasan serupa sebagai bahan testimoni atau materi promosi."],
                       "Tim Customer Care & Marketing", soft=True)
    else:
        ui.action_card("😐", "Belum ada keluhan atau pujian yang jelas", "Sentimen netral",
                       ui.chips(topics, "yellow") if topics else "",
                       ["Balas dengan ucapan terima kasih dan ajak pengguna menceritakan pengalamannya.",
                        "Ajukan pertanyaan terbuka untuk menggali apa yang bisa ditingkatkan.",
                        "Pantau apakah ulasan serupa muncul berulang."],
                       "Tim Customer Care", soft=True)
