import pandas as pd


def compute_daily_revenue(orders_df: pd.DataFrame) -> pd.DataFrame:
    grouped = orders_df.groupby("date")
    daily_revenue = grouped["paid_price"].sum()
    return daily_revenue


def find_5_highest_revenues(orders_df: pd.DataFrame) -> pd.DataFrame:
    daily_revenue = compute_daily_revenue(orders_df)
    daily_revenue = daily_revenue.sort_values(ascending=False)
