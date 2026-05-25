"""
Polymarket BTC Trading Bot — Multi-Signal Ensemble (Option 4)
Data source: Kraken REST API
Strategy: RSI + EMA Crossover + MACD + Volume → weighted confidence score
Trades when confidence >= 95% | Bet size: 5% of bankroll
Markets: Same-day BTC resolution on Polymarket
"""

import time
import logging
import requests
import numpy as np
from datetime import datetime, timezone
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType, Side

# ─────────────────────────────────────────────
# CONFIGURATION — fill in your credentials
# ─────────────────────────────────────────────

POLYMARKET_HOST      = "https://clob.polymarket.com"
PRIVATE_KEY          = "YOUR_PRIVATE_KEY"       # Polygon wallet private key
API_KEY              = "YOUR_API_KEY"
API_SECRET           = "YOUR_API_SECRET"
API_PASSPHRASE       = "YOUR_API_PASSPHRASE"
CHAIN_ID             = 137                       # Polygon mainnet

BANKROLL             = 120.0                     # Starting USDC
BET_FRACTION         = 0.05                      # 5% per trade
CONFIDENCE_THRESHOLD = 0.95                      # 95% required to fire
POLL_INTERVAL        = 60                        # seconds between checks

# Kraken pair
KRAKEN_PAIR          = "XBTUSD"
KRAKEN_INTERVAL      = 5                         # candle size in minutes

# ─────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# KRAKEN DATA
# ─────────────────────────────────────────────

def fetch_ohlcv(pair: str, interval: int = 5, limit: int = 100) -> list:
    """Fetch OHLCV candles from Kraken REST API."""
    url = "https://api.kraken.com/0/public/OHLC"
    params = {"pair": pair, "interval": interval}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        if data.get("error"):
            log.error(f"Kraken error: {data['error']}")
            return []
        result_key = list(data["result"].keys())[0]
        candles = data["result"][result_key]
        # Each candle: [time, open, high, low, close, vwap, volume, count]
        return candles[-limit:]
    except Exception as e:
        log.error(f"Kraken fetch failed: {e}")
        return []

def parse_closes_volumes(candles: list):
    closes  = np.array([float(c[4]) for c in candles])
    volumes = np.array([float(c[6]) for c in candles])
    return closes, volumes

# ─────────────────────────────────────────────
# INDICATORS
# ─────────────────────────────────────────────

def compute_rsi(closes: np.ndarray, period: int = 14) -> float:
    if len(closes) < period + 1:
        return 50.0
    deltas = np.diff(closes)
    gains  = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    if avg_loss == 0:
        return 100.0
    rs  = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def ema(values: np.ndarray, period: int) -> np.ndarray:
    k = 2 / (period + 1)
    result = np.zeros(len(values))
    result[0] = values[0]
    for i in range(1, len(values)):
        result[i] = values[i] * k + result[i - 1] * (1 - k)
    return result

def compute_macd(closes: np.ndarray):
    if len(closes) < 26:
        return 0.0, 0.0
    fast   = ema(closes, 12)
    slow   = ema(closes, 26)
    macd   = fast - slow
    signal = ema(macd, 9)
    return macd[-1], signal[-1]

def compute_ema_crossover(closes: np.ndarray):
    if len(closes) < 21:
        return 0.0, 0.0
    fast = ema(closes, 9)
    slow = ema(closes, 21)
    return fast[-1], slow[-1]

def compute_volume_score(volumes: np.ndarray, period: int = 20) -> float:
    """Returns ratio of latest volume to rolling average (capped at 3)."""
    if len(volumes) < period:
        return 1.0
    avg = np.mean(volumes[-period:-1])
    if avg == 0:
        return 1.0
    ratio = volumes[-1] / avg
    return min(ratio, 3.0)

# ─────────────────────────────────────────────
# ENSEMBLE CONFIDENCE SCORE
# ─────────────────────────────────────────────

def compute_confidence(closes: np.ndarray, volumes: np.ndarray) -> tuple:
    """
    Returns (confidence: float 0-1, direction: 'UP'|'DOWN'|'NEUTRAL')
    Weights: RSI 30% | EMA crossover 25% | MACD 25% | Volume 20%
    """
    signals = {}

    # --- RSI ---
    rsi = compute_rsi(closes)
    if rsi >= 70:
        signals["rsi"] = ("UP",   (rsi - 70) / 30)       # 0–1 as rsi goes 70→100
    elif rsi <= 30:
        signals["rsi"] = ("DOWN", (30 - rsi) / 30)
    else:
        signals["rsi"] = ("NEUTRAL", 0.0)

    # --- EMA Crossover ---
    fast_ema, slow_ema = compute_ema_crossover(closes)
    spread = (fast_ema - slow_ema) / slow_ema if slow_ema else 0
    if spread > 0:
        signals["ema"] = ("UP",   min(abs(spread) * 500, 1.0))
    elif spread < 0:
        signals["ema"] = ("DOWN", min(abs(spread) * 500, 1.0))
    else:
        signals["ema"] = ("NEUTRAL", 0.0)

    # --- MACD ---
    macd_val, signal_val = compute_macd(closes)
    macd_diff = macd_val - signal_val
    if macd_diff > 0:
        signals["macd"] = ("UP",   min(abs(macd_diff) / 100, 1.0))
    elif macd_diff < 0:
        signals["macd"] = ("DOWN", min(abs(macd_diff) / 100, 1.0))
    else:
        signals["macd"] = ("NEUTRAL", 0.0)

    # --- Volume ---
    vol_score = compute_volume_score(volumes)
    vol_boost = min((vol_score - 1.0) / 2.0, 1.0)   # 0 if avg, 1 if 3x avg

    # --- Weighted score per direction ---
    weights = {"rsi": 0.30, "ema": 0.25, "macd": 0.25}
    up_score   = 0.0
    down_score = 0.0

    for key, (direction, strength) in signals.items():
        w = weights[key]
        if direction == "UP":
            up_score   += w * strength
        elif direction == "DOWN":
            down_score += w * strength

    # Volume amplifies whichever side is winning
    vol_weight = 0.20
    if up_score >= down_score:
        up_score   += vol_weight * vol_boost * up_score
    else:
        down_score += vol_weight * vol_boost * down_score

    # Normalize
    total = up_score + down_score
    if total == 0:
        return 0.0, "NEUTRAL"

    if up_score > down_score:
        confidence = up_score / (up_score + (1 - down_score))
        return min(confidence, 1.0), "UP"
    else:
        confidence = down_score / (down_score + (1 - up_score))
        return min(confidence, 1.0), "DOWN"

# ─────────────────────────────────────────────
# POLYMARKET CLIENT
# ─────────────────────────────────────────────

def get_client() -> ClobClient:
    return ClobClient(
        host=POLYMARKET_HOST,
        key=PRIVATE_KEY,
        chain_id=CHAIN_ID,
        api_key=API_KEY,
        api_secret=API_SECRET,
        api_passphrase=API_PASSPHRASE,
    )

def find_btc_same_day_market(client: ClobClient) -> dict | None:
    """
    Find an active same-day BTC market on Polymarket.
    Looks for markets with 'BTC' and today's date in the question.
    """
    today = datetime.now(timezone.utc).strftime("%B %d").lstrip("0")
    try:
        markets = client.get_markets()
        for m in markets.get("data", []):
            question = m.get("question", "").upper()
            end_date = m.get("end_date_iso", "")
            if "BTC" not in question:
                continue
            # Check same-day expiry
            if end_date:
                expiry = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
                now    = datetime.now(timezone.utc)
                hours_left = (expiry - now).total_seconds() / 3600
                if 0 < hours_left <= 24:
                    log.info(f"Found market: {m['question']} | expires in {hours_left:.1f}h")
                    return m
    except Exception as e:
        log.error(f"Market search failed: {e}")
    return None

def place_order(client: ClobClient, market: dict, direction: str, amount_usdc: float):
    """Place a market order on Polymarket."""
    try:
        token_id = market["tokens"][0]["token_id"] if direction == "UP" else market["tokens"][1]["token_id"]
        price    = client.get_last_trade_price(token_id)
        if not price:
            log.warning("Could not fetch price, skipping order.")
            return

        size = round(amount_usdc / float(price), 2)

        order_args = OrderArgs(
            token_id=token_id,
            price=float(price),
            size=size,
            side=Side.BUY,
        )
        signed_order = client.create_order(order_args)
        resp = client.post_order(signed_order, OrderType.FOK)
        log.info(f"Order placed | direction={direction} | size={size} | price={price} | response={resp}")
    except Exception as e:
        log.error(f"Order failed: {e}")

# ─────────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────────

def main():
    log.info("=== Polymarket BTC Bot starting (Multi-Signal Ensemble) ===")
    client   = get_client()
    bankroll = BANKROLL
    trades_today = 0
    last_trade_date = None

    while True:
        try:
            now = datetime.now(timezone.utc)

            # Reset daily trade counter
            if last_trade_date != now.date():
                trades_today    = 0
                last_trade_date = now.date()

            # 1. Fetch Kraken data
            candles = fetch_ohlcv(KRAKEN_PAIR, KRAKEN_INTERVAL)
            if len(candles) < 30:
                log.warning("Not enough candle data, waiting...")
                time.sleep(POLL_INTERVAL)
                continue

            closes, volumes = parse_closes_volumes(candles)
            btc_price = closes[-1]

            # 2. Compute ensemble confidence
            confidence, direction = compute_confidence(closes, volumes)
            log.info(f"BTC=${btc_price:,.2f} | confidence={confidence:.2%} | direction={direction}")

            # 3. Check threshold
            if confidence >= CONFIDENCE_THRESHOLD and direction != "NEUTRAL":
                # 4. Find same-day market
                market = find_btc_same_day_market(client)
                if not market:
                    log.info("No suitable same-day BTC market found.")
                else:
                    bet_size = round(bankroll * BET_FRACTION, 2)
                    log.info(f"SIGNAL FIRED | direction={direction} | confidence={confidence:.2%} | bet=${bet_size}")
                    place_order(client, market, direction, bet_size)
                    trades_today += 1
                    log.info(f"Trades today: {trades_today}")
            else:
                log.info(f"Below threshold ({confidence:.2%} < {CONFIDENCE_THRESHOLD:.0%}), holding.")

        except KeyboardInterrupt:
            log.info("Bot stopped by user.")
            break
        except Exception as e:
            log.error(f"Unexpected error: {e}")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
