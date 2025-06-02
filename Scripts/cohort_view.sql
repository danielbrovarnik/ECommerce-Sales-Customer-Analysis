CREATE OR REPLACE VIEW public.cohort_analysis
AS WITH customer_rev AS (
         SELECT s.customerkey,
            s.orderdate,
            sum(s.quantity::double precision * s.netprice / s.exchangerate) AS sum,
            count(s.orderkey) AS count,
            c.countryfull,
            c.age,
            c.givenname,
            c.surname
           FROM sales s
             LEFT JOIN customer c ON c.customerkey = s.customerkey
          GROUP BY s.orderdate, s.customerkey, c.countryfull, c.age, c.givenname, c.surname
        )
 SELECT customerkey,
    orderdate,
    sum AS total_net_rev,
    count,
    countryfull,
    age,
    concat(givenname, ' ', surname) AS concat_name,
    min(orderdate) OVER (PARTITION BY customerkey) AS first_purchase_date,
    EXTRACT(year FROM min(orderdate) OVER (PARTITION BY customerkey)) AS cohort_year
   FROM customer_rev cr;