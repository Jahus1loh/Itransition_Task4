import pandas as pd
from itertools import combinations
from collections.abc import Sequence


def find_unique_users(users_df: pd.DataFrame) -> pd.DataFrame:
    return deduplicate_users_df(users_df).shape[0]


def get_users_df_cols_without_id(users_df: pd.DataFrame) -> Sequence[str]:
    all_cols = users_df.columns
    id_col_location = all_cols.get_loc("id")
    return all_cols.delete(id_col_location)

def deduplicate_users_df(users_df: pd.DataFrame) -> pd.DataFrame:
    cols_without_id = get_users_df_cols_without_id(users_df)
    for comb in combinations(cols_without_id, len(cols_without_id) - 1):
        users_df = users_df.drop_duplicates(subset=list(comb))

    return users_df