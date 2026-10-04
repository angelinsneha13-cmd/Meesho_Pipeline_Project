-- Query 1: Monthly revenue by category (Direct feed for Part 2 & Part 4)
SELECT 
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY 
    CASE month 
        WHEN 'April' THEN 1 
        WHEN 'May' THEN 2 
        WHEN 'June' THEN 3 
    END,
    CASE category
        WHEN 'Ethnic Wear' THEN 1
        WHEN 'Western Wear' THEN 2
        WHEN 'Kids Wear' THEN 3
        WHEN 'Home & Kitchen' THEN 4
        WHEN 'Beauty & Personal Care' THEN 5
    END;

-- Query 2: Region-wise total revenue and order count
SELECT 
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
    COUNT(o.order_id) AS n_orders
FROM resellers r
JOIN orders o ON r.reseller_id = o.reseller_id
GROUP BY r.region
ORDER BY total_revenue DESC;

-- Query 3: Top resellers by total spend (> 50,000)
SELECT 
    r.reseller_id,
    r.reseller_name,
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM resellers r
JOIN orders o ON r.reseller_id = o.reseller_id
GROUP BY r.reseller_id, r.reseller_name, r.region
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;

-- Query 4a: Reseller who has never placed an order
SELECT 
    r.reseller_id,
    r.reseller_name,
    r.region,
    r.city
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;

-- Query 4b: Demonstrating COUNT(*) vs COUNT(order_id) on zero-match
SELECT 
    r.reseller_id,
    r.reseller_name,
    COUNT(*) AS count_star,
    COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id, r.reseller_name;

-- Query 5: Average Order Value (AOV) for June Delivered orders
SELECT 
    ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS june_delivered_aov
FROM orders
WHERE month = 'June' AND status = 'Delivered';