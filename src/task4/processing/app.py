import pandas as pd
import streamlit as st
from processing.process_data import compute_metrics

ITERATIONS = range(1, 6)


def load_metrics(iteration: int) -> dict:
    return compute_metrics(iteration)

def prepare_daily_revenue(metrics: dict) -> pd.Series:
    daily = metrics["daily_revenue"].copy()
    daily.index = pd.to_datetime(daily.index)
    return daily.sort_index()
 
 
def build_top_days_table(daily: pd.Series, n: int = 5) -> pd.DataFrame:
    top = daily.nlargest(n)
    return pd.DataFrame(
        {"Date": top.index.strftime("%Y-%m-%d"), "Revenue": top.round(2).values}
    )
 
 
def select_iteration() -> int:
    return st.sidebar.selectbox("Dataset iteration", list(ITERATIONS))
 
 
def render_revenue_tab(daily: pd.Series) -> None:
    st.subheader("Top 5 days by revenue")
    st.table(build_top_days_table(daily))
    st.subheader("Daily revenue")
    st.line_chart(daily)
 
 
def render_customers_tab(metrics: dict) -> None:
    print(metrics)
    records = metrics["best_buyer_records"]
    left, right = st.columns(2)
    left.metric("Unique users", f"{metrics['n_users']:,}")
    right.metric("Best buyer total spent", f"{metrics['best_buyer_total']:,.2f}")
    st.subheader("Best buyer (with aliases)")
    st.code(str(records["id"].astype(int).tolist()), language="python")
    st.dataframe(records, hide_index=True)
 
 
def render_authors_tab(metrics: dict) -> None:
    st.metric("Unique sets of authors", metrics["n_author_sets"])
    st.subheader("Most popular author(s)")
    st.write(metrics["top_authors"].head(1))
 
 
def render_dashboard() -> None:
    st.set_page_config(page_title="Sales dashboard", layout="wide")
    st.title("Sales dashboard")
 
    metrics = load_metrics(select_iteration())
    daily = prepare_daily_revenue(metrics)
 
    revenue_tab, customers_tab, authors_tab = st.tabs(
        ["Revenue", "Customers", "Authors"]
    )
    with revenue_tab:
        render_revenue_tab(daily)
    with customers_tab:
        render_customers_tab(metrics)
    with authors_tab:
        render_authors_tab(metrics)
 