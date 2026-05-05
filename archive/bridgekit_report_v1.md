# Bridge Kit Custom Fee Feature — Usage Report
**Data source**: `birdgekit20260505_013439.csv`
**Generated**: 2026-05-05
**Total transactions in dataset**: 491 across 11 source chains, spanning 2025-10 to 2026-05

---

## 1. Feature Adoption

| Segment | Transactions | Share |
|---|---|---|
| Used custom fee (Circle collected fee > 0) | 19 | 3.9% |
| Did not use custom fee (fee = 0) | 472 | 96.1% |
| **Total** | **491** | |

**Custom fee adoption is very low: only 19 of 491 transactions (3.9%) carry a developer fee.** This is a stark contrast to the swap dataset where 91.9% of wallets had fees configured. The bridge feature either has fewer developers enabled for custom fees, or most are still using the default zero-fee configuration.

---

## 2. Fee Levels Used

Bridge Kit fees are **flat per-transaction amounts in USDC**, not percentage-of-volume rates (unlike swap). Circle collects 10% and the developer collects 90%.

| Fee Total (USDC) | Circle Gets | Dev Gets | # Transactions | Notes |
|---|---|---|---|---|
| 0.0001 | 0.00001 | 0.00009 | 7 | Minimum/test level |
| 0.0100 | 0.00100 | 0.00900 | 2 | |
| 0.0200 | 0.00200 | 0.01800 | 6 | Most common by fee value |
| 0.0300 | 0.00300 | 0.02700 | 2 | |
| 0.0500 | 0.00500 | 0.04500 | 1 | |
| 0.6900 | 0.06900 | 0.62100 | 1 | Outlier — 34.5% of tx amount |

**The most frequently used fee levels are 0.0001 USDC (7 txns) and 0.02 USDC (6 txns).** These are both very small flat fees suggesting developers are testing the feature rather than deploying it at production scale.

### Effective fee rates (fee / source amount)

Because fees are flat, the effective rate varies wildly with transaction size:

| Effective Rate | # Transactions | Context |
|---|---|---|
| 0.005–1.0% | 7 | Normal-sized transactions (0.25–3 USDC bridged) |
| ~1.0% | 8 | SOL->ETH small test transactions ($0.01 bridged) |
| 4–5% | 2 | Mid-sized with flat fee |
| 10% | 2 | Micro-transactions ($0.001 bridged) |
| 34.5% | 1 | ARB->MONAD outlier — likely a test or misconfiguration |
| 200% | 4 | SOL->BASE: $0.01 bridged with $0.02 fee — clearly test transactions |

**The 200% rate cases and the 34.5% case are test transactions**, not production usage. The $0.01 volumes with $0.02 fees indicate developers probing fee behavior at minimum amounts.

---

## 3. When Was the Feature Used

| Month | Total Txns | Fee-Bearing Txns | Adoption Rate |
|---|---|---|---|
| 2025-10 | 22 | 1 | 4.5% |
| 2025-11 | 80 | 9 | 11.3% |
| 2025-12 | 34 | 0 | 0% |
| 2026-01 | 191 | 5 | 2.6% |
| 2026-02 | 88 | 1 | 1.1% |
| 2026-03 | 37 | 3 | 8.1% |
| 2026-04 | 38 | 0 | 0% |
| 2026-05 | 1 | 0 | — |

November 2025 had the highest both in absolute count (9 fee txns) and adoption rate (11.3%), coinciding with the SOL->BASE cluster. Usage has been intermittent since then with no sustained adoption pattern.

---

## 4. Chain Pairs for Fee-Bearing Transactions

| Route | Transactions | Notes |
|---|---|---|
| SOL -> BASE | 8 | Dominant — all Nov 2025, likely one developer |
| SOL -> ETH | 5 | Jan 2026 cluster |
| ARB -> MONAD | 1 | Outlier with $0.69 fee |
| BASE -> EDGE | 1 | |
| BASE -> POLYGON | 1 | |
| BASE -> ARB | 1 | |
| SOL -> MORPH | 1 | |
| SOL -> EDGE | 1 | |

SOL as source accounts for 14 of 19 fee transactions (74%). The SOL->BASE cluster in November likely represents a single developer testing custom fees on Solana bridges.

---

## 5. Circle Fee Collections Summary

| Metric | Value |
|---|---|
| Total Circle fees collected | **0.09407 USDC** |
| Total developer fees collected | **0.84664 USDC** |
| Total bridge fees generated | **0.94071 USDC** |
| Total transaction volume (all txns) | **1,748.10 USDC** |
| Volume on fee-bearing txns only | **15.34 USDC (0.9% of total)** |
| Largest single-tx Circle fee | **0.06900 USDC** (ARB->MONAD, 73% of total) |

Circle's total collection of **$0.094 USDC** is negligible. One transaction (ARB->MONAD, $0.69 total fee) accounts for 73% of it.

---

## 6. Comparison: Bridge vs Swap Custom Fee Usage

| Metric | Swap (`appkitusage`) | Bridge (`birdgekit`) |
|---|---|---|
| Data granularity | Per wallet | Per transaction |
| Total records | 2,343 wallets | 491 transactions |
| Fee adoption | 91.9% | 3.9% |
| Fee structure | % of volume (bps) | Flat USDC per txn |
| Most common fee level | 20–30 bps | 0.0001–0.02 USDC flat |
| Circle fees collected | **$301.42** | **$0.094** |
| Total volume | $2,312,568 | $1,748 |
| Signals | Arc Testnet at scale | Early / test-only usage |

---

## 7. Summary Answers

| Question | Answer |
|---|---|
| How many transactions used the custom fee feature? | **19 of 491 (3.9%)** — very limited adoption |
| What is the most common fee level? | **0.0001 USDC** (7 txns) and **0.02 USDC** (6 txns) — both flat amounts, likely test-level |
| How much did Circle collect? | **0.09407 USDC total** — one transaction accounts for 73% of it |
| Overall signal | Bridge custom fee feature is in early/testing stage; no production-scale adoption observed in this dataset |
