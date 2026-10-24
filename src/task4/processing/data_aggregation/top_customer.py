import pandas as pd
from processing.data_aggregation.unique_users import label_users


def sum_person_spending(labeled_df: pd.DataFrame, orders_df: pd.DataFrame) -> pd.DataFrame:
    joined_df = join_labeled_persons_to_orders(labeled_df, orders_df)
    summed_spendings = joined_df.groupby("person_id")["paid_price"].sum()

    return summed_spendings

def join_labeled_persons_to_orders(labeled_df: pd.DataFrame, orders_df: pd.DataFrame) -> pd.DataFrame:
    joined_df = orders_df.merge(
        labeled_df[["id", "person_id"]], left_on="user_id", right_on="id"
    )

    return joined_df

def find_top_spender_user_ids(users_df: pd.DataFrame, orders_df: pd.DataFrame) -> pd.DataFrame:
    labeled_df = label_users(users_df)
    summed_spendings = sum_person_spending(labeled_df, orders_df)

    top_spending = summed_spendings.idxmax()
    print(f"Total spent: {summed_spendings[top_spending]}")
    return labeled_df[labeled_df["person_id"] == top_spending].drop(columns="person_id")
