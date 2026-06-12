#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
certify_rstar.py
================
Numerical certification of the inner basin boundary r* for the dm3
contact-geometric ODE system.

Author  : Pablo Nogueira Grossi  |  G6 LLC  |  Newark, NJ  |  2026
ORCID   : 0009-0000-6496-2186
Zenodo  : 10.5281/zenodo.19117400
License : MIT

System (cylindrical contact coordinates; contact form alpha = dz - r^2 dtheta)
-------------------------------------------------------------------------------
    r_dot = r(1 - r^2) + 2(r - 1) exp(-z)          [radial + z-coupling]
    theta_dot = 1                                     [uniform rotation]
    z_dot = r^2 - 2(r - 1)^2 exp(-z)                [axial / contact]

Parameters : epsilon = 2 (fixed throughout)
Initial section : theta(0) = 0, z(0) = 0

Attractor : Gamma = {r = 1, theta_dot = 1, z_dot = 1}  (helical limit cycle)

Basin boundary definition
--------------------------
r* = inf { r0 > 0 : trajectory with (r(0), z(0)) = (r0, 0) converges to Gamma }.

For r0 > r*  the trajectory converges  (r(t) -> 1, z(t) -> +inf).
For r0 < r*  the trajectory escapes    (r(t) -> 0, z(t) -> -inf).

Mechanism : for r < 1, z decreases (z_dot < 0 when exp(-z) is large), which
amplifies the coupling exp(-z) further, driving r to zero in finite time.
The Gronwall estimate predicts the inner boundary at 2/3 ~ 0.667; the true
boundary r* ~ 0.77594 lies strictly above 2/3.

Dependencies : Python >= 3.9, scipy >= 1.9, numpy >= 1.22
Run          : python3 certify_rstar.py
Expected output (on any IEEE-754 compliant machine) :
    r* = 0.77594059  (to 8 decimal places)

Reproducibility note
---------------------
The bisection algorithm is deterministic; the only floating-point sensitivity
is in the DOP853 integrator (double precision, rtol=1e-12, atol=1e-14).
Results should agree to >= 6 significant figures across platforms.
"""

import sys
import numpy as np
from scipy.integrate import solve_ivp

# ---------------------------------------------------------------------------
# ODE parameters
# ---------------------------------------------------------------------------
EPSILON = 2.0        # coupling strength (fixed)

# ---------------------------------------------------------------------------
# Integration / classification parameters
# ---------------------------------------------------------------------------
T_MAX      = 600.0   # maximum integration time
ESCAPE_R   = 1e-3    # r below this threshold -> escaped
ESCAPE_Z   = -500.0  # z below this threshold -> escaped
CONV_R     = 1.0 - 1e-6   # r above this threshold -> converged
RTOL       = 1e-12
ATOL       = 1e-14
MAX_STEP   = 0.05

# Bisection parameters
BISECT_LO  = 0.770   # known escape point
BISECT_HI  = 0.780   # known converge point
BISECT_TOL = 1e-7    # stop when interval < this


# ---------------------------------------------------------------------------
def dm3_rhs(t: float, y: list) -> list:
    """Right-hand side of the dm3 system (theta decoupled; evolve r and z)."""
    r, z = y
    # Clamp exponent to avoid overflow; exp(-z) is large when z is very negative
    ez = np.exp(min(-z, 200.0))
    r_dot = r * (1.0 - r**2) + EPSILON * (r - 1.0) * ez
    z_dot = r**2 - EPSILON * (r - 1.0)**2 * ez
    return [r_dot, z_dot]


def classify(r0: float, z0: float = 0.0) -> str:
    """
    Integrate from (r0, z0) and return 'converge' or 'escape'.

    Uses terminal events for early stopping:
      - escape: r falls below ESCAPE_R  OR  z falls below ESCAPE_Z
      - converge: r rises above CONV_R
    """
    def ev_esc_r(t, y):  return y[0] - ESCAPE_R
    def ev_esc_z(t, y):  return y[1] - ESCAPE_Z
    def ev_cvg(t, y):    return y[0] - CONV_R

    ev_esc_r.terminal = True;  ev_esc_r.direction = -1
    ev_esc_z.terminal = True;  ev_esc_z.direction = -1
    ev_cvg.terminal   = True;  ev_cvg.direction   = +1

    sol = solve_ivp(
        dm3_rhs, [0.0, T_MAX], [r0, z0],
        method='DOP853',
        rtol=RTOL, atol=ATOL,
        events=[ev_esc_r, ev_esc_z, ev_cvg],
        max_step=MAX_STEP,
        dense_output=False,
    )

    if sol.t_events[2].size > 0:                         # converge event fired
        return 'converge'
    if sol.t_events[0].size > 0 or sol.t_events[1].size > 0:  # escape event
        return 'escape'
    # No terminal event: classify by final state
    return 'converge' if sol.y[0, -1] > 0.999 else 'escape'


def bisect_rstar(lo: float = BISECT_LO,
                 hi: float = BISECT_HI,
                 tol: float = BISECT_TOL) -> float:
    """
    Bisect for r* = sup{ r0 : trajectory from (r0,0) escapes }.
    Invariant: classify(lo) == 'escape', classify(hi) == 'converge'.
    """
    c_lo = classify(lo)
    c_hi = classify(hi)
    if c_lo != 'escape':
        raise ValueError(f"Lower bound r0={lo:.6f} does not escape (got {c_lo}). "
                         f"Adjust BISECT_LO.")
    if c_hi != 'converge':
        raise ValueError(f"Upper bound r0={hi:.6f} does not converge (got {c_hi}). "
                         f"Adjust BISECT_HI.")

    iterations = 0
    while (hi - lo) > tol:
        mid = 0.5 * (lo + hi)
        result = classify(mid)
        if result == 'escape':
            lo = mid
        else:
            hi = mid
        iterations += 1
        if iterations % 5 == 0:
            print(f"    [{iterations:2d}]  lo={lo:.9f}  hi={hi:.9f}  "
                  f"width={hi-lo:.2e}")

    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------
def main():
    print()
    print("=" * 62)
    print("  dm3 Inner Basin Boundary Certification")
    print("  Pablo Nogueira Grossi  |  G6 LLC  |  2026")
    print("  DOI: 10.5281/zenodo.19117400")
    print("=" * 62)
    print()
    print("  System:")
    print("    r_dot = r(1 - r^2) + 2(r-1) exp(-z)")
    print("    z_dot = r^2 - 2(r-1)^2 exp(-z)")
    print(f"    epsilon = {EPSILON},  z(0) = 0,  theta(0) = 0")
    print()
    print("  Integrator: DOP853")
    print(f"  rtol = {RTOL},  atol = {ATOL}")
    print(f"  T_max = {T_MAX},  max_step = {MAX_STEP}")
    print(f"  Bisection tolerance: {BISECT_TOL}")
    print()

    # ------------------------------------------------------------------
    # Outer basin verification
    # ------------------------------------------------------------------
    print("Outer basin (r0 > 1): all must converge")
    outer_ok = True
    for r0 in [1.01, 1.10, 1.33, 1.50, 2.00, 3.00]:
        c = classify(r0)
        ok = "OK" if c == 'converge' else "FAIL"
        if c != 'converge':
            outer_ok = False
        print(f"    r0 = {r0:.2f}  ->  {c}  [{ok}]")
    print()

    # ------------------------------------------------------------------
    # Gronwall gap illustration
    # ------------------------------------------------------------------
    print("Gronwall gap (2/3, r*): trajectories in this interval")
    print("lie inside the Gronwall ball |r-1| < 1/3 but escape.")
    for r0 in [0.68, 0.70, 0.72, 0.74, 0.75]:
        c = classify(r0)
        in_gronwall = abs(r0 - 1.0) < 1.0 / 3.0
        print(f"    r0 = {r0:.2f}  |r0-1| = {abs(r0-1):.2f} "
              f"({'in' if in_gronwall else 'out'} Gronwall ball)  ->  {c}")
    print()

    # ------------------------------------------------------------------
    # Bisection
    # ------------------------------------------------------------------
    print(f"Bisecting for r* in [{BISECT_LO}, {BISECT_HI}]...")
    rstar = bisect_rstar()
    print()

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------
    print("=" * 62)
    print(f"  CERTIFIED VALUE:  r* = {rstar:.8f}")
    print(f"  Rounded (5 d.p.): r* ~ {rstar:.5f}")
    print("=" * 62)
    print()

    # ------------------------------------------------------------------
    # Verification sweep
    # ------------------------------------------------------------------
    print("Verification sweep around r*:")
    print(f"  {'r0':>12}  {'outcome':>10}  {'|r0-r*|':>12}")
    for delta in [-1e-2, -5e-3, -2e-3, -1e-3, -1e-4,
                   0.0,
                  +1e-4, +1e-3, +2e-3, +5e-3, +1e-2]:
        r0 = rstar + delta
        c  = classify(r0)
        mk = "  <- r*" if delta == 0.0 else ""
        print(f"  {r0:12.8f}  {c:>10}  {abs(delta):12.1e}{mk}")
    print()

    # ------------------------------------------------------------------
    # Stability constants summary
    # ------------------------------------------------------------------
    print("Stability constant hierarchy:")
    eps0   = 1.0 / 3.0
    gronwall_inner = 2.0 / 3.0
    kappa_star = np.sqrt(7.0 / 9.0)
    print(f"  eps_0        = 1/3              = {eps0:.6f}  [Gronwall outer radius]")
    print(f"  2/3          = 2/3              = {gronwall_inner:.6f}  [symmetric estimate, WRONG]")
    print(f"  r*           = {rstar:.6f}        [true inner boundary, certified here]")
    print(f"  kappa*       = sqrt(7/9)        = {kappa_star:.6f}  [K-operator Lipschitz bound]")
    print()
    assert gronwall_inner < rstar < kappa_star < 1.0, "Hierarchy violated!"
    print(f"  Hierarchy confirmed:  eps_0 < 2/3 < r* < kappa* < 1  [PASS]")
    print()

    # ------------------------------------------------------------------
    # Deviation from claimed value
    # ------------------------------------------------------------------
    claimed = 0.77594
    deviation = abs(rstar - claimed)
    print(f"  Deviation from published value 0.77594:  {deviation:.2e}")
    if deviation < 1e-4:
        print("  Agreement: PASS (within 1e-4)")
    else:
        print("  Agreement: REVIEW — check T_MAX and tolerances")
    print()
    print("Run complete. Reproducible on any IEEE-754 double-precision platform.")
    print()

    return 0 if outer_ok else 1


if __name__ == '__main__':
    sys.exit(main())
