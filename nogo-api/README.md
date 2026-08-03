# Contact No-Go API

A minimal Flask service exposing the transverse-stability and cosmological
no-go results from `HelixToyModel.lean` (companion to
`helix_toy_model.tex` / `helix_toy_model.pdf`, Book 6) as HTTP endpoints.

Every route computes something backed by a named theorem in
`HelixToyModel.lean` — this is a thin numeric wrapper around proved (or
precisely stated, honestly-tracked) math, not a black box.

## Run

```
pip install flask --break-system-packages
python3 nogo_api.py
```

Serves on `http://127.0.0.1:8420`.

## Endpoints

| Route | Backing theorem | Returns |
|---|---|---|
| `GET /trichotomy?z=<float>` | `neutral_line_trichotomy` (fully proved, no `sorry`) | sign of the transverse rate at `z`: repelling / neutral / attracting |
| `GET /epsilon?eps0=<float>&z0=<float>&t=<float>` | `epsSol` (closed form, issue #H1) | the transverse deviation ε(t) |
| `GET /lyapunov?eps0=<float>&z0=<float>&t=<float>` | `lyapunov_exponent_eq` (issue #H2) | numerical estimate of the Lyapunov rate; converges to −2 as `t → ∞` for any `eps0 ≠ 0` |
| `GET /nogo?limit=<float>` | `nogo_attractor_not_deSitter` + `attractor_excludes_deSitter` (issue #H3/#H3b) | whether a claimed transverse-rate limit forces exclusion of any positive finite (de Sitter) expansion rate |

## Numerical note

`/lyapunov` computes `log|ε(t)/ε0|` directly from the closed-form exponent
(`-2t + 2·e^{-z0}(1-e^{-t})`) rather than evaluating `ε(t)` and then taking
its log — the latter underflows to exactly `0.0` in floating point for
`t` much beyond a few hundred, and `log(0)` throws. Verified this session
against `t` from 10 up to 1e7: the rate converges monotonically to `-2`
(error `2e-1 → 2e-7` over that range), matching `lyapunov_exponent_eq`.

## Status

Prototype 0.1. No auth, no rate limiting, no persistence — a working proof
of concept for "the no-go theorem's parameter, served behind an API," not
a production deployment. See Book 6, WP-25, for the product framing.

Pablo Nogueira Grossi · G6 LLC · Newark, NJ
