import re
from decimal import Decimal

import pandas as pd
from dateutil import parser
from price_parser import Price

conversion_rate = Decimal("1.2")


def clean_orders_data(orders_df: pd.DataFrame) -> pd.DataFrame:
    orders_df = fix_orders_unit_price(orders_df)
    orders_df["paid_price"] = orders_df["unit_price"] * orders_df["quantity"]
    orders_df = add_timestamp_parts(orders_df)
    orders_df = fix_shipping_formatting(orders_df)

    return orders_df


def normalize_cents(s: str) -> str:
    s = str(s).strip()
    if "¢" not in s:
        return s
    major, minor = re.findall(r"\d+", s)[:2]
    sym = re.search(r"USD|EUR|[$€]", s)
    return f"{sym.group() if sym else ''}{major}.{minor}"


def extract_price_from_string(unit_price: str) -> str:
    price = Price.fromstring(unit_price)
    return (
        price.amount
        if price.currency in ["USD", "$"]
        else price.amount * conversion_rate
    )


def fix_orders_unit_price(orders_df: pd.DataFrame) -> pd.DataFrame:
    orders_df["unit_price"] = orders_df["unit_price"].apply(normalize_cents)
    orders_df["unit_price"] = orders_df["unit_price"].apply(
        extract_price_from_string
    )
    orders_df["unit_price"] = pd.to_numeric(
        orders_df["unit_price"], errors="coerce"
    )

    return orders_df


def normalize_timestamp_text(raw_timestamp: str) -> str:
    am_pm_standarized = re.sub(r"(?i)\b([ap])\.m\.", r"\1m", raw_timestamp)
    sep_to_one_white_space = re.sub(r"[;,]", " ", am_pm_standarized)
    return re.sub(r"\s+", " ", sep_to_one_white_space).strip()


def parse_timestamp(timestamp: str) -> pd.Timestamp:
    day_first_dotted_date_pattern = re.compile(
        r"(?<![\d:])\d{1,2}\.\d{1,2}\.\d{4}"
    )
    timestamp = normalize_timestamp_text(timestamp)
    return pd.Timestamp(
        parser.parse(
            timestamp,
            dayfirst=bool(day_first_dotted_date_pattern.search(timestamp)),
        )
    )


def fix_timestamp_formatting(orders_df: pd.DataFrame) -> pd.DataFrame:
    orders_df["timestamp"] = orders_df["timestamp"].map(parse_timestamp)

    return orders_df


def add_timestamp_parts(orders_df: pd.DataFrame) -> pd.DataFrame:
    orders_df = fix_timestamp_formatting(orders_df)
    orders_df["day"] = orders_df["timestamp"].dt.day
    orders_df["month"] = orders_df["timestamp"].dt.month
    orders_df["year"] = orders_df["timestamp"].dt.year
    orders_df["date"] = pd.to_datetime(orders_df[["year", "month", "day"]])

    return orders_df


def fix_shipping_formatting(orders_df: pd.DataFrame) -> pd.DataFrame:
    orders_df["shipping"] = (
        orders_df["shipping"]
        .astype("string")
        .str.strip()
        .replace(r"(?i)^(|null|none|nan|n/a)$", pd.NA, regex=True)
        .fillna("Unknown")
    )
    return orders_df
