import streamlit as st

from src import components as ui
from src.components import BRAND
from src.data import issue_table


def render(c):
    ui.page_header("Insights & Recommendations", "Apa yang sebaiknya diperhatikan dari seluruh review yang dibaca model.", "ACTIONABLE INSIGHTS")
    if not c.has_detail:
        return ui.empty_state("Dataset detail belum tersedia. Letakkan model_predictions_common_test_set.csv di data/final/.")
    neg, s = c.neg, issue_table(c.neg)
    rising = max(((k, v) for k, v in c.trend_values.items() if k in set(s["kategori"])), key=lambda x: x[1], default=None)
    up = rising is not None and rising[1] > 0

    c1, c2, c3, c4 = st.columns(4)
    ui.metric_card(c1, "Review Negatif", f"{len(neg):,}", f"{len(neg) / max(len(c.fdf), 1) * 100:.1f}% dari review", BRAND["red"])
    ui.metric_card(c2, "Prioritas", s.iloc[0].kategori if not s.empty else "-", "Volume tertinggi", BRAND["yellow"])
    ui.metric_card(c3, "Naik Tercepat", rising[0] if up else "-",
                   f"▲ {rising[1]:.0f}% vs 90 hari lalu" if up else "Belum ada kenaikan berarti", BRAND["navy"])
    ui.metric_card(c4, "Model Insight", "IndoBERT" if c.prediction_col == "indobert_pred" else c.prediction_col, "Prediksi yang dibaca", "#64748B")
    st.write("")
    if s.empty:
        return ui.empty_state("Belum ada issue yang dapat dipetakan.")

    top = s.iloc[0]
    text = (f"Dari {len(neg):,} review negatif, “{top.kategori}” paling dominan ({top.persentase:.1f}%)."
            + (f" Masalah dengan kenaikan tertajam dalam 90 hari terakhir: “{rising[0]}” (naik {rising[1]:.0f}%)." if up else ""))
    ui.insight_card("Ringkasan otomatis", text, "blue")
    ui.section_label("APA YANG PERLU DIPERBAIKI?")
    n, sort = c.example_controls("in")
    for r in s.itertuples():
        c.show_issue(r.kategori, int(r.jumlah), float(r.persentase), n, sort)
    if c.has_thumbs:
        ui.section_label("KELUHAN PALING BANYAK DIDUKUNG PENGGUNA")
        c.render_quotes(c.pick_examples(neg, min(n, 10), "Paling banyak disukai"))
    ui.insight_card("Cara membaca rekomendasi",
        "Jumlah review menunjukkan seberapa sering suatu area muncul dalam review negatif. Label ▲/▼ membandingkan 90 hari "
        "terakhir dengan 90 hari sebelumnya. Kategori issue berasal dari keyword pada review, sehingga hasil sebaiknya "
        "divalidasi dengan data operasional perusahaan.", "yellow")
