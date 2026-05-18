# Arc Testnet Wallet Activity Report

**Network:** Arc Public Testnet (Circle's stablecoin-native L1)
**Explorer source:** `arc-testnet-explorer.stg.blockchain.circle.com` (Blockscout API v2)
**Report date:** 2026-05-18
**Wallets covered:**
- `0x6063e834928EaC1ca47ac5Da27838079a103e305`
- `0x34e785eef1e465e5db4de4b47c1bb64d9c237742`

> **Caveat on data freshness.** Blockscout's `/addresses/{addr}/counters` endpoint
> returns zeros for both wallets, which is incorrect — the live transactions and
> token-transfers tables are densely populated. We rely on paginated
> `/transactions` and `/token-transfers` sampling, not the counter aggregates.

---

## Executive Summary

Both wallets are **automated bots** routing traffic through the same unverified
swap router on Arc testnet:

- Router proxy: `0xBBD70b01a1CAbC96d5b7b129AE1AaABdF50Dd40b` (EIP-1967)
- Implementation: `0xCeA69a03A998002296b5c6b089B94B2B498d8751` (unverified)
- Dominant function selector: `0xaa3e079c` (unverified, not auto-decoded)

The two wallets differ sharply in **scale, capital, and strategy**, but share
the same target infrastructure. That suggests either one operator running
multiple bots or several operators hitting the same Arc-testnet DEX.

| Dimension | `0x6063…3e305` | `0x34e7…7742` |
|---|---|---|
| Native ARC balance | ~3,353,970 | ~16.36 |
| Real stablecoin float | 2.36M USDT, 234k WUSDC, 12k USDC | 16 USDC, 2,313 EURC |
| Distinct ERC-20 holdings | 50+ | ~30 |
| Sampled tx window | ~2 hours (2026-05-15 09:27–11:15Z) | ~2 days (2026-05-15 → 2026-05-17) |
| Calls to router `0xBBD7…40b` | 288 / 300 sampled | 252 / 300 sampled |
| Dominant flow | USDC → router → USDC (multi-leg fee split) | USDC ⇄ EURC round-tripping |
| Avg swap size (sampled) | ~10 USDC | ~$340 |
| Net stablecoin delta | Inbound-only sampled window (likely PnL/settlement leg) | +$18.30 USDC, −$78.59 EURC over $135k two-way volume |
| Behavior signature | Burst trader / micro-swap bot | Delta-neutral USDC/EURC market-maker or arbitrage bot |

---

## Wallet 1 — `0x6063e834928EaC1ca47ac5Da27838079a103e305`

### Profile

- EOA, no contract code, no name/ENS, not flagged as scam.
- Native balance: **3,353,969.80 ARC** (testnet faucet allocation).
- Balance last updated at block 42,325,338.

### Notable token holdings (selection from 50+ ERC-20s)

| Symbol | Name | Balance | Holders | Notes |
|---|---|---:|---:|---|
| *(unnamed)* | — | 900,000,000.00 | 5 | Self-deployed test token (`0x858E…2455`) |
| *(unnamed)* | — | 900,000,000.00 | 5 | Self-deployed test token (`0x683D…F036`) |
| FLOW | FLOW | 701,452,884.05 | 486 | |
| WON | WON | 590,000,000.00 | 514 | |
| AFF-V25 | ArcFlow V25 | 100,000,000.00 | 1 | Sole holder — self-mint |
| SYNPLP | Synthra Perp Liquidity | 21,723,929.82 | 585 | LP receipt token |
| SYN | Synthra | 8,080,318.77 | 119,441 | Widely held |
| USDT | USDT | 2,356,364.53 | 154,412 | **Real stablecoin float** |
| WUSDC | Wrapped USDC | 234,613.65 | 577,756 | **Real stablecoin float** |
| WETH | WRAPPED ETHEREUM | 147,000.00 | 3 | Suspicious low holder count |
| USDC | USDC native | 12,000.00 | 3 | Suspicious low holder count |

Single-holder tokens with eight- or nine-figure balances are almost certainly
**self-deployed test mints**, not legitimate inventory. The economically
meaningful holdings are USDT, WUSDC, and (more cautiously) SYN/SYNPLP.

### Activity pattern (300 most recent transactions)

- **Time range:** 2026-05-15 09:27:03Z → 11:15:56Z (~108 minutes)
- **Direction:** 300 / 300 outbound — pure sender in the sample.
- **Cadence:** ~1 call every 22 seconds → automated.

| Method selector | Count | Target |
|---|---:|---|
| `0xaa3e079c` | 288 | `0xBBD7…40b` (router proxy) |
| `0x65c72805` | 7 | `0xb798…424c` |
| `0xc9c261d8` | 4 | various |
| `0xb97d4b6f` | 1 | `0x0270…dc22` (looks like an `addLiquidity` shape) |

### Decoded sample call

Tx `0x906ec2c5717b13f1029eff419f41f57ce572d9fe4d52c26b396cd50b7e05eb3f`
calls `0xaa3e079c` on `0xBBD7…40b`. Attached token transfers:

```
 in : 10,000,000 USDC raw  (= 10.000 USDC, 6 decimals)  wallet -> router
 out:        200            router -> 0xb499efCd
 out:      1,800            router -> 0xC06ebbef
 out:  9,998,000            router -> 0xFf70F4A1
 out:      2,999            0xFf70F4A1 -> 0x20F6ee51
 out:  9,995,001            0xFf70F4A1 -> 0x09AD820a
```

Pattern: ~10 USDC in, ~9.998 USDC out, with two small-bps slivers split off to
other addresses. Classic **swap-with-fee-split** routing (LP / protocol /
referrer cut). Gas burned per call: ~667k.

### Token-transfer side (400 sampled, ~37 minutes)

| Token | Count | Inbound | Outbound |
|---|---:|---:|---:|
| USDC | 272 | 3.86 | 0.00 |
| EURC | 81 | 1.85 | 0.00 |
| USDT | 40 | 1.31 | 0.00 |
| SYN | 6 | 0.01 | 0.00 |
| WUSDC | 1 | 0.00 | 0.00 |

All sampled transfers were inbound — likely the router-side settlement leg of
the wallet's own outbound calls. Individual values are small (median per-call
value ≪ 1 USDC), pointing toward a **micro-swap / fee-harvesting style bot**
rather than a directional trader.

### Takeaways

1. Automated DEX/swap bot churning USDC micro-trades against an unverified router.
2. The 100M-to-900M token positions are visual noise from self-minted test tokens.
3. The real working capital is USDT + WUSDC + USDC, sized in the low millions.

---

## Wallet 2 — `0x34e785eef1e465e5db4de4b47c1bb64d9c237742`

### Profile

- EOA, no contract code, no name/ENS, not flagged as scam.
- Native balance: **16.36 ARC** — modest, working-balance sized.
- Balance last updated at block 42,655,045.

### Notable token holdings (selection from ~30 ERC-20s)

| Symbol | Name | Balance | Holders | Notes |
|---|---|---:|---:|---|
| jefe | yeah | 1,000,000,000.00 | 1 | Self-deployed (`0x19Db…CcB8`) |
| jefe | yeah | 1,000,000,000.00 | 1 | Self-deployed (`0x37db…7523`) |
| 2 | one | 1,000,000,000.00 | 1 | Self-deployed (`0x24c1…5D2b`) |
| SV877 | Neon Core 3GHG | 7,647,256.00 | 1 | Self-deployed |
| VO253 | Plasma Vault FLT9 | 5,191,010.00 | 1 | Self-deployed |
| SV102 | Neon Circuit S3LL | 4,008,173.00 | 1 | Self-deployed |
| *(several others)* | various "Neon/Plasma/Flux/Turbo" vault tokens | 1M–10M | 1 each | Self-deployed test mints |
| EURC | EURC | 2,313.49 | 1,329,340 | **Real stablecoin float** |
| USDC | USDC (native) | 16.36 | 1,331,842 | **Real stablecoin float** |
| WUSDC | Wrapped USDC | 0.08 | 592,486 | Dust |

The pattern of single-holder, randomly-named tokens with millions in balance is
the same self-deployed-test-mint signature seen in Wallet 1.

### Activity pattern (300 most recent transactions)

- **Time range:** 2026-05-15 07:09:17Z → 2026-05-17 10:04:51Z (~51 hours)
- **Direction:** 300 / 300 outbound.
- **Cadence:** steady over two days (not a single burst, unlike Wallet 1).

| Method selector | Count | Target | Likely meaning |
|---|---:|---|---|
| `0xaa3e079c` | 252 | `0xBBD7…40b` (router) | same swap function as Wallet 1 |
| `0x095ea7b3` | 39 | EURC + USDC contracts | `approve(address,uint256)` — token approvals |
| `0x3df02124` | 3 | various | Curve-style `exchange(...)` |
| `0x1e59c529` | 3 | various | unknown |
| `0x2c39c058` | 3 | various | unknown |

### Token-transfer side (400 sampled, 51-hour window)

| Token | Count | Inbound | Outbound | Net |
|---|---:|---:|---:|---:|
| EURC | 199 | 66,070.27 | 66,148.85 | **−78.59** |
| USDC | 198 | 69,480.63 | 69,462.36 | **+18.27** |
| INAME | 3 | 0.00 | 0.00 | 0.00 |

- ~98% of inbound and outbound transfers go to/from `0xBBD7…40b` — the same
  router. This wallet is round-tripping USDC ⇄ EURC through it.
- Two-way volume of ~$135k closes with a sub-0.06% net delta on each leg —
  effectively **delta-neutral**.

### Takeaways

1. **USDC/EURC market-making or arbitrage bot.** Balanced two-way flow rules
   out directional trading.
2. Average ticket size (~$340) is ~30× larger than Wallet 1's (~$10) — this is
   a different strategy on the same plumbing.
3. The 39 `approve()` calls are routine token-allowance warm-ups for the
   router.

---

## Shared Infrastructure

Both wallets concentrate ~85–96% of their calls on the same target:

- **Router proxy:** `0xBBD70b01a1CAbC96d5b7b129AE1AaABdF50Dd40b`
  - EIP-1967 proxy, unverified
  - Implementation: `0xCeA69a03A998002296b5c6b089B94B2B498d8751` (also unverified)
- **Dominant function selector:** `0xaa3e079c` (not in default 4byte
  dictionaries; decoded input not surfaced by the explorer)

Neither contract is verified on the Arc-testnet explorer, so its purpose can
only be inferred from on-chain behavior. The observed shape — token in, slightly
less token out, with small slivers fanned to satellite addresses — is consistent
with a **multi-hop DEX router with split fees** (LP cut + protocol cut +
optional referrer/fee-recipient).

### Open follow-ups

If deeper attribution is needed:

1. Pull bytecode of `0xCeA69a03A998002296b5c6b089B94B2B498d8751` and disassemble
   the dispatcher to recover function selectors and identify the protocol.
2. Cross-reference the satellite recipients (e.g. `0xb499efCd…`, `0xC06ebbef…`,
   `0xFf70F4A1…`) to find an LP-token / fee-recipient cluster.
3. Expand the transaction sample beyond the first ~300 to estimate the bots'
   lifetime cumulative volume and uptime.
4. Check whether other Arc-testnet wallets hit the same `0xaa3e079c` selector —
   if it's a popular bot pattern, an aggregate cohort analysis is more useful
   than per-wallet drilldowns.

---

---

## Addendum — Follow-up Findings (2026-05-18)

The initial report flagged the router `0xBBD70b01a1CAbC96d5b7b129AE1AaABdF50Dd40b`
as an "unverified DEX router." Pulling the implementation bytecode and
disassembling its dispatcher fundamentally **revises that read**: the router
is a Circle-style multi-signer execution contract, the dominant call is a
signed instruction bundle, and the wallets are doing more than the original
~300-tx sample suggested.

### 1. The "router" is a multi-signer instruction executor (not a DEX)

Bytecode for impl `0xCeA69a03A998002296b5c6b089B94B2B498d8751` was fetched via
the Blockscout JSON-RPC endpoint (`/api/eth-rpc`, `eth_getCode`) and parsed
for `PUSH4 selector EQ` dispatcher entries. All **35 selectors** resolve via
the openchain.xyz 4byte database. Highlights:

| Selector | Function |
|---|---|
| `0xaa3e079c` | `execute(((address,bytes,uint256,address,uint256,address,uint256)[],(address,address)[],uint256,uint256,bytes),(uint8,address,uint256,bytes)[],bytes)` |
| `0xeb12d61e` | `addSigner(address)` |
| `0x0e316ab7` | `removeSigner(address)` |
| `0x7df73e27` | `isSigner(address)` |
| `0x7ca548c6` | `signerCount()` |
| `0xa4a4f390` | `signerThreshold()` |
| `0x251b8192` | `setSignerThreshold(uint256)` |
| `0x9fd0506d` | `pauser()` |
| `0x554bab3c` | `updatePauser(address)` |
| `0xa75f1a12` | `removePauser()` |
| `0x38a63183` | `rescuer()` |
| `0x2ab60045` | `updateRescuer(address)` |
| `0x0737d275` | `removeRescuer()` |
| `0xb2118a8d` | `rescueERC20(address,address,uint256)` |
| `0x1291f79d` | `rescueNative(address,uint256)` |
| `0x2b507df8` | `configurator()` |
| `0xb57873a5` | `updateConfigurator(address)` |
| `0x15333235` | `removeConfigurator()` |
| `0x9c8ded8a` | `isExecIdUsed(uint256)` |
| `0x977ad38c` | `maxInstructions()` |
| `0x27bf7e0b` | `maxTokenInputs()` |
| `0x84b0196e` | `eip712Domain()` |
| `0x1794bb3c` | `initialize(address,address,uint256)` |
| `0x79ba5097` / `0xe30c3978` / `0x92fede00` / `0x8da5cb5b` / `0xf2fde38b` / `0x715018a6` | Ownable2Step |
| `0x8456cb59` / `0x3f4ba83a` / `0x5c975abb` | Pausable |
| `0x31f7d964` | `NATIVE_TOKEN()` |

The combination — **threshold-signer admin set, `rescuer`/`pauser`/`configurator`
role triad, `rescueERC20`/`rescueNative`, EIP-712 typed data, `isExecIdUsed`
replay protection, capped instruction lists** — matches the
`FiatTokenV2 / CCTP TokenMessenger / Bridged USDC Standard` admin pattern
that Circle uses across its production contracts. The decoded `execute(...)`
signature is consistent with **a Gateway-style on-chain executor**: it takes
a batch of `(target, calldata, value, token, amount, recipient, fee)`
instructions plus an array of signer authorizations
`(v, signer, ?, signature)`, and atomically applies them after verifying the
threshold.

The proxy `0xBBD70b01a1CAbC96d5b7b129AE1AaABdF50Dd40b` is OpenZeppelin's
TransparentUpgradeableProxy v5. Its **proxy admin (immutable in the
preamble)** is the EOA `0x6a736b8dea7d4b18b881b7fc4fc16072f6018b7a` — almost
certainly the deployer / upgrade key for the Gateway on Arc testnet.

### 2. Settlement graph around the executor

For 30 sampled `execute()` calls from each wallet, the per-tx token-transfer
graph is highly repetitive. Profile of recurring counterparties:

| Address | Code size | Blockscout label | Role inferred from flow |
|---|---:|---|---|
| `0x913dc46f…c9a8` | 18,095 B | **"USDC/cirBTC"** | Liquidity pool (named pair) |
| `0x09AD820a…4Afa` | 7,570 B | — | Pool / hub router |
| `0x20F6ee51…860c` | 8,679 B | — | Pool / hub router |
| `0xFf70F4A1…04b2` | 254 B | — | Minimal forwarder / clone receiver |
| `0xb499efCd…0320` | 0 B | — | Fee-recipient EOA (~0.002% / trade) |
| `0xC06eBbeF…264b` | 0 B | — | Fee-recipient EOA (~0.018% / trade) |
| `0x311d3f55…e956` | 23,635 B | **"EllySalvador"** | End-user smart account |
| `0x0714027e…4c24` | 23,635 B | **"WUSDC/EURC"** | End-user smart account |
| `0xbbc2a38a…6f6e` | 23,635 B | **"as"** | End-user smart account |
| `0x269b4797…fcfe` | 23,635 B | **"arc"** | End-user smart account |

The four 23,635-byte addresses all carry **identical bytecode** but were
flagged `is_contract: false` by Blockscout — a misclassification. They are
factory-deployed smart-account clones (one common implementation, many
per-user instances) with user-supplied display names. The 0-byte recipients
`0xb499efCd…` and `0xC06eBbeF…` collect ≈0.020% combined fee per swap.

### 3. cirBTC is in the loop

Sampled `execute()` token transfers for Wallet 1 included **both USDC and
cirBTC** legs (90 cirBTC transfers across 30 sampled txs). Wallet 1's true
trade pair is **USDC ↔ cirBTC** through the named `0x913dc46f` pool — not
USDC ⇄ USDC. The earlier interpretation as "USDC micro-swap fee harvesting"
was an artifact of the address-level token-transfer endpoint returning only
the wallet-facing leg.

### 4. Cumulative activity is two orders of magnitude larger than the initial sample

Deep pagination (~80 pages each, capped by the Blockscout backend at the
furthest reaches):

| | Wallet 1 (`0x6063…3e305`) | Wallet 2 (`0x34e7…7742`) |
|---|---|---|
| First tx | **2025-10-28 13:40 Z** | **2025-11-05 21:07 Z** |
| Last tx in sample | 2026-05-18 07:14 Z | 2026-05-17 10:04 Z |
| Active span | ~6.7 months | ~6.4 months |
| Total txs fetched | **2,837** | **3,099** |
| Native gas burned | **~85.4 ARC** | **~43.0 ARC** |
| `execute()` calls (`0xaa3e079c`) | 1,721 | 1,563 |
| `approve()` calls (`0x095ea7b3`) | — | **1,357** |

So Wallet 1's "burst" we saw in the initial 300-tx slice (~108 minutes on
2026-05-15) was one episode of a 6+ month activity history.

### 5. Wallet 1 is a multi-protocol trader, not a single-router bot

The deep sample exposes function selectors the 300-tx window missed:

| Selector | Function | W1 calls |
|---|---|---:|
| `0xaa3e079c` | Gateway `execute(...)` | 1,721 |
| `0x3593564c` | **Uniswap Universal Router `execute(bytes,bytes[],uint256)`** | 436 |
| `0xac9650d8` | `multicall(bytes[])` | 91 |
| `0xde26fdcd` | **`createIncreaseOrder(...)` (GMX-/Synthra-style perpetual)** | 78 |
| `0x97701f19` | **`createDecreaseOrder(...)` (perpetual close)** | 53 |
| `0xc9c261d8` | `cancelCloseOrder(uint256)` | 4 |

Wallet 1 routes through (a) the Circle Gateway executor, (b) a Uniswap
Universal Router, **and** (c) a GMX-style perp DEX (likely Synthra given the
SYNPLP and SYN holdings flagged in the initial report). Wallet 2, by
contrast, is far simpler: ~50/50 split between Gateway `execute()` and ERC-20
`approve()` warm-ups, with a long tail of dust.

### 6. Wallet 2's true cumulative volume

Aggregating all paginated token transfers (3,223 records, full history fits
in pagination):

| Token | In | Out | Net | Two-way |
|---|---:|---:|---:|---:|
| USDC | **646,205.41** | **646,333.98** | −128.57 | ~$1.29M |
| EURC | 591,028.32 | 588,714.83 | **+2,313.49** | ~$1.18M |
| WUSDC | 0.42 | 0.35 | +0.075 | dust |

Two-way stablecoin volume across the wallet's lifetime is **~$2.47M**. Net
EURC delta (+2,313.49) **exactly equals** the current EURC balance
reported in section 2 of the original report — confirming the pagination
captured the full history. Net USDC delta is essentially zero (−$128 across
$1.29M turnover, ≈0.01%).

This refines the strategy hypothesis: **Wallet 2 is a delta-neutral
USDC/EURC market-making / arbitrage bot** (already the original read), now
attributable to a verified $2.47M lifetime two-way volume on a multi-signer
settlement rail — not a DEX. The thin loss (~$130) is plausibly cumulative
spread/fees over ~3,000 swaps, which matches a ≈1 bp fee level.

### 7. Cohort context

A small (60-tx) random sample of recent `execute()` calls to the router
yielded **43 distinct initiators**. The router is broadly used — Wallet 1
and Wallet 2 are part of a multi-wallet user base, not the sole callers.
Top initiators in the sample (none of which are our two wallets) appear
between 1 and 7 times each, with no clear "dominant" sender, suggesting an
open Gateway rail rather than a captive bot setup.

### 8. Revised one-line characterizations

- **`0x6063e834…3e305`** — Multi-protocol bot active since 2025-10-28: routes
  Gateway `execute()` payloads, Uniswap Universal Router swaps, and GMX-style
  perp orders against an Arc-testnet DEX cluster that includes a named
  **USDC/cirBTC pool**. Holdings dominated by self-minted test tokens; real
  stablecoin/cirBTC float is the working capital.
- **`0x34e785ee…7742`** — Delta-neutral USDC ⇄ EURC arbitrage / market-making
  bot active since 2025-11-05. ~$2.47M lifetime two-way volume through the
  Circle-style Gateway executor with near-zero net P&L, exactly matching the
  bot's current EURC balance of 2,313.49.

---

## Methodology Notes

- All data was retrieved through the public Blockscout API v2 at
  `https://arc-testnet-explorer.stg.blockchain.circle.com/api/v2/`.
- Transactions and token-transfers were sampled by paginating up to 6–8 pages
  (≈300 txs, ≈400 transfers) per wallet. Counts are sample-bounded, not
  lifetime totals.
- The on-explorer `counters` aggregate is currently unreliable for both
  wallets; sampled data is treated as ground truth.
- Token amounts are decimal-adjusted using each token contract's declared
  `decimals`. USDC/USDT/EURC are treated as 6-decimal; most everything else as
  18-decimal.
