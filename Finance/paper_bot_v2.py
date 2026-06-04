"""
paper_bot_v2.py — Two-phase momentum-then-fade strategy
Phase 1: LONG on breakout, exit on trailing stop or fixed TP
Phase 2: SHORT immediately after Phase 1 exit, fixed TP/SL
"""

import time
import requests
import csv
import os
from datetime import datetime

# ── Strategy parameters ──────────────────────────────────────────────────────
LONG_TRAIL_PCT  = 0.015   # trailing stop: lock in gains, exit when price drops this far from peak
LONG_TP_PCT     = 0.04    # long hard take-profit (4%)
LONG_SL_PCT     = 0.02    # long stop-loss (2%)

SHORT_TP_PCT    = 0.025   # short take-profit (2.5%)
SHORT_SL_PCT    = 0.03    # short stop-loss (3%)

BET_PCT         = 0.10    # risk 10% of bank per trade
MIN_VOL_USD     = 1_000_000
MIN_MOVE_PCT    = 5.0     # coin must be up ≥5% on the day to qualify
SCAN_SECS       = 60
MAX_HOLD_SECS   = 4 * 3600   # 4-hour max per phase
FEE             = 0.006   # 0.6% per side (taker)
BANK            = 200.0

LOG_FILE        = os.path.expanduser("~/trades_v2.csv")

# ── HTTP helper ───────────────────────────────────────────────────────────────
def fetch(url):
    try:
        return requests.get(url, timeout=5).json()
    except Exception:
        return None

def get_price(pid):
    data = fetch(f"https://api.exchange.coinbase.com/products/{pid}/ticker")
    return float(data["price"]) if data and "price" in data else None

# ── CSV logger ────────────────────────────────────────────────────────────────
def log_trade(trade_num, phase, pid, entry, exit_price, size, pnl, reason, bank):
    write_header = not os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(["#", "phase", "pair", "entry", "exit", "size",
                        "pnl", "reason", "bank", "time"])
        w.writerow([trade_num, phase, pid,
                    f"{entry:.6f}", f"{exit_price:.6f}",
                    f"{size:.2f}", f"{pnl:+.2f}",
                    reason, f"{bank:.2f}",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

# ── Scanner ───────────────────────────────────────────────────────────────────
seen_tickers = {}   # pid → first-seen timestamp (cooldown: 30 min)
COOLDOWN = 1800

def get_movers():
    products = fetch("https://api.exchange.coinbase.com/products")
    if not products:
        return []
    movers = []
    now = time.time()
    for p in products:
        pid = p.get("id", "")
        if not pid.endswith("-USD") or p.get("status") != "online":
            continue
        # skip tickers on cooldown
        if pid in seen_tickers and now - seen_tickers[pid] < COOLDOWN:
            continue
        stats = fetch(f"https://api.exchange.coinbase.com/products/{pid}/stats")
        if not stats:
            continue
        try:
            open_  = float(stats["open"])
            last   = float(stats["last"])
            vol    = float(stats["volume"])
        except (KeyError, ValueError):
            continue
        if open_ <= 0 or last <= 0:
            continue
        chg     = (last - open_) / open_ * 100
        vol_usd = vol * last
        if chg >= MIN_MOVE_PCT and vol_usd >= MIN_VOL_USD:
            movers.append((pid, last, chg, vol_usd))
    return sorted(movers, key=lambda x: x[2], reverse=True)

# ── Phase 1: LONG with trailing stop ─────────────────────────────────────────
def phase1_long(pid, entry, size, trade_num):
    tp_price = entry * (1 + LONG_TP_PCT)
    sl_price = entry * (1 - LONG_SL_PCT)
    peak     = entry
    deadline = time.time() + MAX_HOLD_SECS

    print(f"  [P1 LONG]  entry={entry:.6f}  TP={tp_price:.6f}  SL={sl_price:.6f}  trail={LONG_TRAIL_PCT*100}%")

    while time.time() < deadline:
        price = get_price(pid)
        if price is None:
            time.sleep(30)
            continue

        if price > peak:
            peak = price
            trail_stop = peak * (1 - LONG_TRAIL_PCT)
            print(f"  {pid} {price:.6f}  peak={peak:.6f}  trail_stop={trail_stop:.6f}", end="\r")
        else:
            trail_stop = peak * (1 - LONG_TRAIL_PCT)
            print(f"  {pid} {price:.6f}  trail_stop={trail_stop:.6f}              ", end="\r")

        # Hard TP
        if price >= tp_price:
            pnl = size * LONG_TP_PCT - size * FEE * 2
            print(f"\n  P1 TP HIT @ {price:.6f}  PnL=+{pnl:.2f}")
            log_trade(trade_num, "LONG", pid, entry, price, size, pnl, "TP", BANK + pnl)
            return price, pnl

        # Hard SL
        if price <= sl_price:
            pnl = -(size * LONG_SL_PCT) - size * FEE * 2
            print(f"\n  P1 SL HIT @ {price:.6f}  PnL={pnl:.2f}")
            log_trade(trade_num, "LONG", pid, entry, price, size, pnl, "SL", BANK + pnl)
            return None, pnl   # SL hit → skip short phase

        # Trailing stop
        if price <= trail_stop and price > entry:   # only trigger if we're in profit
            pnl = size * ((price - entry) / entry) - size * FEE * 2
            print(f"\n  P1 TRAIL HIT @ {price:.6f}  peak={peak:.6f}  PnL={pnl:+.2f}")
            log_trade(trade_num, "LONG", pid, entry, price, size, pnl, "TRAIL", BANK + pnl)
            return price, pnl   # good exit → proceed to short

        time.sleep(30)

    price = get_price(pid) or entry
    pnl   = size * ((price - entry) / entry) - size * FEE * 2
    print(f"\n  P1 TIMEOUT @ {price:.6f}  PnL={pnl:+.2f}")
    log_trade(trade_num, "LONG", pid, entry, price, size, pnl, "TIMEOUT", BANK + pnl)
    return price, pnl

# ── Phase 2: SHORT after exhaustion ──────────────────────────────────────────
def phase2_short(pid, entry, size, trade_num):
    tp_price = entry * (1 - SHORT_TP_PCT)
    sl_price = entry * (1 + SHORT_SL_PCT)
    deadline = time.time() + MAX_HOLD_SECS

    print(f"  [P2 SHORT] entry={entry:.6f}  TP={tp_price:.6f}  SL={sl_price:.6f}")

    while time.time() < deadline:
        price = get_price(pid)
        if price is None:
            time.sleep(30)
            continue

        print(f"  {pid} {price:.6f}", end="\r")

        if price <= tp_price:
            pnl = size * SHORT_TP_PCT - size * FEE * 2
            print(f"\n  P2 TP HIT @ {price:.6f}  PnL=+{pnl:.2f}")
            log_trade(trade_num, "SHORT", pid, entry, price, size, pnl, "TP", BANK + pnl)
            return pnl

        if price >= sl_price:
            pnl = -(size * SHORT_SL_PCT) - size * FEE * 2
            print(f"\n  P2 SL HIT @ {price:.6f}  PnL={pnl:.2f}")
            log_trade(trade_num, "SHORT", pid, entry, price, size, pnl, "SL", BANK + pnl)
            return pnl

        time.sleep(30)

    price = get_price(pid) or entry
    pnl   = size * ((entry - price) / entry) - size * FEE * 2
    print(f"\n  P2 TIMEOUT @ {price:.6f}  PnL={pnl:+.2f}")
    log_trade(trade_num, "SHORT", pid, entry, price, size, pnl, "TIMEOUT", BANK + pnl)
    return pnl

# ── Main loop ─────────────────────────────────────────────────────────────────
def run():
    global BANK
    trade_num = 0
    print(f"PAPER BOT v2  Bank={BANK:.2f}")
    print(f"Strategy: LONG breakout (trail={LONG_TRAIL_PCT*100}% / TP={LONG_TP_PCT*100}% / SL={LONG_SL_PCT*100}%)")
    print(f"          then SHORT exhaustion (TP={SHORT_TP_PCT*100}% / SL={SHORT_SL_PCT*100}%)")
    print(f"Log: {LOG_FILE}\n")

    while True:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Scanning...")
        movers = get_movers()

        if not movers:
            print("No candidates. Retrying in 60s...")
            time.sleep(SCAN_SECS)
            continue

        print("Top movers (eligible):")
        for m in movers[:5]:
            print(f"  {m[0]:<18} +{m[2]:.2f}%  vol=${m[3]:,.0f}")

        pid, price, chg, vol = movers[0]
        seen_tickers[pid] = time.time()   # mark cooldown start

        size = round(BANK * BET_PCT, 2)
        trade_num += 1
        print(f"\n[Trade {trade_num}] {pid} +{chg:.2f}%  size={size:.2f}")

        # ── Phase 1: LONG ──
        exit_price, pnl1 = phase1_long(pid, price, size, trade_num)
        BANK += pnl1
        print(f"  Bank after P1: {BANK:.2f}")

        # ── Phase 2: SHORT (only if P1 exited cleanly, not on SL) ──
        if exit_price is not None:
            trade_num += 1
            print(f"\n[Trade {trade_num}] Flipping SHORT {pid} @ {exit_price:.6f}  size={size:.2f}")
            pnl2 = phase2_short(pid, exit_price, size, trade_num)
            BANK += pnl2
            print(f"  Bank after P2: {BANK:.2f}")
        else:
            print("  P1 SL hit — skipping short phase.")

        print(f"\n{'─'*50}  Bank: {BANK:.2f}\n")
        time.sleep(SCAN_SECS)

try:
    run()
except KeyboardInterrupt:
    print(f"\nStopped. Final bank: {BANK:.2f}")
    print(f"Trade log: {LOG_FILE}")
