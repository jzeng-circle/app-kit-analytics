# App Kit Custom Fee Feature — Usage Report
**Data source**: `appkitusage_20260505_012612.csv`
**Generated**: 2026-05-05
**Total wallets in dataset**: 2,343 across 5 chains (arc_testnet 99.3%, base, arbitrum, ethereum, solana)

---

## 1. Feature Adoption

| Segment | Wallets | Share |
|---|---|---|
| Used custom fee (Circle collected fee > $0) | 2,153 | 91.9% |
| Did not use custom fee (fee = $0) | 187 | 8.0% |
| **Total** | **2,343** | |

**91.9% of wallets have some fee collected by Circle**, indicating broad adoption of the custom fee feature. However, the depth of usage varies significantly — see Section 2.

---

## 2. Fee Level Distribution

Fee rates are back-calculated from: `dev_fee_rate = Circle Fee / (Volume × 10%)`.

| Fee Tier | Wallets | Transactions | Volume | Circle Fee Collected | Dev Fee (est.) |
|---|---|---|---|---|---|
| <2 bps (<0.02%) | 1,642 | 18,018 | $1,148,717 | $1.03 | $10.30 |
| 2–5 bps (0.02–0.05%) | 196 | 652 | $65,024 | $1.32 | $13.23 |
| 5–10 bps (0.05–0.10%) | 19 | 280 | $11,240 | $0.79 | $7.88 |
| 10–20 bps (0.10–0.20%) | 62 | 733 | $275,031 | $34.19 | $341.86 |
| 20–30 bps (0.20–0.30%) | 76 | 687 | $444,695 | $105.64 | $1,056.38 |
| 30–40 bps (0.30–0.40%) | 32 | 271 | $76,881 | $26.84 | $268.45 |
| 40–50 bps (0.40–0.50%) | 35 | 292 | $249,900 | $115.36 | $1,153.65 |
| 50+ bps (>0.50%) | 91 | 337 | $31,563 | $16.24 | $162.44 |
| **Total** | **2,153** | **21,270** | **$2,303,052** | **$301.42** | **$3,014.19** |

### Key observations

**The <2 bps cluster (1,642 wallets) is likely not deliberate fee configuration.** These wallets have 1–4 transactions each with tiny volumes (typically under $50/wallet), producing fee rates that are effectively rounding noise. They collectively generate only $1.03 in Circle fees — 0.3% of total — despite representing 70% of fee-paying wallets. These likely reflect test activity or end-user wallets transacting at a fixed minimum fee.

**The meaningful fee configurers are the 315 wallets using 10 bps or higher.** This group generates $298.28 (99.0%) of all Circle fees and operates with clear, deliberate fee bands.

---

## 3. Most Common Fee Levels Among Active Configurers

Among the 315 wallets with fee rates ≥10 bps:

| Fee Band | Wallets | % of Active Configurers | Volume | Circle Fee |
|---|---|---|---|---|
| 10–20 bps | 62 | 19.7% | $275,031 | $34.19 |
| **20–30 bps** | **76** | **24.1%** | **$444,695** | **$105.64** |
| 30–40 bps | 32 | 10.2% | $76,881 | $26.84 |
| 40–50 bps | 35 | 11.1% | $249,900 | $115.36 |
| 50+ bps | 91 | 28.9% | $31,563 | $16.24 |

**The most common deliberate fee tier is 20–30 bps (0.20–0.30%)** — 76 wallets, the single largest band.
**The second most popular tier is 50+ bps** — 91 wallets, but these have small per-transaction volumes (avg. $94/wallet), suggesting developers testing at the ceiling or applying high fees to micro-transactions.
**The highest-fee-generating tier is 40–50 bps** — just 35 wallets but $249,900 in volume and $115.36 in Circle fees (38% of total).

---

## 4. Circle Fee Collections Summary

| Metric | Value |
|---|---|
| Total Circle fees collected | **$301.42** |
| Implied total developer fees | **$3,014.19** |
| Total transaction volume | **$2,312,568** |
| Effective Circle fee rate on volume | 0.013% |
| Top single wallet contribution | $114.22 (37.9% of total) |

**One wallet dominates**: `0x528dd366...` on arc_testnet — 15 transactions, $247,383 volume, 46 bps fee rate — generated $114.22 in Circle fees alone. Excluding this outlier, the remaining 314 active-fee wallets generated $184.06 collectively.

**All non-arc_testnet chains (base, arbitrum, ethereum, solana) show zero Circle fees collected**, even where transactions occurred. This suggests either no custom fee was configured on these chains or the fee pipeline is only active on arc_testnet at this stage.

---

## 5. Summary Answers

| Question | Answer |
|---|---|
| How many customers used the custom fee feature? | **2,153 wallets** have any fee > $0; **315 wallets** show deliberate fee configuration (≥10 bps) |
| What is the most common fee level? | **20–30 bps (0.20–0.30%)** among active configurers; the broader dataset has ~2 bps as modal but this appears to be noise/defaults |
| How much did Circle collect? | **$301.42 total**; $298.28 (99%) from wallets at ≥10 bps |
