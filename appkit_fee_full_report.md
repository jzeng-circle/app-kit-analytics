# App Kit Custom Fee Feature — Full Report
**Generated**: 2026-05-08
**Sources**: `data/swap_mainnet_txns.csv` · `data/swap_testnet_txns.csv` · `data/bridge_mainnet_txns.csv` · `data/bridge_testnet_txns.csv`

---

## Executive Summary

| | Swap — Testnet | Swap — Mainnet | Bridge — Testnet | Bridge — Mainnet |
|---|---|---|---|---|
| Data | Sample | Full dataset | Sample | Full dataset |
| Date range | 2026-03-13 → 2026-05-05 | 2026-03-13 → 2026-05-05 | n/a (timestamps not in export) | n/a (timestamps not in export) |
| Transactions | 9,976 | 56 | 10,000 | 4,452 |
| Unique wallets | 1,820 | 22 | — | — |
| Fee adoption (txn-level) | 60.0% | ~0% | 1.7% | 18.8% |
| Total volume | $603,301 | $65.80 | $51.8M | $26.9M |
| Circle fees collected | **$147.71** | **~$0** | **$0.61** | **$91.54** |
| Developer fees collected | **$1,477** | **~$0** | **$5.48** | **$823.85** |
| Revenue concentration | ~51 bps tier: 253 wallets, 97.4% of fees | — | — | — |

*Bridge wallet counts are excluded — the address fields in the bridge exports do not reliably identify a unique developer or end-user, so wallet-level statistics for bridge are not accurate.*

*The observations below are deductions from observed transaction data. The report does not have direct visibility into how developers configure fees in their applications, so configuration claims are inferences, not direct evidence.*

### Swap Kit — Key Insights

**Effective fee rates cluster at recognizable bps values.** Observed rates fall into clear bands — ~1, ~2, ~10, and ~51 bps — a pattern consistent with percentage-rate configuration. Clustering by bps gives the cleanest separation in the swap data; whether this reflects how developers actually configure fees is not directly observable from this dataset.

**Adoption is broad on testnet but revenue is concentrated.** Testnet has 60.0% txn-level fee adoption across 1,820 unique wallets. The **~51 bps tier alone (6.6% of txns, 253 wallets) generates 97.4% of Circle fees** ($143.93 of $147.71). The ~2 bps tier dominates by transaction count (51.8%) but contributes only $0.64, because its average transaction size is $6.20.

**Wallets appear in multiple fee-rate clusters.** 437 of 1,820 testnet wallets show up in more than one cluster. This is consistent with the same developer using different rates across transactions, but could also reflect app-level fee logic, A/B tests, or other factors not visible in the data.

**Blended effective Circle rate on testnet is ~2.45 bps** ($147.71 Circle / $603K volume). The Circle:developer share in the observed data is **9.1:90.9** ($147.71 of $1,624.84 total fees).

**Mainnet shows minimal fee activity.** 56 transactions across 22 wallets, $66 total volume, ~$0 in fees — only 2 of 56 transactions carry any fee at all, both at $0.00000001. Whatever has been configured, no meaningful fee revenue is being collected on swap mainnet in this sample.

### Bridge Kit — Key Insights

**Observed fees cluster around discrete dollar values.** In the >$1 mainnet tier, the most common fee values are $1.00, $1.25, $5.00, $50.00, and $100.00 — round dollar figures that appear on widely varying notional sizes. The same $1.00 fee is observed on both a $5 bridge (2,000 bps effective) and a $1.99M bridge (0.005 bps effective). **This pattern is consistent with flat-dollar fee configuration; the underlying configuration mechanism is not directly observable from this data.** Effective bps may therefore be a less meaningful lens for bridge than for swap.

**Mainnet revenue is concentrated in one tier.** The **>$1.0 tier (1.8% of txns, just 78 transactions) generates 95.5% of Circle fees** ($87.38 of $91.54), with average notional of **$221K per transaction**. The remaining 4,374 transactions contribute $4.16 combined.

**ETH is the dominant fee-generating destination.** 64.1% of mainnet Circle fees route to ETH, followed by HYPEREVM (16.1%), BASE (6.1%), and ARB (5.6%). The top four destinations together account for 91.9% of Circle fees.

**Testnet has wide volume reach but minimal fee activity.** $51.8M in testnet volume but only **1.7% txn-level fee adoption** and $0.61 in Circle fees. Most testnet bridges are fee-free; whether this reflects integration testing, unconfigured fees, or other usage patterns cannot be determined from the data alone. Mainnet, by contrast, has 18.8% txn-level fee adoption.

**Effective rate falls as notional grows.** Blended effective Circle rate is **0.034 bps** on $26.9M total volume, or **0.051 bps** on fee-bearing volume only. This is what would be expected under flat-fee behavior, and is consistent with — but not direct evidence of — flat-amount configuration.

**Circle's share of fee revenue is consistently 10%** in the observed data — Circle $91.54 / total $915.39 on mainnet, Circle $0.609 / total $6.091 on testnet. Whether this 10:90 split is a fixed protocol parameter or a configuration default is not determinable from this dataset alone.

---

## Swap Kit

*Transactions are clustered by effective fee rate in basis points (bps); this produces the clearest separation in the swap data. Whether developers configure fees as percentages or by some other mechanism is not directly visible in this dataset, so the clustering is an analytical lens, not direct evidence of configuration.*

### Testnet (arc_testnet) — 9,976 transactions (sample)

*1,820 unique wallets. 437 wallets appear in more than one cluster, consistent with the same developer using different fee rates across transactions, though other explanations (app-level fee logic, A/B tests) cannot be ruled out from the data.*

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

### Mainnet (base, arbitrum, ethereum, solana) — 56 transactions

56 transactions across 22 wallets, total volume $65.80. 2 transactions carry a fee of $0.00000001 each — negligibly small, effectively zero. No meaningful fee revenue is being collected on swap mainnet in this sample; whether this is because no fees are configured or for other reasons is not visible in the data.

---

## Bridge Kit

*Transactions are clustered by absolute fee amount per transaction; within each cluster the fee value has low variance while effective bps varies widely, which is consistent with flat-amount fee structures. This is an observation about the data, not direct evidence of how fees are configured.*

**Observed fee structure**: Bridge fee values in the data cluster around round dollar figures. In the >$1 mainnet tier, the most common observed values are $1.00, $1.25, $5.00, $50.00, and $100.00, appearing on widely varying notional sizes. Circle's share of total fees is exactly **10:90** in every observed fee-bearing transaction (mainnet $91.54 / $915.39 = 10.0%; testnet $0.609 / $6.091 = 10.0%). The underlying developer configuration is not directly visible in this dataset, so these are deductions from observed behavior rather than concrete evidence of how fees are set.

### Testnet (arc_testnet, arbitrum_sepolia, polygon_amoy) — 10,000 transactions (sample)

*Source: `bridgekit_testnet20260508_075520.csv`. Chain mix: arc_testnet 8,533 · arbitrum_sepolia 884 · polygon_amoy 583. Wallet-level statistics are not included for bridge data — the address fields in the bridge export do not reliably identify a unique developer or end-user. Fee tiers below are consolidated into four buckets to ensure each cluster has enough transactions to be statistically meaningful.*

| Cluster | Txns | % Txns | Avg Amt/Txn | Avg Fee/Txn | Volume | Circle Fee | % of Circle Fee |
|---|---|---|---|---|---|---|---|
| No fee | 9,832 | 98.3% | $5,269.57 | $0 | $51,810,446 | $0 | 0.0% |
| Sub-cent (<$0.01) | 32 | 0.3% | $6.38 | $0.00269 | $204 | $0.0086 | 1.4% |
| $0.01–$1.0 | 133 | 1.3% | $33.63 | $0.02184 | $4,473 | $0.2905 | 47.7% |
| >$1.0 | 3 | 0.0% | $1.73 | $1.03333 | $5 | $0.3100 | 50.9% |
| **Total** | **10,000** | **100%** | | | **$51,815,129** | **$0.609** | 100% |

- **No fee (98.3% of txns)**: 9,832 transactions across $51.8M of testnet volume. Testnet fee adoption (1.7%) is much lower than mainnet (18.8%) — what drives this gap (integration testing, unconfigured fees, or other usage patterns) cannot be determined from this data alone.
- **Sub-cent (0.3% of txns)**: 32 transactions on very small notionals (avg $6.38). Combined Circle fees $0.009 — 1.4% of total.
- **$0.01–$1.0 (1.3% of txns)**: 133 transactions, avg amount $33.63, avg fee $0.022/txn. Largest fee-paying tier by transaction count, generating 47.7% of Circle fees.
- **>$1.0 (3 txns)**: Three $1.00–$1.10 fees on $0.10–$5.00 notionals (one arbitrum_sepolia, two polygon_amoy). Together they generate 50.9% of all testnet bridge Circle fees — three outlier transactions account for half the fee revenue at this volume scale.

| Total Circle fees | **$0.609** | Total developer fees | **$5.482** | Total volume | **$51,815,129** |
|---|---|---|---|---|---|

---

### Mainnet (19 destination chains) — 4,452 transactions (full dataset)

*Source: `bridgekit_mainnet20260508_031102.csv`. Wallet-level statistics are not included for bridge data — the address fields in the bridge export do not reliably identify a unique developer or end-user. The export does not include `block_timestamp` or source `blockchain`, so monthly trend and source-chain breakdown are not available for this revision. Fee tiers are consolidated into four buckets to ensure each cluster has enough transactions to be statistically meaningful.*

| Cluster | Txns | % Txns | Avg Amt/Txn | Avg Fee/Txn | Volume | Circle Fee | % of Circle Fee |
|---|---|---|---|---|---|---|---|
| No fee | 3,613 | 81.2% | $2,430.82 | $0 | $8,782,562 | $0 | 0.0% |
| Sub-cent (<$0.01) | 531 | 11.9% | $28.11 | $0.00144 | $14,927 | $0.0763 | 0.1% |
| $0.01–$1.0 | 230 | 5.2% | $3,549.72 | $0.17762 | $816,436 | $4.0852 | 4.5% |
| **>$1.0** | **78** | **1.8%** | **$221,167.45** | **$11.20216** | **$17,251,061** | **$87.3769** | **95.5%** |
| **Total** | **4,452** | **100%** | | | **$26,864,986** | **$91.54** | 100% |

- **No fee (81.2% of txns)**: 3,613 transactions, $8.8M in volume — the dominant pattern by transaction count.
- **Sub-cent (11.9% of txns)**: 531 transactions across very small notional sizes (avg $28.11). Combined Circle fees $0.08, only 0.1% of total.
- **$0.01–$1.0 (5.2% of txns)**: 230 transactions, avg amount $3,550, avg fee $0.18/txn. Generates 4.5% of Circle fees ($4.09).
- **>$1.0 (1.8% of txns)**: 78 transactions, avg fee $11.20/txn, avg transaction size $221,167. Generates **95.5% of all mainnet bridge Circle fees** ($87.38 of $91.54). Most common observed fee values: $5.00 (4 txns), $100.00 (3), $1.25 (3), $1.00 (3), $50.00 (2), $1.75 (2), $2.00 (2), $2.25 (2). Largest single source amount in this tier: $1.99M.

### Destination chain (mainnet, fee-bearing only)

| Destination | Fee Txns | Volume | Circle Fee | % of Circle Fee |
|---|---|---|---|---|
| ETH | 107 | $11,740,135 | $58.7036 | 64.1% |
| HYPEREVM | 43 | $2,941,066 | $14.7061 | 16.1% |
| BASE | 283 | $1,114,496 | $5.5741 | 6.1% |
| ARB | 215 | $1,026,150 | $5.1321 | 5.6% |
| OP | 21 | $561,550 | $2.8079 | 3.1% |
| MONAD | 9 | $403,729 | $2.0187 | 2.2% |
| AVAX | 32 | $23,712 | $1.2358 | 1.4% |
| POLYGON | 32 | $117,731 | $0.5898 | 0.6% |
| SONIC | 16 | $88,055 | $0.4403 | 0.5% |
| Other (10 chains) | 81 | $66,326 | $0.3300 | 0.4% |
| **Total** | **839** | **$18,082,950** | **$91.54** | **100%** |

ETH is the dominant fee-generating destination (64.1% of Circle fees). The top four destinations (ETH, HYPEREVM, BASE, ARB) together account for 91.9% of Circle fees.

| Total Circle fees | **$91.54** | Total developer fees | **$823.85** | Total volume | **$26,864,986** |
|---|---|---|---|---|---|
