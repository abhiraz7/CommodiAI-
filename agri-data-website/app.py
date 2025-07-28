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

    # Analytics: Top 10 Commodities by Traded Quantity in selected state
    graphJSON = None
    if "Commodity" in filtered_df.columns and "Traded Quantity" in filtered_df.columns:
        filtered_df["Traded Quantity"] = pd.to_numeric(filtered_df["Traded Quantity"], errors='coerce')
        summary = filtered_df.groupby("Commodity")["Traded Quantity"].sum().reset_index()
        summary = summary.sort_values("Traded Quantity", ascending=False).head(10)
        fig = px.bar(summary, x="Commodity", y="Traded Quantity", title=f"Top 10 Commodities in {selected_state}")
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Show the latest 20 rows in the table
    table_data = filtered_df.tail(20).to_dict(orient="records")

    return render_template(
        "index.html",
        table_data=table_data,
        graphJSON=graphJSON,
        states=states,
        selected_state=selected_state
    )

if __name__ == "__main__":
    app.run(debug=True)