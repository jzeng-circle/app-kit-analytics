# App Kit Custom Fee Feature — Swap vs Bridge Comparison
**Generated**: 2026-05-05
**Sources**: `appkit_txn_20260505_014246.csv` (swap, txn-level) · `birdgekit20260505_013439.csv` (bridge, txn-level)

---

## Overview

| | Swap — Testnet | Swap — Mainnet | Bridge — Mainnet |
|---|---|---|---|
| **Data** | arc_testnet | base, arb, eth, solana | 11 chains |
| **Total transactions** | 9,970 | 30 | 491 |
| **Fee-bearing txns** | 6,030 (60.5%) | 0 (0%) | 19 (3.9%) |
| **Fee structure** | % of volume (bps) | % of volume (bps) | Flat USDC per txn |
| **Most common fee level** | ~51–52 bps (active users) | — | 0.0001–0.02 USDC flat |
| **Total volume** | $1,683,696 | $34 | $1,748 |
| **Circle fees collected** | **$143.40** | **$0** | **$0.094** |
| **Dev fees collected** | **$1,434.04** | **$0** | **$0.847** |
| **Stage** | Active at scale | No adoption yet | Early testing |

---

## 1. Feature Adoption

### Swap
- **Testnet**: 60.5% of transactions carry a fee. Of those, the ~51–52 bps tier (627 txns) generates 96.8% of all Circle revenue. The remaining fee-bearing transactions are low-rate noise (<10 bps).
- **Mainnet**: Zero. 30 mainnet swap transactions across base, arbitrum, ethereum, and solana — all with $0 Circle fees. Volume is also negligible ($34 total), indicating this is early exploratory usage by a handful of wallets, not production traffic.

### Bridge
- **Mainnet only**: 19 of 491 transactions (3.9%) carry a developer fee. All fee activity is concentrated among a small set of developer tests — no evidence of production-scale deployment. The ARB→MONAD transaction alone accounts for 73% of total Circle bridge fees.

---

## 2. Fee Structures Are Different

Swap and bridge use fundamentally different fee models:

| Aspect | Swap | Bridge |
|---|---|---|
| Fee type | Basis points (% of volume) | Flat USDC amount per transaction |
| Dominant active tier | 51–52 bps | 0.02 USDC flat |
| Fee scales with volume? | Yes | No |
| Developer control | Per-wallet rate or global policy | Per-transaction flat fee |

This means bridge fees can be disproportionately large for small transactions (e.g., $0.02 fee on a $0.01 bridge = 200% effective rate in the test data) but relatively cheap for large ones. Swap fees are always proportional.

---

## 3. Revenue Comparison

### Circle fees collected (all environments)

| Product | Environment | Circle Fee | Dev Fee | Volume |
|---|---|---|---|---|
| Swap | Testnet | $143.40 | $1,434.04 | $1,683,696 |
| Swap | Mainnet | $0.00 | $0.00 | $34 |
| Bridge | Mainnet | $0.094 | $0.847 | $1,748 |
| **Total** | | **$143.49** | **$1,434.89** | **$1,685,478** |

- **Swap testnet dominates** — 99.9% of all Circle fees.
- **Mainnet is nascent across both products** — combined $0.094 in Circle fees from 521 transactions.
- Bridge mainnet volume ($1,748) is already larger than swap mainnet volume ($34), but neither product has fee adoption on mainnet yet.

---

## 4. Maturity Assessment

| | Swap | Bridge |
|---|---|---|
| **Testnet maturity** | High — active developer base, clear fee tiers, $1.68M volume | Not in dataset |
| **Mainnet maturity** | Very early — 30 txns, no fees configured | Early — 491 txns, 3.9% fee adoption, testing-level amounts |
| **Fee feature rollout** | Developer has configured and is using 51–52 bps on testnet; not yet ported to mainnet | Small number of devs testing flat fees on mainnet; no production deployment |
| **Next milestone to watch** | Will 51–52 bps swap configurers move to mainnet? | Will any dev configure fees at production volumes (>$1,000/txn)? |
