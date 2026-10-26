import pandas as pd
from nameparser import parse


def clean_books_data(books_df: pd.DataFrame) -> pd.DataFrame:
    books_df = fix_books_column_names(books_df)
    books_df = fix_books_data_types(books_df)
    books_df = handle_missing_publishers(books_df)
    books_df = normalize_author_names(books_df)
    books_df = rename_books_columns(books_df)
    return books_df


def fix_books_column_names(books_df: pd.DataFrame) -> pd.DataFrame:
    books_df.columns = (
        books_df.columns.str.strip().str.lower().str.replace(":", "")
    )
    return books_df


def fix_books_data_types(books_df: pd.DataFrame) -> pd.DataFrame:
    books_df["year"] = pd.to_numeric(books_df["year"], errors="coerce")
    books_df["year"] = books_df["year"].astype("Int64")
    return books_df


def handle_missing_publishers(books_df: pd.DataFrame) -> pd.DataFrame:
    books_df["publisher"] = books_df["publisher"].fillna("Unknown")
    return books_df


def extract_f_name_and_surname(name: str) -> str:
    parsed_name = parse(name)
    return parsed_name.given + " " + parsed_name.family


def fix_names_formatting(author_names: str) -> list[str]:
    authors = author_names.split(",")
    return sorted(extract_f_name_and_surname(name.strip()) for name in authors)


def normalize_author_names(books_df: pd.DataFrame) -> pd.DataFrame:
    books_df["author"] = books_df["author"].apply(fix_names_formatting)
    return books_df


def rename_books_columns(books_df: pd.DataFrame) -> pd.DataFrame:
    books_df = books_df.rename(
        columns={
            "id": "book_id",
            "year": "book_year",
        }
    )
    return books_df
