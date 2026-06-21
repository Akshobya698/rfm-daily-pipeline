
from datetime import date
import pandas as pd


def assign_segment(row):
    """
    Assign customer segment based on RFM scores.
    """

    if row["r_score"] >= 4 and row["f_score"] >= 4 and row["m_score"] >= 4:
        return "Champions"

    elif row["f_score"] >= 4 and row["r_score"] >= 3:
        return "Loyal"

    elif row["m_score"] >= 4 and row["f_score"] <= 3:
        return "Big Spenders"

    elif row["r_score"] <= 2 and row["f_score"] >= 3:
        return "At Risk"

    elif row["r_score"] <= 2 and row["f_score"] <= 2:
        return "Hibernating"

    else:
        return "Others"


def calculate_rfm_scores(rfm_df, run_date):
    """
    Create RFM scores and customer segments.
    """
    # Add run date to the DataFrame
    rfm_df["run_date"] = run_date

    # Recency Score (lower recency is better)
    rfm_df["r_score"] =pd.qcut(
        rfm_df["recency_days"].rank(method="first"),
        q=5,
        labels=[5,4,3,2,1]
    ).astype(int)

    # Frequency Score (higher frequency is better)
    rfm_df["f_score"] = pd.qcut(
        rfm_df["frequency_orders"].rank(method="first"),
        q=5,
        labels=[1, 2, 3, 4, 5]
    ).astype(int)

    # Monetary Score (higher spend is better)
    rfm_df["m_score"] = pd.qcut(
        rfm_df["monetary_value"].rank(method="first"),
        q=5,
        labels=[1, 2, 3, 4, 5]
    ).astype(int)

    # Combine scores into one string
    rfm_df["rfm_score"] = (
        rfm_df["r_score"].astype(str)
        + rfm_df["f_score"].astype(str)
        + rfm_df["m_score"].astype(str)
    )

    # Assign customer segments
    rfm_df["rfm_segment"] = rfm_df.apply(
        assign_segment,
        axis=1
    )

  

    return rfm_df