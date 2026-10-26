import tomllib
from pathlib import Path

import pandas as pd
import streamlit as st
from processing.nlm_processing.duck_db_query import create_service, run_query
from processing.process_data import compute_metrics

ITERATIONS = range(1, 6)

with Path("src/task4/config/config.toml").open("rb") as f:
    cfg = tomllib.load(f)
    table_names = cfg["duck_db"]["table_names"]


@st.cache_data
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
    return st.sidebar.selectbox("Store number", list(ITERATIONS))


@st.cache_resource
def load_query_service(iteration: int) -> dict:
    metrics = load_metrics(iteration)
    frames = {name: metrics[f"{name}_df"] for name in table_names}
    return create_service(frames)


def render_revenue_tab(daily: pd.Series) -> None:
    st.subheader("Top 5 days by revenue")
    st.table(build_top_days_table(daily))
    st.subheader("Daily revenue")
    st.line_chart(daily)


def render_customers_tab(metrics: dict) -> None:
    records = metrics["best_buyer_records"]
    left, right = st.columns(2)
    left.metric("Unique users", f"{metrics['n_users']:,}")
    right.metric("Best buyer total spent", f"{metrics['best_buyer_total']:,.2f}")
    st.subheader("Best buyer (with aliases)")
    st.code(str(records["user_id"].astype(int).tolist()), language="python")
    st.dataframe(records, hide_index=True)


def render_authors_tab(metrics: dict) -> None:
    st.metric("Unique sets of authors", metrics["n_author_sets"])
    st.subheader("Most popular author(s)")
    st.write(metrics["top_authors"].head(1))


def get_chat_messages(iteration: int) -> list:
    return st.session_state.setdefault(f"ask_messages_{iteration}", [])


def show_query_result(message: dict) -> None:
    st.dataframe(message["result"], hide_index=True)
    with st.expander("Generated SQL"):
        st.code(message["sql"], language="sql")


def render_chat_history(messages: list) -> None:
    for message in messages:
        show_chat_message(message)


def show_chat_message(message: dict) -> None:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "result" in message:
            show_query_result(message)
        if "error" in message:
            st.error(message["error"])


def query_with_spinner(iteration: int, question: str) -> str:
    service = load_query_service(iteration)
    with st.spinner("Generating and executing SQL"):
        return run_query(service, question)


def make_result_message(sql: str, result: pd.DataFrame) -> dict:
    return {
        "role": "assistant",
        "content": f"Returned {len(result):,} rows",
        "sql": sql,
        "result": result,
    }


def make_error_message(error: Exception) -> dict:
    return {
        "role": "assistant",
        "content": "Could not process the query",
        "error": str(error),
    }


def answer_question(iteration: int, question: str) -> dict:
    try:
        return make_result_message(*query_with_spinner(iteration, question))
    except Exception as e:
        return make_error_message(e)


def handle_question(iteration: int, question: str, messages: list) -> None:
    messages.append({"role": "user", "content": question})
    show_chat_message(messages[-1])
    answer = answer_question(iteration, question)
    messages.append(answer)
    show_chat_message(answer)


def render_ask_tab(iteration: int) -> None:
    st.subheader(f"Ask questions about dataset {iteration}")
    messages = get_chat_messages(iteration)
    render_chat_history(messages)
    question = st.chat_input("Ask about books, orders, or users")
    if question:
        handle_question(iteration, question, messages)


def render_dashboard() -> None:
    st.set_page_config(page_title="Sales dashboard", layout="wide")
    st.title("Sales dashboard")

    iteration = select_iteration()

    metrics = load_metrics(iteration)
    daily = prepare_daily_revenue(metrics)

    revenue_tab, customers_tab, authors_tab, ask_tab = st.tabs(
        ["Revenue", "Customers", "Authors", "Ask"]
    )
    with revenue_tab:
        render_revenue_tab(daily)
    with customers_tab:
        render_customers_tab(metrics)
    with authors_tab:
        render_authors_tab(metrics)
    with ask_tab:
        render_ask_tab(iteration)
