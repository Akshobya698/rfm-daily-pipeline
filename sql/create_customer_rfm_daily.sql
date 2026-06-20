CREATE TABLE IF NOT EXISTS ecom.customer_rfm_daily (
    run_date DATE NOT NULL,
    customer_id BIGINT NOT NULL,

    recency_days INTEGER NOT NULL,
    frequency_orders INTEGER NOT NULL,
    monetary_value NUMERIC(18,2) NOT NULL,

    r_score SMALLINT NOT NULL CHECK (r_score BETWEEN 1 AND 5),
    f_score SMALLINT NOT NULL CHECK (f_score BETWEEN 1 AND 5),
    m_score SMALLINT NOT NULL CHECK (m_score BETWEEN 1 AND 5),

    rfm_score VARCHAR(3) NOT NULL,
    rfm_segment VARCHAR(50) NOT NULL,

    CONSTRAINT customer_rfm_daily_pk
        PRIMARY KEY (run_date, customer_id)
);
