import pandas as pd
from processing.data_aggregation.daily_revenue import find_5_highest_revenues
from processing.data_aggregation.most_popular_author import find_most_popular_author
from processing.data_aggregation.unique_authors import find_unique_authors_sets
from processing.data_aggregation.unique_users import find_unique_users
from processing.data_cleaning.clean_books import clean_books_data
from processing.data_cleaning.clean_orders import clean_orders_data
from processing.data_cleaning.clean_users import clean_users_data
from processing.load_data import read_csv, read_parquet, read_yaml


def load_data() -> tuple[pd.DataFrame]:
    books_df = read_yaml()
    orders_df = read_parquet()
    users_df = read_csv()
    return (books_df, orders_df, users_df)


def clean_data() -> tuple[pd.DataFrame]:
    books_df, orders_df, users_df = load_data()
    books_df = clean_books_data(books_df)
    orders_df = clean_orders_data(orders_df)
    users_df = clean_users_data(users_df)
    return books_df, orders_df, users_df


def aggreage_data():
    books_df, orders_df, users_df = clean_data()

    find_5_highest_revenues(orders_df)
    find_unique_authors_sets(books_df)
    find_most_popular_author(orders_df, books_df)
    print(find_unique_users(users_df))
