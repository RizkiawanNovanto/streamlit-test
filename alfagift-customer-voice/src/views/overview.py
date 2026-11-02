import pandas as pd
import plotly.express as px
import streamlit as st

from src import components as ui
from src.components import BRAND, SENTIMENT_COLORS as SC
from src.config import ORDER, RATINGS
from src.data import issue_table, monthly


def go_predict():
    st.session_state["page"] = "Coba Prediksi"


def render(c):
    ui.page_header("Overview", "Ringkasan kondisi pengalaman pengguna Alfagift.", "CUSTOMER VOICE")
    if c.df.empty or "sentiment" not in c.df.columns:
        return ui.empty_state("Dataset review tidak ditemukan di folder data/final/.")
    fdf = c.fdf

    with st.container(border=True):
        a, b = st.columns([4, 1.2])
        a.markdown("**🧪 Coba prediksi ulasanmu**  \nTulis ulasan dan beri bintang, lalu lihat sentimen yang terbaca model dan apa yang sebaiknya dilakukan.")
        b.button("Coba sekarang →", type="primary", use_container_width=True, on_click=go_predict, key="cta_pred")

    counts = (fdf["sentiment"].value_counts().reindex(ORDER).fillna(0).astype(int)
              .rename_axis("sentiment").reset_index(name="jumlah"))
    val, total = dict(zip(counts.sentiment, counts.jumlah)), int(counts.jumlah.sum()) or 1
    avg = fdf["score"].mean() if "score" in fdf.columns else None

    cols = st.columns(5)
    ui.metric_card(cols[0], "Total Review", f"{total:,}", "Data yang dianalisis", BRAND["navy"])
    ui.metric_card(cols[1], "Rating Rata-rata", f"{avg:.2f} ⭐" if pd.notna(avg) else "-", "Skor 1–5", BRAND["yellow"])
    for col, s in zip(cols[2:], ORDER):
        ui.metric_card(col, s, f"{val[s] / total * 100:.1f}%", f"{val[s]:,} review", SC[s])
    st.write("")

    left, right = st.columns([1, 1.35], gap="large")
    with left:
        ui.section_label("SENTIMENT OVERVIEW")
        fig = px.pie(counts, names="sentiment", values="jumlah", hole=.68, color="sentiment", color_discrete_map=SC)
        fig.update_traces(textinfo="percent", textposition="outside", sort=False,
                          marker=dict(line=dict(color="#fff", width=3)))
        fig.add_annotation(text=f"<b>{total:,}</b><br><span style='font-size:11px'>review</span>",
                           showarrow=False, font=dict(size=22, color=BRAND["ink"]))
        st.plotly_chart(ui.style_fig(fig, 345), use_container_width=True)
    with right:
        ui.section_label("WHAT NEEDS ATTENTION?")
        s = issue_table(c.neg) if c.has_detail and not c.neg.empty else pd.DataFrame()
        if s.empty:
            ui.empty_state("Belum ada issue yang dapat dipetakan.")
        for i, r in enumerate(s.head(5).itertuples(), 1):
            ui.rank_card(i, r.kategori, int(r.jumlah), float(r.persentase), c.tag(r.kategori))

    if c.has_detail and "score" in fdf.columns:
        a, b = st.columns(2, gap="large")
        with a:
            ui.section_label("DISTRIBUSI RATING")
            rc = fdf["score"].value_counts().reindex(RATINGS).fillna(0).reset_index()
            rc.columns = ["rating", "jumlah"]
            fig = px.bar(rc, x="rating", y="jumlah", text="jumlah", color_discrete_sequence=[BRAND["red"]])
            fig.update_layout(xaxis=dict(tickmode="linear", title="Rating"), yaxis_title=None)
            st.plotly_chart(ui.style_fig(fig, 300, legend=False), use_container_width=True)
        with b:
            ui.section_label("PERSENTASE REVIEW NEGATIF PER BULAN")
            if "at" in fdf.columns:
                m = monthly(fdf).groupby("month")["is_neg"].mean().mul(100).reset_index(name="persen")
                fig = px.line(m, x="month", y="persen", markers=True, color_discrete_sequence=[BRAND["red"]])
                fig.update_layout(xaxis_title=None, yaxis_title="% negatif")
                st.plotly_chart(ui.style_fig(fig, 300, legend=False), use_container_width=True)

    ui.insight_card("Catatan utama",
        "Dashboard berfokus pada pengalaman pengguna. Hasil model digunakan di belakang layar untuk memilih review negatif, "
        "lalu review tersebut diringkas menjadi area masalah yang lebih mudah dipahami. Gunakan menu Filter data di sidebar "
        "untuk mempersempit periode, rating, atau versi aplikasi.", "yellow")
