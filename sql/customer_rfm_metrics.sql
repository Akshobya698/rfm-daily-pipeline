WITH valid_orders AS (
    SELECT
        order_id,
        customer_id,
        created_at,
        total
    FROM ecom.orders
    WHERE LOWER(status) <> 'cancelled'
      AND created_at < %(run_date)s::date + INTERVAL '1 day'
),

recency_cte AS (
    SELECT
        customer_id,
        MAX(created_at) AS last_order_date,
        %(run_date)s::date - MAX(created_at)::date AS recency_days
    FROM valid_orders
    GROUP BY customer_id
),

fm_cte AS (
    SELECT
        customer_id,
        COUNT(order_id) AS frequency_orders,
        SUM(total) AS monetary_value
    FROM valid_orders
    WHERE created_at >= %(run_date)s::date - INTERVAL '90 days'
    GROUP BY customer_id
)

SELECT
    r.customer_id,
    r.last_order_date,
    r.recency_days,
    COALESCE(f.frequency_orders, 0) AS frequency_orders,
    COALESCE(f.monetary_value, 0) AS monetary_value
FROM recency_cte r
LEFT JOIN fm_cte f
    ON r.customer_id = f.customer_id
ORDER BY r.customer_id;
