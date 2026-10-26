import pandas as pd


def find_unique_authors_sets(books_df: pd.DataFrame):
    return books_df["author"].apply(frozenset).nunique()
