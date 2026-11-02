import plotly.express as px
import streamlit as st

from src import components as ui
from src.components import SENTIMENT_COLORS as SC
from src.config import ORDER, PALETTE
from src.data import issue_table, monthly


def render(c):
    ui.page_header("Tren Sentimen", "Perubahan volume review berdasarkan waktu.", "TREND")
    if c.df.empty or "at" not in c.df.columns or "sentiment" not in c.df.columns:
        return ui.empty_state("Data tanggal belum tersedia.")
    mode = st.radio("Tampilan", ["Jumlah review", "Persentase"], horizontal=True)
    m = (monthly(c.fdf).groupby(["month", "sentiment"]).size().unstack(fill_value=0)
         .reindex(columns=ORDER, fill_value=0))
    if mode == "Persentase":
        m = m.div(m.sum(axis=1).replace(0, 1), axis=0) * 100
    long = m.reset_index().melt("month", var_name="sentiment", value_name="nilai")
    fig = px.line(long, x="month", y="nilai", color="sentiment", markers=True, color_discrete_map=SC)
    fig.update_traces(line=dict(width=2.5), marker=dict(size=5))
    fig.update_layout(xaxis_title=None, yaxis_title="% review" if mode == "Persentase" else "Jumlah review", hovermode="x unified")
    st.plotly_chart(ui.style_fig(fig, 400), use_container_width=True)

    if c.has_detail and not c.neg.empty:
        ui.section_label("TREN MASALAH PER BULAN")
        cats = issue_table(c.neg)["kategori"].tolist()
        sel = st.multiselect("Masalah yang ditampilkan", cats, default=cats[:3])
        mi = monthly(c.neg[c.neg["kategori"].isin(sel)]).groupby(["month", "kategori"]).size().reset_index(name="jumlah")
        if mi.empty:
            return ui.empty_state("Pilih minimal satu masalah.")
        fig = px.line(mi, x="month", y="jumlah", color="kategori", markers=True, color_discrete_sequence=PALETTE)
        fig.update_layout(xaxis_title=None, yaxis_title="Review negatif", hovermode="x unified")
        st.plotly_chart(ui.style_fig(fig, 380), use_container_width=True)
