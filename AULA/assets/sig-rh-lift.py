#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sig-rh-lift.py — regenerates sig-rh-lift.svg, the series mark.

The mark is not a drawing. It is zeta(1/2 + it) for t in [0, 35], lifted
out of the complex plane into the extended phase space (U, V, t) of
Principia Orthogona Book 4 Ch 12, and projected with t running left to
right. The dashed line is the axis U = V = 0. The five dots are the first
five non-trivial zeros of zeta, and each one sits exactly on that line,
because a zero IS a puncture of the axis. That is the whole content of
the picture and it is checked below rather than asserted.

  zeta via Borwein's algorithm 2 for the Dirichlet eta function,
  eta(s) = sum (-1)^(n-1) n^-s, zeta(s) = eta(s) / (1 - 2^(1-s)).
  Accuracy check: |zeta(1/2 + i*rho)| < 1e-8 at the five known zeros,
  and zeta(2) = pi^2/6 to 15 digits.

  Curve simplified by Ramer-Douglas-Peucker at eps = 0.05 SVG units,
  which is below a pixel at the size the mark is used, so the drawn
  curve and the computed curve are the same curve.

Requires: standard library only.   Run: python3 sig-rh-lift.py

Principia Orthogona / AXLE - G6 LLC - CC BY-NC-ND 4.0
"""

import math, sys

ZEROS = [14.134725142, 21.022039639, 25.010857580, 30.424876126, 32.935061588]
SIGMA, T0, T1, NT = 0.5, 0.0, 35.0, 1600
W, H, PAD = 260.0, 74.0, 6.0
TILT_DEG, DEPTH, EPS = 26.0, 3.2, 0.05
INK, GOLD, NAVY = "#8b1a1a", "#c9a84c", "#1a2744"


def eta(s, N=60):
    d = []
    for k in range(N + 1):
        tot = 0.0
        for i in range(k + 1):
            tot += math.exp(math.lgamma(N + i) + i * math.log(4.0)
                            - math.lgamma(N - i + 1) - math.lgamma(2 * i + 1))
        d.append(N * tot)
    dn = d[N]
    return -sum(((-1) ** k) * (d[k] - dn) / ((k + 1) ** s) for k in range(N)) / dn


def zeta(s, N=60):
    return eta(s, N) / (1 - 2 ** (1 - s))


def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    (ax, ay), (bx, by) = pts[0], pts[-1]
    dx, dy = bx - ax, by - ay
    L = math.hypot(dx, dy) or 1e-9
    best, bi = 0.0, 0
    for i in range(1, len(pts) - 1):
        px, py = pts[i]
        dist = abs(dy * px - dx * py + bx * ay - by * ax) / L
        if dist > best:
            best, bi = dist, i
    if best <= eps:
        return [pts[0], pts[-1]]
    return rdp(pts[:bi + 1], eps)[:-1] + rdp(pts[bi:], eps)


def main():
    sys.setrecursionlimit(10000)
    print("accuracy of the zeta routine")
    worst = 0.0
    for t in ZEROS:
        v = abs(zeta(complex(SIGMA, t)))
        worst = max(worst, v)
        print(f"    |zeta(1/2 + {t:.9f}i)| = {v:.3e}")
    z2 = zeta(complex(2, 0)).real
    print(f"    zeta(2) = {z2:.15f}   pi^2/6 = {math.pi**2/6:.15f}")
    assert worst < 1e-8, "zeta is not accurate enough at the known zeros"
    assert abs(z2 - math.pi ** 2 / 6) < 1e-12, "zeta(2) is wrong"

    ca, sa = math.cos(math.radians(TILT_DEG)), math.sin(math.radians(TILT_DEG))
    proj = lambda U, V, t: (t + (U + V) * sa * DEPTH, -(U - V) * ca)
    curve = [proj(zeta(complex(SIGMA, t)).real, zeta(complex(SIGMA, t)).imag, t)
             for t in (T0 + (T1 - T0) * i / NT for i in range(NT + 1))]
    axis = [proj(0, 0, T0), proj(0, 0, T1)]
    xs = [p[0] for p in curve + axis]
    ys = [p[1] for p in curve + axis]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    S = lambda p: (PAD + (p[0] - x0) / (x1 - x0) * (W - 2 * PAD),
                   PAD + (p[1] - y0) / (y1 - y0) * (H - 2 * PAD))

    simp = rdp([S(p) for p in curve], EPS)
    a0, a1 = S(axis[0]), S(axis[1])
    dots = [S(proj(zeta(complex(SIGMA, t)).real, zeta(complex(SIGMA, t)).imag, t))
            for t in ZEROS]

    off = max(abs(d[1] - a0[1]) for d in dots)
    print(f"\n    curve points {len(curve)} -> {len(simp)} after RDP at eps={EPS}")
    print(f"    every zero lies on the axis: worst offset {off:.4f} SVG units")
    assert off < 0.4, "a zero did not land on the axis — the mark would be lying"

    pts = " ".join(f"{a:.1f},{b:.1f}" for a, b in simp)
    svg = (f'<svg viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg" role="img"'
           f' aria-label="The Riemann zeta function on the critical line lifted into (U,V,t);'
           f' the five dots are its first five non-trivial zeros, each a puncture of the axis">\n'
           f'    <line x1="{a0[0]:.1f}" y1="{a0[1]:.1f}" x2="{a1[0]:.1f}" y2="{a1[1]:.1f}"'
           f' stroke="{GOLD}" stroke-width=".7" stroke-dasharray="3 3"/>\n'
           f'    <polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="1.15"'
           f' stroke-linejoin="round" stroke-linecap="round"/>\n    '
           + "".join(f'<circle cx="{d[0]:.1f}" cy="{d[1]:.1f}" r="2.1" fill="{NAVY}"/>' for d in dots)
           + "\n</svg>")
    with open("sig-rh-lift.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"    wrote sig-rh-lift.svg  ({len(svg)} bytes)\n\nALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
