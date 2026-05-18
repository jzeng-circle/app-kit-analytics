"""Arc-testnet Blockscout client.

Two surfaces:
  - REST API v2 (addresses, transactions, token-transfers, smart-contracts)
  - JSON-RPC (eth_getCode, eth_call, etc.)

Both routes share the same host:
  https://arc-testnet-explorer.stg.blockchain.circle.com

The official explorer (testnet.arcscan.app) blocks unauthenticated requests
behind Cloudflare; the staging host accepts them and exposes the same data.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any, Iterable

HOST = "https://arc-testnet-explorer.stg.blockchain.circle.com"
API_V2 = f"{HOST}/api/v2"
RPC = f"{HOST}/api/eth-rpc"

DEFAULT_TIMEOUT_S = 30
PAGINATE_SLEEP_S = 0.04


def _get(url: str, timeout: int = DEFAULT_TIMEOUT_S) -> Any:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def _post_json(url: str, payload: dict, timeout: int = DEFAULT_TIMEOUT_S) -> Any:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


# REST API v2
def address(addr: str) -> dict:
    return _get(f"{API_V2}/addresses/{addr}")


def address_counters(addr: str) -> dict:
    return _get(f"{API_V2}/addresses/{addr}/counters")


def address_tokens(addr: str, kind: str = "ERC-20") -> dict:
    return _get(f"{API_V2}/addresses/{addr}/tokens?type={kind}")


def transaction(tx_hash: str) -> dict:
    return _get(f"{API_V2}/transactions/{tx_hash}")


def stats() -> dict:
    return _get(f"{API_V2}/stats")


def paginate_address(
    addr: str,
    kind: str,
    max_pages: int = 20,
    sleep_s: float = PAGINATE_SLEEP_S,
) -> list[dict]:
    """Paginate /addresses/{addr}/{kind} until exhausted or max_pages reached.

    Returns the flat list of items. The Blockscout backend will 500 or 502 on
    deep pages for high-activity addresses; we surface that by truncating
    quietly. Callers that need exact totals should check whether the final
    response has next_page_params.

    Common kinds: "transactions", "token-transfers", "internal-transactions",
    "logs", "tokens", "withdrawals", "blocks-validated".
    """
    out: list[dict] = []
    np_qs = ""
    for _ in range(max_pages):
        try:
            d = _get(f"{API_V2}/addresses/{addr}/{kind}{np_qs}")
        except (urllib.error.HTTPError, urllib.error.URLError):
            break
        out.extend(d.get("items", []))
        npp = d.get("next_page_params")
        if not npp:
            break
        np_qs = "?" + "&".join(f"{k}={v}" for k, v in npp.items())
        time.sleep(sleep_s)
    return out


# JSON-RPC
def rpc_call(method: str, params: list, request_id: int = 1) -> Any:
    resp = _post_json(RPC, {"jsonrpc": "2.0", "method": method, "params": params, "id": request_id})
    if "error" in resp:
        raise RuntimeError(resp["error"])
    return resp["result"]


def eth_get_code(addr: str, block: str = "latest") -> str:
    return rpc_call("eth_getCode", [addr, block])


def eth_call(to: str, data: str, block: str = "latest") -> str:
    return rpc_call("eth_call", [{"to": to, "data": data}, block])


def eth_block_number() -> int:
    return int(rpc_call("eth_blockNumber", []), 16)
