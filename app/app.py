"""
Zomato Sales Analysis Dashboard
Flask backend — loads CSV data, computes analytics, serves REST endpoints
"""

import os
import json
from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# ── Load & process data once at startup ───────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "zomato_sales.csv")

def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    df["month"]      = df["date"].dt.to_period("M").astype(str)
    df["month_name"] = df["date"].dt.strftime("%b %Y")
    df["weekday"]    = df["date"].dt.day_name()
    return df

DF = load_data()

# ── Helper ─────────────────────────────────────────────────────────────────────
def safe_json(obj):
    """Convert numpy/pandas types to plain Python for JSON serialisation."""
    if isinstance(obj, (np.integer,)):  return int(obj)
    if isinstance(obj, (np.floating,)): return round(float(obj), 2)
    if isinstance(obj, np.ndarray):     return obj.tolist()
    return obj

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/kpis")
def kpis():
    """Top-level KPI cards."""
    total_revenue  = DF["order_value"].sum()
    total_orders   = len(DF)
    avg_order      = DF["order_value"].mean()
    avg_rating     = DF["rating"].mean()
    avg_delivery   = DF["delivery_time_mins"].mean()
    top_city       = DF.groupby("city")["order_value"].sum().idxmax()

    return jsonify({
        "total_revenue":  safe_json(total_revenue),
        "total_orders":   safe_json(total_orders),
        "avg_order":      safe_json(avg_order),
        "avg_rating":     safe_json(avg_rating),
        "avg_delivery":   safe_json(avg_delivery),
        "top_city":       top_city,
    })


@app.route("/api/revenue-by-month")
def revenue_by_month():
    """Monthly revenue trend."""
    grp = (
        DF.groupby("month_name")["order_value"]
        .sum()
        .reset_index()
        .sort_values("month_name")
    )
    return jsonify({
        "labels": grp["month_name"].tolist(),
        "values": grp["order_value"].apply(safe_json).tolist(),
    })


@app.route("/api/revenue-by-city")
def revenue_by_city():
    """Revenue split by city."""
    grp = (
        DF.groupby("city")["order_value"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    return jsonify({
        "labels": grp["city"].tolist(),
        "values": grp["order_value"].apply(safe_json).tolist(),
    })


@app.route("/api/orders-by-cuisine")
def orders_by_cuisine():
    """Order count by cuisine type."""
    grp = (
        DF.groupby("cuisine")["order_id"]
        .count()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"order_id": "orders"})
    )
    return jsonify({
        "labels": grp["cuisine"].tolist(),
        "values": grp["orders"].apply(safe_json).tolist(),
    })


@app.route("/api/payment-modes")
def payment_modes():
    """Payment mode distribution."""
    grp = (
        DF.groupby("payment_mode")["order_id"]
        .count()
        .reset_index()
        .rename(columns={"order_id": "count"})
    )
    return jsonify({
        "labels": grp["payment_mode"].tolist(),
        "values": grp["count"].apply(safe_json).tolist(),
    })


@app.route("/api/top-restaurants")
def top_restaurants():
    """Top 8 restaurants by revenue."""
    grp = (
        DF.groupby("restaurant_name")
        .agg(revenue=("order_value", "sum"), orders=("order_id", "count"))
        .sort_values("revenue", ascending=False)
        .head(8)
        .reset_index()
    )
    return jsonify({
        "labels":  grp["restaurant_name"].tolist(),
        "revenue": grp["revenue"].apply(safe_json).tolist(),
        "orders":  grp["orders"].apply(safe_json).tolist(),
    })


@app.route("/api/rating-distribution")
def rating_distribution():
    """Histogram of order ratings."""
    bins   = [3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0]
    labels = ["3.5-3.75", "3.75-4.0", "4.0-4.25", "4.25-4.5", "4.5-4.75", "4.75-5.0"]
    counts, _ = np.histogram(DF["rating"].dropna(), bins=bins)
    return jsonify({"labels": labels, "values": counts.tolist()})


@app.route("/api/weekday-heatmap")
def weekday_heatmap():
    """Average order value per weekday."""
    order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    grp = (
        DF.groupby("weekday")["order_value"]
        .mean()
        .reindex(order)
        .reset_index()
    )
    return jsonify({
        "labels": grp["weekday"].tolist(),
        "values": grp["order_value"].apply(safe_json).tolist(),
    })


@app.route("/api/weekend-vs-weekday")
def weekend_vs_weekday():
    """Weekend vs weekday order volumes."""
    grp = (
        DF.groupby("is_weekend")["order_id"]
        .count()
        .reset_index()
    )
    labels = ["Weekday", "Weekend"]
    values = [
        safe_json(grp.loc[grp["is_weekend"] == 0, "order_id"].sum()),
        safe_json(grp.loc[grp["is_weekend"] == 1, "order_id"].sum()),
    ]
    return jsonify({"labels": labels, "values": values})


@app.route("/health")
def health():
    """Kubernetes / Render health probe."""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
