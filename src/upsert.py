# src/upsert.py

from psycopg2.extras import execute_values


# Columns expected in the final RFM dataframe
OUTPUT_COLUMNS = [
    "run_date",
    "customer_id",
    "recency_days",
    "frequency_orders",
    "monetary_value",
    "r_score",
    "f_score",
    "m_score",
    "rfm_score",
    "rfm_segment",
]


# PostgreSQL UPSERT query
UPSERT_SQL = """
INSERT INTO ecom.customer_rfm_daily (
    run_date,
    customer_id,
    recency_days,
    frequency_orders,
    monetary_value,
    r_score,
    f_score,
    m_score,
    rfm_score,
    rfm_segment
)
VALUES %s
ON CONFLICT (run_date, customer_id)
DO UPDATE SET
    recency_days = EXCLUDED.recency_days,
    frequency_orders = EXCLUDED.frequency_orders,
    monetary_value = EXCLUDED.monetary_value,
    r_score = EXCLUDED.r_score,
    f_score = EXCLUDED.f_score,
    m_score = EXCLUDED.m_score,
    rfm_score = EXCLUDED.rfm_score,
    rfm_segment = EXCLUDED.rfm_segment;
"""


def prepare_records(rfm_df):
    """
    Convert dataframe rows into tuples that
    PostgreSQL can insert.
    """

    records = list(
        rfm_df[OUTPUT_COLUMNS].itertuples(
            index=False,
            name=None
        )
    )

    return records


def upsert_rfm_results(conn, rfm_df):
    """
    Insert or update RFM records in PostgreSQL.
    """

    records = prepare_records(rfm_df)

    # Nothing to insert
    if not records:
        print("No records found.")
        return 0

    try:

        with conn.cursor() as cursor:

            execute_values(
                cursor,
                UPSERT_SQL,
                records,
                page_size=1000
            )

        conn.commit()

        print(
            f"Successfully upserted {len(records)} rows."
        )

        return len(records)

    except Exception as e:

        conn.rollback()

        print(
            f"Error while upserting data: {e}"
        )

        raise