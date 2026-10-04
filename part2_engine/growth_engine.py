import csv
import os


def mom_growth(previous: float, current: float) -> float:
  """Calculates Month-on-Month growth percentage rounded to 2 decimal places."""
  if previous == 0:
    raise ValueError("Previous revenue cannot be zero for MoM calculation.")
  return round(((current - previous) / previous) * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
  """Evaluates whether MoM percentage exceeds, is below, or sits on threshold boundary."""
  magnitude = abs(mom_pct)
  if magnitude > threshold:
    return "flagged"
  elif magnitude < threshold:
    return "not_flagged"
  else:
    return "escalate_exact_boundary"


def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
  """Input guardrail validating month,category,revenue,n_orders CSV schema and row validity."""
  if not os.path.exists(csv_path):
    return False, [f"File not found: {csv_path}"]

  errors = []
  with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    try:
      header = next(reader)
    except StopIteration:
      return False, ["File is empty"]

    expected_cols = ["month", "category", "revenue", "n_orders"]
    clean_header = [c.strip() for c in header]
    if clean_header != expected_cols:
      return False, [
          f"Invalid header structure. Expected {expected_cols}, got"
          f" {clean_header}"
      ]

    for line_idx, row in enumerate(
        reader, start=2
    ):  # line 2 onward, 1-indexed
      if not row or all(c.strip() == "" for c in row):
        continue

      month = row[0].strip() if len(row) > 0 else ""
      category = row[1].strip() if len(row) > 1 else ""
      revenue_str = row[2].strip() if len(row) > 2 else ""

      # Check 1: Missing category
      if not category:
        errors.append(f"line {line_idx}: missing category (month={month})")
        continue

      # Check 2: Missing revenue
      if not revenue_str:
        errors.append(f"line {line_idx}: missing revenue (category={category})")
        continue

      # Check 3: Non-numeric revenue
      try:
        rev_val = float(revenue_str)
      except ValueError:
        errors.append(
            f"line {line_idx}: revenue not numeric: {revenue_str!r}"
        )
        continue

      # Check 4: Negative revenue
      if rev_val < 0:
        errors.append(
            f"line {line_idx}: negative revenue ({rev_val}) for"
            f" category={category}"
        )

  is_valid = len(errors) == 0
  return is_valid, errors