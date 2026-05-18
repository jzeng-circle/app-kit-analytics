# BridgeKit Phase Analysis Skill

## Purpose
Analyze BridgeKit (or any bridge protocol) usage data to separate organic platform behavior from event-driven outlier activity, characterize each user population, and produce actionable growth insights.

## Usage
```
/bridgekit-phase-analysis [--data <csv_path>] [--cutoff <YYYY-MM-DD>] [--outlier-threshold <usd>]
```

## Parameters
- `data`: Path to raw transaction CSV (columns: dev_entity, dev_address, source_blockchain, Amount, Tx Count)
- `cutoff`: Date to split Phase 1 / Phase 2 — identify from volume drop analysis if not known
- `outlier-threshold`: USD volume threshold above which a wallet is a candidate outlier (default: $250K)

---

## Analysis Framework

### Step 1 — Identify the Phase Cutoff
Look for a single-day volume drop ≥ 70%. Plot weekly volume; the natural breakpoint is the end of any spike week.
Do not use arbitrary calendar splits — find the behavioral breakpoint in the data.

### Step 2 — Classify Outliers Before Comparing Phases
**A wallet is an outlier if ALL THREE apply:**
1. Volume > threshold OR tx count > 200 with programmatic signature (near-uniform tx sizes, high frequency, abrupt stop)
2. Behavior tied to an identifiable external event (chain launch, CEX operation, institutional settlement, exact round-number amounts)
3. Zero or near-zero activity in the subsequent phase (confirming non-recurring nature)

**Outlier types to look for:**
- **Systematic Operator**: High tx count, consistent direction, multi-day execution window — treasury/vault rebalancing
- **Single-Op Whale**: 1-5 txs, exact round numbers (e.g. $2,000,000.00), zero recurrence — planned institutional operation
- **CEX Institutional**: Labeled exchange deposit address (OKX, Binance, Coinbase hot wallet) operating at unusual scale
- **Ecosystem Positioner**: Concentrated activity on a single new chain during its launch window, then exits
- **Bot/Farmer**: Very high tx count, small uniform sizes, abrupt stop — incentive-driven automation

**Edge cases:**
- A wallet with high P1 volume that retains a small P2 residual: classify as outlier for P1 volume but count the P2 activity as its organic run rate
- A wallet that participated in a launch event but continued using the platform after: do NOT classify as outlier — they are a retained organic user

### Step 3 — Analyze the Organic Layer
With outliers removed, recompute all metrics:
- Total volume, avg daily volume, avg tx size
- Chain distribution (source chain, destination chain, avg tx size per chain)
- Volume tier segmentation: Whale >$100K / Large $10K-$100K / Mid $1K-$10K / Small $100-$1K / Micro <$100
- Unique wallets and retention rate phase-over-phase

**Key diagnostic questions:**
- Are chain preferences consistent across phases? (Same ranking = same underlying user base)
- Is the tier structure consistent? (Same dominant tier = structural continuity)
- What is the organic daily run rate, and how does it compare across phases?

### Step 4 — Organic Retained Wallet Analysis
Cross-reference wallet addresses across phases. For each retained wallet:
- Compute volume change (%) P1 → P2
- Classify as: Growing (+20%), Stable (±20%), Declining (-20%)
- For top growers: identify behavior pattern (what chain, what size, what frequency) — these are the product-market fit signal
- For top decliners: identify whether decline is event-linked (had a specific P1 operation) or genuine disengagement

### Step 5 — Outlier Deep Dive
For each outlier type, answer:
- What external event triggered this activity?
- What is the recurrence potential? (High = systematic operators with ongoing needs; Low = single-op whales; Unpredictable = CEX)
- What does competitive selection tell us? (If a large institutional actor chose this platform, what does that imply about capability?)
- What is the event map? (Plot outlier timing against known external events to confirm event-driven thesis)

---

## Visualizations (in order of report appearance)

### Organic Analysis Charts (A–E)

**A. Stacked area chart** — organic vs outlier volume per week
- Purpose: establish the two-layer thesis visually before any numbers
- Key: shade outlier layer red, organic layer teal; annotate the spike week explicitly
- Note: for weeks where only wallet-aggregate data exists, estimate organic layer as the P1 organic run rate

**B. Phase comparison dashboard** — 4-panel: key metrics P1 vs P2
- Panels: total volume, avg tx size, whale wallet %, micro tx %
- Side-by-side bars; label the % change on each panel

**C. Organic 3-panel comparison** — organic P1 vs P2 side by side
- Panel 1: total volume bars; Panel 2: chain share horizontal bars; Panel 3: tier share horizontal bars
- Purpose: show structural continuity — same chains, same tiers = same underlying user base

**D. Organic growth trajectory** — continuous weekly line with spike period omitted
- Connect P1 organic run-rate weeks directly to P2 weeks; add dotted trendline
- Annotate the removed spike window explicitly

**E. Retained wallet slope chart** — P1 → P2 volume per retained wallet
- Two columns connected by lines; color-code: green growing (+20%), grey stable, red declining
- Purpose: individual-wallet signal for product-market fit depth

### ML Outlier Separation Charts (F–I)

**F. Three diagnostic dimensions** — 3-panel scatter (one per criterion)
- Panel 1 (C1 Materiality): log(volume) on x, wallets as dots; shade outlier zone
- Panel 2 (C2 Behavioral signature): avg tx size vs tx count scatter; outliers labeled
- Panel 3 (C3 Non-recurrence): P1 volume vs P2 volume; cluster near zero-P2 axis is the outlier zone
- Purpose: show each criterion independently before combining them

**G. PCA with confidence ellipses** — 4 features reduced to 2 principal components
- Features: log(volume), log(avg_tx_size), log(tx_count), num_chains
- Plot PC1 vs PC2 scatter; draw 2σ confidence ellipse per group (organic vs outlier)
- Add biplot arrows for each feature loading (direction = which dimension drives separation)
- Annotate PC1/PC2 explained variance; label outlier cluster
- Result benchmark: PC1 + PC2 should capture ≥ 85% variance; outlier cluster should be visually separated

**H. K-means clustering** — unsupervised validation in PCA space
- Run k=2 through k=6; select k via silhouette score (typically k=2 scores highest ~0.47)
- Plot k=2 result in PC1/PC2 space with cluster membership colors
- Add inset table: cluster profile (mean volume, mean tx count, outlier wallet count per cluster)
- Key message: unsupervised algorithm independently recovers the analyst-defined outlier set

**I. Logistic regression decision boundary** — supervised separation proof
- Train on log(volume) + log(avg_tx_size) only (2 features for interpretability)
- Plot decision boundary as contourf in 2D space; overlay wallet scatter colored by true label
- Add probability distribution subplot: KDE of P(outlier) for organic vs outlier groups
- Report accuracy, log(volume) coefficient, log(avg_tx_size) coefficient
- Key message: 2 features achieve ≥ 95% accuracy → separation is not marginal

### Charting Conventions

- Organic / retail: teal `#2A9D8F`
- Outlier / whale / event-driven: red `#E63946`
- Phase 2 / neutral comparisons: blue `#457B9D`
- Mid-tier / secondary: amber `#E9C46A`
- Growing wallets: green `#2D6A4F`; declining: red `#E63946`; stable: grey `#ADB5BD`
- Background: `#F8F9FA`, remove top/right spines, light y-grid only
- Confidence ellipses: same hue as group, alpha=0.15 fill + 1.5pt edge
- Decision boundary contourf: blue-red diverging, alpha=0.3

### ML Feature Engineering Reference

```python
# Log-transform skewed features before any ML
wallet_df['lv']  = np.log10(wallet_df['volume'].clip(lower=1))
wallet_df['lAt'] = np.log10(wallet_df['avg_tx'].clip(lower=1))
wallet_df['lTx'] = np.log10(wallet_df['tx_count'].clip(lower=1))

# PCA
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
X_sc = StandardScaler().fit_transform(wallet_df[['lv','lAt','lTx','num_chains']])
pcs = PCA(n_components=2, random_state=42).fit_transform(X_sc)

# K-Means silhouette selection
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
scores = {k: silhouette_score(pcs, KMeans(n_clusters=k, random_state=42, n_init=20).fit_predict(pcs))
          for k in range(2, 7)}

# Logistic regression
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(C=0.5, random_state=42)
lr.fit(wallet_df[['lv','lAt']], labels)

# Confidence ellipse helper
def confidence_ellipse(x, y, ax, n_std=2.0, **kwargs):
    from matplotlib.patches import Ellipse
    import matplotlib.transforms as transforms
    cov = np.cov(x, y)
    pearson = cov[0,1] / np.sqrt(cov[0,0] * cov[1,1])
    rx, ry = np.sqrt(1 + pearson), np.sqrt(1 - pearson)
    ellipse = Ellipse((0,0), width=rx*2, height=ry*2, **kwargs)
    scale_x = np.sqrt(cov[0,0]) * n_std
    scale_y = np.sqrt(cov[1,1]) * n_std
    t = transforms.Affine2D().rotate_deg(45).scale(scale_x, scale_y).translate(np.mean(x), np.mean(y))
    ellipse.set_transform(t + ax.transData)
    return ax.add_patch(ellipse)
```

---

## Report Structure

```
## Executive Summary
- Core argument in 2 sentences
- Key findings as bullets with precise numbers

## Part 1: The Organic Platform
### 1.1 Two Layers in One Dataset          [Chart A: stacked area]
### 1.2 Organic Metrics — Phase 1 vs P2    [Chart B: 4-panel dashboard]
### 1.3 Chain Story                         [Chart C: 3-panel organic comparison + table]
### 1.4 Volume Tier Structure               [tier table]
### 1.5 Organic Growth Trajectory           [Chart D: continuous line + trendline]
### 1.6 Retained Wallets                    [Chart E: slope chart + tables]

## Part 2: Outlier Deep Dive
### 2.0 Defining Outliers                  [3-criteria table + evidence table]
    - C1 Materiality criterion
    - C2 Behavioral signature criterion
    - C3 Non-recurrence criterion
    - Threshold sensitivity table
### 2.1 Visual Separation                  [Chart F: 3 diagnostic dims]
                                           [Chart G: PCA + confidence ellipses + biplot]
                                           [Chart H: K-means clustering]
                                           [Chart I: logistic decision boundary]
### 2.2 Outlier Types & Event Map          [4-panel chart + timeline table]
### 2.3 Strategic Implications of Outliers

## Part 3: Strategy Implications
### 3.1 Revised Platform Metrics            [before/after table]
### 3.2 Organic Growth Levers              [named, data-backed]
### 3.3 What to Stop Doing

## Appendix: Outlier Classification Methodology
```

---

## Persona Archetypes (reusable across bridge analyses)

| Persona | Volume Range | Tx Pattern | Chain Preference | Recurrence |
|---------|-------------|------------|-----------------|------------|
| Systematic Operator | $1M-$10M | High freq, consistent direction | ARB, ETH | Medium-high |
| Single-Op Whale | $250K-$5M | 1-5 txs, round numbers | ETH, OP, ARB | Very low |
| CEX Institutional | $500K-$5M | Irregular, large blocks | ETH, ARB | Episodic |
| Ecosystem Positioner | $100K-$1M | Burst at chain launch | New chains | Launch-event only |
| Bot Farmer | Any | Very high freq, uniform size | Polygon, Base | Incentive-dependent |
| Mid-Tier DeFi Operator | $10K-$100K | Regular, multi-chain | Polygon, Base, ARB | High |
| Polygon/Base Grinder | $100-$10K | High freq, small size | Polygon, Base | High |
| Micro Explorer | <$100 | Scattered, multi-chain | Any | Pipeline only |

---

## Key Metrics to Track (post-analysis)

| Metric | What it measures |
|--------|-----------------|
| Organic daily run rate | True platform health, immune to whale noise |
| Mid-tier tx count | Growth of recurring professional users |
| Organic retention rate | Product-market fit signal |
| Micro-to-mid conversion | Onboarding funnel health |
| Growing retained wallet count | Engagement depth |
| Chain share consistency P1→P2 | Whether the same user base persists |

---

## Common Pitfalls

- **Do not compare raw phase metrics without outlier removal first.** Volume swings of 70%+ triggered by 5-15 wallets will produce false conclusions about platform health.
- **Do not use "churn rate" as a health metric if whales churned.** 80% churn that is 95% whale churn is a very different story from 80% retail churn.
- **Do not assume all Arbitrum volume is the same.** High avg tx size on Arbitrum = whale signal; low avg tx size = retail signal. Always segment by avg tx size per chain.
- **Do not treat micro-transaction growth as noise.** Sub-$100 transactions with high counts are onboarding behavior — track what % graduate to larger sizes.
- **Bot wallets look organic on chain but behavioral analysis reveals them.** Key tells: uniform transaction sizes, abrupt complete stop (not gradual decline), activity perfectly correlated with incentive program dates.

---

## Related Reports
- `data/analysis_results/BRIDGEKIT_USAGE_ANALYSIS.md` — Latest: organic-first analysis with outliers as a separate section
- `data/analysis_results/REVISED_PHASE_ANALYSIS_DEC14_CUTOFF.md` — Previous: raw phase comparison with outlier analysis integrated
