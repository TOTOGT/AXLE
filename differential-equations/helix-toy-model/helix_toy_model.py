"""
helix_toy_model.py
==================================================================
Numerical companion to
  "A Contact-Geometric Toy Model on the Solid Cylinder:
   Transverse Stability, Closure-Dependent Escape, Degenerate Hopf
   Structure, and a Cosmological No-Go."

Reproduces every numerical claim in the paper and regenerates all
figures.  Integrator: DOP853, rtol=1e-10, atol=1e-12 (paper standard).

Model (paper eq. 2):   r' = f(r)(1 - e^{-z}),  theta' = 1,  z' = 1
Closures:  f_cub(r) = r - r^3        (super-linear)
           f_sat(r) = -2(r-1)/(1+(r-1)^2)   (bounded)
Both satisfy f(1)=0, f'(1)=-2.

Run `python helix_toy_model.py` to reproduce the console results and
write the five figures to the current directory.
==================================================================
"""
from __future__ import annotations
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit

RTOL, ATOL, METHOD = 1e-10, 1e-12, "DOP853"

# ---------------------------------------------------------------- closures
def f_cub(r):  return r - r**3
def f_sat(r):  u = r - 1.0; return -2.0 * u / (1.0 + u * u)

def rhs_r(t, y, f, z0):
    """Transverse ODE r' = f(r)(1 - e^{-z}) with z = z0 + t."""
    (r,) = y
    return [f(r) * (1.0 - np.exp(-(z0 + t)))]

# ---------------------------------------------------------- analytic solution
def eps_closed_form(t, z0, eps0):
    """Paper eq. (6): exact linear transverse deviation."""
    return eps0 * np.exp(-2 * t + 2 * np.exp(-z0) * (1 - np.exp(-t)))

def lyapunov_from_closed_form(z0, eps0, T=40.0):
    """Empirical mu = (1/T) ln|eps(T)/eps0|; should approach -2."""
    return np.log(abs(eps_closed_form(T, z0, eps0) / eps0)) / T

# ------------------------------------------------------------ escape / basin
def _blow(t, y, f, z0):  return y[0] - 1e6
_blow.terminal = True; _blow.direction = 1

def escapes(f, z0, eps0, T=12.0):
    """True iff the trajectory blows up in FINITE TIME (super-linear escape).

    Note: 'escape' means a genuine blow-up event, NOT merely 'has not yet
    returned to the helix by time T'.  A bounded closure can drift to large r
    for very negative z0 and recover only slowly; that is convergence with a
    long transient, not escape (see `recovers`).  This distinction is the
    content of Prop. 4 and was the subtle point that closure-dependence hinges
    on."""
    s = solve_ivp(rhs_r, [0, T], [1 + eps0], method=METHOD, rtol=RTOL,
                  atol=ATOL, args=(f, z0), events=_blow, max_step=0.01)
    if s.t_events[0].size > 0:
        return True, s.t_events[0][0]
    return False, None

def recovers(f, z0, eps0, T=400.0, tol=1e-6):
    """True if the (non-escaping) trajectory returns to the helix by time T.
    Used to confirm global attraction for bounded closures over long transients."""
    esc, _ = escapes(f, z0, eps0, T=min(T, 12.0))
    if esc:
        return False
    s = solve_ivp(rhs_r, [0, T], [1 + eps0], method=METHOD, rtol=RTOL,
                  atol=ATOL, args=(f, z0), max_step=0.05)
    return abs(s.y[0, -1] - 1) < tol

def find_z0_star(f, eps0, lo=-6.0, hi=-0.01, iters=60):
    """Bisection for the escape threshold z0*(eps0); None if no escape."""
    if not escapes(f, lo, eps0)[0]:
        return None
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if escapes(f, mid, eps0)[0] else (lo, mid)
    return 0.5 * (lo + hi)

def basin_curve(f, eps_grid):
    return np.array([find_z0_star(f, e) if find_z0_star(f, e) is not None
                     else np.nan for e in eps_grid])

# ------------------------------------------------------------------ cosmology
def hubble_lcdm(z, OmL=0.69, Omm=0.31, Omr=9e-5):
    """H(z)/H0 in e-folds z = ln a (paper, Prop. 6)."""
    return np.sqrt(OmL + Omm * np.exp(-3 * z) + Omr * np.exp(-4 * z))

# ------------------------------------------------------------------- reporting
def report():
    print("=" * 64)
    print(" NUMERICAL VERIFICATION  (DOP853, rtol=1e-10)")
    print("=" * 64)

    print("\n[Thm 1] Lyapunov exponent -> -2 (closed form):")
    for z0 in (-2, 0, 2):
        print(f"   z0={z0:+d}:  mu ~ {lyapunov_from_closed_form(z0, 0.01):+.4f}")

    print("\n[Thm 3] Escape threshold z0*(eps0), cubic closure:")
    for e0 in (0.1, 0.01, 0.001):
        z = find_z0_star(f_cub, e0)
        print(f"   eps0={e0:<6}: z0* = {z:+.4f}")

    print("\n[Prop 4] Bounded closure never escapes; recovers over long transient:")
    for z0 in (-2.4, -5.0):
        esc, _ = escapes(f_sat, z0, 0.01)
        rec = recovers(f_sat, z0, 0.01)
        s = solve_ivp(rhs_r, [0, 400], [1.01], method=METHOD, rtol=RTOL,
                      atol=ATOL, args=(f_sat, z0), max_step=0.05)
        print(f"   z0={z0:+.1f}: blow_up={esc}  recovers={rec}"
              f"  r_max={s.y[0].max():6.2f}  eps_final={s.y[0,-1]-1:+.2e}")
    print("   (contrast) cubic closure at z0=-2.0: blow_up =",
          escapes(f_cub, -2.0, 0.01)[0])

    print("\n[Thm 3] Double-log fit of the basin boundary:")
    eps_grid = np.array([0.5, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005,
                         0.002, 0.001])
    zc = basin_curve(f_cub, eps_grid)
    model = lambda e, C: -np.log((-np.log(e) + C) / 2)
    C, _ = curve_fit(model, eps_grid, zc, p0=[4.0])
    resid = np.max(np.abs(model(eps_grid, C[0]) - zc))
    print(f"   z0* = -ln[(-ln eps0 + C)/2],  C = {C[0]:.3f},"
          f"  max resid = {resid:.3f}")
    print("=" * 64)


# ---------------------------------------------------------------- figure gen
def make_figures():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    # --- Fig 1: 3D helix ---
    def rhs3(t, y):
        r, th, z = y
        return [f_cub(r) * (1 - np.exp(-z)), 1.0, 1.0]
    fig = plt.figure(figsize=(9, 6.2)); ax = fig.add_subplot(111, projection="3d")
    zc = np.linspace(0, 6, 600)
    ax.plot(np.cos(zc), np.sin(zc), zc, color="#c0392b", lw=3, label=r"$\Gamma=\{r=1\}$")
    for (r0, th0), col in [((1.6, 0.0), "#2980b9"), ((0.55, 1.5), "#27ae60")]:
        s = solve_ivp(rhs3, [0, 6], [r0, th0, 0.3], method=METHOD, rtol=RTOL,
                      atol=ATOL, t_eval=np.linspace(0, 6, 1500))
        r, th, z = s.y
        ax.plot(r*np.cos(th), r*np.sin(th), z, color=col, lw=1.6)
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    ax.set_box_aspect([1, 1, 1.6]); ax.view_init(18, -60)
    ax.set_title("Helical attractor on the contact 3-manifold")
    plt.tight_layout(); plt.savefig("fig1_helix3d.png", dpi=150); plt.close()

    # --- Fig 2: escape split ---
    fig, ax = plt.subplots(figsize=(9, 5.6))
    cols = {-2.: "#c0392b", -1.: "#e67e22", -.5: "#f1c40f",
            0.: "#27ae60", .5: "#2980b9", 2.: "#8e44ad"}
    tg = np.linspace(0, 8, 4000)
    for z0, c in cols.items():
        s = solve_ivp(rhs_r, [0, 8], [1.01], method=METHOD, rtol=1e-11,
                      atol=1e-13, args=(f_cub, z0), events=_blow, max_step=0.005)
        ax.semilogy(s.t, np.abs(s.y[0]-1), color=c, lw=2.2, label=f"$z_0={z0:+.1f}$")
        ax.semilogy(tg, np.abs(eps_closed_form(tg, z0, 0.01)), color=c, lw=1, ls=":", alpha=.6)
    ax.set_xlabel("t"); ax.set_ylabel(r"$|\varepsilon(t)|$"); ax.set_ylim(1e-9, 3e2)
    ax.legend(fontsize=8, ncol=2); ax.grid(True, which="both", alpha=.2)
    ax.set_title("Nonlinear (solid) vs linear-exact (dotted)")
    plt.tight_layout(); plt.savefig("helix_split.png", dpi=150); plt.close()

    # --- Fig 3: basin boundary ---
    eps_grid = np.array([0.5, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001])
    zc = basin_curve(f_cub, eps_grid)
    model = lambda e, C: -np.log((-np.log(e) + C) / 2)
    C, _ = curve_fit(model, eps_grid, zc, p0=[4.0])
    ef = np.logspace(-3.3, -0.15, 200)
    fig, ax = plt.subplots(figsize=(9, 5.6))
    ax.fill_between(ef, model(ef, C[0]), 1.5, color="#27ae60", alpha=.12)
    ax.fill_between(ef, -3.2, model(ef, C[0]), color="#c0392b", alpha=.12)
    ax.plot(eps_grid, zc, "o", color="#c0392b", ms=7)
    ax.plot(ef, model(ef, C[0]), "-", color="#c0392b", lw=1.6,
            label=f"$z_0^*=-\\ln[(-\\ln\\varepsilon_0+{C[0]:.2f})/2]$")
    ax.set_xscale("log"); ax.set_xlabel(r"$\varepsilon_0$"); ax.set_ylabel("$z_0$")
    ax.set_ylim(-3.2, 1.5); ax.legend(loc="lower right"); ax.grid(True, which="both", alpha=.15)
    ax.set_title("Basin boundary: converge (above) vs escape (below)")
    plt.tight_layout(); plt.savefig("basin_boundary.png", dpi=150); plt.close()

    # --- Fig 4: Hopf diagram ---
    z = np.linspace(-2, 3, 600); lam = 1 - np.exp(-z)
    fig, ax = plt.subplots(figsize=(9, 5.4))
    ax.plot(z[z > 0], np.ones_like(z[z > 0]), "-", color="#c0392b", lw=2.6,
            label="degenerate: radius $\\equiv 1$")
    ax.plot(z[z < 0], np.ones_like(z[z < 0]), "--", color="#c0392b", lw=1.8, alpha=.7)
    ax.plot(z, np.where(lam > 0, np.sqrt(np.clip(lam, 0, None)), np.nan), "-",
            color="#2980b9", lw=2.4, label="generic: $\\sqrt{1-e^{-z}}$")
    ax.axvline(0, color="gray", ls=":"); ax.set_xlabel("z"); ax.set_ylabel("$r^*$")
    ax.legend(); ax.grid(True, alpha=.15); ax.set_title("Axis bifurcation: degenerate vs generic Hopf")
    plt.tight_layout(); plt.savefig("hopf_diagram.png", dpi=150); plt.close()

    # --- Fig 5: cosmology parallel ---
    z = np.linspace(-3, 4, 700)
    fig, ax = plt.subplots(figsize=(9, 5.4))
    ax.axhline(1, color="gray", ls="--", alpha=.7)
    ax.plot(z, hubble_lcdm(z)/np.sqrt(0.69), color="#2980b9", lw=2.4,
            label=r"$\Lambda$CDM $H/H_{dS}$")
    ax.plot(z, 1-np.exp(-z), color="#c0392b", lw=2.4,
            label=r"framework $1-e^{-z}$")
    ax.axvline(0, color="k", ls=":", alpha=.5); ax.set_ylim(-1.6, 3)
    ax.set_xlabel(r"$z=\ln a$"); ax.set_ylabel("rate / de Sitter asymptote")
    ax.legend(); ax.grid(True, alpha=.15)
    ax.set_title("Shared asymptotic structure (opposite sides)")
    plt.tight_layout(); plt.savefig("cosmo_parallel.png", dpi=150); plt.close()
    print("figures written: fig1_helix3d, helix_split, basin_boundary, "
          "hopf_diagram, cosmo_parallel")


if __name__ == "__main__":
    report()
    make_figures()
