import matplotlib.pyplot as plt
import pandas as pd
from processing.data_aggregation.daily_revenue import compute_daily_revenue


def create_revenue_plot(orders_df: pd.DataFrame) -> None:
    daily_revenue = compute_daily_revenue(orders_df)

    plt.plot(daily_revenue)
    plt.xlabel("Date")
    plt.ylabel("Revenue in USD")
    plt.title("Daily revenue")
    plt.show()
