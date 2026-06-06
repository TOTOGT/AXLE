#!/usr/bin/env python3
"""
strategy_sim.py — JOMO Strategy Simulator (Python)
====================================================
Reproducibility spec
  Data source : Binance BTCUSDT 1d klines  (public REST API, no key required)
  Endpoint    : https://api.binance.com/api/v3/klines
  Symbol      : BTCUSDT
  Interval    : 1d  (daily open-to-close, UTC midnight boundary)
  Start date  : 2020-01-01  (fixed — change START_DATE to alter the window)
  Returns     : log(close_t / close_{t-1})
  Arb seed    : 42  (fixed — controls the synthetic arbitrage payoff stream)

Install:
    pip install requests pandas numpy

Run:
    cd /path/to/monsterlaw_env
    python strategy_sim.py

Outputs:
    → terminal: stats table sorted by Sharpe
    → btc_data.json: bars + meta for strategy_sim.html

Serve HTML with real data:
    python -m http.server 8080
    open http://localhost:8080/strategy_sim.html
"""

import json
import math
import random
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import requests

# ── REPRODUCIBILITY CONSTANTS ──────────────────────────────────────
DATA_SOURCE = "Binance BTCUSDT 1d klines (public REST API, no key)"
API_URL     = "https://api.binance.com/api/v3/klines"
SYMBOL      = "BTCUSDT"
INTERVAL    = "1d"
START_DATE  = "2020-01-01"   # ← change this to alter the backtest window
ARB_SEED    = 42             # ← fixed for reproducible arbitrage stream


# ── DATA FETCH ─────────────────────────────────────────────────────

def _date_to_ms(s: str) -> int:
    return int(datetime.strptime(s, "%Y-%m-%d")
               .replace(tzinfo=timezone.utc).timestamp() * 1000)

def _ms_to_date(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d")


def fetch_klines(symbol: str = SYMBOL,
                 interval: str = INTERVAL,
                 start: str = START_DATE) -> pd.DataFrame:
    """
    Fetch all daily klines from Binance from start to today.
    Paginates automatically (1 000 bars per request).
    No API key required — uses the public /api/v3/klines endpoint.
    """
    start_ms = _date_to_ms(start)
    end_ms   = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    rows: list = []

    print(f"Fetching {symbol} {interval} from {start}  ", end="", flush=True)
    while start_ms < end_ms:
        r = requests.get(API_URL, params={
            "symbol":    symbol,
            "interval":  interval,
            "startTime": start_ms,
            "limit":     1000,
        }, timeout=20)
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        rows.extend(batch)
        start_ms = batch[-1][0] + 1
        print(".", end="", flush=True)
        if len(batch) < 1000:
            break

    print()
    # Binance kline column order:
    # 0:open_time 1:open 2:high 3:low 4:close 5:volume ...
    df = pd.DataFrame(rows, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "qav", "n_trades", "tb_vol", "tq_vol", "ignore",
    ])
    df["date"]   = df["open_time"].apply(_ms_to_date)
    df["close"]  = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)
    # Log return: log(close_t / close_{t-1}), first bar = 0
    df["ret"]    = np.log(df["close"] / df["close"].shift(1)).fillna(0.0)
    df["dow"]    = pd.to_datetime(df["date"]).dt.dayofweek   # 0=Mon … 6=Sun

    print(f"  {len(df)} bars  "
          f"({df['date'].iloc[0]} → {df['date'].iloc[-1]})")
    return df[["date", "close", "volume", "ret", "dow"]].reset_index(drop=True)


# ── SIGNAL FUNCTIONS (daily bars) ─────────────────────────────────
# All signals operate on the return history up to (not including) bar i.
# sig_fn(rets_history: list, dow: int) → 1 | 0 | -1


def markov_sig(rets: list, threshold: float = 0.87) -> bool:
    """
    Visible 3-state Markov chain on discretised log-returns.
    States: UP (ret > 0.5%), FLAT, DOWN (ret < -0.5%).
    Fires when UP state is self-persistent ≥ threshold over the last 20 bars.
    Source: btcMarkov.py strategy from the JOMO bot.
    """
    if len(rets) < 8:
        return False
    sl = rets[-20:]
    states = [2 if r > 0.005 else (0 if r < -0.005 else 1) for r in sl]
    last = states[-1]
    tot = sself = 0
    for i in range(1, len(states)):
        if states[i - 1] == last:
            tot += 1
            if states[i] == last:
                sself += 1
    return last == 2 and tot > 0 and sself / tot >= threshold


def diurnal_sig(dow: int) -> bool:
    """
    Daily-bar proxy for Tropics2.pdf diurnal wave trapping at ±30° latitude.
    Weekdays (Mon–Fri = 0–4): institutional flow present → signal eligible.
    Weekend: low institutional volume, high retail noise → skip.

    On intraday data this would be: session overlap hours 07-09 UTC (Tokyo/London)
    and 13-17 UTC (London/NY). On daily bars, weekday is the coarser equivalent.
    """
    return dow < 5


def circadian_sig(dow: int) -> bool:
    """
    Behavioral timing filter (Markov.pdf HMM + trader-quality concept).
    Tue–Thu (1–3): highest institutional signal quality.
    Avoid Monday gap-momentum and Friday afternoon positioning unwind.
    """
    return 1 <= dow <= 3


def hmm_sig(rets: list, lookback: int = 30) -> bool:
    """
    Regime detector approximating HMM + Viterbi on real (unlabelled) data.
    BULL condition: 30-day annualised return > 15% AND annualised vol < 80%.

    On synthetic data the HTML version 'peeks' at the true hidden regime
    with 85% accuracy. On real data we must estimate the regime from returns,
    which is what this function does.

    Reference: Jurafsky & Martin Appendix A (Markov.pdf) — the true regime
    is a hidden variable; we decode it from observations using rolling stats
    as a lightweight alternative to full Baum-Welch training.
    """
    if len(rets) < lookback:
        return False
    sl      = np.array(rets[-lookback:])
    mu_ann  = float(sl.mean() * 252)
    sig_ann = float(sl.std()  * math.sqrt(252))
    return mu_ann > 0.15 and sig_ann < 0.80


def kelly_size(pnls: list, cap: float = 0.25) -> float:
    """
    Full Kelly criterion from the rolling trade P&L log.
    f* = (p·(b+1) − 1) / b   where p = win rate, b = avg win / avg loss.
    Capped at `cap` to avoid over-betting.
    """
    n = min(30, len(pnls))
    if n < 5:
        return 0.08   # default before enough history
    sl     = pnls[-n:]
    wins   = [x for x in sl if x > 0]
    losses = [x for x in sl if x < 0]
    if not wins:
        return 0.02
    p = len(wins) / n
    b = (sum(wins) / len(wins)) / abs(sum(losses) / len(losses) if losses else 1e-9)
    return min(max(0.0, (p * (b + 1) - 1) / b), cap)


# ── BACKTEST ENGINE ────────────────────────────────────────────────

def backtest(bars: list, sig_fn, sz_fn, cret_fn=None) -> dict:
    """
    Single-pass vectorised-style backtest.

    bars     : list of dicts  {"ret": float, "dow": int, "date": str}
    sig_fn   : (rets_history, dow) → int  (1=long, 0=flat, -1=short)
    sz_fn    : (pnls) → float  (fraction of capital to risk)
    cret_fn  : optional — overrides bar["ret"] with a custom payoff
               (used for arbitrage: fixed win/loss independent of BTC price)
    """
    cap   = 1.0
    curve = [1.0]
    pnls: list  = []
    rets: list  = []

    for bar in bars[1:]:
        sig = sig_fn(rets, bar["dow"])
        if sig != 0:
            sz  = sz_fn(pnls)
            ret = cret_fn() if cret_fn else bar["ret"]
            p   = sig * sz * ret
            cap *= 1 + p
            pnls.append(p)
        rets.append(bar["ret"])
        curve.append(cap)

    return {"curve": curve, "pnls": pnls}


# ── STATS ──────────────────────────────────────────────────────────

def compute_stats(curve: list, pnls: list) -> dict:
    total_ret = (curve[-1] - 1) * 100
    dr    = [curve[i] / curve[i - 1] - 1 for i in range(1, len(curve))]
    mu    = float(np.mean(dr))
    sigma = float(np.std(dr))
    sharpe = (mu / sigma) * math.sqrt(252) if sigma > 1e-8 else 0.0
    peak = 0.0; dd = 0.0
    for v in curve:
        if v > peak:
            peak = v
        dd = max(dd, (peak - v) / peak)
    wr = (len([x for x in pnls if x > 0]) / len(pnls) * 100) if pnls else 0.0
    return {
        "ret":     round(total_ret, 1),
        "sharpe":  round(sharpe, 2),
        "maxdd":   round(dd * 100, 1),
        "trades":  len(pnls),
        "winrate": round(wr, 0),
    }


# ── STRATEGY DEFINITIONS ───────────────────────────────────────────

def run_all(bars: list) -> list:
    """
    Run all 10 strategies against `bars`.
    Arbitrage uses a fixed random seed (ARB_SEED) for reproducibility.
    """
    arb_rng = random.Random(ARB_SEED)

    def arb_sig(r, d):
        return 1 if arb_rng.random() < 0.08 else 0

    def arb_ret():
        # 65% hit rate, +2% win / -1.5% loss (independent of BTC price)
        return 0.02 if arb_rng.random() < 0.65 else -0.015

    strat_defs = [
        # (name, signal_fn, size_fn, custom_return_fn)
        ("Buy & Hold",
            lambda r, d: 1,
            lambda p: 1.0,
            None),

        ("Kelly",
            lambda r, d: 1 if len(r) > 5 else 0,
            kelly_size,
            None),

        ("Markov",
            lambda r, d: 1 if markov_sig(r) else 0,
            kelly_size,
            None),

        ("Diurnal",
            lambda r, d: 1 if diurnal_sig(d) else 0,
            lambda p: 0.20,
            None),

        ("Circadian",
            lambda r, d: 1 if circadian_sig(d) else 0,
            lambda p: 0.18,
            None),

        ("Arbitrage",
            arb_sig,
            lambda p: 0.15,
            arb_ret),

        ("HMM",
            lambda r, d: 1 if hmm_sig(r) else 0,
            kelly_size,
            None),

        ("Markov+HMM",
            lambda r, d: 1 if (markov_sig(r) and hmm_sig(r)) else 0,
            lambda p: kelly_size(p, 0.35),
            None),

        # Chain: ALL gates must pass (precision over recall)
        ("Chain",
            lambda r, d: 1 if (diurnal_sig(d) and hmm_sig(r) and markov_sig(r)) else 0,
            lambda p: kelly_size(p, 0.35),
            None),

        # Lean: majority vote (recall over precision)
        ("Lean",
            lambda r, d: 1 if sum([
                markov_sig(r), diurnal_sig(d), circadian_sig(d), hmm_sig(r)
            ]) >= 3 else 0,
            lambda p: kelly_size(p, 0.30),
            None),
    ]

    results = []
    for name, sig_fn, sz_fn, cret_fn in strat_defs:
        r = backtest(bars, sig_fn, sz_fn, cret_fn)
        s = compute_stats(r["curve"], r["pnls"])
        results.append({"name": name, **s})
    return results


# ── TERMINAL OUTPUT ────────────────────────────────────────────────

def print_table(results: list, meta: dict) -> None:
    W   = 14
    col = f"{'Strategy':<{W}}  {'Return':>8}  {'Sharpe':>7}  {'MaxDD':>7}  {'Trades':>7}  {'Win%':>6}"
    sep = "─" * len(col)

    print()
    print("═" * len(col))
    print(f"  JOMO Strategy Simulator")
    print(f"  Source   : {meta['source']}")
    print(f"  Symbol   : {meta['symbol']}  ·  interval {meta['interval']}")
    print(f"  Period   : {meta['start']} → {meta['end']}  ({meta['n_bars']} bars)")
    print(f"  Fetched  : {meta['fetched']}")
    print(f"  Arb seed : {ARB_SEED}  (fixed)")
    print(f"  API      : {meta['api_url']}")
    print("═" * len(col))
    print(col)
    print(sep)
    for r in sorted(results, key=lambda x: -x["sharpe"]):
        sign = "+" if r["ret"] >= 0 else ""
        print(f"{r['name']:<{W}}  {sign}{r['ret']:>7.1f}%  {r['sharpe']:>7.2f}  "
              f"-{r['maxdd']:>6.1f}%  {r['trades']:>7}  {r['winrate']:>5.0f}%")
    print(sep)
    print()


# ── SAVE JSON ──────────────────────────────────────────────────────

def save_json(df: pd.DataFrame, results: list, meta: dict) -> None:
    """Write btc_data.json consumed by strategy_sim.html."""
    bars_out = [
        {
            "date":  row.date,
            "close": round(float(row.close), 2),
            "ret":   round(float(row.ret),   6),
            "dow":   int(row.dow),
        }
        for row in df.itertuples(index=False)
    ]
    payload = {
        "meta":    meta,
        "bars":    bars_out,
        # pre-computed stats for reference (HTML re-runs its own JS backtest)
        "results": [{k: v for k, v in r.items()} for r in results],
    }

    out_path = "btc_data.json"
    with open(out_path, "w") as f:
        json.dump(payload, f, separators=(",", ":"))

    size_kb = len(json.dumps(payload)) // 1024
    print(f"Saved  {out_path}   ({len(bars_out)} bars · ~{size_kb} KB)")
    print()
    print("─── View in browser with real data ──────────────────────")
    print("  python -m http.server 8080")
    print("  open  http://localhost:8080/strategy_sim.html")
    print("─────────────────────────────────────────────────────────")


# ── MAIN ──────────────────────────────────────────────────────────

def main() -> None:
    try:
        df = fetch_klines()
    except requests.exceptions.RequestException as exc:
        print(f"\nFetch error: {exc}")
        print("Check your connection. Binance may be geo-blocked — try a VPN.")
        sys.exit(1)

    bars = df[["date", "ret", "dow"]].to_dict("records")

    meta = {
        "source":   DATA_SOURCE,
        "api_url":  API_URL,
        "symbol":   SYMBOL,
        "interval": INTERVAL,
        "start":    df["date"].iloc[0],
        "end":      df["date"].iloc[-1],
        "n_bars":   len(df),
        "fetched":  datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    results = run_all(bars)
    print_table(results, meta)
    save_json(df, results, meta)


if __name__ == "__main__":
    main()
