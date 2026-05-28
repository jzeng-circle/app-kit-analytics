# USDC ↔ USDT Spread via Li.fi

Measures the natural spread of the USDC → USDT trading pair as quoted by
Li.fi through Circle's App Kit on Ethereum, Avalanche, and Solana. Probes
trade sizes from `$100` up to `$1M` and reports the size-induced spread in
basis points.

## Reports

| File | Description |
|---|---|
| [`report.md`](report.md) | Main deliverable — per-chain spread tables (per-sweep bips + averages), cross-chain comparison, single-snapshot trimmed view. |

## Folder contents

| Path | Description |
|---|---|
| [`report.md`](report.md) | Main report. |
| [`working/usdc-usdt-spread.ts`](working/usdc-usdt-spread.ts) | Test script (snapshot from `app-kit-feature-tests`). |
| [`working/README.md`](working/README.md) | How to run the script and refresh `data/`. |
| [`data/ethereum-raw.log`](data/ethereum-raw.log) | Raw `estimateSwap` responses + summary for Ethereum (3 interleaved sweeps × 9 amounts). |
| [`data/avalanche-raw.log`](data/avalanche-raw.log) | Raw responses for Avalanche. |
| [`data/solana-raw.log`](data/solana-raw.log) | Raw responses for Solana. |

## Headline findings

Single-snapshot size-induced spread at `$1M` (sweep 1, vs the same sweep's `$100`):

| chain | bips |
|---|---:|
| Ethereum  | 0.18 |
| Solana    | 0.47 |
| Avalanche | 0.62 |

3-sweep averages are 0.25 / 0.73 / 1.27 bips respectively — the inflation
over single-snapshot comes from cross-sweep drift in the `$100` benchmark,
not from real DEX-level spread (large-size `amountOut` is sub-microbip
stable across sweeps on every chain).

Snapshot date: 2026-05-28. On-chain stablecoin liquidity moves intraday,
so the absolute numbers are point-in-time, but the *ordering*
(Ethereum < Solana < Avalanche) is the stable headline.
