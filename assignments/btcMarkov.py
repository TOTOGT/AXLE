import ccxt
import numpy as np
from collections import deque
from datetime import datetime
import csv, os, time

exchange = ccxt.binance()
LOG_FILE = "btc_markov_signals.csv"

def init_log():
    exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["timestamp","price","direction","p_jj","lookback","threshold"])

def log_signal(price, direction, pjj, lookback, threshold):
    with open(LOG_FILE, "a", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            datetime.now().isoformat(timespec="seconds"),
            price,
            direction,
            round(pjj,4),
            lookback,
            threshold
        ])

def btc_markov_alpha(lookback=20, threshold=0.87):
    init_log()
    prices = deque(maxlen=lookback+10)

    while True:
        try:
            t = exchange.fetch_ticker('BTC/USDT')
            last = t['last']
            prices.append(last)

            if len(prices) < lookback:
                time.sleep(10)
                continue

            rets = np.diff(list(prices))
            states = np.clip(np.sign(rets[-lookback:]), -1, 1).astype(int) + 1

            trans = np.zeros((3,3))
            for i in range(len(states)-1):
                trans[states[i], states[i+1]] += 1
            trans = trans / trans.sum(axis=1, keepdims=True)

            cs = states[-1]
            pjj = trans[cs, cs]
            direction = "UP" if cs==2 else "DOWN" if cs==0 else "FLAT"

            if pjj >= threshold:
                print(f"{datetime.now().strftime('%H:%M:%S')} | LOCKED {direction} | p(j,j)={pjj:.3f}")
                log_signal(last, direction, pjj, lookback, threshold)
            else:
                print(f"{datetime.now().strftime('%H:%M:%S')} | p(j,j)={pjj:.3f}")

            time.sleep(10)

        except Exception as e:
            print("ERR:", e)
            time.sleep(10)

btc_markov_alpha()