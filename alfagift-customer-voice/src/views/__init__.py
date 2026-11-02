"""Registry halaman: nama menu -> fungsi render(ctx)."""
from src.views import (about, insights, keywords, model, overview, predict,
                       problems, reviews, sentiment, trend, versions)

PAGES = {
    "Overview": overview.render,
    "Coba Prediksi": predict.render,
    "Sentiment": sentiment.render,
    "Masalah Pengguna": problems.render,
    "Insights": insights.render,
    "Tren": trend.render,
    "Kata Kunci": keywords.render,
    "Versi Aplikasi": versions.render,
    "Reviews": reviews.render,
    "Performa Model": model.render,
    "Tentang Alfagift": about.render,
}
