import pandas as pd
from nameparser import parse


def clean_users_data(users_df: pd.DataFrame) -> pd.DataFrame:
    users_df = fix_address_formatting(users_df)
    users_df = fix_names_formatting(users_df)
    users_df = fix_phone_formatting(users_df)
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
    parsed_name = parse(name)
    return parsed_name.given + " " + parsed_name.family


def fix_names_formatting(users_df: pd.DataFrame) -> pd.DataFrame:
    users_df["name"] = users_df["name"].apply(extract_f_name_and_surname)

    return users_df


def fix_phone_formatting(users_df: pd.DataFrame) -> pd.DataFrame:
    users_df["phone"] = (
        users_df["phone"].astype("string").str.replace(r"\D", "", regex=True)
    )
    return users_df
