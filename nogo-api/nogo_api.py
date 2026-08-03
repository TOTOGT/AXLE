"""
nogo_api.py — The Contact No-Go, served as an API.

Every endpoint here computes something that is either a real, proved theorem
in HelixToyModel.lean (github.com/TOTOGT/AXLE), or a direct numerical
evaluation of a closed form from that paper. Nothing here is a black box:
each route's docstring names the theorem it implements.

Model (helix_toy_model.tex, eq. 2/5/6):
  Transverse linearization about the cycle Gamma = {r=1}, eps := r - 1:
    eps_dot = 2 * eps * (exp(-z) - 1),   z = z0 + t
  Closed form (Thm 1 / epsSol):
    eps(t) = eps0 * exp(-2t + 2 exp(-z0) (1 - exp(-t)))
  Instantaneous transverse rate (Thm 2 / transRate):
    rho(z) = 2 (exp(-z) - 1)
  Sign trichotomy (neutral_line_trichotomy, fully proved, no sorry):
    z < 0  -> rho(z) > 0   (repelling)
    z = 0  -> rho(z) = 0   (neutral line)
    z > 0  -> rho(z) < 0   (attracting)
  Lyapunov exponent (lyapunov_exponent_eq):
    lim_{t->inf} (1/t) log|eps(t)/eps0| = -2   for every eps0 != 0, z0
  No-go (nogo_attractor_not_deSitter / attractor_excludes_deSitter):
    If the transverse rate c(z) -> a negative constant (a genuine attractor)
    and the locking identity c = H' holds, then H(z) -> -infinity, which
    excludes any positive finite (de Sitter) expansion limit L.

Run:
    python3 nogo_api.py
Then:
    curl "http://127.0.0.1:8420/trichotomy?z=1.5"
    curl "http://127.0.0.1:8420/epsilon?eps0=0.01&z0=0&t=5"
    curl "http://127.0.0.1:8420/lyapunov?eps0=0.01&z0=0&t=50"
    curl "http://127.0.0.1:8420/nogo?limit=-2"
"""
import math
from flask import Flask, request, jsonify

app = Flask(__name__)


def trans_rate(z: float) -> float:
    """rho(z) = 2(e^{-z} - 1) — HelixToyModel.lean: def transRate."""
    return 2.0 * (math.exp(-z) - 1.0)


def eps_sol(eps0: float, z0: float, t: float) -> float:
    """eps(t) = eps0 * exp(-2t + 2 e^{-z0}(1 - e^{-t})) — def epsSol."""
    return eps0 * math.exp(-2.0 * t + 2.0 * math.exp(-z0) * (1.0 - math.exp(-t)))


def classify(rho: float) -> str:
    if rho > 1e-12:
        return "repelling"
    if rho < -1e-12:
        return "attracting"
    return "neutral"


@app.route("/")
def index():
    return jsonify({
        "service": "Contact No-Go API",
        "backing_theorem_file": "https://github.com/TOTOGT/AXLE/blob/main/HelixToyModel.lean",
        "endpoints": {
            "/trichotomy?z=<float>": "sign of the transverse rate at z (neutral_line_trichotomy)",
            "/epsilon?eps0=<float>&z0=<float>&t=<float>": "closed-form transverse deviation (epsSol)",
            "/lyapunov?eps0=<float>&z0=<float>&t=<float>": "numerical Lyapunov rate estimate, should -> -2 (lyapunov_exponent_eq)",
            "/nogo?limit=<float>": "de Sitter exclusion check given a claimed transverse-rate limit (nogo_attractor_not_deSitter)",
        },
    })


@app.route("/trichotomy")
def trichotomy():
    try:
        z = float(request.args["z"])
    except (KeyError, ValueError):
        return jsonify({"error": "pass a numeric z, e.g. /trichotomy?z=1.5"}), 400
    rho = trans_rate(z)
    return jsonify({
        "z": z,
        "transRate": rho,
        "classification": classify(rho),
        "theorem": "neutral_line_trichotomy (HelixToyModel.lean, fully proved, no sorry)",
    })


@app.route("/epsilon")
def epsilon():
    try:
        eps0 = float(request.args.get("eps0", 0.01))
        z0 = float(request.args.get("z0", 0.0))
        t = float(request.args["t"])
    except (KeyError, ValueError):
        return jsonify({"error": "pass eps0, z0, and a numeric t, e.g. /epsilon?eps0=0.01&z0=0&t=5"}), 400
    return jsonify({
        "eps0": eps0, "z0": z0, "t": t,
        "epsilon_t": eps_sol(eps0, z0, t),
        "theorem": "epsSol (closed-form transverse solution, AXLE issue #H1)",
    })


@app.route("/lyapunov")
def lyapunov():
    try:
        eps0 = float(request.args.get("eps0", 0.01))
        z0 = float(request.args.get("z0", 0.0))
        t = float(request.args.get("t", 50.0))
    except ValueError:
        return jsonify({"error": "eps0, z0, t must be numeric"}), 400
    if t <= 0:
        return jsonify({"error": "t must be positive"}), 400
    # log|eps(t)/eps0| = -2t + 2 e^{-z0}(1 - e^{-t}) exactly (the exponent
    # itself, from epsSol) -- computed directly rather than via eps_sol/eps0,
    # which underflows to exactly 0.0 for large t and breaks log(0).
    log_ratio = -2.0 * t + 2.0 * math.exp(-z0) * (1.0 - math.exp(-t))
    rate = log_ratio / t
    return jsonify({
        "eps0": eps0, "z0": z0, "t": t,
        "numerical_rate": rate,
        "theoretical_limit": -2.0,
        "abs_error": abs(rate - (-2.0)),
        "theorem": "lyapunov_exponent_eq (AXLE issue #H2): rate -> -2 as t -> infinity for any eps0 != 0",
    })


@app.route("/nogo")
def nogo():
    try:
        limit = float(request.args["limit"])
    except (KeyError, ValueError):
        return jsonify({"error": "pass the claimed transverse-rate limit, e.g. /nogo?limit=-2"}), 400
    is_attractor = limit < 0
    verdict = {
        "claimed_transverse_rate_limit": limit,
        "is_genuine_attractor": is_attractor,
    }
    if is_attractor:
        verdict["H_behavior"] = "H(z) -> -infinity (H' = c -> negative constant, integrated)"
        verdict["deSitter_possible"] = False
        verdict["explanation"] = (
            "A transverse attractor (rate -> negative constant) forces the expansion "
            "rate H to diverge to -infinity via H(z) = H(z0) + integral(c). No positive "
            "finite (de Sitter) limit L can be reached. This excludes de Sitter for every "
            "positive L simultaneously, not just one candidate value."
        )
        verdict["theorem"] = "nogo_attractor_not_deSitter + attractor_excludes_deSitter (AXLE issue #H3/#H3b)"
    else:
        verdict["H_behavior"] = "not constrained by this theorem"
        verdict["deSitter_possible"] = "not excluded by this result"
        verdict["explanation"] = (
            "The no-go theorem only fires when the transverse rate limit is negative "
            "(a genuine attractor). A non-negative limit is outside this theorem's scope; "
            "it neither confirms nor excludes a de Sitter correspondence."
        )
        verdict["theorem"] = "n/a — precondition (limit < 0) not met"
    return jsonify(verdict)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8420)
