"""Function-selector helpers.

- extract_from_bytecode: find PUSH4 selector EQ entries in a contract's runtime
  dispatcher (the standard Solidity dispatch pattern).
- lookup: resolve 0x-prefixed selectors to human-readable signatures via the
  openchain.xyz signature database (no auth needed).
"""

from __future__ import annotations

import json
import re
import urllib.request
from typing import Iterable

OPENCHAIN_LOOKUP = "https://api.openchain.xyz/signature-database/v1/lookup"
DISPATCH_PATTERN = re.compile(r"63([0-9a-f]{8})14")


def extract_from_bytecode(bytecode: str) -> list[str]:
    """Return sorted, unique 8-char selectors (no 0x prefix) from a dispatcher.

    Matches the Solidity `DUP1 PUSH4 sel EQ` shape (`80 63 XX XX XX XX 14`).
    This catches every selector in the standard linear if-else dispatcher and
    most jump-table dispatchers used by modern Solidity. Contracts using
    non-standard dispatchers (e.g. mapping-based routing) may return 0.
    """
    if not bytecode or bytecode == "0x":
        return []
    return sorted(set(DISPATCH_PATTERN.findall(bytecode.lower())))


def lookup(selectors: Iterable[str], filter_pruned: bool = True) -> dict[str, str]:
    """Resolve 4-byte selectors to their first-known signature.

    Accepts selectors with or without '0x' prefix. Returns a dict mapping the
    0x-prefixed selector to its best signature, or '?' when no match exists.
    """
    norm = []
    for s in selectors:
        s = s.lower()
        if not s.startswith("0x"):
            s = "0x" + s
        norm.append(s)
    if not norm:
        return {}
    ids = ",".join(norm)
    flt = "true" if filter_pruned else "false"
    url = f"{OPENCHAIN_LOOKUP}?function={ids}&filter={flt}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read())
    fmap = (data.get("result") or {}).get("function") or {}
    out: dict[str, str] = {}
    for s in norm:
        hits = fmap.get(s) or []
        out[s] = hits[0]["name"] if hits else "?"
    return out
