# Swap Kit Custom Fee Feature — Usage Report
**Data source**: `appkit_txn_20260505_014246.csv` (transaction-level)
**Generated**: 2026-05-05
**Total transactions**: 10,000 — 9,970 testnet (arc_testnet), 30 mainnet (base, arbitrum, ethereum, solana)

---

## 1. Feature Adoption

### Testnet (arc_testnet)

| Segment | Transactions | Share |
|---|---|---|
| Used custom fee (Circle fee > $0) | 6,030 | 60.5% |
| No custom fee (Circle fee = $0) | 3,940 | 39.5% |
| **Total testnet** | **9,970** | |

### Mainnet (base, arbitrum, ethereum, solana)

| Segment | Transactions | Share |
|---|---|---|
| Used custom fee (Circle fee > $0) | 0 | 0% |
| No custom fee | 30 | 100% |
| **Total mainnet** | **30** | |

**No developer has configured custom fees on swap for mainnet.** All 30 mainnet transactions show zero Circle fees collected.

---

## 2. Fee Level Distribution (Testnet)

Fee rates back-calculated as: `dev_fee_rate = Circle Fee / (Volume × 10%)`

| Fee Tier | Transactions | Volume | Circle Fee | Dev Fee | Notes |
|---|---|---|---|---|---|
| <2 bps (<0.02%) | 3,759 | $13,241 | $0.26 | $2.63 | Noise / rounding artifacts |
| 2–10 bps (0.02–0.10%) | 1,629 | $96,331 | $1.93 | $19.27 | Likely default config |
| 10–20 bps (0.10–0.20%) | 10 | $20,952 | $2.31 | $23.09 | |
| 40–50 bps (0.40–0.50%) | 5 | $0.08 | $0.00 | $0.00 | Micro-transactions |
| **50+ bps (>0.50%)** | **627** | **$269,637** | **$138.90** | **$1,389.04** | **Active fee configurers** |
| Zero-fee txns | 3,935 | — | $0 | $0 | No fee set |

The data clusters into two meaningful groups:

**Cluster A — ~2 bps (5,388 txns)**: Mostly noise or a very low default rate applied automatically. Generates only $2.19 in Circle fees despite large transaction count.

**Cluster B — ~51–52 bps (627 txns)**: The real custom fee users. Generates $138.90 in Circle fees — **96.8% of all testnet fees** — from $269,637 in volume.

### Fee rate percentiles (testnet fee-bearing txns)

| Percentile | Fee Rate |
|---|---|
| P50 | 2.0 bps |
| P75 | 2.0 bps |
| P90 | 51.5 bps |
| P95 | 51.5 bps |
| P99 | 51.5 bps |

The sharp jump from P75 (2 bps) to P90 (51.5 bps) confirms the bimodal distribution — there is no gradual spread of fee levels.

---

## 3. Circle Fee Collections Summary

### Testnet

| Metric | Value |
|---|---|
| Total Circle fees collected | **$143.40** |
| Implied total developer fees | **$1,434.04** |
| Total transaction volume | **$1,683,696** |
| Fees from 50+ bps cluster only | **$138.90 (96.8%)** |
| Volume in 50+ bps cluster | $269,637 (16% of total) |

### Mainnet

| Metric | Value |
|---|---|
| Total Circle fees collected | **$0.00** |
| Total transaction volume | **$34.15** |
| Unique wallets | 5 |

---

## 4. Summary Answers

| Question | Answer |
|---|---|
| How many transactions used the custom fee feature? | **6,030 testnet (60.5%); 0 mainnet** |
| What is the most common fee level? | **~51–52 bps** among active configurers (627 txns); the broader dataset has a 2 bps cluster but this is noise/defaults |
| How much did Circle collect? | **$143.40 testnet; $0 mainnet** — 96.8% from the 51–52 bps tier alone |
