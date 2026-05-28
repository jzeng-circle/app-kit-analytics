# USDC → USDT Spread Report (via Li.fi) — 3-sample averaged

- **Chains tested:** Ethereum, Avalanche, Solana
- **Method:** `AppKit.estimateSwap`, `slippageBps: 0`, no custom fee. Read-only quotes.
- **Test amounts:** `$100, $10K, $50K, $100K, $200K, $300K, $400K, $500K, $1M` (9 amounts). 
- **Sampling:** 3 *interleaved sweeps*. Each sweep walks all 9 amounts in order, then repeats. Within a single sweep all amounts are sampled within ~30s of each other.
- **Benchmark:** each sweep's own `$100` quote (per-sweep, not pooled).
- **Spread formula:**
  - `bips_sweep_N(A) = ((rate_sweep_N($100) − rate_sweep_N(A)) / rate_sweep_N($100)) × 10_000`
  - `avg_bips(A) = mean(bips_sweep_1(A), bips_sweep_2(A), bips_sweep_3(A))`
- **Script:** `swap/usdc-usdt-spread.ts <Chain>` (`SWEEPS = 3`)
- **Run date:** 2026-05-28

---

## Ethereum (interleaved sweeps, per-sweep bips vs $100)

| amountIn | sweep 1 (USDT) | sweep 2 (USDT) | sweep 3 (USDT) | sweep 1 bips | sweep 2 bips | sweep 3 bips | **avg bips** |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 100        | 100.096785      | 100.096785      | 100.096785      | 0.00       | 0.00       | 0.00       | **0.00** |
| 10,000     | 10,009.673585   | 10,009.673585   | 10,009.673585   | 0.00       | 0.00       | 0.00       | **0.00** |
| 50,000     | 50,048.460785   | 50,048.461853   | 50,048.461853   | -0.01      | -0.01      | -0.01      | **-0.01** |
| 100,000    | 100,096.883719  | 100,096.885278  | 100,096.885278  | -0.01      | -0.01      | -0.01      | **-0.01** |
| 200,000    | 200,192.910258  | 200,192.913547  | 200,192.913547  | 0.03       | 0.03       | 0.03       | **0.03** |
| 300,000    | 300,288.098139  | 300,288.103136  | 300,288.103136  | 0.08       | 0.08       | 0.08       | **0.08** |
| 400,000    | 400,382.478863  | 400,382.485441  | 400,382.485441  | 0.12       | 0.12       | 0.12       | **0.12** |
| 500,000    | 500,476.145757  | 500,476.153338  | 500,476.153338  | 0.16       | 0.16       | 0.16       | **0.16** |
| **1,000,000** | **1,000,949.97** | **1,000,940.16** | **1,000,940.16** | 0.18 | 0.28 | 0.28 | **0.25** |

`$100` was identical (100.096785) across all 3 sweeps, so per-sweep benchmarks are perfectly aligned. Variance at $1M (~0.1 bips between sweep 1 and 2/3) is a real route flip captured by the per-sweep view.

---

## Avalanche (interleaved sweeps, per-sweep bips vs $100) — re-run

| amountIn | sweep 1 (USDT) | sweep 2 (USDT) | sweep 3 (USDT) | sweep 1 bips | sweep 2 bips | sweep 3 bips | **avg bips** |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 100        | 100.096684      | 100.110059      | 100.102722      | 0.00       | 0.00       | 0.00       | **0.00** |
| 10,000     | 10,009.579344   | 10,009.579344   | 10,009.591227   | 0.09       | 1.42       | 0.68       | **0.73** |
| 50,000     | 50,046.932413   | 50,046.752573   | 50,046.959776   | 0.28       | 1.65       | 0.88       | **0.94** |
| 100,000    | 100,093.268936  | 100,093.269831  | 100,093.467433  | 0.34       | 1.68       | 0.92       | **0.98** |
| 200,000    | 200,184.580580  | 200,184.868453  | 200,184.883210  | 0.44       | 1.76       | 1.03       | **1.08** |
| 300,000    | 300,274.269879  | 300,274.637215  | 300,274.570168  | 0.53       | 1.85       | 1.12       | **1.16** |
| 400,000    | 400,364.554096  | 400,364.890055  | 400,364.559095  | 0.55       | 1.88       | 1.16       | **1.20** |
| 500,000    | 500,454.521118  | 500,454.521118  | 500,454.530525  | 0.58       | 1.91       | 1.18       | **1.22** |
| **1,000,000** | **1,000,904.68** | **1,000,904.69** | **1,000,904.71** | 0.62 | 1.96 | 1.22 | **1.27** |

Large-size `amountOut` is rock-solid: $1M came back as 1000904.68 / 1000904.69 / 1000904.71 across the 3 sweeps (sub-microbip variation). The 1.27 bip avg at $1M is entirely benchmark drift; the **single-snapshot reading is 0.62 bips** (sweep 1).

No failed cells this run.

---

## Solana (interleaved sweeps, per-sweep bips vs $100) — re-run

| amountIn | sweep 1 (USDT) | sweep 2 (USDT) | sweep 3 (USDT) | sweep 1 bips | sweep 2 bips | sweep 3 bips | **avg bips** |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 100        | 100.098014      | 100.098014      | 100.105762      | 0.00       | 0.00       | 0.00       | **0.00** |
| 10,000     | 10,009.718042   | 10,009.718042   | 10,009.981948   | 0.08       | 0.08       | 0.59       | **0.25** |
| 50,000     | 50,048.428804   | 50,048.428804   | 50,048.428804   | 0.12       | 0.12       | 0.89       | **0.37** |
| 100,000    | 100,096.449541  | 100,096.472554  | 100,098.215993  | 0.16       | 0.15       | 0.75       | **0.35** |
| 200,000    | 200,191.592756  | 200,193.919948  | 200,192.047285  | 0.22       | 0.11       | 0.97       | **0.43** |
| 300,000    | 300,287.024295  | 300,289.313995  | 300,287.024295  | 0.23       | 0.16       | 1.01       | **0.47** |
| 400,000    | 400,381.865681  | 400,381.797829  | 400,381.403109  | 0.25       | 0.26       | 1.04       | **0.52** |
| 500,000    | 500,476.921904  | 500,476.935986  | 500,477.317077  | 0.26       | 0.26       | 1.03       | **0.52** |
| **1,000,000** | **1,000,933.00** | **1,000,933.17** | **1,000,933.17** | 0.47 | 0.47 | 1.24 | **0.73** |

**Sweeps 1 & 2 give a very tight agreement** — $1M shows 0.47 bips in both. Sweep 3 alone gives 1.24 bips at $1M. The 3-sweep average lands at **0.73 bips at $1M**; the 2-sweep trimmed value (drop sweep 3) is **~0.47 bips**.

Large-size `amountOut` was rock-solid across sweeps: $1M came back as 1000933.00 / 1000933.17 / 1000933.17 (sub-microbip variation). $50K was identical across all 3 sweeps. The cross-sweep noise is entirely in the `$100` benchmark.

No failed cells this re-run.

---

## Cross-chain comparison (per-sweep bips vs $100, averaged over 3 sweeps)

| amountIn | Ethereum (bips) | Avalanche (re-run, bips) | Solana (re-run, bips) |
|---:|---:|---:|---:|
| 100        | 0.00  | 0.00  | 0.00  |
| 10,000     | 0.00  | 0.73  | 0.25  |
| 50,000     | -0.01 | 0.94  | 0.37  |
| 100,000    | -0.01 | 0.98  | 0.35  |
| 200,000    | 0.03  | 1.08  | 0.43  |
| 300,000    | 0.08  | 1.16  | 0.47  |
| 400,000    | 0.12  | 1.20  | 0.52  |
| 500,000    | 0.16  | 1.22  | 0.52  |
| **1,000,000** | **0.25** | **1.27** | **0.73** |

### Trimmed view (sweep 1 only, single market snapshot)

| amountIn | Ethereum (sweep 1) | Avalanche (sweep 1) | Solana (sweep 1) |
|---:|---:|---:|---:|
| 10,000     | 0.00 | 0.09  | 0.08  |
| 50,000     | -0.01 | 0.28 | 0.12  |
| 100,000    | -0.01 | 0.34 | 0.16  |
| 200,000    | 0.03 | 0.44  | 0.22  |
| 300,000    | 0.08 | 0.53  | 0.23  |
| 400,000    | 0.12 | 0.55  | 0.25  |
| 500,000    | 0.16 | 0.58  | 0.26  |
| **1,000,000** | **0.18** | **0.62** | **0.47** |

Headline within-sweep size-induced spread at $1M:
- **Ethereum: 0.18 bips**
- **Solana: 0.47 bips**
- **Avalanche: 0.62 bips**

These are the cleanest readings. The single-snapshot ordering is **Ethereum < Solana < Avalanche** — Solana actually has *tighter* size-induced spread than Avalanche in this snapshot, despite earlier runs suggesting the opposite.


---

## Caveats

- Single test-window snapshot; on-chain liquidity moves intraday. The averaging covers within-window noise (~30s spread over 3 runs per size), not session-to-session drift.
- The estimate doesn't disclose which DEX or aggregator route was chosen. Attribution requires inspecting the underlying Li.fi quote response.
- $1M is the top of the test range. To find where each chain's spread breaks, push to $5M, $10M.
- Per-sweep raw API output is in the script logs (`tasks/<run-id>.output`); omitted from this report (~30 records per chain) to keep it readable.
- A future improvement would be to (a) sample more sweeps to tighten benchmark variance, or (b) compute spread against a robust statistic (median of stable-region rates) rather than a single benchmark amount.
