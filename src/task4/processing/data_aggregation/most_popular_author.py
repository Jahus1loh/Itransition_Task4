import pandas as pd


def find_most_popular_author(orders_df, books_df):
    joined_df = join_books_and_orders_df(orders_df, books_df)
    grouped_df = group_by_authors(joined_df)
    return grouped_df


def join_books_and_orders_df(orders_df: pd.DataFrame, books_df: pd.DataFrame):
    joined_df = orders_df.merge(
        books_df,
        left_on="book_id",
        right_on="id",
        how="left"
    )
    return joined_df

def group_by_authors(joined_df: pd.DataFrame):
    joined_df = joined_df.groupby("author")["quantity"].sum()
    joined_df = joined_df.sort_values(ascending=False)
    return joined_df
