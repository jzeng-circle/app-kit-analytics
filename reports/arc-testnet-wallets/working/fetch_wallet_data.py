"""Reproduce the data behind the Arc-testnet wallet analysis.

Run from the repo root so `tools` is importable:

    cd ~/app-kit-analytics
    python reports/arc-testnet-wallets/working/fetch_wallet_data.py

Prints a structured summary for each wallet plus router/impl info. Designed as
both a worked example of the shared `tools.arc_explorer` client and as a way
to refresh the report if Arc-testnet state shifts.
"""

from __future__ import annotations

import collections
import decimal
import json
import os
import sys
from pathlib import Path

# Make repo-root imports work whether the script is run from anywhere
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.arc_explorer import client, selectors  # noqa: E402

D = decimal.Decimal
ME_WALLETS = {
    "wallet_1": "0x6063e834928EaC1ca47ac5Da27838079a103e305",
    "wallet_2": "0x34e785eef1e465e5db4de4b47c1bb64d9c237742",
}
ROUTER = "0xBBD70b01a1CAbC96d5b7b129AE1AaABdF50Dd40b"


def summarize_wallet(label: str, addr: str, max_pages: int = 60) -> dict:
    ov = client.address(addr)
    txs = client.paginate_address(addr, "transactions", max_pages=max_pages)
    tts = client.paginate_address(addr, "token-transfers", max_pages=max_pages)

    me = addr.lower()
    methods = collections.Counter((t.get("method") or "none") for t in txs)

    # Token-transfer aggregates
    sym_in, sym_out, sym_cnt = collections.Counter(), collections.Counter(), collections.Counter()
    for t in tts:
        tok = t.get("token") or {}
        sym = tok.get("symbol") or (tok.get("address_hash", "")[:10])
        dec = int(tok.get("decimals") or "18")
        val = D((t.get("total") or {}).get("value", "0")) / (D(10) ** dec)
        sym_cnt[sym] += 1
        if (t.get("from") or {}).get("hash", "").lower() == me:
            sym_out[sym] += val
        if (t.get("to") or {}).get("hash", "").lower() == me:
            sym_in[sym] += val

    fees_wei = D(0)
    for t in txs:
        try:
            fees_wei += D((t.get("fee") or {}).get("value") or "0")
        except Exception:
            pass

    return {
        "label": label,
        "address": addr,
        "is_contract": ov.get("is_contract"),
        "coin_balance_raw": ov.get("coin_balance"),
        "tx_count_sampled": len(txs),
        "tt_count_sampled": len(tts),
        "tx_time_range": (txs[-1]["timestamp"], txs[0]["timestamp"]) if txs else None,
        "method_top": methods.most_common(10),
        "tt_per_token": [
            (s, sym_cnt[s], float(sym_in[s]), float(sym_out[s])) for s, _ in sym_cnt.most_common(10)
        ],
        "native_fees_wei": str(fees_wei),
    }


def inspect_router() -> dict:
    ov = client.address(ROUTER)
    impl = (ov.get("implementations") or [{}])[0].get("address_hash")
    impl_bc = client.eth_get_code(impl) if impl else ""
    sels = selectors.extract_from_bytecode(impl_bc)
    names = selectors.lookup(sels) if sels else {}
    return {
        "proxy": ROUTER,
        "impl": impl,
        "proxy_type": ov.get("proxy_type"),
        "impl_bytecode_size": (len(impl_bc) - 2) // 2 if impl_bc else 0,
        "selectors": names,
    }


def main() -> None:
    out = {"router": inspect_router()}
    for label, addr in ME_WALLETS.items():
        out[label] = summarize_wallet(label, addr)
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
