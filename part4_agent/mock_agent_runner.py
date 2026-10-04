import csv
import json
import os
import sys

# Connect Part 2 engine directly without duplicating code
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "part2_engine"))
)
from growth_engine import is_flagged, mom_growth, validate_feed


def load_category_revenues(csv_path: str, target_month: str) -> dict[str, float]:
  """Extracts {category: revenue} mapping for a specific month from validated CSV."""
  revenues = {}
  with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
      if row["month"].strip() == target_month:
        revenues[row["category"].strip()] = float(row["revenue"].strip())
  return revenues


def draft_template_narrative(
    category: str,
    month: str,
    prev_month: str,
    prev_rev: float,
    curr_rev: float,
    mom_pct: float,
) -> str:
  """Part 3 deterministic offline template filler (zero external APIs)."""
  sign = "+" if mom_pct > 0 else ""
  return (
      f"Context: Performance update for {category} during {month} vs."
      f" {prev_month}.\n"
      f"Insight (Fact): Revenue moved from INR {prev_rev:.2f} to INR"
      f" {curr_rev:.2f}, recording a Month-on-Month shift of {sign}{mom_pct:.2f}%.\n"
      f"Implication (Operational): Category leads should review inventory"
      f" allocations and supplier fulfillment in response to this"
      f" {sign}{mom_pct:.2f}% movement."
  )


def run(
    run_month: str,
    prev_month: str,
    previous_month_csv: str,
    current_month_csv: str,
) -> dict:
  """Executes subtasks 1-8 of the reseller growth-monitoring workflow."""
  # Subtasks 1 & 2: Validate input feed; if invalid, trigger Hard Stop
  is_valid, errors = validate_feed(current_month_csv)
  if not is_valid:
    return {
        "run_month": run_month,
        "validation_status": "invalid",
        "validation_errors": errors,
        "flagged_categories": [],
        "suppressed_categories": [],
        "escalated_categories": [],
        "action_taken": "hard_stop",
    }

  # Subtask 3: Compute MoM growth for each category against previous month
  prev_data = load_category_revenues(previous_month_csv, prev_month)
  curr_data = load_category_revenues(current_month_csv, run_month)

  computed = []
  escalated_categories = []

  # Subtask 4: Run is_flagged on every category
  for cat, curr_rev in curr_data.items():
    if cat not in prev_data:
      continue
    prev_rev = prev_data[cat]
    growth = mom_growth(prev_rev, curr_rev)
    status = is_flagged(growth)

    # Subtask 7b: Exact boundary escalation
    if status == "escalate_exact_boundary":
      escalated_categories.append(cat)
    elif status == "flagged":
      computed.append({
          "category": cat,
          "mom_pct": growth,
          "previous_revenue": prev_rev,
          "current_revenue": curr_rev,
          "abs_mom": abs(growth),
      })

  # Subtask 5: Sort flagged categories by abs(mom_pct) descending
  computed.sort(key=lambda x: x["abs_mom"], reverse=True)

  # Subtasks 6 & 7: Draft top 3 by magnitude, suppress the rest
  flagged_categories = []
  suppressed_categories = []

  for idx, item in enumerate(computed):
    if idx < 3:
      msg = draft_template_narrative(
          category=item["category"],
          month=run_month,
          prev_month=prev_month,
          prev_rev=item["previous_revenue"],
          curr_rev=item["current_revenue"],
          mom_pct=item["mom_pct"],
      )
      flagged_categories.append({
          "category": item["category"],
          "mom_pct": item["mom_pct"],
          "previous_revenue": item["previous_revenue"],
          "current_revenue": item["current_revenue"],
          "drafted": True,
          "message": msg,
      })
    else:
      suppressed_categories.append(item["category"])

  # Subtask 8: Emit structured JSON object
  return {
      "run_month": run_month,
      "validation_status": "valid",
      "validation_errors": [],
      "flagged_categories": flagged_categories,
      "suppressed_categories": suppressed_categories,
      "escalated_categories": escalated_categories,
      "action_taken": "drafted_and_held_for_approval",
  }


if __name__ == "__main__":
  base = os.path.dirname(os.path.abspath(__file__))
  feed_csv = os.path.join(
      base, "..", "part1_sql", "output", "monthly_category_revenue.csv"
  )
  corrupted_csv = os.path.join(
      base, "..", "part2_engine", "fixtures", "corrupted_feed.csv"
  )

  print("\n================ MAY SCENARIO (April -> May) ================")
  may_res = run("May", "April", feed_csv, feed_csv)
  print(json.dumps(may_res, indent=2))

  print("\n================ JUNE SCENARIO (May -> June) ================")
  june_res = run("June", "May", feed_csv, feed_csv)
  print(json.dumps(june_res, indent=2))

  print("\n================ CORRUPTED FEED SCENARIO ================")
  bad_res = run("July", "June", feed_csv, corrupted_csv)
  print(json.dumps(bad_res, indent=2))