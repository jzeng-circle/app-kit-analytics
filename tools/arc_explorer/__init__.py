"""Shared client for the Arc testnet Blockscout explorer.

Reports that need on-chain data from Arc Public Testnet should import from
this package rather than re-implementing pagination, RPC, or 4byte lookups.

    from tools.arc_explorer import client, selectors

    addr = client.address("0x6063e834928EaC1ca47ac5Da27838079a103e305")
    txs  = client.paginate_address(addr["hash"], "transactions", max_pages=20)
    names = selectors.lookup(["0xaa3e079c", "0x095ea7b3"])
"""

from . import client, selectors  # noqa: F401

__all__ = ["client", "selectors"]
