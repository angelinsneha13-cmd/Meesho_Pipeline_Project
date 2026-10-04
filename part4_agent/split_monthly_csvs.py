import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_CSV = os.path.join(BASE_DIR, "..", "part1_sql", "output", "monthly_category_revenue.csv")

# Ensure the source file exists
if not os.path.exists(SOURCE_CSV):
    raise FileNotFoundError(f"Source file not found at: {SOURCE_CSV}")

# Read and group rows by month
monthly_rows = {"April": [], "May": [], "June": []}
fieldnames = ["month", "category", "revenue", "n_orders"]

with open(SOURCE_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        m = row["month"].strip()
        if m in monthly_rows:
            monthly_rows[m].append(row)

# Export individual monthly CSVs into part4_agent/
for month, rows in monthly_rows.items():
    out_file = os.path.join(BASE_DIR, f"{month.lower()}_revenue.csv")
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Created: {out_file} ({len(rows)} categories)")