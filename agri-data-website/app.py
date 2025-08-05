import os
from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly
import json

app = Flask(__name__)

# Dynamically build the path to the data file relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "enam_trade_data.csv")

@app.route("/", methods=["GET"])
def index():
    df = pd.read_csv(DATA_PATH)
    df.columns = [col.strip() for col in df.columns]

    # Get unique states for dropdown
    states = sorted(df["State"].dropna().unique())
    selected_state = request.args.get("state", states[0] if states else "")

    # Filter data by selected state
    filtered_df = df[df["State"] == selected_state] if selected_state else df

    # --- Summary Calculations ---
    # Total Traded Quantity
    if "Traded Quantity" in filtered_df.columns and not filtered_df.empty:
        filtered_df["Traded Quantity"] = pd.to_numeric(filtered_df["Traded Quantity"], errors="coerce")
        total_traded_quantity = int(filtered_df["Traded Quantity"].sum())
    else:
        total_traded_quantity = "N/A"

    # Commodities count
    if "Commodity" in filtered_df.columns and not filtered_df.empty:
        commodities_count = int(filtered_df["Commodity"].nunique())
    else:
        commodities_count = "N/A"

    # Latest date
    if "Date" in filtered_df.columns and not filtered_df.empty:
        filtered_df["Date"] = pd.to_datetime(filtered_df["Date"], dayfirst=True, errors="coerce")
        latest_date_val = filtered_df["Date"].max()
        latest_date = latest_date_val.strftime("%d-%m-%Y") if pd.notnull(latest_date_val) else "N/A"
    else:
        latest_date = "N/A"

    # --- Commodity Price Trends ---
    # List of commodities to show trends for (add more as needed)
    trend_commodities = ["ONION", "LEMON", "TURMERIC", "COTTON", "GROUND NUT", "RED CHILLI-DRY"]
    trend_graphs = []

    if "Commodity" in filtered_df.columns and "Modal Price (Rs.)" in filtered_df.columns and "Date" in filtered_df.columns:
        filtered_df["Modal Price (Rs.)"] = pd.to_numeric(filtered_df["Modal Price (Rs.)"].astype(str).str.replace(",", ""), errors="coerce")
        filtered_df["Date"] = pd.to_datetime(filtered_df["Date"], dayfirst=True, errors="coerce")
        for commodity in trend_commodities:
            comm_df = filtered_df[filtered_df["Commodity"].str.contains(commodity, case=False, na=False)]
            if not comm_df.empty:
                comm_df = comm_df.sort_values("Date")
                fig = px.line(comm_df, x="Date", y="Modal Price (Rs.)", title=f"{commodity.title()} Price Trend in {selected_state}")
                graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                trend_graphs.append({"commodity": commodity.title(), "graphJSON": graphJSON})

    return render_template(
        "index.html",
        total_traded_quantity=total_traded_quantity,
        commodities_count=commodities_count,
        latest_date=latest_date,
        trend_graphs=trend_graphs,
        states=states,
        selected_state=selected_state
    )

if __name__ == "__main__":
    app.run(debug=True)