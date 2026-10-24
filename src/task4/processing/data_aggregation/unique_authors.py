import pandas as pd


def find_unique_authors_sets(books_df: pd.DataFrame):
    print(books_df["author"].value_counts().shape[0])