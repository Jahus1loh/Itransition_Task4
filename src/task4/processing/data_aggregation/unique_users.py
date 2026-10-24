from collections.abc import Sequence
from itertools import combinations

import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

# def find_unique_users(users_df: pd.DataFrame) -> pd.DataFrame:
#     return deduplicate_users_df(users_df).shape[0]


def get_users_df_cols_without_id(users_df: pd.DataFrame) -> Sequence[str]:
    all_cols = users_df.columns
    id_col_location = all_cols.get_loc("id")
    return all_cols.delete(id_col_location)


def label_users(users_df: pd.DataFrame) -> pd.DataFrame:
    users_df = users_df.reset_index(drop=True)
    cols = users_df.columns.drop("id")

    source, dest = [], []
    for comb in combinations(cols, len(cols) - 1):
        for indicies in users_df.groupby(list(comb)).groups.values():
            source += list(indicies[1:])
            dest += [indicies[0]] * (len(indicies) - 1)

    graph = coo_matrix(
        ([1] * len(source), (source, dest)), shape=(len(users_df), len(users_df))
    )
    _, labels = connected_components(graph, directed=False)
    return users_df.assign(person_id=labels)


def find_unique_users(users_df: pd.DataFrame) -> int:
    return label_users(users_df)["person_id"].nunique()
