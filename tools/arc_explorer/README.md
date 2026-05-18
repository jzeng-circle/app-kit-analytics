# arc_explorer

Shared Python client for the Arc Public Testnet Blockscout explorer. Used by
every report that needs on-chain data from Arc.

Hosts:
- REST API v2: `https://arc-testnet-explorer.stg.blockchain.circle.com/api/v2`
- JSON-RPC: `https://arc-testnet-explorer.stg.blockchain.circle.com/api/eth-rpc`

> The official explorer (`testnet.arcscan.app`) returns 403 to unauthenticated
> requests. The staging host accepts them and exposes the same data.

## Why this exists

Blockscout endpoints have a few sharp edges that every report would otherwise
re-discover:
- The `/addresses/{addr}/counters` aggregate returns 0 for many busy
  addresses — treat it as unreliable, paginate transactions/transfers instead.
- Deep pagination eventually 500s on the busiest addresses; the client
  truncates quietly rather than raising.
- Bytecode is exposed via `eth_getCode` over RPC, not via the REST
  `/smart-contracts/{addr}` endpoint (which returns an empty string for
  unverified contracts).

## Usage

```python
from tools.arc_explorer import client, selectors

# Address overview
ov = client.address("0x6063e834928EaC1ca47ac5Da27838079a103e305")
print(ov["coin_balance"], ov["is_contract"], ov["proxy_type"])

# Deep paginate all transactions or token-transfers
txs = client.paginate_address(ov["hash"], "transactions", max_pages=80)
tts = client.paginate_address(ov["hash"], "token-transfers", max_pages=80)

# Pull bytecode and recover dispatcher selectors
impl_bc = client.eth_get_code("0xCeA69a03A998002296b5c6b089B94B2B498d8751")
sels    = selectors.extract_from_bytecode(impl_bc)
names   = selectors.lookup(sels)
for sel, name in names.items():
    print(sel, name)
```

## Public API

`client`:
- `address(addr)` → overview JSON
- `address_counters(addr)` → counts (unreliable)
- `address_tokens(addr, kind="ERC-20")` → holdings
- `transaction(hash)` → tx detail incl. attached token_transfers
- `paginate_address(addr, kind, max_pages=20)` → flat list
- `stats()` → chain stats
- `rpc_call(method, params)` → raw JSON-RPC
- `eth_get_code(addr)`, `eth_call(to, data)`, `eth_block_number()`

`selectors`:
- `extract_from_bytecode(bytecode)` → sorted list of unique 8-char selectors
- `lookup(selectors)` → `{ "0x<sel>": "name(...)" }` via openchain.xyz

## Where this fits

Each report under `reports/<name>/` imports from `tools.arc_explorer`. Reports
should not duplicate API logic — if something is missing here, add it here,
not in the report's working/ folder.
