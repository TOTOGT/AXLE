#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DPS-1 power and transfer arithmetic
===================================
G6 LLC · supports WP-36 · MIT

Question: how little data settles the obvious?

If duplicate provisioning is common, we do not need a large survey to say so
with a defensible confidence interval. This computes the minimum n, and the
transfer arithmetic that follows, with explicit sensitivity — so that no number
in the paper is a point estimate pretending to be a fact.

Run: python3 power.py
"""
from __future__ import annotations
import math
from scipy import stats

Z = 1.959963985            # 95%


# ---------------------------------------------------------------- precision
def ci_wilson(k: int, n: int, z: float = Z) -> tuple[float, float]:
    """Wilson score interval — correct for small n and proportions near 0/1."""
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def n_for_halfwidth(p: float, halfwidth: float, z: float = Z) -> int:
    """Smallest n whose Wilson half-width at proportion p is <= halfwidth."""
    for n in range(10, 5000):
        lo, hi = ci_wilson(round(p * n), n, z)
        if (hi - lo) / 2 <= halfwidth:
            return n
    return 5000


def n_for_lowerbound(p: float, floor: float, z: float = Z) -> int:
    """Smallest n such that the 95% lower bound exceeds `floor`.
    This is the real question for policy: 'more than HALF of users do X'."""
    for n in range(10, 5000):
        lo, _ = ci_wilson(round(p * n), n, z)
        if lo > floor:
            return n
    return 5000


# ---------------------------------------------------------------- transfer
def transfer(dps: float, incr_monthly: float, population: int) -> float:
    return dps * incr_monthly * 12 * population


def main() -> None:
    print("=" * 68)
    print("  DPS-1 · how little data do we need?")
    print("=" * 68)

    print("\n[1] Precision vs n, if true prevalence is 40%")
    print(f"  {'n':>6}  {'95% CI':>22}  {'half-width':>11}")
    for n in (50, 100, 150, 200, 400, 1000):
        lo, hi = ci_wilson(round(0.40 * n), n)
        print(f"  {n:>6}  [{lo:6.3f}, {hi:6.3f}]{'':>7}  ±{(hi-lo)/2:>9.3f}")

    print("\n[2] n required to state 'more than X of users' with 95% confidence")
    print(f"  {'true p':>8}  {'claim':>22}  {'n needed':>9}")
    for p, floor, label in [(0.40, 0.25, "more than a quarter"),
                            (0.40, 0.30, "more than 30%"),
                            (0.55, 0.50, "a majority"),
                            (0.30, 0.20, "more than a fifth"),
                            (0.25, 0.15, "more than 15%")]:
        print(f"  {p:>8.0%}  {label:>22}  {n_for_lowerbound(p, floor):>9}")

    print("\n[3] n for a given precision (±)")
    for p in (0.25, 0.40, 0.55):
        for hw in (0.10, 0.07, 0.05):
            print(f"  p={p:.0%}  ±{hw:.0%} → n = {n_for_halfwidth(p, hw):>4}")

    # ---------------------------------------------------------------
    print("\n" + "=" * 68)
    print("  Transfer arithmetic — sensitivity, not a point estimate")
    print("=" * 68)
    print("\n[4] Annual incremental spend per 100,000 affected professionals")
    print(f"  {'DPS':>6} | " + " | ".join(f"${m:>3}/mo".rjust(9) for m in (20, 40, 60, 100)))
    print("  " + "-" * 62)
    for dps in (0.15, 0.25, 0.40, 0.55):
        row = " | ".join(f"${transfer(dps, m, 100_000)/1e6:>7.1f}M"
                         for m in (20, 40, 60, 100))
        print(f"  {dps:>5.0%} | {row}")

    print("\n  Read: rows are prevalence, columns are incremental monthly spend")
    print("  per duplicating user. Nothing here is measured — this is the")
    print("  arithmetic the survey plugs into. [MODEL]")

    # ---------------------------------------------------------------
    print("\n[5] The conservatism rule, shown numerically")
    print("  Reporting rule fixed in advance: publish both estimates, lead")
    print("  with the lower. Suppose the survey returns:")
    stated, revealed = 0.42, 0.28
    lo_s, hi_s = ci_wilson(round(stated * 150), 150)
    lo_r, hi_r = ci_wilson(round(revealed * 150), 150)
    print(f"    stated attribution  n=150: {stated:.0%}  CI [{lo_s:.0%}, {hi_s:.0%}]")
    print(f"    revealed preference n=150: {revealed:.0%}  CI [{lo_r:.0%}, {hi_r:.0%}]")
    lead = min(stated, revealed)
    print(f"    → headline uses {lead:.0%}; the gap ({stated-revealed:+.0%}) is")
    print(f"      reported as the attribution premium, not hidden.")
    print(f"    → transfer @ $40/mo, 100k users: "
          f"${transfer(lead, 40, 100_000)/1e6:.1f}M/yr (conservative)")

    # ---------------------------------------------------------------
    print("\n[6] Detecting the revealed-preference signal (R1, Plan A vs B)")
    print("  H0: users are indifferent (50/50). n to reject at 80% power:")
    for true_p in (0.60, 0.65, 0.70, 0.75):
        n = 10
        while n < 3000:
            se = math.sqrt(0.25 / n)
            crit = 0.5 + Z * se
            pw = 1 - stats.norm.cdf((crit - true_p) / math.sqrt(true_p * (1 - true_p) / n))
            if pw >= 0.80:
                break
            n += 2
        print(f"    if {true_p:.0%} choose the gauge → n = {n:>4}")

    print("\n" + "=" * 68)
    print("  BOTTOM LINE")
    print("=" * 68)
    print("""
  If the effect is as large as the premise implies, n ≈ 150 is enough
  to state a defensible claim, and n ≈ 100 is enough to show the
  revealed-preference tradeoff is not a coin flip.

  A 150-response survey, pre-registered, stratified by usage intensity,
  and reported by frame, is a stronger evidentiary base than a
  1,000-response one that was not pre-registered.

  What n CANNOT fix: sampling frame bias. Ten thousand responses from
  one community still over-represent heavy users. Triangulation across
  unlike frames does more for credibility than any increase in n. [OPEN]
""")


if __name__ == "__main__":
    main()
