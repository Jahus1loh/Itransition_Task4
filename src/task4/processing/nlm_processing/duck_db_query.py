import re
import tomllib
from pathlib import Path

import duckdb
import pandas as pd
import sqlglot
import streamlit as st
from google import genai
from groq import Groq
from sqlglot import exp

with Path("src/task4/config/config.toml").open("rb") as f:
    cfg = tomllib.load(f)
    prompt = cfg["duck_db"]["query_prompt"]
    model_name = cfg["duck_db"]["model_name"]
    table_names = cfg["duck_db"]["table_names"]

api_key = st.secrets["GROK_API_KEY"]


def build_schema(frames: dict) -> str:
    columns = [
        f"{name}: {', '.join(map(str, frames[name].columns))}" for name in table_names
    ]
    joins = "Join orders.book_id = books.book_id; orders.user_id = users.user_id."
    return "\n".join([*columns, joins])


def create_service(frames: dict) -> dict:
    connection = duckdb.connect(":memory:")
    for name in table_names:
        connection.register(name, frames[name])
    connection.execute("SET enable_external_access = false")
    return {
        "conn": connection,
        "client": Groq(api_key=api_key),
        # "client": genai.Client(api_key=api_key),
        "schema": build_schema(frames),
    }


def generate_sql(service: dict, question: str) -> str:
    final_prompt = prompt.replace("$schema", service["schema"]).replace(
        "$question", question
    )
    # response = service["client"].models.generate_content(
    #     model=model_name,
    #     contents=final_prompt,
    # )
    response = service["client"].chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": final_prompt}],
        temperature=0,
    )
    if not response.choices[0].message.content:
        raise ValueError("The model didnt return SQL")
    return re.sub(
        r"^```(?:sql)?|```$", "", response.choices[0].message.content.strip(), flags=re.IGNORECASE
    ).strip()


def ensure_single_query(statements) -> None:
    if len(statements) != 1 or not isinstance(statements[0], exp.Select):
        raise ValueError("Only one SELECT query is allowed")


def gather_allowed_tables_and_cte(statements):
    query = statements[0]
    ctes = {cte.alias_or_name.lower() for cte in query.find_all(exp.CTE)}
    tables = {table.name.lower() for table in query.find_all(exp.Table)}
    return (ctes, tables)


def ensure_valid_table_in_query(tables, ctes):
    allowed = {name.lower() for name in table_names} | ctes
    if not tables or not tables <= allowed:
        raise ValueError("The query uses non existing table")


def add_query_limit(query):
    if query.args.get("limit") is None:
        query = query.limit(100)
    return query


def validate_sql_query(sql_query: str):
    statements = sqlglot.parse(sql_query, read="duckdb")
    ensure_single_query(statements)
    ctes, tables = gather_allowed_tables_and_cte(statements)
    ensure_valid_table_in_query(tables, ctes)
    query = add_query_limit(statements[0])
    return query.sql(dialect="duckdb")


def run_query(service: dict, question: str) -> tuple[str, pd.DataFrame]:
    sql = validate_sql_query(generate_sql(service, question))
    result = service["conn"].execute(sql).fetchdf()
    return (sql, result)
