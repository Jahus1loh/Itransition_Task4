import pandas as pd


def find_unique_authors_sets(books_df: pd.DataFrame):
    author_sets = books_df["author"].map(lambda names: tuple(sorted(set(names))))
    return author_sets.nunique()
