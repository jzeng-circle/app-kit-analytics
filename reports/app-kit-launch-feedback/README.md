# App Kit Launch — Customer Feedback

Two-angle reception analysis of Circle's App Kit launch on April 10, 2026:
public developer adoption (GitHub) and social-media response (Twitter/X).
Both snapshots taken in the two weeks following launch.

## Reports

- [**`github-repos-report.md`**](github-repos-report.md) — Adoption analysis of 23 confirmed public repos across App Kit (12), Bridge Kit (11), and Swap Kit (0). 35 stars, 22 forks total. Compiled 2026-04-14.
- [**`twitter-feedback-report.md`**](twitter-feedback-report.md) — Sentiment + theme analysis of 100 replies (out of 129) to the @arc launch post. Compiled 2026-04-14. Tweet ID `2042595956819120176`.

## Supporting files

| Path | Description |
|---|---|
| [`data/TwCommentExport-arc-2047668757745840263-2026-04-30_114403.xlsx`](data/TwCommentExport-arc-2047668757745840263-2026-04-30_114403.xlsx) | Raw Twitter reply export (104 KB). |

## Headline findings

### GitHub adoption
- **App Kit**: 12 repos, all within 2 weeks of launch, **Arc Testnet exclusive**.
  Notable cross-pollination with AI: Claude-powered agent-to-agent commerce
  (`freelance-arc`, ERC-8183), GenLayer intelligent-contract escrow
  (`proofpay-escrow`, `sourcebounty-arc-genlayer`), Gemini trading agents
  (`PolyAgents`).
- **Bridge Kit**: 11 repos, broader adoption going back to Nov 2025, mature
  patterns (Permit2 relayer, LavaMoat, SDK patches in production).
- **Swap Kit**: zero public adoption — builders use App Kit's bundled swap or
  build custom AMMs instead.
- **Pain points**: App Kit swap is mainnet-only (blocks the full
  send/bridge/swap loop on Arc Testnet); no Solana App Kit usage; the fee
  atomicity question from Twitter is not addressed in any community repo
  either.

### Twitter response
- **Post performance**: 65,905 views, 511 likes, 129 replies, 86 RTs, 56
  quotes, 90 bookmarks.
- **Sentiment**: Strongly positive. Dominant themes — relief at unified
  bridge/swap/send SDK, excitement about built-in monetization, multiple
  builders signaling integration intent.
- **Unanswered technical question**: @Albatros_0x raised a substantive
  question about **fee atomicity** that went unanswered and warrants a
  documentation follow-up.
- **Engaged builders worth contacting**: @Meridian_Fi (already in production
  on Bridge Kit), @btcmonie / UnitFlow Finance (named integration intent).

## Caveats

- GitHub report counts exclude one unverified repo (`TarunKoushal6/J14-75`)
  that could not be confirmed as using `@circle-fin/app-kit`. Dashboard data
  showing `swap-kit` adoption for `developermynk/Arc-Wallet` was a false
  positive — only `app-kit` was found in its `package.json`.
- Twitter sample is the first 100 replies (out of 129); roughly 25 replies
  are non-English / low-effort filler and ~3 are unrelated spam, leaving ~70
  signal-bearing replies in the sample.

## Source data dependencies

- GitHub: `~/circle-developer-kit-radar/docs/github-repos-snapshot.json`
  (READMEs fetched via GitHub API on 2026-04-14).
- Twitter: the `.xlsx` export under `data/`.
