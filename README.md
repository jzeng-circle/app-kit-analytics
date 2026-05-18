# app-kit-analytics

Umbrella project for App Kit / on-chain analytics work. Each analysis lives in
its own folder under `reports/` with self-contained working files and final
deliverables. Reusable infrastructure (Blockscout client, selector lookup,
future shared helpers) lives under `tools/`.

## Layout

```
app-kit-analytics/
├── tools/                          # shared code reused across reports
│   ├── arc_explorer/               # Arc-testnet Blockscout REST + JSON-RPC client
│   │   ├── client.py
│   │   ├── selectors.py
│   │   └── README.md
│   └── common/                     # placeholder for future shared helpers
└── reports/
    ├── custom-fee/                 # App Kit Custom Fee Analytics
    │   ├── README.md
    │   ├── report.md
    │   └── data/                   # CSV exports backing the report
    ├── app-kit-launch-feedback/    # GitHub adoption + Twitter response
    │   ├── README.md
    │   ├── github-repos-report.md
    │   ├── twitter-feedback-report.md
    │   └── data/                   # raw Twitter export
    ├── bridge-kit-usage/           # On-chain usage analysis (Oct 2025 - Mar 2026)
    │   ├── README.md
    │   ├── report.md               # main investigative report
    │   ├── revised-phase-analysis.md
    │   ├── report.html
    │   ├── charts/                 # 19 PNGs
    │   └── data/                   # raw CSVs (full + phase splits)
    └── arc-testnet-wallets/        # Arc Testnet wallet behavioral analysis
        ├── README.md
        ├── report.md               # narrative + addendum
        ├── report.html             # standalone HTML render
        ├── working/                # scripts and intermediate artifacts
        │   ├── fetch_wallet_data.py
        │   ├── arc_impl_selectors.txt
        │   └── arc_satellite_recipients.txt
        └── data/                   # cached API responses (empty by default)
```

## Reports

| Report | Subject | Status |
|---|---|---|
| [custom-fee](reports/custom-fee/README.md) | App Kit custom-fee adoption across Swap Kit + Bridge Kit, testnet + mainnet. | Snapshot as of 2026-05-08. |
| [app-kit-launch-feedback](reports/app-kit-launch-feedback/README.md) | GitHub adoption + Twitter response to the App Kit launch on 2026-04-10. | Snapshots as of 2026-04-14. |
| [bridge-kit-usage](reports/bridge-kit-usage/README.md) | On-chain BridgeKit usage analysis (Oct 2025–Mar 2026). Separates a December whale spike from organic adoption; cross-validated with PCA / K-means / logistic regression. | Snapshot as of 2026-03-16. |
| [arc-testnet-wallets](reports/arc-testnet-wallets/README.md) | Behavioral analysis of two automated wallets on Arc Public Testnet, plus the Gateway-style executor they hit. | Snapshot as of 2026-05-18 with follow-up addendum. |

## Adding a new report

1. Create `reports/<short-name>/` with this skeleton:
   ```
   reports/<short-name>/
     README.md          # one-page index: subject, files, headline findings
     report.md          # main deliverable
     working/           # scripts, notebooks, intermediate exports
     data/              # raw/cached inputs (gitignore if large)
   ```
2. Reuse anything in `tools/` rather than copy-pasting. If you need a helper
   that two reports would both use, add it under `tools/` instead of putting
   it in the report's `working/`.
3. List the new report in the table above.

## Shared tools

- **`tools/arc_explorer`** — Blockscout REST + JSON-RPC client for the Arc
  Public Testnet explorer, plus selector extraction and 4byte lookup. See
  [tools/arc_explorer/README.md](tools/arc_explorer/README.md) for the public
  API.

## Skills

- **`.claude/skills/bridgekit-phase-analysis.md`** — methodology for
  separating organic from event-driven activity in BridgeKit-style usage
  data. Backs the `bridge-kit-usage` report and is invocable from Claude
  Code in this project.

## Running scripts

Scripts under `reports/<name>/working/` assume the repo root is on
`sys.path`. Run them from the repo root:

```bash
cd ~/app-kit-analytics
python3 reports/arc-testnet-wallets/working/fetch_wallet_data.py
```
