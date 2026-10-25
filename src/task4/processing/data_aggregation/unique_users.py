from collections.abc import Sequence
from itertools import combinations

import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components


def buildEdges(
    users_df: pd.DataFrame, cols: pd.Index
) -> tuple[Sequence[int], Sequence[int]]:
    source, dest = [], []

    for comb in combinations(cols, len(cols) - 1):
        for indices in users_df.groupby(list(comb)).groups.values():
            source.extend(indices[1:])
            dest.extend([indices[0]] * (len(indices) - 1))

    return source, dest


def buildGraph(users_df: pd.DataFrame, source: Sequence[int], dest: Sequence[int]):
    size = len(users_df)
    return coo_matrix(
        ([1] * len(source), (source, dest)),
        shape=(size, size),
    )


def findComponents(graph) -> list[int]:
    _, labels = connected_components(graph, directed=False)
    return labels


def identifyDuplicates(users_df: pd.DataFrame) -> list[int]:
    users_df = users_df.reset_index(drop=True)
    cols = users_df.columns.drop("id")

    source, dest = buildEdges(users_df, cols)
    graph = buildGraph(users_df, source, dest)

    return findComponents(graph)


def label_users(users_df: pd.DataFrame) -> pd.DataFrame:
    labels = identifyDuplicates(users_df)
    return users_df.assign(person_id=labels)


def find_unique_users(users_df: pd.DataFrame) -> int:
    return label_users(users_df)["person_id"].nunique()
