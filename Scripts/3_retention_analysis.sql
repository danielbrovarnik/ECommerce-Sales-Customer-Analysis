WITH customer_latest_purchase_details AS (
    SELECT
        customerkey,
        MAX(orderdate) AS last_purchase_date, 
        first_purchase_date,                 
        cohort_year                          
    FROM
        cohort_analysis
    GROUP BY
        customerkey,
        first_purchase_date,
        cohort_year
)
SELECT
    cld.cohort_year,
    CASE
        WHEN cld.last_purchase_date < (SELECT MAX(s.orderdate) FROM sales s) - INTERVAL '6 months' THEN 'Churned'
        ELSE 'Active'
    END AS customer_status,
    COUNT(cld.customerkey) AS num_customers,
    SUM(COUNT(cld.customerkey)) OVER (PARTITION BY cld.cohort_year) AS total_customers,
    ROUND(
        COUNT(cld.customerkey) * 1.0 / SUM(COUNT(cld.customerkey)) OVER (PARTITION BY cld.cohort_year),
        2
    ) AS cohort_percentage
FROM
    customer_latest_purchase_details cld
WHERE
    -- This condition was originally in the 'churned_customers' CTE,
    -- filtering which customers are even considered for churn analysis.
    cld.first_purchase_date < (SELECT MAX(s.orderdate) FROM sales s) - INTERVAL '6 months'
GROUP BY
    cld.cohort_year,
    customer_status -- Grouping by the calculated CASE expression
ORDER BY
    cld.cohort_year,
    customer_status;