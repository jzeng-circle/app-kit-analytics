# Arc Testnet Wallet Analysis

Behavioral analysis of two automated wallets on Circle's Arc Public Testnet,
covering activity profile, holdings, and the Gateway-style multi-signer
execution contract they share.

## Files

| Path | Description |
|---|---|
| `report.md` | Main report (Markdown). Initial findings plus an addendum with follow-up findings dated 2026-05-18. |
| `report.html` | Same content, standalone HTML with inline styling. |
| `working/fetch_wallet_data.py` | Reproduces the data using the shared `tools.arc_explorer` client. |
| `working/arc_impl_selectors.txt` | Disassembled dispatcher selectors for impl `0xCeA69a03A998002296b5c6b089B94B2B498d8751`. |
| `working/arc_satellite_recipients.txt` | Frequent token-transfer recipients across sampled `execute()` calls. |
| `data/` | Cached API responses (empty by default; populated by the working script if you wire caching in). |

## Subjects

- `0x6063e834928EaC1ca47ac5Da27838079a103e305`
- `0x34e785eef1e465e5db4de4b47c1bb64d9c237742`

## Headline findings

- The contract both wallets hit (`0xBBD70b01a1CAbC96d5b7b129AE1AaABdF50Dd40b`)
  is a **Circle-style multi-signer instruction executor**, not a DEX router.
  Disassembly recovered all 35 dispatcher selectors;
  `0xaa3e079c` decodes to a signed
  `execute((tuple[],tuple[],uint256,uint256,bytes),(uint8,address,uint256,bytes)[],bytes)`
  bundle. Admin set matches Circle's `FiatTokenV2`/`TokenMessenger` pattern
  (`rescuer`/`pauser`/`configurator`, `rescueERC20`/`rescueNative`,
  `isExecIdUsed`).
- Wallet `0x6063…3e305` is a **multi-protocol bot** active since 2025-10-28
  (2,837 txs sampled): Gateway `execute()` + Uniswap Universal Router
  `execute(bytes,bytes[],uint256)` + GMX/Synthra-style
  `createIncreaseOrder` / `createDecreaseOrder`. Real counter-asset is
  **cirBTC**, traded against USDC through the named pool `0x913dc46f`
  ("USDC/cirBTC").
- Wallet `0x34e7…7742` is a **delta-neutral USDC ⇄ EURC** market-maker /
  arbitrage bot active since 2025-11-05. Lifetime two-way volume **~$2.47M**
  (USDC $1.29M, EURC $1.18M). Net EURC delta exactly matches the current EURC
  balance of 2,313.49 — pagination captured the full history.

See `report.md` for the full narrative and the addendum for the follow-up
investigations (bytecode disassembly, settlement graph, deep cumulative
volume, cohort breadth).

## Reproducing

```bash
cd ~/app-kit-analytics
python reports/arc-testnet-wallets/working/fetch_wallet_data.py
```

Numbers will drift over time as the wallets keep trading. The report's
absolute counts are snapshots, not live values.
