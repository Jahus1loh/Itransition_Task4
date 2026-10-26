# import pandas as pd
# import streamlit as st
# from llama_index.core.tools import QueryEngineTool
# from llama_index.experimental.query_engine import PandasQueryEngine
# from llama_index.llms.google_genai import GoogleGenAI

# PANDAS_OPTIONS = {
#     "verbose": False,
#     "synthesize_response": True,
# }

# TOOL_DESCRIPTIONS = {
#     "books": (
#         "Questions about the complete book catalog: titles, authors, "
#         "genres, publishers, publication years, and book counts."
#     ),
#     "orders": (
#         "Questions about orders alone: order counts, quantities, dates, "
#         "shipping, unit prices, and paid prices."
#     ),
#     "users": (
#         "Questions about all registered users and their attributes. "
#         "Use for user counts and user details, not purchase history."
#     ),
#     "merged": (
#         "Questions requiring relationships between orders, users, and books, "
#         "such as spending by user, sales by author, or popular genres. "
#         "Each row represents an order record enriched with book and user data. "
#         "Use paid_price for the recorded paid amount; use book_year for "
#         "the publication year."
#     ),
# }


# def create_llm() -> GoogleGenAI:
#     api_key = st.secrets["GEMINI_API_KEY"]
#     return GoogleGenAI(
#         model="gemini-3.8-flash",
#         api_key=api_key,
#     )


# def create_engine(df: pd.DataFrame, llm: GoogleGenAI, name: str) -> PandasQueryEngine:
#     instructions = f"""
#     The DataFrame is named df.
#     Dataset: {name}
#     Available columns: {list(df.columns)}

#     Use only the listed columns. Never invent column names.
#     unit_price means the price per unit in an order record.
#     paid_price means the recorded total paid amount.
#     Count buyers using the number of unique user_id values.
#     If a required column does not exist, explain the limitation.
#     Return one valid pandas expression.
#     """
#     return PandasQueryEngine(
#         df=df, llm=llm, instruction_str=instructions, **PANDAS_OPTIONS
#     )


# def create_engines(frames: dict, llm: GoogleGenAI) -> dict:
#     return {name: create_engine(df, llm, name) for name, df in frames.items()}


# def create_query_tools(engines: dict) -> list:
#     return [
#         QueryEngineTool.from_defaults(
#             query_engine=engine, name=name, description=TOOL_DESCRIPTIONS[name]
#         )
#         for name, engine in engines.items()
#     ]
