from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="MavenTech Sales Dashboard",
    page_icon="📊",
    layout="wide",
)


def require_columns(
    frame: pd.DataFrame, table_name: str, required: set[str]
) -> None:
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(
            f"{table_name}.csv is missing required columns: "
            f"{', '.join(sorted(missing))}"
        )


@st.cache_data
def load_dashboard_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    data_dir = Path(__file__).resolve().parent
    filenames = (
        "sales_pipeline.csv",
        "accounts.csv",
        "sales_teams.csv",
        "products.csv",
    )
    missing_files = [name for name in filenames if not (data_dir / name).is_file()]
    if missing_files:
        raise FileNotFoundError(
            f"Missing required CSV file(s) in {data_dir}: "
            f"{', '.join(missing_files)}"
        )

    pipeline = pd.read_csv(data_dir / "sales_pipeline.csv")
    accounts = pd.read_csv(data_dir / "accounts.csv")
    teams = pd.read_csv(data_dir / "sales_teams.csv")
    products = pd.read_csv(data_dir / "products.csv")

    require_columns(
        pipeline,
        "sales_pipeline",
        {"opportunity_id", "sales_agent", "product", "account", "deal_stage",
         "close_date", "close_value"},
    )
    require_columns(accounts, "accounts", {"account", "sector", "revenue"})
    require_columns(teams, "sales_teams", {"sales_agent", "regional_office"})
    require_columns(products, "products", {"product", "series", "sales_price"})

    data = pipeline.merge(
        accounts, on="account", how="left", validate="many_to_one"
    ).merge(teams, on="sales_agent", how="left", validate="many_to_one")

    data["close_date"] = pd.to_datetime(data["close_date"], errors="coerce")
    data["close_value"] = pd.to_numeric(data["close_value"], errors="coerce")
    data["won_revenue"] = data["close_value"].fillna(0).where(
        data["deal_stage"].eq("Won"), 0
    )
    for column in ("account", "sector", "regional_office", "sales_agent", "product"):
        data[column] = data[column].fillna("Unknown")

    return data, products


st.title("MavenTech Sales Dashboard")
st.caption("Explore sales performance across opportunities, customers, and regions.")

try:
    df, products = load_dashboard_data()
except FileNotFoundError as error:
    st.error(str(error))
    st.stop()

with st.sidebar:
    st.header("Filters")
    regions = sorted(df["regional_office"].unique())
    sectors = sorted(df["sector"].unique())
    stages = ["Prospecting", "Engaging", "Won", "Lost"]

    selected_regions = st.multiselect("Regional office", regions, default=regions)
    selected_sectors = st.multiselect("Sector", sectors, default=sectors)
    selected_stages = st.multiselect("Deal stage", stages, default=stages)

filtered = df[
    df["regional_office"].isin(selected_regions)
    & df["sector"].isin(selected_sectors)
    & df["deal_stage"].isin(selected_stages)
]

if filtered.empty:
    st.info("No opportunities match the selected filters.")
    st.stop()

won = filtered[filtered["deal_stage"].eq("Won")]
closed_count = filtered["deal_stage"].isin(["Won", "Lost"]).sum()
win_rate = len(won) / closed_count if closed_count else 0
active_count = filtered["deal_stage"].isin(["Prospecting", "Engaging"]).sum()

metric_columns = st.columns(4)
metric_columns[0].metric("Won revenue", f"${won['won_revenue'].sum():,.0f}")
metric_columns[1].metric("Won deals", f"{len(won):,}")
metric_columns[2].metric("Win rate", f"{win_rate:.1%}")
metric_columns[3].metric("Open opportunities", f"{active_count:,}")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Won revenue over time")
    monthly_revenue = (
        won.dropna(subset=["close_date"])
        .groupby(pd.Grouper(key="close_date", freq="MS"), as_index=False)[
            "won_revenue"
        ]
        .sum()
    )
    if monthly_revenue.empty:
        st.info("No won deals with a close date match these filters.")
    else:
        st.plotly_chart(
            px.line(
                monthly_revenue,
                x="close_date",
                y="won_revenue",
                markers=True,
                labels={"close_date": "Close month", "won_revenue": "Won revenue"},
            ),
            use_container_width=True,
        )

with right:
    st.subheader("Opportunities by stage")
    stage_counts = (
        filtered.groupby("deal_stage", as_index=False)["opportunity_id"]
        .count()
        .rename(columns={"opportunity_id": "opportunities"})
    )
    st.plotly_chart(
        px.funnel(
            stage_counts,
            x="opportunities",
            y="deal_stage",
            category_orders={"deal_stage": stages},
            labels={"opportunities": "Opportunities", "deal_stage": "Deal stage"},
        ),
        use_container_width=True,
    )

left, right = st.columns(2)

with left:
    st.subheader("Won revenue by sector")
    sector_revenue = (
        won.groupby("sector", as_index=False)["won_revenue"]
        .sum()
        .sort_values("won_revenue", ascending=True)
    )
    st.plotly_chart(
        px.bar(
            sector_revenue,
            x="won_revenue",
            y="sector",
            orientation="h",
            labels={"won_revenue": "Won revenue", "sector": "Sector"},
        ),
        use_container_width=True,
    )

with right:
    st.subheader("Won revenue by product")
    product_revenue = (
        won.groupby("product", as_index=False)["won_revenue"]
        .sum()
        .sort_values("won_revenue", ascending=True)
    )
    st.plotly_chart(
        px.bar(
            product_revenue,
            x="won_revenue",
            y="product",
            orientation="h",
            labels={"won_revenue": "Won revenue", "product": "Product"},
        ),
        use_container_width=True,
    )

st.subheader("Top sales agents")
agent_summary = (
    filtered.groupby("sales_agent", as_index=False)
    .agg(
        won_revenue=("won_revenue", "sum"),
        opportunities=("opportunity_id", "count"),
        won_deals=("deal_stage", lambda values: values.eq("Won").sum()),
    )
    .sort_values("won_revenue", ascending=False)
    .head(10)
)
st.dataframe(agent_summary, hide_index=True, use_container_width=True)

with st.expander("Product catalog"):
    st.dataframe(products, hide_index=True, use_container_width=True)

with st.expander("Filtered opportunities"):
    display_columns = [
        "opportunity_id",
        "account",
        "product",
        "sales_agent",
        "regional_office",
        "sector",
        "deal_stage",
        "close_date",
        "close_value",
    ]
    st.dataframe(
        filtered[display_columns].sort_values(
            "close_date", ascending=False, na_position="last"
        ),
        hide_index=True,
        use_container_width=True,
    )