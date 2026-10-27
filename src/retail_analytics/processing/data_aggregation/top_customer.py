import pandas as pd


def sum_person_spending(
    users_df: pd.DataFrame, orders_df: pd.DataFrame
) -> pd.DataFrame:
    joined_df = join_labeled_persons_to_orders(users_df, orders_df)
    summed_spendings = joined_df.groupby("person_id")["paid_price"].sum()

    return summed_spendings


def join_labeled_persons_to_orders(
    users_df: pd.DataFrame, orders_df: pd.DataFrame
) -> pd.DataFrame:
    joined_df = orders_df.merge(
        users_df[["user_id", "person_id"]],
        left_on="user_id",
        right_on="user_id",
    )

    return joined_df


def find_top_spender_user_ids(
    users_df: pd.DataFrame, orders_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    summed_spendings = sum_person_spending(users_df, orders_df)
    top_spending = summed_spendings.idxmax()
    return (
        users_df[users_df["person_id"] == top_spending].drop(
            columns="person_id"
        ),
        top_spending,
    )
