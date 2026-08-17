# Economics — algorithmic credit, forced urgency, and extraction

Applied economics line of the *Principia Orthogona* programme. Same discipline as the rest of
AXLE: reproducible pipelines, kernel-checked constants where a constant is claimed, and empirical
content deliberately left **outside** the Lean files rather than encoded as trivially-true theorems.

Grounded in eleven years inside international capital markets — Banco do Brasil (Brasília
headquarters and the New York international office) and JPMorgan Chase. The mechanisms analysed
here — margin calls, forced liquidation, collateral repricing, dual credit markets — were observed
from inside the institutions that operate them.

---

## Papers

### The Response Gap
*How Algorithmic Credit Engineers Forced Urgency and Misattributes Loss — and How Mathematics Can Correct It*

- [`ResponseGap_Grossi2026_paper_v1.pdf`](ResponseGap_Grossi2026_paper_v1.pdf) — working paper
- [`ResponseGap_Grossi2026_deposit.pdf`](ResponseGap_Grossi2026_deposit.pdf) — deposit edition
- DOI: [10.5281/zenodo.21752834](https://doi.org/10.5281/zenodo.21752834)

A governance, ethical, legal and social implications (GELSI) treatment of automated liquidation as
an **auditable governance object**. Unifies the fire-sale, DeFi-liquidation, and algorithmic-lending
fairness literatures, and proposes two correctives: **response-time budgets** — a disclosed, bounded
minimum on the interval a counterparty is given to respond — and **epistemic-disclosure standards**
for underwriting models.

The structural argument: when an automated system compresses response time toward zero, the loss
that follows is attributed to the borrower's decision, but the decision window was engineered. That
is an attribution error with a measurable parameter attached.

### The Forced Urgency Gap (WP-32)

- [`ForcedUrgencyGap_WP32_Grossi2026.pdf`](ForcedUrgencyGap_WP32_Grossi2026.pdf) — working paper
- [`ForcedUrgency.lean`](ForcedUrgency.lean) — kernel-verified core of §4

Non-identification of loss aversion under latent liquidity constraints: the shadow price λ as the
missing state variable. Reproducible **FRED / Federal Reserve Z.1 pipeline in Python, 1971–2026**,
using the 2020 and 2022 liquidity shocks as natural experiments.

`ForcedUrgency.lean` certifies the amplification cascade A(ρ) = ∑ₖ ρᵏ = 1/(1−ρ) for 0 ≤ ρ < 1 —
that the cascade sums to A(ρ), that A(ρ) ≥ 1 with equality iff ρ = 0, that A is strictly increasing
and unbounded as ρ → 1⁻, and the policy corollary that anything strictly lowering ρ strictly lowers
cumulative displacement.

> **Kernel status:** verified 2026-07-25 against a built Mathlib (Lean v4.33.0-rc1). All six
> theorems return `#print axioms → [propext, Classical.choice, Quot.sound]` — no `sorryAx`.

The file carries an explicit design rule: only non-vacuous, kernel-certifiable statements live in
it. The paper's empirical content is **not** encoded as theorems, and is marked `[OPEN]` instead.
Encoding an empirical claim as a trivially-true Lean statement would be exactly the defect this
corpus exists to prevent.

### The Banking Butterfly — a Brazilian supplement

- [`BankingButterfly_preprint.html`](BankingButterfly_preprint.html) — preprint with figures

The precision asymmetry in Brazilian retail banking: the spread between the rate at which a
concentrated banking sector funds large borrowers with alternatives and the rate it charges captive
retail borrowers with none. Traces the mechanism through compounding divergence, ACT/360 premium,
five extraction channels, settlement architecture, and historical cumulative effect, against the
2003 dismantling of protections standing since 1988 and limits dating to 1933.

The argument is that the spread is not a risk premium. It is the price of the absence of an exit.

Figures: `fig1_compounding_divergence.png` · `fig2_act360_premium.png` · `fig3_five_channels.png` ·
`fig4_settlement_architecture.png` · `fig5_latam_estimates.png` · `fig6_big4_auc.png` ·
`fig7_historical_cumulative.png`

---

## Related work elsewhere in this repository

| Work | Location |
|---|---|
| Positional Dominance under Non-Contestability · One-Third Invariant | [`../NetworkGamesJOMO/`](../NetworkGamesJOMO) |
| CapitalGuard Trader · grid-bot backtests · Ponte Nova | [`../Finance/`](../Finance) |
| dm³ stability radius ε₀ = 1/3 — the threshold these lines share | [`../Main_v6.lean`](../Main_v6.lean) |

---

Author: Pablo Nogueira Grossi · ORCID [0009-0000-6496-2186](https://orcid.org/0009-0000-6496-2186)
G6 LLC · Newark, NJ · Papers CC BY 4.0 · Lean files MIT
