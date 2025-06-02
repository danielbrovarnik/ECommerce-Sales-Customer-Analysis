WITH customer_ltv AS (
	SELECT
		customerkey,
		concat_name,
		
		sum(total_net_rev) AS LTV
	FROM
		cohort_analysis
	GROUP BY
		customerkey,
		concat_name
),
customer_segments AS (
	SELECT
		percentile_cont(0.25) WITHIN GROUP 
		(ORDER BY ltv) AS ltv_25th_precentile,
		percentile_cont(0.75) WITHIN GROUP (
		ORDER BY
			ltv
		) AS ltv_75th_precentile
	FROM
		customer_ltv
), segment_values AS (
	SELECT
		c.*,
		CASE
			WHEN c.ltv < cs.ltv_25th_precentile THEN '1- LOW VALUE'
			WHEN c.ltv <= cs.ltv_75th_precentile THEN '2- MID VALUE'
			ELSE '3-HIGH VALUE'
		END AS CUSTOMER_VALUE
	FROM
		customer_ltv c,
		customer_segments cs
)
 SELECT 
 count(customer_value),
 customer_value,
 sum(ltv) AS total_ltv,
 sum(ltv) / count(customer_value) AS avg
 
 FROM segment_values
 GROUP BY customer_value