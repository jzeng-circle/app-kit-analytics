# Working — usdc-usdt-spread (both directions)

## Pipeline

`usdc-usdt-spread.ts` (forward, USDC → USDT) and `usdt-usdc-spread.ts` (reverse, USDT → USDC) are snapshots of the test scripts from the `app-kit-feature-tests` repo. They depend on the Circle `@circle-fin/app-kit` and `@circle-fin/adapter-*` packages plus a `KIT_KEY` and signing keys (`PRIVATE_KEY` for EVM, `SOLANA_PRIVATE_KEY` base58 for Solana), so they cannot be run directly from this repo — copy them back into a Node project that has those packages installed.

The two scripts are nearly identical; they differ only in `TOKEN_IN` / `TOKEN_OUT`.

### Source repo

- `~/app-kit-feature-tests/swap/usdc-usdt-spread.ts` (forward) — canonical location
- `~/app-kit-feature-tests/swap/usdt-usdc-spread.ts` (reverse) — canonical location

The scripts are reproduced here for the record at the snapshot used to produce the report.

### How to refresh the data

From the `app-kit-feature-tests` project root:

```bash
# Forward direction (USDC → USDT)
npx tsx swap/usdc-usdt-spread.ts Ethereum  > eth-forward.log  2>&1
npx tsx swap/usdc-usdt-spread.ts Avalanche > avax-forward.log 2>&1
npx tsx swap/usdc-usdt-spread.ts Solana    > sol-forward.log  2>&1

# Reverse direction (USDT → USDC)
npx tsx swap/usdt-usdc-spread.ts Ethereum  > eth-reverse.log  2>&1
npx tsx swap/usdt-usdc-spread.ts Avalanche > avax-reverse.log 2>&1
npx tsx swap/usdt-usdc-spread.ts Solana    > sol-reverse.log  2>&1
```

Each invocation produces 27 `estimateSwap` API calls (9 amounts × 3 interleaved sweeps) plus a `SPREAD ANALYSIS` table at the end. Read-only — no on-chain transactions.

Bracket each run with Binance USDCUSDT bookTicker fetches (before and after) so the report can use a same-window Binance reference:

```bash
curl -s "https://data-api.binance.vision/api/v3/ticker/bookTicker?symbol=USDCUSDT"
```

(Use `data-api.binance.vision` — the main `api.binance.com` is geo-restricted from some locations.)

For the per-minute Binance kline matching each test's finish minute:

```bash
curl -s "https://data-api.binance.vision/api/v3/klines?symbol=USDCUSDT&interval=1m&startTime=<unix_ms>&endTime=<unix_ms>"
```

Copy the resulting Li.fi logs into `data/{chain}-{direction}-{date}.log` and rebuild `report.md` from the `SPREAD ANALYSIS` sections plus the corresponding Binance kline close per chain.

## Methodology notes

- **Sampling is interleaved sweeps**, not 3 back-to-back samples per amount. Every sweep walks all 9 amounts in order, then the next sweep repeats. This minimizes intra-test market drift for cross-amount comparisons.
- **Per-sweep bips, then averaged.** Spread for each amount is computed *within* its own sweep using that sweep's `$100` quote as benchmark, then bips are averaged across sweeps. This is more robust to inter-sweep market drift than averaging rates first.
- **`$1` was dropped** from `TEST_AMOUNTS`. Earlier iterations showed `$1` quotes landing on small-trade routes that don't reflect the market at typical sizes; `$100` is the smallest "real" amount and is used as the benchmark instead.
- **Binance reference is direction-dependent.**
  - Forward (USDC → USDT): compare Li.fi USDT-per-USDC rate against Binance **bid** (the rate you'd get selling USDC for USDT on Binance, = kline close in our snapshots).
  - Reverse (USDT → USDC): compare Li.fi USDC-per-USDT rate against Binance **ask**, inverted to USDC-per-USDT (`1/ask`).
- **Forward `$100` route on Ethereum** occasionally hits a special small-trade pool returning rates well above par. From `$10K` upward the rate settles on the normal AMM route; report flags this in the per-chain section.
