# Working — usdc-usdt-spread

## Pipeline

`usdc-usdt-spread.ts` is a snapshot of the test script from the
`app-kit-feature-tests` repo. It depends on the Circle `@circle-fin/app-kit`
and `@circle-fin/adapter-*` packages and a `KIT_KEY` + signing keys
(`PRIVATE_KEY` for EVM, `SOLANA_PRIVATE_KEY` base58 for Solana), so it cannot
be run directly from this repo — copy it back into a Node project that has
those packages installed.

### Source repo

`~/app-kit-feature-tests/swap/usdc-usdt-spread.ts` is the canonical location.
The script is reproduced here for the record at the snapshot used to produce
the report.

### How to refresh the data

From the `app-kit-feature-tests` project root:

```bash
npx tsx swap/usdc-usdt-spread.ts Ethereum  > eth.log  2>&1
npx tsx swap/usdc-usdt-spread.ts Avalanche > avax.log 2>&1
npx tsx swap/usdc-usdt-spread.ts Solana    > sol.log  2>&1
```

Each invocation produces 27 `estimateSwap` API calls (9 amounts × 3
interleaved sweeps) plus a SPREAD ANALYSIS table at the end. Read-only —
no on-chain transactions.

Copy the resulting logs into `data/{chain}-raw.log` (overwriting) and
rebuild `report.md` from the SPREAD ANALYSIS sections at the bottom of
each log.

## Methodology notes

- **Sampling is interleaved sweeps**, not 3 back-to-back samples per
  amount. Every sweep walks all 9 amounts in order, then the next sweep
  repeats. This minimizes intra-test market drift for cross-amount
  comparisons.
- **Per-sweep bips, then averaged.** Spread for each amount is computed
  *within* its own sweep using that sweep's `$100` quote as benchmark,
  then bips are averaged across sweeps. This is more robust to
  inter-sweep market drift than averaging rates first.
- **`$1` was dropped** from `TEST_AMOUNTS`. Earlier iterations showed
  `$1` quotes landing on small-trade routes that don't reflect the
  market at typical sizes; `$100` is the smallest "real" amount and is
  used as the benchmark instead.
- **`slippageBps: 0`** is passed explicitly so the SDK's default 3%
  slippage doesn't perturb the `stopLimit` field. The report reads only
  `estimatedOutput`, which is the pre-slippage quote and unaffected by
  this setting — but setting it to 0 keeps everything in the response
  honest.
