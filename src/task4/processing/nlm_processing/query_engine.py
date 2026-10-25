import pandas as pd
import streamlit as st
from llama_index.core.tools import QueryEngineTool
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.llms.openai import OpenAI

PANDAS_INSTRUCTIONS = """
Answer the user's question using the DataFrame named df.
Use only existing columns.
Generate one valid Pandas expression.
Do not modify the DataFrame.
"""

PANDAS_OPTIONS = {
    "instruction_str": PANDAS_INSTRUCTIONS,
    "verbose": False,
    "synthesize_response": True,
}

TOOL_DESCRIPTIONS = {
    "books": (
        "Questions about the complete book catalog: titles, authors, "
        "genres, publishers, publication years, and book counts."
    ),
    "orders": (
        "Questions about orders alone: order counts, quantities, dates, "
        "shipping, unit prices, and paid prices."
    ),
    "users": (
        "Questions about all registered users and their attributes. "
        "Use for user counts and user details, not purchase history."
    ),
    "merged": (
        "Questions requiring relationships between orders, users, and books, "
        "such as spending by user, sales by author, or popular genres. "
        "Each row represents an order record enriched with book and user data. "
        "Use paid_price for the recorded paid amount; use book_year for "
        "the publication year."
    ),
}


def create_llm() -> OpenAI:
    api_key = st.secrets["OPENAI_API_KEY"]
    return OpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)


def create_engine(df: pd.DataFrame, llm: OpenAI) -> PandasQueryEngine:
    return PandasQueryEngine(df=df, llm=llm, **PANDAS_OPTIONS)


def create_engines(frames: dict, llm: OpenAI) -> dict:
    return {name: create_engine(df, llm) for name, df in frames.items()}


def create_query_tools(engines: dict) -> list:
    return [
        QueryEngineTool.from_defaults(
            query_engine=engine, name=name, description=TOOL_DESCRIPTIONS[name]
        )
        for name, engine in engines.items()
    ]
