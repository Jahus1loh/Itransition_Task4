from collections.abc import Sequence
from itertools import combinations

import pandas as pd
from nameparser import parse
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components


def clean_users_data(users_df: pd.DataFrame) -> pd.DataFrame:
    users_df = fix_address_formatting(users_df)
    users_df = fix_names_formatting(users_df)
    users_df = fix_phone_formatting(users_df)
    users_df = rename_users_columns(users_df)
    users_df = label_users(users_df)
    return users_df


def fix_address_formatting(users_df: pd.DataFrame) -> pd.DataFrame:
    users_df["address"] = (
        users_df["address"]
        .astype("string")
        .str.strip()
        .replace(r"(?i)^(|null|none|nan|n/a)$", pd.NA, regex=True)
        .fillna("Unknown")
    )
    return users_df


def extract_f_name_and_surname(name: str) -> str:
    if pd.isna(name):
        return pd.NA
    parsed_name = parse(name)
    return f"{parsed_name.given} {parsed_name.family}".strip()


def fix_names_formatting(users_df: pd.DataFrame) -> pd.DataFrame:
    users_df["name"] = users_df["name"].apply(extract_f_name_and_surname)

    return users_df


def fix_phone_formatting(users_df: pd.DataFrame) -> pd.DataFrame:
    users_df["phone"] = (
        users_df["phone"].astype("string").str.replace(r"\D", "", regex=True)
    )
    return users_df


def rename_users_columns(users_df: pd.DataFrame) -> pd.DataFrame:
    users_df = users_df.rename(columns={"id": "user_id"})
    return users_df


def buildEdges(
    users_df: pd.DataFrame, cols: pd.Index
) -> tuple[Sequence[int], Sequence[int]]:
    source, dest = [], []

    for comb in combinations(cols, len(cols) - 1):
        for indices in users_df.groupby(list(comb)).groups.values():
            source.extend(indices[1:])
            dest.extend([indices[0]] * (len(indices) - 1))

    return source, dest


def buildGraph(
    users_df: pd.DataFrame, source: Sequence[int], dest: Sequence[int]
):
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
    cols = users_df.columns.drop("user_id")
    source, dest = buildEdges(users_df, cols)
    graph = buildGraph(users_df, source, dest)
    return findComponents(graph)


def label_users(users_df: pd.DataFrame) -> pd.DataFrame:
    labels = identifyDuplicates(users_df)
    return users_df.assign(person_id=labels)
