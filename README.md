# Meesho Reseller Growth & Alert Intelligence Pipeline

A modular, reproducible monitoring pipeline built for Meesho's reseller-operations team. It replaces manual spreadsheet checking with:
1. A deterministic SQL aggregation layer answering five standing business questions.
2. A Python growth engine that enforces schema guardrails and evaluates numeric MoM thresholds.
3. An offline, hallucination-free narrative layer with PII masking.
4. An autonomous mock agent orchestrating the entire Intake → Validate → Flag → Cap → Hold-for-Approval workflow.

**Zero External Dependencies & Zero API Keys**: Operates 100% offline using standard Python 3 libraries (`sqlite3`, `csv`, `unittest`, `json`, `os`, `sys`, `random`).

---

## 1. Project Architecture & Workflow Patterns

| Component | Directory | Operational Workflow Pattern | Responsibility |
|---|---|---|---|
| **Part 1** | `part1_sql/` | SQL Business Query Layer | Seeded SQLite database queries computing category revenue, regional revenue, top spenders, zero-order resellers, and June Delivered AOV. |
| **Part 2** | `part2_engine/` | Input Guardrail & Growth Engine | Feed validation (line-numbered error reporting), signed MoM percentage calculation, and ternary boundary classification (`flagged`, `not_flagged`, `escalate_exact_boundary`). |
| **Part 3** | `part3_narrative/` | Prompt Pack & PII Masking | Context-Insight-Implication prompt pack, 4-criterion self-scoring, chart-choice justifications (no images), and reseller ID aliasing (`ALIAS-XX`). |
| **Part 4** | `part4_agent/` | Agentic Workflow & Mock Runner | Orchestrates the 8-step reporting lifecycle: Intake → Validation Guardrail → MoM Evaluation → Magnitude Sort → Top-3 Cap → Suppress Remaining → Staged Human Approval. |

---

## 2. Directory Structure

```text
meesho-pipeline/
├── data/
│   ├── generate_dataset.py
│   ├── resellers.csv
│   ├── orders.csv
│   └── meesho_reseller.db
├── part1_sql/
│   ├── queries.sql
│   ├── run_queries.py
│   └── output/
│       ├── monthly_category_revenue.csv
│       ├── region_revenue.csv
│       ├── top_resellers_spend.csv
│       ├── zero_order_resellers.csv
│       ├── zero_order_count_check.csv
│       ├── june_delivered_aov.csv
│       └── README.md
├── part2_engine/
│   ├── fixtures/
│   │   ├── corrupted_feed.csv
│   │   └── monthly_category_revenue.csv
│   ├── growth_engine.py
│   └── test_growth_engine.py
├── part3_narrative/
│   ├── prompt_pack.md
│   ├── narrative_report.md
│   ├── masking.py
│   └── test_masking.py
├── part4_agent/
│   ├── agent_spec.md
│   ├── split_monthly_csvs.py
│   ├── april_revenue.csv
│   ├── may_revenue.csv
│   ├── june_revenue.csv
│   └── mock_agent_runner.py
└── README.md