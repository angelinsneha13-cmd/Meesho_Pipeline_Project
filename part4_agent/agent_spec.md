# Autonomous Reseller Growth-Monitoring Agent Specification

## 1. Five Core Agent Components
- **Goal**: Keep Meesho category managers informed of any category whose month-on-month revenue moves beyond the 8% threshold, with a human approving every message before it goes out.
- **Tools**:
  - `validate_feed(csv_path)`: Input schema guardrail from Part 2.
  - `mom_growth(previous, current)`: Numeric calculation engine from Part 2.
  - `is_flagged(mom_pct, threshold=8.0)`: Ternary boundary evaluator from Part 2.
  - `draft_template_narrative(...)`: Deterministic offline prompt template-filler from Part 3.
- **Memory / State**: Stores baseline category revenues from the previous month (`dict[str, float]`) to compute growth rates against the active reporting month.
- **Planner**: Ordered sequence of subtasks 1 through 8 (detailed below).
- **Feedback Loop**: Human approval gate represented by `action_taken="drafted_and_held_for_approval"`. No message is ever auto-dispatched to recipients without operator verification.

## 2. Guardrails
- **Input Guardrail**: `validate_feed` must pass with `(True, [])` before any analytical operations execute. Any malformed row, negative revenue, or missing column produces an immediate Hard Stop.
- **Action Guardrail**: The runner cannot send emails or external messages; drafts are created and strictly held for review.
- **Output Guardrail**: Every numeric figure rendered inside a drafted notification originates directly from verified SQL or deterministic math calculations. No figures are hallucinated.

## 3. Stopping Conditions
- **Success Stopping Condition**: Output feed validated, MoM computed, flagged items prioritized, drafts generated for up to top 3 categories, remainder logged as suppressed, and JSON state emitted.
- **Error Stopping Condition (Hard Stop)**: Input feed validation failure halts pipeline execution immediately with detailed line-numbered errors surfaced.

## 4. Agent Given-When-Then Specifications
1. **Spec 1 (High Growth Flag)**:
   - GIVEN April->May Ethnic Wear revenue moves from 104520.77 to 185107.61,
   - WHEN the agent evaluates the monthly feed,
   - THEN mom_growth computes 77.1%, is_flagged marks it as "flagged", and a message is drafted.
2. **Spec 2 (Sub-Threshold Inactive)**:
   - GIVEN May->June Beauty & Personal Care moves from 35542.11 to 37559.07,
   - WHEN evaluated,
   - THEN mom_growth computes 5.67%, is_flagged marks it as "not_flagged", and it is omitted from both flagged and suppressed lists.
3. **Spec 3 (Boundary Escalation)**:
   - GIVEN a category with previous=100000.0 and current=108000.0,
   - WHEN evaluated,
   - THEN is_flagged marks it as "escalate_exact_boundary", and it is appended to `escalated_categories` without automated drafting.
4. **Spec 4 (Corrupted Input Hard Stop)**:
   - GIVEN a corrupted feed fixture containing missing headers or negative revenues,
   - WHEN the agent executes `run()`,
   - THEN `validation_status` is "invalid", `action_taken` is "hard_stop", validation errors are surfaced, and zero analytical drafts are generated.