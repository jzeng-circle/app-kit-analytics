"""
Fetch wallet addresses (tx sender) for bridge transactions using public RPCs.
Reads archive/bridge_mainnet_raw.csv, writes data/bridge_mainnet_txns.csv.
"""
import csv
import json
import time
import urllib.request
from collections import defaultdict

INPUT_FILE = "archive/bridge_mainnet_raw.csv"
OUTPUT_FILE = "data/bridge_mainnet_txns.csv"

HEADERS = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

EVM_RPCS = {
    "ETH":        "https://1rpc.io/eth",
    "ARB":        "https://1rpc.io/arb",
    "BASE":       "https://1rpc.io/base",
    "POLYGON":    "https://1rpc.io/matic",
    "AVAX":       "https://api.avax.network/ext/bc/C/rpc",
    "OP":         "https://mainnet.optimism.io",
    "LINEA":      "https://rpc.linea.build",
    "SONIC":      "https://rpc.soniclabs.com",
    "HYPEREVM":   "https://rpc.hyperliquid.xyz/evm",
    "INK":        "https://rpc-gel.inkonchain.com",
    "XDC":        "https://rpc.xdcrpc.com",
    "UNICHAIN":   "https://mainnet.unichain.org",
    "WORLDCHAIN": "https://worldchain-mainnet.g.alchemy.com/public",
    # SEI, PLUME, CODEX — no working public RPC found; skipped
}

SOL_RPC = "https://api.mainnet-beta.solana.com"


def rpc_post(url, payload_obj, timeout=20):
    data = json.dumps(payload_obj).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"      RPC error: {e}")
        return None


def evm_fetch(rpc_url, tx_hashes):
    """Batch fetch tx senders. Returns {hash: from}."""
    out = {}
    batch_size = 50
    for i in range(0, len(tx_hashes), batch_size):
        batch = tx_hashes[i:i + batch_size]
        # id = index within this batch, used to map response back to input hash
        payload = [
            {"jsonrpc": "2.0", "id": j, "method": "eth_getTransactionByHash", "params": [h]}
            for j, h in enumerate(batch)
        ]
        resp = rpc_post(rpc_url, payload)
        if resp is None:
            continue
        if not isinstance(resp, list):
            resp = [resp]
        # Sort by id to align with batch order
        resp_by_id = {item["id"]: item for item in resp if isinstance(item, dict) and "id" in item}
        for j, original_hash in enumerate(batch):
            item = resp_by_id.get(j)
            if not item:
                continue
            tx = item.get("result")
            if tx and isinstance(tx, dict) and tx.get("from"):
                out[original_hash.lower()] = tx["from"].lower()
        time.sleep(0.15)
    return out


def sol_fetch(tx_sigs):
    """Fetch Solana transaction senders one at a time to avoid rate limits. Returns {sig: from}."""
    out = {}
    for sig in tx_sigs:
        payload = {"jsonrpc": "2.0", "id": 1, "method": "getTransaction",
                   "params": [sig, {"encoding": "json", "maxSupportedTransactionVersion": 0}]}
        resp = rpc_post(SOL_RPC, payload, timeout=20)
        if not resp:
            time.sleep(1)
            continue
        tx = resp.get("result")
        if tx:
            try:
                keys = tx["transaction"]["message"]["accountKeys"]
                from_addr = keys[0] if isinstance(keys[0], str) else keys[0].get("pubkey", "")
                if from_addr:
                    out[sig] = from_addr
            except (KeyError, IndexError, TypeError):
                pass
        time.sleep(0.4)
    return out


def main():
    rows = []
    with open(INPUT_FILE) as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    fee_rows = [r for r in rows if float(r.get("bridge_kit_fee_circle_collected") or 0) > 0]
    print(f"Total rows: {len(rows)}, fee-bearing: {len(fee_rows)}")

    chain_txns = defaultdict(list)
    for r in fee_rows:
        chain_txns[r["blockchain"]].append(r["source_tx_hash"])

    hash_to_wallet = {}

    for chain, hashes in sorted(chain_txns.items()):
        if chain == "SOL":
            continue
        rpc = EVM_RPCS.get(chain)
        if not rpc:
            print(f"  [{chain:12s}] {len(hashes):3d} txns — no RPC, skipping")
            continue
        print(f"  [{chain:12s}] {len(hashes):3d} txns — fetching...", end=" ", flush=True)
        result = evm_fetch(rpc, hashes)
        hash_to_wallet.update(result)
        print(f"resolved {len(result)}/{len(hashes)}")

    if "SOL" in chain_txns:
        hashes = chain_txns["SOL"]
        print(f"  [{'SOL':12s}] {len(hashes):3d} txns — fetching...", end=" ", flush=True)
        result = sol_fetch(hashes)
        hash_to_wallet.update(result)
        print(f"resolved {len(result)}/{len(hashes)}")

    resolved = sum(
        1 for r in fee_rows
        if hash_to_wallet.get(r["source_tx_hash"].lower()) or hash_to_wallet.get(r["source_tx_hash"])
    )
    print(f"\nTotal resolved: {resolved}/{len(fee_rows)} fee-bearing txns")

    out_fieldnames = list(fieldnames) + ["from_wallet"]
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fieldnames)
        writer.writeheader()
        for row in rows:
            tx = row["source_tx_hash"]
            row["from_wallet"] = hash_to_wallet.get(tx.lower()) or hash_to_wallet.get(tx) or ""
            writer.writerow(row)

    print(f"Written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
