-- ====================================================================
-- PROJECT 1: ENTERPRISE E-COMMERCE SALES & SUPPLY CHAIN ANALYTICS
-- AUTHOR: AMAN KANOJIA
-- DATA BASE PLATFORM: POSTGRESQL
-- ====================================================================

-- --------------------------------------------------------------------
-- SCENARIO A: MONTH-OVER-MONTH REVENUE DYNAMICS (FINANCIAL INTELLIGENCE)
-- Objective: Track transactional revenue fluctuations across billing periods.
-- Technical Showcase: Common Table Expressions (CTEs), Window Functions (LAG)
-- --------------------------------------------------------------------
WITH MonthlySales AS (
    SELECT 
        DATE_TRUNC('month', order_date) AS order_month,
        SUM(total_amount) AS current_month_sales
    FROM orders
    GROUP BY 1
)
SELECT 
    TO_CHAR(order_month, 'YYYY-Month') AS billing_period,
    current_month_sales AS total_revenue_inr,
    LAG(current_month_sales, 1) OVER (ORDER BY order_month) AS previous_month_revenue,
    ROUND(
        ((current_month_sales - LAG(current_month_sales, 1) OVER (ORDER BY order_month)) 
        / LAG(current_month_sales, 1) OVER (ORDER BY order_month)) * 100, 
        2
    ) AS mom_growth_percentage
FROM MonthlySales;


-- --------------------------------------------------------------------
-- SCENARIO B: SUPPLY CHAIN LOGISTICS LATENCY & GEOGRAPHIC BOTTLENECKS
-- Objective: Compute fulfillment speed and isolate regional distribution delays.
-- Technical Showcase: Relational Inner Joins, Subqueries, Conditional Aggregations
-- --------------------------------------------------------------------
SELECT 
    c.region AS geographical_market,
    COUNT(o.order_id) AS total_shipped_orders,
    ROUND(AVG(o.shipping_date - o.order_date), 1) AS avg_days_to_ship,
    ROUND(AVG(o.delivery_date - o.shipping_date), 1) AS avg_transit_days,
    SUM(CASE WHEN o.delivery_date > o.shipping_date + 5 THEN 1 ELSE 0 END) AS operational_delays
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'Delivered'
GROUP BY c.region;