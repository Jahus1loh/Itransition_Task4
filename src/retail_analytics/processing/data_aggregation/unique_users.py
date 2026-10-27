import pandas as pd


def find_unique_users(users_df: pd.DataFrame) -> int:
    return users_df["person_id"].nunique()
