# BridgeKit On-Chain Usage Analysis

On-chain analysis of BridgeKit usage from launch (Oct 14, 2025) through Mar 3,
2026. The headline question: what's the real platform run-rate after the
December spike?

## Reports

- [**`report.md`**](report.md) — Main report. Investigative arc from raw aggregate numbers down to the organic baseline. Compiled 2026-03-16.
- [**`report.html`**](report.html) — Standalone HTML render of the main report. Image paths rewritten to use `./charts/`.
- [**`revised-phase-analysis.md`**](revised-phase-analysis.md) — Earlier companion piece (2026-03-04) with the raw Phase 1 vs Phase 2 comparison and outlier identification. The main report supersedes this on conclusions but the companion has the detailed phase tables.

## Supporting files

| Path | Description |
|---|---|
| [`charts/`](charts/) | 19 PNGs. `01_` through `10_` are the raw-data exhibits from the earlier draft; `A_` through `I_` are the final-report exhibits including ML separation (PCA, K-means, logistic regression). |
| [`data/bridgekit-full-2026-03-04.csv`](data/bridgekit-full-2026-03-04.csv) | Full dataset: 550 wallet-chain records, 245 unique wallets, ~$34.5M volume. |
| [`data/phase-1.csv`](data/phase-1.csv) | Phase 1 wallets (Oct 14 – Dec 14, 2025). |
| [`data/phase-2.csv`](data/phase-2.csv) | Phase 2 wallets (Dec 15, 2025 – Mar 3, 2026). |

## Headline findings

- **The 74% headline collapse was a whale exit, not user churn.** 15
  event-driven wallets accounted for 82% of Phase 1 volume and vanished after
  December 14 (HyperEVM launch, institutional rebalancing, OKX hot wallet).
- **Organic platform declined 38%** — a real but manageable decline. Chain
  preferences and user tier structure were consistent across both phases.
- **The right recovery target is $107K/day organic run-rate**, not the
  outlier-inflated $490K/day headline.
- **ML cross-validation**: PCA (88.8% variance in 2 PCs), K-means (k=2,
  silhouette 0.47, 100% agreement with the behavioral C1/C2/C3 labels), and
  a 2-feature logistic regression (98% accuracy) independently recover the
  same organic-vs-outlier partition. The separation is structural, not
  marginal.
- **Highest-value next step**: convert the Systematic Operator user type
  into a recurring enterprise relationship. Other growth comes from
  deepening the organic cohort.

## Methodology

Documented as a Claude skill at
`.claude/skills/bridgekit-phase-analysis.md` (in this repo). The skill
captures the investigative arc and the outlier-separation playbook so the
same analysis can be re-run on a fresher data cut.

## Scope note

This report covers **BridgeKit only**. The matching SwapKit on-chain usage
analysis does not exist yet — the [custom-fee](../custom-fee/) report covers
SwapKit usage from a fee-adoption angle, but a parallel "from headline to
organic" treatment for SwapKit has not been written.
