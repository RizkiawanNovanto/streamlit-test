import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from src import components as ui
from src.components import BRAND
from src.config import ORDER


def render(c):
    ui.page_header("Performa Model", "Seberapa baik IndoBERT menebak sentimen dibanding label sebenarnya.", "MODEL EVALUATION")
    col = c.prediction_col
    d = c.fdf[c.fdf["sentiment"].isin(ORDER) & c.fdf[col].isin(ORDER)]
    if d.empty:
        return ui.empty_state("Tidak ada data dengan label dan prediksi yang valid.")

    cm = pd.crosstab(d["sentiment"], d[col]).reindex(index=ORDER, columns=ORDER, fill_value=0)
    v = cm.values
    tp = np.diag(v)
    prec, rec = tp / np.maximum(v.sum(0), 1), tp / np.maximum(v.sum(1), 1)
    f1 = 2 * prec * rec / np.maximum(prec + rec, 1e-9)
    neg_idx = ORDER.index("Negatif")

    c1, c2, c3, c4 = st.columns(4)
    ui.metric_card(c1, "Akurasi", f"{tp.sum() / v.sum() * 100:.1f}%", f"{v.sum():,} review dievaluasi", BRAND["navy"])
    ui.metric_card(c2, "Macro F1", f"{f1.mean():.3f}", "Rata-rata F1 tiga kelas", BRAND["yellow"])
    ui.metric_card(c3, "F1 Negatif", f"{f1[neg_idx]:.3f}", "Kelas penting untuk insight", BRAND["red"])
    ui.metric_card(c4, "Salah Prediksi", f"{v.sum() - tp.sum():,}", "Label ≠ prediksi", "#64748B")
    st.write("")

    a, b = st.columns([1.1, 1], gap="large")
    with a:
        ui.section_label("CONFUSION MATRIX")
        fig = px.imshow(cm, text_auto=True, x=ORDER, y=ORDER, aspect="auto",
                        labels=dict(x="Prediksi", y="Label sebenarnya", color="Jumlah"),
                        color_continuous_scale=["#FFFFFF", BRAND["red"]])
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(ui.style_fig(fig, 340, legend=False), use_container_width=True)
    with b:
        ui.section_label("METRIK PER KELAS")
        st.dataframe(pd.DataFrame({"Kelas": ORDER, "Precision": prec.round(3), "Recall": rec.round(3),
                                   "F1": f1.round(3), "Jumlah": v.sum(1)}), hide_index=True, use_container_width=True)
        ui.info_card("Cara membaca", "Precision: dari yang ditebak kelas X, berapa yang benar. "
                     "Recall: dari semua review kelas X, berapa yang berhasil ditemukan.", "blue")

    ui.section_label("REVIEW YANG SALAH DIPREDIKSI")
    n = st.select_slider("Jumlah baris", [10, 20, 50, 100], value=20)
    wrong = d[d["sentiment"] != d[col]]
    cols = [x for x in ["content", "sentiment", col, "score", "at"] if x in wrong.columns]
    st.dataframe(wrong[cols].head(n), hide_index=True, use_container_width=True,
                 column_config={"content": st.column_config.TextColumn("Review", width="large")})
