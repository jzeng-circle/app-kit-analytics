# App Kit Custom Fee Analytics

Analysis of the custom fee feature across Circle's Swap Kit and Bridge Kit products.

## Report

`appkit_fee_full_report.md` — main report covering fee adoption, fee tier distribution, Circle fee collections, and wallet concentration across testnet and mainnet for both products.

## Data

| File | Description |
|---|---|
| `data/swap_testnet_txns.csv` | Swap Kit testnet — 10,000 txns (arc_testnet + 24 mainnet chain rows), 1,820 wallets |
| `data/swap_mainnet_txns.csv` | Swap Kit mainnet — 56 txns across base, arbitrum, ethereum, solana, 22 wallets |
| `data/bridge_mainnet_txns.csv` | Bridge Kit mainnet — 10,000 txns across 11 chains, enriched with resolved wallet addresses |
| `data/bridge_testnet_txns.csv` | Bridge Kit testnet — 1,000 txns (arbitrum_sepolia, polygon_amoy), includes dev_address |

## Scripts

`scripts/fetch_bridge_wallets.py` — fetches transaction sender addresses from public EVM and Solana RPCs for bridge mainnet transactions. Reads `archive/bridge_mainnet_raw.csv`, writes `data/bridge_mainnet_txns.csv`. Coverage: 950/1,080 fee-bearing txns (88%); SOL, CODEX, PLUME, SEI unresolved due to no reliable public RPC.

## Archive

Superseded data and earlier draft reports. The raw bridge mainnet CSV (before wallet resolution) is kept here as the source input for the fetch script.
