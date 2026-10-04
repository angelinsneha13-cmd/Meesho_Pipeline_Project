# Reusable Category Growth Narrative Prompt Pack

## 1. Trigger
This prompt is automatically triggered whenever a category's Month-on-Month growth calculation results in `is_flagged(mom_pct) == "flagged"` (i.e., $\vert{}MoM\%\vert{} > 8.0\%$).

## 2. Input List
The template requires the following validated inputs:
- `{category}`: The specific product category name (e.g., Ethnic Wear, Western Wear).
- `{month}`: Current reporting month (e.g., May, June).
- `{prev_month}`: Baseline prior month (e.g., April, May).
- `{previous_revenue}`: Verified revenue from previous month rounded to 2 decimals.
- `{current_revenue}`: Verified revenue from current month rounded to 2 decimals.
- `{mom_pct}`: Calculated Month-on-Month percentage growth formatted to 2 decimals.

## 3. Prompt Template
```text
You are an executive operations analyst for Meesho's reseller-operations team.
Draft a concise, stakeholder-ready category update using strictly the verified inputs below:

INPUT VARIABLES:
- Category: {category}
- Comparison Window: {month} vs. {prev_month}
- Previous Revenue: INR {previous_revenue}
- Current Revenue: INR {current_revenue}
- Month-on-Month Growth: {mom_pct}%

INSTRUCTIONS:
Structure the briefing into three distinct, explicit sections:
1. Context: State the category being evaluated and the exact comparison timeframe ({month} vs. {prev_month}).
2. Insight: Report the baseline revenue, current revenue, and calculated MoM percentage. Label these figures explicitly as verified facts. Never invent, extrapolate, or modify any numbers.
3. Implication: Provide a concrete, actionable operational next step for regional category managers. If suggesting reasons or market drivers for this change, label them explicitly as hypotheses that require on-the-ground operational verification.