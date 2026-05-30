# Li.fi Liquidity Competitiveness — USDC ↔ USDT

## Background

Planning to support larger USDC ↔ USDT swap volume in App Kit. This report quantifies how competitive Li.fi's stablecoin liquidity and swap offering is, across three chains (Ethereum, Avalanche, Solana) and both directions (USDC → USDT and USDT → USDC).

The report covers each direction in sequence, with two sections per direction, plus a cross-direction third section:
- **Section 1** — Internal Li.fi slippage (how Li.fi price changes with trade amount, no external benchmark).
- **Section 2** — Binance price comparison (Li.fi rate vs Binance rate in the same 1-minute window; reported as a "price difference" in bips).
- **Section 3** — Round-trip spread (forward × reverse) on Ethereum, sampled in the same minute. Compares Li.fi's implicit bid-ask spread per trade size against Binance's top-of-book spread.

---

## Test configuration

- **Chains tested:** Ethereum, Avalanche, Solana
- **Method:** `AppKit.estimateSwap`, no custom fee. Read-only quotes.
- **Test amounts:** `$100, $10K, $50K, $100K, $200K, $300K, $400K, $500K, $1M` (9 amounts per direction).
- **Sampling:** 3 interleaved sweeps. Each sweep walks all 9 amounts in order, then repeats (~30s per sweep).
- **Benchmark:** each sweep's own `$100` quote (per-sweep, not pooled).
- **Slippage formula:**
  - `bips_sweep_N(A) = ((rate_sweep_N($100) − rate_sweep_N(A)) / rate_sweep_N($100)) × 10_000`
  - `avg_bips(A) = mean(bips_sweep_1(A), bips_sweep_2(A), bips_sweep_3(A))`
- **Scripts:** `swap/usdc-usdt-spread.ts` (forward), `swap/usdt-usdc-spread.ts` (reverse). `SWEEPS = 3`.
- **Run dates:** Forward 2026-05-28 / 2026-05-29. Reverse 2026-05-30.

---

## Direction A — USDC → USDT (forward)

### Section 1 — Internal Li.fi slippage

Per-chain Binance bid references (kline close of each test's finish minute, included in tables for cross-reference; summary in Section 2):
- Ethereum: 1.00117 · window 01:22:58–01:23:58 UTC
- Avalanche: 1.00114 · window 02:11:11–02:12:11 UTC
- Solana: 1.00116 · window 02:15:19–02:16:19 UTC

#### Ethereum (interleaved sweeps, USDC → USDT)

Test window: 2026-05-28T01:22:58Z – 01:23:58Z · Binance bid: 1.00117

| amountIn (USDC) | sweep 1 (USDT) | sweep 2 (USDT) | sweep 3 (USDT) | avg rate (USDT/USDC) | slippage vs $100 (bips, avg) | price diff vs Binance bid (bips) |
|---:|---:|---:|---:|---:|---:|---:|
| 100        | 100.096785      | 100.096785      | 100.096785      | 1.00096785 | 0.00 (bench) | 2.02 |
| 10,000     | 10,009.673585   | 10,009.673585   | 10,009.673585   | 1.00096736 | 0.00 | 2.03 |
| 50,000     | 50,048.460785   | 50,048.461853   | 50,048.461853   | 1.00096923 | -0.01 | 2.01 |
| 100,000    | 100,096.883719  | 100,096.885278  | 100,096.885278  | 1.00096885 | -0.01 | 2.01 |
| 200,000    | 200,192.910258  | 200,192.913547  | 200,192.913547  | 1.00096456 | 0.03 | 2.05 |
| 300,000    | 300,288.098139  | 300,288.103136  | 300,288.103136  | 1.00096034 | 0.08 | 2.09 |
| 400,000    | 400,382.478863  | 400,382.485441  | 400,382.485441  | 1.00095621 | 0.12 | 2.14 |
| 500,000    | 500,476.145757  | 500,476.153338  | 500,476.153338  | 1.00095230 | 0.16 | 2.18 |
| **1,000,000** | **1,000,949.97** | **1,000,940.16** | **1,000,940.16** | **1.00094343** | **0.25** | **2.26** |

#### Avalanche (interleaved sweeps, USDC → USDT)

Test window: 2026-05-28T02:11:11Z – 02:12:11Z · Binance bid: 1.00114

| amountIn (USDC) | sweep 1 (USDT) | sweep 2 (USDT) | sweep 3 (USDT) | avg rate (USDT/USDC) | slippage vs $100 (bips, avg) | price diff vs Binance bid (bips) |
|---:|---:|---:|---:|---:|---:|---:|
| 100        | 100.096684      | 100.110059      | 100.102722      | 1.00103155 | 0.00 (bench) | 1.08 |
| 10,000     | 10,009.579344   | 10,009.579344   | 10,009.591227   | 1.00095833 | 0.73 | 1.81 |
| 50,000     | 50,046.932413   | 50,046.752573   | 50,046.959776   | 1.00093763 | 0.94 | 2.02 |
| 100,000    | 100,093.268936  | 100,093.269831  | 100,093.467433  | 1.00093335 | 0.98 | 2.06 |
| 200,000    | 200,184.580580  | 200,184.868453  | 200,184.883210  | 1.00092389 | 1.08 | 2.16 |
| 300,000    | 300,274.269879  | 300,274.637215  | 300,274.570168  | 1.00091498 | 1.16 | 2.25 |
| 400,000    | 400,364.554096  | 400,364.890055  | 400,364.559095  | 1.00091167 | 1.20 | 2.28 |
| 500,000    | 500,454.521118  | 500,454.521118  | 500,454.530525  | 1.00090905 | 1.22 | 2.31 |
| **1,000,000** | **1,000,904.68** | **1,000,904.69** | **1,000,904.71** | **1.00090469** | **1.27** | **2.35** |

#### Solana (interleaved sweeps, USDC → USDT)

Test window: 2026-05-28T02:15:19Z – 02:16:19Z · Binance bid: 1.00116

| amountIn (USDC) | sweep 1 (USDT) | sweep 2 (USDT) | sweep 3 (USDT) | avg rate (USDT/USDC) | slippage vs $100 (bips, avg) | price diff vs Binance bid (bips) |
|---:|---:|---:|---:|---:|---:|---:|
| 100        | 100.098014      | 100.098014      | 100.105762      | 1.00100597 | 0.00 (bench) | 1.54 |
| 10,000     | 10,009.718042   | 10,009.718042   | 10,009.981948   | 1.00098060 | 0.25 | 1.79 |
| 50,000     | 50,048.428804   | 50,048.428804   | 50,048.428804   | 1.00096858 | 0.37 | 1.91 |
| 100,000    | 100,096.449541  | 100,096.472554  | 100,098.215993  | 1.00097046 | 0.35 | 1.89 |
| 200,000    | 200,191.592756  | 200,193.919948  | 200,192.047285  | 1.00096260 | 0.43 | 1.97 |
| 300,000    | 300,287.024295  | 300,289.313995  | 300,287.024295  | 1.00095929 | 0.47 | 2.00 |
| 400,000    | 400,381.865681  | 400,381.797829  | 400,381.403109  | 1.00095422 | 0.52 | 2.05 |
| 500,000    | 500,476.921904  | 500,476.935986  | 500,477.317077  | 1.00095412 | 0.52 | 2.05 |
| **1,000,000** | **1,000,933.00** | **1,000,933.17** | **1,000,933.17** | **1.00093311** | **0.73** | **2.27** |

#### Cross-chain comparison — slippage vs $100 (avg of 3 sweeps)

| amountIn | Ethereum (bips) | Avalanche (bips) | Solana (bips) |
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

### Section 2 — Binance price comparison

**Binance benchmark (2026-05-29 01:33–01:35 UTC):** USDCUSDT **bid = 1.00095** (kline close, fetched via `data-api.binance.vision`).

For the forward direction (selling USDC for USDT), Li.fi's USDT-per-USDC rate is compared against the Binance bid (kline close = bid in this run).

Formula: `((binance_close − lifi_rate) / binance_close) × 10_000`. Positive = Li.fi worse than Binance.

#### Cross-chain comparison (USDC → USDT, vs Binance bid)

| chain     | test window (UTC) | Binance close | Li.fi $100 rate | price diff @ $100 (bips) | Li.fi $1M rate | price diff @ $1M (bips) |
|---|---|---:|---:|---:|---:|---:|
| Ethereum  | 2026-05-29T01:33:50–01:34:50 | 1.00095 | 1.00076191 | 1.88 | 1.00074554 | **2.04** |
| Avalanche | 2026-05-29T01:34:04–01:35:04 | 1.00095 | 1.00107659 | **−1.26** (anomalous $100 sweep) | 1.00068028 | **2.70** |
| Solana    | 2026-05-29T01:33:42–01:34:42 | 1.00095 | 1.00079480 | 1.55 | 1.00071913 | **2.31** |

All three chains within ~2–3 bips of Binance at $1M. Avalanche's $100 row shows a negative price difference because sweep 1 hit an anomalous small-trade route (100.159964 vs ~100.0815 in sweeps 2–3); $10K+ tracks normally.

---

## Direction B — USDT → USDC (reverse)

### Section 1 — Internal Li.fi slippage

Per-chain Binance ask references (kline close of each test's finish minute, inverted to USDC-per-USDT for comparison with Li.fi's rate; included in tables for cross-reference; summary in Section 2):
- Ethereum: ask 1.00100 → 1/ask 0.99900100 · window 13:21:45–13:22:45 UTC
- Avalanche: ask 1.00100 → 1/ask 0.99900100 · window 13:21:52–13:22:52 UTC
- Solana: ask 1.00100 → 1/ask 0.99900100 · window 13:21:37–13:22:37 UTC

#### Ethereum (interleaved sweeps, USDT → USDC)

Test window: 2026-05-30T13:21:45Z – 13:22:45Z · Binance ask: 1.00100 (1/ask = 0.99900100)

| amountIn (USDT) | sweep 1 (USDC) | sweep 2 (USDC) | sweep 3 (USDC) | avg rate (USDC/USDT) | slippage vs $100 (bips, avg) | price diff vs Binance ask (bips) |
|---:|---:|---:|---:|---:|---:|---:|
| 100        | **100.186010** | **100.266226** | **100.263112** | 1.00238449 | 0.00 (bench) | **−33.87** |
| 10,000     | 9,989.940983   | 9,990.755371   | 9,990.755585   | 0.99904840 | 33.28 | **−0.47** |
| 50,000     | 49,940.635573  | 49,941.010096  | 49,943.253914  | 0.99883266 | 35.43 | 1.69 |
| 100,000    | 99,881.240307  | 99,883.051273  | 99,881.992293  | 0.99882095 | 35.55 | 1.80 |
| 200,000    | 199,764.402193 | 199,762.352573 | 199,764.402193 | 0.99881859 | 35.57 | 1.82 |
| 300,000    | 299,643.248300 | 299,643.248300 | 299,644.522963 | 0.99881224 | 35.64 | 1.89 |
| 400,000    | 399,524.355451 | 399,524.441807 | 399,524.330470 | 0.99881094 | 35.65 | 1.90 |
| 500,000    | 499,404.952052 | 499,404.934198 | 499,404.934198 | 0.99880988 | 35.66 | 1.91 |
| **1,000,000** | **998,804.73** | **998,804.73** | **998,804.30** | **0.99880459** | **35.71** | **1.97** |

`$100` hit an anomalous small-trade route in all 3 sweeps (rates 1.0019–1.0027, 186–267 bps above par); `$10K` also got a favorable route. From `$50K` upward, the rates settle on the normal route (~1.7–2.0 bips below Binance).

#### Avalanche (interleaved sweeps, USDT → USDC)

Test window: 2026-05-30T13:21:52Z – 13:22:52Z · Binance ask: 1.00100 (1/ask = 0.99900100)

| amountIn (USDT) | sweep 1 (USDC) | sweep 2 (USDC) | sweep 3 (USDC) | avg rate (USDC/USDT) | slippage vs $100 (bips, avg) | price diff vs Binance ask (bips) |
|---:|---:|---:|---:|---:|---:|---:|
| 100        | 99.886839       | 99.885123       | 99.886829       | 0.99886264 | 0.00 (bench) | 1.39 |
| 10,000     | 9,988.604843    | 9,988.569027    | 9,988.567318    | 0.99885804 | 0.05 | 1.43 |
| 50,000     | 49,941.089118   | 49,941.043443   | 49,941.464220   | 0.99882398 | 0.39 | 1.77 |
| 100,000    | 99,881.137203   | 99,881.150483   | 99,881.148814   | 0.99881146 | 0.51 | 1.90 |
| 200,000    | 199,760.336956  | 199,760.162738  | 199,760.171968  | 0.99880112 | 0.62 | 2.00 |
| 300,000    | 299,638.174080  | 299,638.118634  | 299,638.472199  | 0.99879418 | 0.69 | 2.07 |
| 400,000    | 399,514.614724  | 399,513.597874  | 399,513.701795  | 0.99878493 | 0.78 | 2.16 |
| 500,000    | 499,388.254543  | 499,389.644787  | 499,388.437538  | 0.99877756 | 0.85 | 2.24 |
| **1,000,000** | **998,733.37** | **998,733.39** | **998,731.51** | **0.99873276** | **1.30** | **2.69** |

#### Solana (interleaved sweeps, USDT → USDC)

Test window: 2026-05-30T13:21:37Z – 13:22:37Z · Binance ask: 1.00100 (1/ask = 0.99900100)

| amountIn (USDT) | sweep 1 (USDC) | sweep 2 (USDC) | sweep 3 (USDC) | avg rate (USDC/USDT) | slippage vs $100 (bips, avg) | price diff vs Binance ask (bips) |
|---:|---:|---:|---:|---:|---:|---:|
| 100        | 99.880139       | 99.880139       | 99.880020       | 0.99880099 | 0.00 (bench) | 2.00 |
| 10,000     | 9,988.002000    | 9,988.002000    | 9,988.002000    | 0.99880020 | 0.01 | 2.01 |
| 50,000     | 49,940.010000   | 49,940.010000   | 49,939.990163   | 0.99880007 | 0.01 | 2.01 |
| 100,000    | 99,879.746408   | 99,879.714271   | 99,879.670521   | 0.99879710 | 0.04 | 2.04 |
| 200,000    | 199,758.554772  | 199,758.351838  | 199,758.413725  | 0.99879220 | 0.09 | 2.09 |
| 300,000    | 299,636.772549  | 299,636.689944  | 299,636.772549  | 0.99878915 | 0.12 | 2.12 |
| 400,000    | 399,514.251349  | 399,514.105380  | 399,514.251349  | 0.99878551 | 0.16 | 2.16 |
| 500,000    | 499,391.716188  | 499,391.473009  | 499,391.473009  | 0.99878311 | 0.18 | 2.19 |
| **1,000,000** | **998,760.72** | **998,760.57** | **998,760.98** | **0.99876076** | **0.40** | **2.40** |

### Section 2 — Binance price comparison

**Binance benchmark (2026-05-30 13:21–13:22 UTC):** USDCUSDT **ask = 1.00100** → inverted to **1/ask = 0.99900100** USDC per USDT (kline close, fetched via `data-api.binance.vision`).

For the reverse direction (buying USDC with USDT), Li.fi's USDC-per-USDT rate is compared against the inverted ask, so the value is directly comparable in the same units.

Formula: `((binance_close − lifi_rate) / binance_close) × 10_000`. Positive = Li.fi worse than Binance.

#### Cross-chain comparison (USDT → USDC, vs Binance ask)

| chain     | test window (UTC) | Binance close | Li.fi $100 rate | price diff @ $100 (bips) | Li.fi $1M rate | price diff @ $1M (bips) |
|---|---|---:|---:|---:|---:|---:|
| Ethereum  | 2026-05-30T13:21:45–13:22:45 | 0.99900100 | 1.00238449 | **−33.87** (anomalous $100 route) | 0.99880459 | **1.97** |
| Avalanche | 2026-05-30T13:21:52–13:22:52 | 0.99900100 | 0.99886264 | 1.39 | 0.99873276 | **2.69** |
| Solana    | 2026-05-30T13:21:37–13:22:37 | 0.99900100 | 0.99880099 | 2.00 | 0.99876076 | **2.40** |

All three chains within ~2–3 bips of Binance at $1M. Ethereum's $100 quote landed on an anomalous "small-trade route" in all 3 sweeps (rate 1.002+ vs Binance 0.999); the $1M reading is on the normal route.

---

## Section 3 — Round-trip spread (forward × reverse) — Ethereum same-window

Implicit bid-ask spread at each trade size, computed as the round-trip cost of swapping USDC → USDT → USDC on the same venue at the same amount:

`spread_bips = (1 − forward_rate × reverse_rate) × 10_000`

where `forward_rate` is USDT-per-USDC and `reverse_rate` is USDC-per-USDT. Positive bips = round-trip loss; negative bips = round-trip gain (anomalous, only on Ethereum's small-trade routes).

Ethereum only, with both forward and reverse runs in the same minute (no cross-day drift). Binance comparison is from the same-window bookTicker.

**Test details (2026-05-30):**
- Forward Ethereum: finished `14:05:50 UTC` · `usdc-usdt-spread.ts Ethereum`
- Reverse Ethereum: finished `14:05:54 UTC` (4 seconds later) · `usdt-usdc-spread.ts Ethereum`
- Binance USDCUSDT: bid 1.00099 · ask 1.00100 (stable in pre/post brackets at 14:04:10Z and 14:06:10Z)

### Li.fi Ethereum round-trip spread

| amountIn | forward rate (USDT/USDC) | reverse rate (USDC/USDT) | round-trip spread (bips) |
|---:|---:|---:|---:|
| 100        | 1.00077663 | 1.00202950 | **−28.08** (anomalous $100 routes both directions) |
| 10,000     | 1.00077573 | 0.99901615 | 2.09 |
| 50,000     | 1.00078030 | 0.99883814 | 3.82 |
| 100,000    | 1.00078011 | 0.99883497 | 3.86 |
| 200,000    | 1.00077973 | 0.99881833 | 4.03 |
| 300,000    | 1.00077390 | 0.99880849 | 4.19 |
| 400,000    | 1.00077212 | 0.99880750 | 4.21 |
| 500,000    | 1.00077198 | 0.99880673 | 4.22 |
| **1,000,000** | **1.00076576** | **0.99880201** | **4.33** |

### Binance round-trip spread (same window, USDCUSDT top-of-book)

| bid | ask | bid × (1/ask) | round-trip spread (bips) |
|---:|---:|---:|---:|
| 1.00099 | 1.00100 | 0.99999001 | **0.10** |

Binance bid-ask is constant at top-of-book regardless of trade size (within displayed depth of ~$3–4M each side at this snapshot). For larger trades the effective Binance spread would widen by walking the book — not directly measurable from the public bookTicker.

### Side-by-side

| amountIn | Li.fi Ethereum (bips) | Binance top-of-book (bips) |
|---:|---:|---:|
| 100        | −28.08 (anomalous) | 0.10 |
| 10,000     | 2.09  | 0.10 |
| 50,000     | 3.82  | 0.10 |
| 100,000    | 3.86  | 0.10 |
| 200,000    | 4.03  | 0.10 |
| 300,000    | 4.19  | 0.10 |
| 400,000    | 4.21  | 0.10 |
| 500,000    | 4.22  | 0.10 |
| **1,000,000** | **4.33** | **0.10** |

Li.fi Ethereum's round-trip spread at $1M is **~43× wider** than Binance's top-of-book bid-ask. This is the cost of using an on-chain AMM (per-swap fee + routing overhead) for a USDC ↔ USDT round-trip vs Binance's order book.

The round-trip spread grows monotonically with size from ~2 bips at $10K to ~4.3 bips at $1M; the jump from $10K (2.09) to $50K (3.82) is the biggest step (size impact begins to matter past $10K). Above $200K the spread stabilizes near 4.0–4.3 bips.

---

## Caveats

- Single test-window snapshot per direction; on-chain pool ratios and CEX prices drift intraday. Forward and reverse snapshots are from different days (2026-05-29 / 2026-05-30); the directional comparison is approximate.
- The estimate doesn't disclose which DEX or aggregator route Li.fi selected.
- $1M is the top of the test range. To find where each chain's slippage breaks, push to $5M+.
- Ethereum `$100` quotes hit an anomalous "small-trade route" in multiple runs (rates well above par); flagged in per-chain sections. Treat `$100` quotes on Ethereum with caution.
- The Binance main API (`api.binance.com`) is geo-restricted from this location. Switched to `data-api.binance.vision` CDN for the latest run; same market data, no restriction.
- Per-sweep raw API output is in script logs (`tasks/<run-id>.output`); omitted here.
- Future improvements: more sweeps to tighten benchmark variance; slippage vs a robust statistic (median of stable region) instead of a single $100 benchmark; same-minute forward and reverse runs for a true single-snapshot directional comparison.
