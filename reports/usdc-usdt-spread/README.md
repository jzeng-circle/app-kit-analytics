# Li.fi Liquidity Competitiveness — USDC ↔ USDT

Measures how competitive Li.fi's USDC ↔ USDT swap offering is on Ethereum, Avalanche, and Solana, in both directions (USDC → USDT and USDT → USDC). Probes trade sizes from `$100` up to `$1M`, compares Li.fi rates against a same-window Binance benchmark, and reports both internal Li.fi slippage and the price difference vs Binance in basis points.

Motivation: App Kit is planning to support larger USDC ↔ USDT swap volume based on internal demand. This report establishes the baseline competitiveness before scaling.

## Reports

| File | Description |
|---|---|
| [`report.md`](report.md) | Main deliverable — both directions in sequence, with per-chain tables, internal Li.fi slippage (Section 1) and Binance price comparison (Section 2) per direction, plus a cross-direction summary. |

## Folder contents

| Path | Description |
|---|---|
| [`report.md`](report.md) | Main report (combined, both directions). |
| [`working/usdc-usdt-spread.ts`](working/usdc-usdt-spread.ts) | Test script for forward direction (USDC → USDT), snapshot from `app-kit-feature-tests`. |
| [`working/usdt-usdc-spread.ts`](working/usdt-usdc-spread.ts) | Test script for reverse direction (USDT → USDC). |
| [`working/README.md`](working/README.md) | How to run the scripts and refresh `data/`. |
| [`data/ethereum-usdc-usdt-2026-05-28.log`](data/ethereum-usdc-usdt-2026-05-28.log) | Forward Ethereum, 3 interleaved sweeps × 9 amounts (Section 1 forward source). |
| [`data/avalanche-usdc-usdt-2026-05-28.log`](data/avalanche-usdc-usdt-2026-05-28.log) | Forward Avalanche, same snapshot. |
| [`data/solana-usdc-usdt-2026-05-28.log`](data/solana-usdc-usdt-2026-05-28.log) | Forward Solana, same snapshot. |
| [`data/ethereum-usdc-usdt-2026-05-29.log`](data/ethereum-usdc-usdt-2026-05-29.log) | Forward Ethereum, rerun (Section 2 forward source). |
| [`data/avalanche-usdc-usdt-2026-05-29.log`](data/avalanche-usdc-usdt-2026-05-29.log) | Forward Avalanche, rerun. |
| [`data/solana-usdc-usdt-2026-05-29.log`](data/solana-usdc-usdt-2026-05-29.log) | Forward Solana, rerun. |
| [`data/ethereum-usdt-usdc-2026-05-30.log`](data/ethereum-usdt-usdc-2026-05-30.log) | Reverse Ethereum (Section 1 & 2 reverse source). |
| [`data/avalanche-usdt-usdc-2026-05-30.log`](data/avalanche-usdt-usdc-2026-05-30.log) | Reverse Avalanche. |
| [`data/solana-usdt-usdc-2026-05-30.log`](data/solana-usdt-usdc-2026-05-30.log) | Reverse Solana. |
| [`data/ethereum-usdc-usdt-2026-05-30-spread.log`](data/ethereum-usdc-usdt-2026-05-30-spread.log) | Same-window Ethereum forward run for Section 3 round-trip spread (finished 14:05:50Z). |
| [`data/ethereum-usdt-usdc-2026-05-30-spread.log`](data/ethereum-usdt-usdc-2026-05-30-spread.log) | Same-window Ethereum reverse run for Section 3 round-trip spread (finished 14:05:54Z, 4 sec after forward). |

## Headline findings

Li.fi tracks Binance to within ~2–3 bips at $1M on all three chains, in both directions:

| chain | USDC → USDT $1M price diff vs Binance bid (bips) | USDT → USDC $1M price diff vs Binance ask (bips) |
|---|---:|---:|
| Ethereum  | 2.04 | 1.97 |
| Avalanche | 2.70 | 2.69 |
| Solana    | 2.31 | 2.40 |

The ~2-bip gap is consistent with the AMM fee on the underlying pool (Curve / Uniswap v3 stablecoin pools at ~1–3 bps per side), not a CEX/DEX dislocation. Forward and reverse are essentially symmetric (within ~0.1 bip per chain), confirming the on-chain market is well-arbed to Binance mid.

Per-chain ordering is consistent across directions: **Ethereum tightest < Solana < Avalanche** at $1M.

Internal Li.fi slippage ($100 → $1M) is sub-1-bip on Avalanche and Solana in both directions; Ethereum has occasional anomalous `$100` quotes (small-trade routes paying well above par) but normal-route rates from $10K up.

Section 3 of the report computes the round-trip spread (`spread = 1 − forward × reverse`) using a same-window Ethereum run (forward and reverse 4 seconds apart). At $1M, Li.fi Ethereum's implicit bid-ask is **4.33 bips** vs Binance's **0.10 bips** top-of-book — about 43× wider, the cost of using an on-chain AMM vs an order book.

Snapshot dates: forward 2026-05-28 / 2026-05-29 · reverse 2026-05-30. Both Binance and on-chain rates drift intraday, so absolute numbers are point-in-time; the structural ordering and ~2-bip magnitude is the stable headline.
