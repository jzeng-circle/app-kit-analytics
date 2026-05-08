# App Kit Custom Fee Analytics

Analysis of the custom fee feature across Circle's Swap Kit and Bridge Kit products.

## Report

`appkit_fee_full_report.md` — main report covering fee adoption, fee tier distribution, and Circle fee collections across testnet and mainnet for Swap Kit and Bridge Kit, with within-product analysis for each.

## Data

| File | Description |
|---|---|
| `data/swap_testnet_txns.csv` | Swap Kit testnet — 10,000 txns (arc_testnet + 24 mainnet chain rows), 1,820 wallets |
| `data/swap_mainnet_txns.csv` | Swap Kit mainnet — 56 txns across base, arbitrum, ethereum, solana, 22 wallets |
| `data/bridge_mainnet_txns.csv` | Bridge Kit mainnet — 4,452 txns across 19 destination chains (full dataset) |
| `data/bridge_testnet_txns.csv` | Bridge Kit testnet — 10,000 txns (arc_testnet, arbitrum_sepolia, polygon_amoy) |

The bridge mainnet export does not include `block_timestamp` or source `blockchain`, so monthly trend and source-chain breakdown are unavailable.

**Note on wallet stats**: Wallet-level statistics (unique wallet counts, per-wallet fee concentration) are not reported for bridge data — the address fields in the bridge exports do not reliably identify a unique developer or end-user, so those numbers are not accurate. Wallet stats are reported for swap.
