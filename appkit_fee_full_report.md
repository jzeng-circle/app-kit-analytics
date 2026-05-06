# App Kit Custom Fee Feature — Full Report
**Generated**: 2026-05-06
**Sources**: `data/swap_mainnet_txns.csv` · `data/swap_testnet_txns.csv` · `data/bridge_mainnet_txns.csv` (wallet-enriched) · `data/bridge_testnet_txns.csv`

| Dataset | Date Range | Note |
|---|---|---|
| Swap — Testnet | unknown | arc_testnet has no public RPC; timestamp not in data |
| Swap — Mainnet | 2026-03-13 → 2026-05-05 | Resolved from on-chain block timestamps (ETH/BASE/ARB/SOL) |
| Bridge — Testnet | 2026-02-18 → 2026-05-05 | Resolved from on-chain block timestamps (arbitrum_sepolia, polygon_amoy) |
| Bridge — Mainnet | 2025-10-30 → 2026-05-03 | From block_timestamp column in source data |

---

## Executive Summary

| | Swap — Testnet | Swap — Mainnet | Bridge — Testnet | Bridge — Mainnet |
|---|---|---|---|---|
| Transactions | 9,976 | 56 | 1,000 | 10,000 |
| Unique wallets | 1,820 | 22 | 207 | 466 (88% resolved) |
| Fee adoption | 60.0% | ~0% | 8.8% | 10.8% |
| Total volume | $603,301 | $65.80 | $52,765 | $72.3M |
| Circle fees collected | **$147.71** | **~$0** | **$0.31** | **$83.72** |
| Developer fees collected | **$1,477** | **~$0** | **$2.79** | **$753** |
| Revenue concentration | ~51 bps tier: 253 wallets, 97.4% of fees | — | Top 1 wallet: 35% of fees | Top 1 wallet: 37% of fees |

**Fee adoption**: Swap testnet has broad adoption (60.0%, 1,820 wallets) with the ~51 bps tier generating 97.4% of Circle fees despite being only 6.6% of transactions. Bridge mainnet has lower adoption (10.8%) but operates at production scale ($72.3M volume); swap mainnet has negligible fee adoption.

**Revenue concentration**: In every fee-bearing environment, a small number of wallets account for the majority of Circle fees — the ~51 bps tier (253 wallets) on swap testnet, and the top 1 wallet (37%) on bridge mainnet. Fee revenue is not evenly distributed across the developer base.

**Bridge revenue driver**: On bridge mainnet, the >$1.0 flat fee tier — just 0.8% of all transactions — generates 92% of Circle fees ($76.99 of $83.72), all from large-volume bridges averaging $181K per transaction. The remaining fee tiers collectively contribute less than 8%.

**Staging gap**: Both products show a testnet-to-mainnet gap. Swap has an established testnet presence but no mainnet fee adoption. Bridge has mainnet production traffic but testnet usage is still small. Neither product has simultaneous scale on both environments.

---

## Swap Kit

*Transactions are clustered by effective fee rate in basis points (bps); this produces the clearest separation in the swap data, though it is not conclusive about how developers configure fees.*

### Testnet (arc_testnet) — 9,976 transactions

*1,820 unique wallets. 437 wallets appear in more than one cluster, meaning the same developer used different fee rates across transactions.*

| Cluster | Txns | % Txns | Wallets | % Wallets | Avg Txns/Wallet | Avg Vol/Txn | Avg Fee/Txn | Avg Bps | Volume | Circle Fee |
|---|---|---|---|---|---|---|---|---|---|---|
| No fee | 3,990 | 40.0% | 512 | 28.1% | 7.8 | $66.00 | $0 | — | $263,337 | $0 |
| ~1 bps | 154 | 1.5% | 145 | 8.0% | 1.1 | $0.08 | $0.000004 | 1.1 | $13 | $0.00 |
| ~2 bps | 5,166 | 51.8% | 1,364 | 74.9% | 3.8 | $6.20 | $0.000124 | 2.0 | $32,025 | $0.64 |
| ~10 bps | 9 | 0.1% | 2 | 0.1% | 4.5 | $3,170.79 | $0.349492 | 11.0 | $28,537 | $3.15 |
| ~51 bps | 657 | 6.6% | 253 | 13.9% | 2.6 | $425.25 | $0.219068 | 51.4 | $279,388 | $143.93 |
| **Total** | **9,976** | **100%** | **1,820** | | | | | | **$603,301** | **$147.71** |

- **No fee (40.0% of txns)**: Largest cluster by transaction count. Highest avg txns/wallet (7.8) and largest avg transaction size ($66.00). 512 wallets, no fees collected.
- **~2 bps (51.8% of txns)**: Dominant fee cluster by transaction count. 5,166 transactions across 1,364 wallets (74.9% of all wallets). Avg transaction size $6.20, avg fee $0.000124/txn. Generates $0.64 Circle fees.
- **~51 bps (6.6% of txns)**: 657 transactions across 253 wallets. Avg transaction size $425.25, avg fee $0.22/txn. Generates 97.4% of all testnet Circle swap fees ($143.93 of $147.71).
- **~10 bps (0.1% of txns)**: 9 transactions across 2 wallets. Highest avg transaction size ($3,170.79) of any fee-paying cluster.
- **~1 bps (1.5% of txns)**: 154 transactions across 145 wallets. Smallest avg transaction size ($0.08) and negligible fee ($0.000004/txn). Generates essentially $0 Circle fees.

| Total Circle fees | **$147.71** | Total developer fees | **$1,477.13** | Total volume | **$603,301** |
|---|---|---|---|---|---|

---

### Mainnet (base, arbitrum, ethereum, solana) — 56 transactions · 2026-03-13 to 2026-05-05

56 transactions across 22 wallets, total volume $65.80. 2 transactions carry a fee of $0.00000001 each — negligibly small, effectively zero. No developer has configured meaningful custom fees on swap for mainnet.

---

## Bridge Kit

*Transactions are clustered by absolute fee amount per transaction; within each fee tier the fee value has low variance while effective bps varies widely, making flat fee the cleaner lens for bridge data, though this is not conclusive.*

### Testnet (arbitrum_sepolia, polygon_amoy) — 1,000 transactions · 2026-02-18 to 2026-05-05

*207 unique wallets. Wallet addresses are included directly in the testnet dataset. Wallets can appear in multiple fee tiers.*

| Cluster | Txns | % Txns | Wallets | % Wallets | Avg Txns/Wallet | Avg Amt/Txn | Avg Fee/Txn | Volume | Circle Fee |
|---|---|---|---|---|---|---|---|---|---|
| No fee | 912 | 91.2% | 182 | 87.9% | 5.0 | $53.71 | $0 | $48,986 | $0 |
| ≤$0.0005 | 7 | 0.7% | 4 | 1.9% | 1.8 | $2.86 | $0.00014 | $20 | $0.0001 |
| $0.001–$0.002 | 3 | 0.3% | 3 | 1.4% | 1.0 | $3.73 | $0.00085 | $11 | $0.0003 |
| $0.003–$0.006 | 9 | 0.9% | 2 | 1.0% | 4.5 | $0.56 | $0.00500 | $5 | $0.0045 |
| ~$0.01 | 46 | 4.6% | 24 | 11.6% | 1.9 | $14.99 | $0.01000 | $689 | $0.0460 |
| ~$0.05 | 18 | 1.8% | 4 | 1.9% | 4.5 | $162.10 | $0.04972 | $2,918 | $0.0895 |
| ~$0.10 | 3 | 0.3% | 1 | 0.5% | 3.0 | $10.00 | $0.10000 | $30 | $0.0300 |
| ~$0.30 | 1 | 0.1% | 1 | 0.5% | 1.0 | $99.70 | $0.30000 | $100 | $0.0300 |
| >$1.0 | 1 | 0.1% | 1 | 0.5% | 1.0 | $5.00 | $1.10000 | $5 | $0.1100 |
| **Total** | **1,000** | **100%** | **207** | | | | | **$52,765** | **$0.310** |

- **No fee (91.2% of txns)**: Dominant cluster. 912 transactions, avg amount $53.71. 182 wallets.
- **~$0.01 (4.6% of txns)**: Largest fee-paying cluster by transaction count. 46 transactions across 24 wallets (11.6% of all wallets). Avg transaction size $14.99. Generates 14.8% of Circle fees.
- **~$0.05 (1.8% of txns)**: 18 transactions across 4 wallets. Largest avg transaction size among fee clusters ($162.10). Generates 28.8% of Circle fees.
- **$0.003–$0.006 (0.9% of txns)**: 9 transactions, 2 wallets, avg transaction size $0.56 — smallest volume of any fee cluster.
- **≤$0.0005 (0.7% of txns)**: 7 transactions, 4 wallets. Very small fees ($0.00014/txn avg) and very small transaction sizes ($2.86 avg).
- **~$0.10 / ~$0.30 / >$1.0**: 5 transactions combined (3 wallets). Single >$1.0 transaction generates 35.4% of all testnet bridge Circle fees.

**Revenue concentration**: top 1 wallet = 35.4% of Circle fees, top 3 = 60.3%, top 5 = 81.0%.

| Total Circle fees | **$0.310** | Total developer fees | **$2.793** | Total volume | **$52,765** | Fee-paying wallets | **37** |
|---|---|---|---|---|---|---|---|

---

### Mainnet (11 chains) — 10,000 transactions · 2025-10-30 to 2026-05-03

*Wallet addresses fetched on-chain. Coverage: 950/1,080 fee-bearing txns (88%). Unresolved: SOL 105, CODEX 13, PLUME 8, SEI 4 — no reliable public RPC available for these chains. Wallet counts reflect resolved txns only.*

| Cluster | Txns | % Txns | Wallets† | Avg Txns/Wallet | Avg Amt/Txn | Avg Fee/Txn | Volume | Circle Fee |
|---|---|---|---|---|---|---|---|---|
| No fee | 8,920 | 89.2% | n/a | — | $6,366 | $0 | $56,785,517 | $0 |
| Dust (<$0.0001) | 160 | 1.6% | 122 | 1.3 | $0.26 | $0.00001 | $41 | $0.0002 |
| $0.0001–$0.0005 | 233 | 2.3% | 113 | 2.1 | $3.50 | $0.00019 | $816 | $0.0044 |
| $0.001–$0.002 | 132 | 1.3% | 55 | 2.4 | $12.48 | $0.00102 | $1,647 | $0.0135 |
| $0.003–$0.006 | 102 | 1.0% | 76 | 1.3 | $68.89 | $0.00395 | $7,026 | $0.0403 |
| ~$0.01 | 89 | 0.9% | 33 | 2.7 | $106.92 | $0.01011 | $9,516 | $0.0900 |
| ~$0.02 | 79 | 0.8% | 25 | 3.2 | $210.43 | $0.02236 | $16,624 | $0.1767 |
| ~$0.05 | 57 | 0.6% | 38 | 1.5 | $870.27 | $0.04797 | $49,605 | $0.2734 |
| ~$0.10 | 33 | 0.3% | 23 | 1.4 | $2,473.29 | $0.10574 | $81,618 | $0.3490 |
| $0.25–$0.60 | 70 | 0.7% | 49 | 1.4 | $6,751.82 | $0.35724 | $472,628 | $2.5007 |
| $0.69–$1.0 | 44 | 0.4% | 16 | 2.8 | $5,202.21 | $0.74626 | $228,897 | $3.2836 |
| **>$1.0** | **81** | **0.8%** | **62** | **1.3** | **$181,305.75** | **$9.50442** | **$14,685,766** | **$76.9857** |
| **Total** | **10,000** | **100%** | **466** | | | | **$72,339,701** | **$83.72** |

*†Wallet counts per tier reflect resolved wallets only. Wallets can appear in multiple fee tiers.*

- **No fee (89.2% of txns)**: 8,920 transactions, $56.8M in volume, no fees collected.
- **Dust to $0.006 (6.2% of txns)**: 627 transactions across the four smallest fee tiers. Transaction sizes are very small (avg $0.26–$68.89). Combined Circle fees $0.054 — less than 0.1% of total.
- **~$0.01 to ~$0.10 (2.6% of txns)**: 258 transactions. Transaction sizes grow steadily from $107 (~$0.01 tier) to $2,473 (~$0.10 tier). Combined Circle fees $0.90 (1.1% of total).
- **$0.25–$1.0 (1.1% of txns)**: 114 transactions across 65 wallets. Avg transaction size $5,202–$6,752. Combined Circle fees $5.78 (6.9% of total).
- **>$1.0 (0.8% of txns)**: 81 transactions, avg fee $9.50/txn, avg transaction size $181,306. Generates **92.0% of all mainnet bridge Circle fees** ($76.99 of $83.72). Most common discrete fee values: $1.25, $1.69 (≈$0.69×2.44), $5.00, $50.00, $100.00. Revenue is highly concentrated: top 1 wallet = 37.0% of Circle fees ($31.00), top 5 = 56.9%, top 10 = 72.1%.

### Monthly Trend (Mainnet)

| Month | Txns | Fee-Bearing | Fee Rate | Circle Fee |
|---|---|---|---|---|
| 2025-10 | 39 | 0 | 0% | $0 |
| 2025-11 | 721 | 129 | 17.9% | $2.34 |
| 2025-12 | 799 | 1 | 0.1% | $0 |
| 2026-01 | 685 | 21 | 3.1% | $0.04 |
| 2026-02 | 637 | 16 | 2.5% | $0.03 |
| 2026-03 | 2,201 | 92 | 4.2% | $1.75 |
| 2026-04 | 4,560 | 754 | 16.5% | $46.43 |
| 2026-05 | 358 | 67 | 18.7% | $33.11 |

Fee adoption dropped to near zero in Dec 2025 after an initial peak in Nov 2025, then recovered from Jan–Mar 2026. Apr–May 2026 generated $79.54 of the $83.72 total Circle bridge mainnet fees.

| Total Circle fees | **$83.72** | Total developer fees | **$753.46** | Total volume | **$72,339,701** |
|---|---|---|---|---|---|

---

## Cross-Product Comparison

| | Swap — Testnet | Bridge — Testnet | Swap — Mainnet | Bridge — Mainnet |
|---|---|---|---|---|
| Transactions | 9,976 | 1,000 | 56 | 10,000 |
| Unique wallets | 1,820 | 207 | 22 | 466 |
| Fee adoption | 60.0% | 8.8% | ~0% | 10.8% |
| Dominant fee tier | ~2 bps (txn count); ~51 bps (revenue) | ~$0.01 (by txn count) | — | >$1.0 (by revenue) |
| Avg fee/txn (dominant tier) | $0.22 (~51 bps) | $0.01 | — | $9.50 |
| Total volume | $603,301 | $52,765 | $65.80 | $72.3M |
| Circle fees | **$147.71** | **$0.31** | **~$0** | **$83.72** |
| Developer fees | **$1,477** | **$2.79** | **~$0** | **$753** |
| Revenue concentration | Top tier (253 wallets): 97.4% of fees | Top 1 wallet: 35.4% of fees | — | Top 1 wallet: 37.0% of fees |

Swap has an established testnet presence with 1,820 wallets and $147.71 in Circle fees, but negligible mainnet fee adoption. Bridge is the reverse — $83.72 in mainnet Circle fees on $72.3M volume, with testnet activity still small. Revenue concentration is high in all fee-bearing environments: a small number of wallets account for the majority of Circle fees collected across both products.
