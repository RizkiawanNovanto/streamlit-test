"""Ctx: satu objek yang membawa data terfilter + helper tampilan, dipakai semua halaman."""
import re

import pandas as pd
import streamlit as st

from src import components as ui
from src.config import INFO
from src.data import issue_table, trends


def _fmt_trend(d):
    if d is None:
        return None
    return (f"{'▲' if d > 0 else '▼'} {abs(d):.0f}% vs 90 hari sebelumnya", "up" if d > 0 else "down")


def csv_button(data, label, name, key=None):
    st.download_button(label, data.to_csv(index=False).encode("utf-8-sig"), name, "text/csv", key=key)


class Ctx:
    def __init__(self, df, fdf, source, prediction_col, chosen):
        self.df, self.fdf = df, fdf
        self.source, self.prediction_col, self.chosen = source, prediction_col, chosen
        self.filtered = len(fdf) != len(df)
        self.has_detail = not df.empty and prediction_col is not None and "content" in df.columns
        self.can_eval = self.has_detail and prediction_col == "indobert_pred" and "sentiment" in df.columns
        self.vcol = next((c for c in ("reviewCreatedVersion", "version") if c in df.columns), None)
        self.has_thumbs = "thumbsUpCount" in df.columns

        empty = pd.DataFrame(columns=["kategori", "jumlah", "persentase"])
        self.neg = fdf[fdf["is_neg"]] if self.has_detail else pd.DataFrame()      # negatif (terfilter)
        self.neg_all = df[df["is_neg"]] if self.has_detail else pd.DataFrame()    # negatif (semua data)
        self.iss_all = issue_table(self.neg_all) if self.has_detail and not self.neg_all.empty else empty
        self._tr = trends(self.neg)
        self._tr_all = trends(self.neg_all) if self.has_detail else {}

    # ---- tren
    def tag(self, cat):
        return _fmt_trend(self._tr.get(cat))

    def tag_all(self, cat):
        return _fmt_trend(self._tr_all.get(cat))

    @property
    def trend_values(self):
        return self._tr

    # ---- contoh review
    def pick_examples(self, sub, n, sort):
        sub = sub.drop_duplicates("content")
        if sort == "Paling banyak disukai" and self.has_thumbs:
            sub = sub.sort_values("thumbsUpCount", ascending=False)
        else:
            if "at" in sub.columns:
                sub = sub.sort_values("at", ascending=False)
            if sort == "Rating terendah" and "score" in sub.columns:
                sub = sub.sort_values("score", kind="stable")
        return sub.head(n)

    @staticmethod
    def _meta(r):
        parts = []
        if pd.notna(r.get("score")):
            parts.append(f"⭐ {int(r['score'])}")
        if pd.notna(r.get("at")):
            parts.append(r["at"].strftime("%d %b %Y"))
        if pd.notna(r.get("reviewCreatedVersion")):
            parts.append(f"v{r['reviewCreatedVersion']}")
        if pd.notna(r.get("thumbsUpCount")) and r["thumbsUpCount"] > 0:
            parts.append(f"👍 {int(r['thumbsUpCount'])}")
        return " • ".join(parts)

    def render_quotes(self, sub):
        for _, r in sub.iterrows():
            ui.quote(re.sub(r"\s+", " ", str(r["content"])).strip(), self._meta(r))

    def example_controls(self, key=""):
        c1, c2 = st.columns([2, 1])
        n = c1.select_slider("Jumlah contoh review per masalah", [3, 5, 10, 15, 20, 30, 50], value=5, key=f"n{key}",
                             help="Geser untuk menampilkan lebih banyak contoh review pada setiap masalah.")
        opts = ["Terbaru", "Rating terendah"] + (["Paling banyak disukai"] if self.has_thumbs else [])
        return n, c2.selectbox("Urutkan contoh", opts, key=f"s{key}")

    def show_issue(self, cat, count, pct, n, sort):
        info = INFO[cat]
        ui.issue_card(cat, info["icon"], count, pct, info["description"], info["recommendation"], self.tag(cat))
        sub = self.pick_examples(self.neg[self.neg["kategori"] == cat], n, sort)
        if sub.empty:
            return st.write("")
        with st.expander(f"Lihat {len(sub)} contoh review — {cat}"):
            self.render_quotes(sub)
