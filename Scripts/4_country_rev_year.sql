SELECT
	EXTRACT(YEAR FROM sa.orderdate) AS order_year,
	c.country,
	SUM(sa.quantity * sa.unitprice) AS total_revenue
FROM
	sales sa
JOIN customer c ON
	sa.customerkey = c.customerkey
GROUP BY
	EXTRACT(YEAR FROM sa.orderdate),
	c.country
