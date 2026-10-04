import csv
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "meesho_reseller.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Query 1: Monthly category revenue
cur.execute("""
    SELECT 
        month,
        category,
        ROUND(SUM(quantity * unit_price), 2) AS revenue,
        COUNT(*) AS n_orders
    FROM orders
    GROUP BY month, category
    ORDER BY 
        CASE month WHEN 'April' THEN 1 WHEN 'May' THEN 2 WHEN 'June' THEN 3 END,
        CASE category
            WHEN 'Ethnic Wear' THEN 1
            WHEN 'Western Wear' THEN 2
            WHEN 'Kids Wear' THEN 3
            WHEN 'Home & Kitchen' THEN 4
            WHEN 'Beauty & Personal Care' THEN 5
        END
""")
rows1 = cur.fetchall()
with open(
    os.path.join(OUTPUT_DIR, "monthly_category_revenue.csv"), "w", newline=""
) as f:
  w = csv.writer(f)
  w.writerow(["month", "category", "revenue", "n_orders"])
  for r in rows1:
    w.writerow(
        [r["month"], r["category"], f"{r['revenue']:.2f}", r["n_orders"]]
    )

# Query 2: Region revenue
cur.execute("""
    SELECT 
        r.region,
        ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
        COUNT(o.order_id) AS n_orders
    FROM resellers r
    JOIN orders o ON r.reseller_id = o.reseller_id
    GROUP BY r.region
    ORDER BY total_revenue DESC
""")
rows2 = cur.fetchall()
with open(os.path.join(OUTPUT_DIR, "region_revenue.csv"), "w", newline="") as f:
  w = csv.writer(f)
  w.writerow(["region", "total_revenue", "n_orders"])
  for r in rows2:
    w.writerow([r["region"], f"{r['total_revenue']:.2f}", r["n_orders"]])

# Query 3: Top resellers spend > 50000
cur.execute("""
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
    LIMIT 5
""")
rows3 = cur.fetchall()
with open(
    os.path.join(OUTPUT_DIR, "top_resellers_spend.csv"), "w", newline=""
) as f:
  w = csv.writer(f)
  w.writerow(["reseller_id", "reseller_name", "region", "total_spend"])
  for r in rows3:
    w.writerow([
        r["reseller_id"],
        r["reseller_name"],
        r["region"],
        f"{r['total_spend']:.2f}",
    ])

# Query 4a: Zero-order resellers
cur.execute("""
    SELECT r.reseller_id, r.reseller_name, r.region, r.city
    FROM resellers r
    LEFT JOIN orders o ON r.reseller_id = o.reseller_id
    WHERE o.order_id IS NULL
""")
rows4a = cur.fetchall()
with open(
    os.path.join(OUTPUT_DIR, "zero_order_resellers.csv"), "w", newline=""
) as f:
  w = csv.writer(f)
  w.writerow(["reseller_id", "reseller_name", "region", "city"])
  for r in rows4a:
    w.writerow([r["reseller_id"], r["reseller_name"], r["region"], r["city"]])

# Query 4b: COUNT(*) vs COUNT(order_id)
cur.execute("""
    SELECT 
        r.reseller_id,
        r.reseller_name,
        COUNT(*) AS count_star,
        COUNT(o.order_id) AS count_order_id
    FROM resellers r
    LEFT JOIN orders o ON r.reseller_id = o.reseller_id
    WHERE r.reseller_id = 'RS024'
    GROUP BY r.reseller_id, r.reseller_name
""")
rows4b = cur.fetchall()
with open(
    os.path.join(OUTPUT_DIR, "zero_order_count_check.csv"), "w", newline=""
) as f:
  w = csv.writer(f)
  w.writerow(["reseller_id", "reseller_name", "count_star", "count_order_id"])
  for r in rows4b:
    w.writerow([
        r["reseller_id"],
        r["reseller_name"],
        r["count_star"],
        r["count_order_id"],
    ])

# Query 5: June Delivered AOV
cur.execute("""
    SELECT ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS june_delivered_aov
    FROM orders
    WHERE month = 'June' AND status = 'Delivered'
""")
row5 = cur.fetchone()
with open(
    os.path.join(OUTPUT_DIR, "june_delivered_aov.csv"), "w", newline=""
) as f:
  w = csv.writer(f)
  w.writerow(["june_delivered_aov"])
  w.writerow([f"{row5['june_delivered_aov']:.2f}"])

conn.close()
print("Part 1: Queries successfully executed and output CSV files generated.")