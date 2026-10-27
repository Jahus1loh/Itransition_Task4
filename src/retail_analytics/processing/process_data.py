import pandas as pd
from processing.data_aggregation.daily_revenue import compute_daily_revenue
from processing.data_aggregation.most_popular_author import (
    find_most_popular_author,
)
from processing.data_aggregation.top_customer import find_top_spender_user_ids
from processing.data_aggregation.unique_authors import find_unique_authors_sets
from processing.data_aggregation.unique_users import find_unique_users
from processing.data_cleaning.clean_books import clean_books_data
from processing.data_cleaning.clean_orders import clean_orders_data
from processing.data_cleaning.clean_users import clean_users_data
from processing.load_data import read_csv, read_parquet, read_yaml


def load_data(
    iteration: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    books_df = read_yaml(iteration)
    orders_df = read_parquet(iteration)
    users_df = read_csv(iteration)
    return (books_df, orders_df, users_df)


def clean_data(
    iteration: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    books_df, orders_df, users_df = load_data(iteration)
    books_df = clean_books_data(books_df)
    orders_df = clean_orders_data(orders_df)
    users_df = clean_users_data(users_df)

    books_df.to_csv("cleaned_books.csv")
    orders_df.to_csv("cleaned_orders.csv")
    users_df.to_csv("cleaned_users.csv")

    return books_df, orders_df, users_df


def compute_metrics(iteration: int) -> dict[str, object]:
    books_df, orders_df, users_df = clean_data(iteration)
    print(books_df.head())
    print(books_df.dtypes)
    books_df.to_csv("books_df.csv")
    best_buyer_df, best_total = find_top_spender_user_ids(users_df, orders_df)

    return {
        "daily_revenue": compute_daily_revenue(orders_df),
        "n_users": find_unique_users(users_df),
        "n_author_sets": find_unique_authors_sets(books_df),
        "top_authors": find_most_popular_author(orders_df, books_df),
        "best_buyer_records": best_buyer_df,
        "best_buyer_total": best_total,
        "users_df": users_df,
        "orders_df": orders_df,
        "books_df": books_df,
    }
