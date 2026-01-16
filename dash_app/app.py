from __future__ import annotations

from pathlib import Path
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# -----------------------------
# Data loading
# -----------------------------
HERE = Path(__file__).resolve().parent
DATA_PATH = HERE.parent / "data" / "processed" / "superstore_cleaned.csv"

STATE_TO_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
    "District of Columbia": "DC"
}


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["Order Date", "Ship Date"], encoding_errors="ignore")

    # Ensure expected cols exist
    needed = ["Order Date", "Region", "Segment", "Category", "Sub-Category", "Sales", "Profit", "Discount", "Ship Mode", "State", "Order ID"]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()

    # Map states to abbreviations for choropleth
    df["State Abbr"] = df["State"].map(STATE_TO_ABBR)
    return df


DF = load_data()

# -----------------------------
# Helpers
# -----------------------------

def kpi_card(title: str, value_id: str) -> html.Div:
    return html.Div(
        [
            html.Div(title, style={"fontSize": "12px", "opacity": 0.75}),
            html.Div(id=value_id, style={"fontSize": "24px", "fontWeight": "700", "marginTop": "4px"}),
        ],
        style={
            "padding": "12px 14px",
            "border": "1px solid rgba(0,0,0,0.08)",
            "borderRadius": "14px",
            "background": "white",
            "boxShadow": "0 2px 12px rgba(0,0,0,0.04)",
        },
    )


def format_currency(x: float) -> str:
    return f"${x:,.0f}"


def format_percent(x: float) -> str:
    return f"{x*100:.1f}%"


def filter_df(region: str, segment: str, category: str, year: int | str) -> pd.DataFrame:
    dff = DF.copy()

    if region != "All":
        dff = dff[dff["Region"] == region]
    if segment != "All":
        dff = dff[dff["Segment"] == segment]
    if category != "All":
        dff = dff[dff["Category"] == category]
    if year != "All":
        dff = dff[dff["Year"] == int(year)]

    return dff


# -----------------------------
# App
# -----------------------------
app = Dash(__name__)
app.title = "Sales Performance Dashboard"

regions = ["All"] + sorted(DF["Region"].dropna().unique().tolist())
segments = ["All"] + sorted(DF["Segment"].dropna().unique().tolist())
categories = ["All"] + sorted(DF["Category"].dropna().unique().tolist())
years = ["All"] + sorted(DF["Year"].dropna().unique().astype(int).tolist())

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Sales Performance Dashboard", style={"margin": "0 0 6px 0"}),
                html.Div(
                    "Interactive analysis of retail sales performance: trends, regions, products, discounts, and shipping.",
                    style={"opacity": 0.8},
                ),
            ],
            style={"marginBottom": "14px"},
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.Div("Filters", style={"fontWeight": "700", "marginBottom": "8px"}),
                        html.Div(
                            [
                                html.Label("Region", style={"fontSize": "12px", "opacity": 0.75}),
                                dcc.Dropdown(regions, "All", id="region", clearable=False),
                            ]
                        ),
                        html.Div(
                            [
                                html.Label("Segment", style={"fontSize": "12px", "opacity": 0.75, "marginTop": "10px", "display": "block"}),
                                dcc.Dropdown(segments, "All", id="segment", clearable=False),
                            ]
                        ),
                        html.Div(
                            [
                                html.Label("Category", style={"fontSize": "12px", "opacity": 0.75, "marginTop": "10px", "display": "block"}),
                                dcc.Dropdown(categories, "All", id="category", clearable=False),
                            ]
                        ),
                        html.Div(
                            [
                                html.Label("Year", style={"fontSize": "12px", "opacity": 0.75, "marginTop": "10px", "display": "block"}),
                                dcc.Dropdown([str(y) for y in years], "All", id="year", clearable=False),
                            ]
                        ),
                    ],
                    style={
                        "padding": "14px",
                        "border": "1px solid rgba(0,0,0,0.08)",
                        "borderRadius": "14px",
                        "background": "white",
                        "boxShadow": "0 2px 12px rgba(0,0,0,0.04)",
                    },
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                kpi_card("Total Sales", "kpi_sales"),
                                kpi_card("Total Profit", "kpi_profit"),
                                kpi_card("Profit Margin", "kpi_margin"),
                                kpi_card("Orders", "kpi_orders"),
                                kpi_card("AOV", "kpi_aov"),
                            ],
                            style={
                                "display": "grid",
                                "gridTemplateColumns": "repeat(5, 1fr)",
                                "gap": "12px",
                            },
                        ),

                        html.Div(
                            [
                                dcc.Graph(id="trend"),
                            ],
                            style={"marginTop": "12px"},
                        ),

                        html.Div(
                            [
                                html.Div([dcc.Graph(id="map")], style={"flex": "1", "minWidth": "380px"}),
                                html.Div([dcc.Graph(id="subcat")], style={"flex": "1", "minWidth": "380px"}),
                            ],
                            style={"display": "flex", "gap": "12px", "marginTop": "12px", "flexWrap": "wrap"},
                        ),

                        html.Div(
                            [
                                html.Div([dcc.Graph(id="discount")], style={"flex": "1", "minWidth": "380px"}),
                                html.Div([dcc.Graph(id="ship")], style={"flex": "1", "minWidth": "380px"}),
                            ],
                            style={"display": "flex", "gap": "12px", "marginTop": "12px", "flexWrap": "wrap"},
                        ),
                    ],
                ),
            ],
            style={"display": "grid", "gridTemplateColumns": "320px 1fr", "gap": "12px"},
        ),

        html.Div(
            "Tip: Use the filters on the left. All charts update together. Hover any chart for exact values.",
            style={"opacity": 0.65, "marginTop": "10px", "fontSize": "12px"},
        ),
    ],
    style={"maxWidth": "1200px", "margin": "18px auto", "padding": "0 14px", "fontFamily": "Arial"},
)


@app.callback(
    Output("kpi_sales", "children"),
    Output("kpi_profit", "children"),
    Output("kpi_margin", "children"),
    Output("kpi_orders", "children"),
    Output("kpi_aov", "children"),
    Output("trend", "figure"),
    Output("map", "figure"),
    Output("subcat", "figure"),
    Output("discount", "figure"),
    Output("ship", "figure"),
    Input("region", "value"),
    Input("segment", "value"),
    Input("category", "value"),
    Input("year", "value"),
)
def update(region: str, segment: str, category: str, year: str):
    dff = filter_df(region, segment, category, year)

    total_sales = float(dff["Sales"].sum())
    total_profit = float(dff["Profit"].sum())
    orders = int(dff["Order ID"].nunique())
    margin = (total_profit / total_sales) if total_sales else 0.0
    aov = (total_sales / orders) if orders else 0.0

    # Trend (monthly)
    by_month = (
        dff.groupby("Month", as_index=False)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .sort_values("Month")
    )
    fig_trend = px.line(by_month, x="Month", y=["Sales", "Profit"], markers=True, title="Sales and Profit Over Time")
    fig_trend.update_layout(legend_title_text="Metric", margin=dict(l=20, r=20, t=50, b=20))

    # Map (state)
    by_state = dff.dropna(subset=["State Abbr"]).groupby(["State Abbr"], as_index=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum")
    )
    fig_map = px.choropleth(
        by_state,
        locations="State Abbr",
        locationmode="USA-states",
        color="Profit",
        scope="usa",
        hover_data={"Sales": ":,.0f", "Profit": ":,.0f", "State Abbr": False},
        title="Profit by State (size implied by hover Sales)",
    )
    fig_map.update_layout(margin=dict(l=20, r=20, t=50, b=20))

    # Sub-category profit
    by_sub = dff.groupby("Sub-Category", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    by_sub = by_sub.sort_values("Profit")
    fig_sub = px.bar(by_sub, x="Profit", y="Sub-Category", orientation="h", title="Profit by Sub-Category", hover_data={"Sales": ":,.0f", "Profit": ":,.0f"})
    fig_sub.update_layout(margin=dict(l=20, r=20, t=50, b=20))

    # Discount bucket vs margin
    if "Discount Bucket" in dff.columns:
        by_disc = dff.groupby("Discount Bucket", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        by_disc["Margin"] = by_disc.apply(lambda r: (r["Profit"] / r["Sales"]) if r["Sales"] else 0.0, axis=1)
        fig_disc = px.bar(by_disc, x="Discount Bucket", y="Margin", title="Profit Margin by Discount Bucket")
        fig_disc.update_yaxes(tickformat=".0%")
    else:
        fig_disc = px.bar(title="Profit Margin by Discount Bucket")
    fig_disc.update_layout(margin=dict(l=20, r=20, t=50, b=20))

    # Ship mode profit per order
    by_ship = dff.groupby("Ship Mode", as_index=False).agg(Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
    by_ship["Profit per Order"] = by_ship.apply(lambda r: (r["Profit"] / r["Orders"]) if r["Orders"] else 0.0, axis=1)
    fig_ship = px.bar(by_ship, x="Ship Mode", y="Profit per Order", title="Average Profit per Order by Ship Mode")
    fig_ship.update_layout(margin=dict(l=20, r=20, t=50, b=20))

    return (
        format_currency(total_sales),
        format_currency(total_profit),
        format_percent(margin),
        f"{orders:,}",
        format_currency(aov),
        fig_trend,
        fig_map,
        fig_sub,
        fig_disc,
        fig_ship,
    )


if __name__ == "__main__":
    app.run(debug=True)
