Here is the complete visual documentation of the path to **platform.worldquantbrain.com/simulate** for Hour House · Newark, NJ · Adult ESL · Lesson 07:

---

## How to Get to Gold — Step-by-Step Documentation

### Step 1 — Open the Simulator
Navigate to: **platform.worldquantbrain.com/simulate**

You will land on the Simulate page with a code editor on the left and a results/tutorial panel on the right.

---

### Step 2 — Set Your Universe (Operator C)
Click the **⚙ Settings** button (top left). Set these exact values:

| Setting | Value |
|---|---|
| Language | Fast Expression |
| Instrument Type | Equity |
| Region | USA |
| Universe | TOP3000 |
| Delay | 1 |
| Neutralization | **Subindustry** |
| Decay | **4** |
| Truncation | **0.08** |
| Pasteurization | **On** |

Click **Apply**. The header will show **USA/D1/TOP3000**.

---

### Step 3 — Enter Your Formula (Operator K)
Click in the dark code editor on the left. Type the winning formula:

```
rank(ts_decay_linear(group_neutralize(rank(sales / close) + rank(-ts_rank(close, 3)), subindustry), 4))
```

What each part does:
- `rank(sales / close)` — value signal: high-sales, low-price companies
- `rank(-ts_rank(close, 3))` — reversal signal: bet on stocks near their 3-day low
- `group_neutralize(..., subindustry)` — removes industry-wide effects
- `ts_decay_linear(..., 4)` — weights recent data more heavily
- outer `rank(...)` — maps everything to 0–1 across all 3,000 stocks

---

### Step 4 — Simulate (Operator F)
Click the green **Simulate** button. Watch the progress bar:
- It starts at **10%**, moves to **15%**, then stalls at **35%** for an extended time — **this is normal, do not click away**
- Total time: 3–5 minutes

---

### Step 5 — Read Your Results
When simulation finishes, click the **IS** button to switch from OS to IS period. You will see:

**IS Summary — Aggregate Data:**
| Sharpe | Turnover | Fitness | Returns | Drawdown | Margin |
|---|---|---|---|---|---|
| **1.79** ✅ | 20.77% | **1.39** ✅ | 12.57% | 8.08% | 12.11‰ |

Both key thresholds pass: Sharpe ≥ 1.25 ✅ and Fitness ≥ 1.0 ✅

---

### Step 6 — Check IS Testing Status
Click **"Open alpha details in new tab"** (bottom bar), then scroll down to find **IS Testing Status**. Click **IS** in the Period selector. Click **7 PASS** to expand it:

| Check | Result |
|---|---|
| ✅ Sharpe of **1.79** above cutoff of **1.25** | PASS |
| ✅ Fitness of **1.39** above cutoff of **1** | PASS |
| ✅ Turnover **20.77%** above cutoff of **1%** | PASS |
| ✅ Turnover **20.77%** below cutoff of **70%** | PASS |
| ✅ Weight well distributed over instruments | PASS |
| ✅ Sub-universe Sharpe **1.09** above cutoff of **0.78** | PASS |
| ✅ Competition Challenge matches | PASS |

Then click **Check Submission** to trigger the 8th check (self-correlation). It shows PENDING briefly, then resolves.

---

### Step 7 — Submit (Operator U)
When all 8 checks pass, click **Submit Alpha**. The alpha enters the WorldQuant live pool, the USA IQC aggregate score goes up, and the alpha is tagged **ACTV** (Active).

---

### Key Warning Signs to Document for Students
- **If tutorial mode appears** after simulation — click "Exit tutorial mode" → confirm "Exit"
- **If progress stalls at 35%** — this is normal, wait it out
- **If self-correlation fails** (e.g., 0.87 or 0.9987) — do not change the window numbers; change the operator family entirely. Switch from `ts_delta/ts_std_dev` (parametric z-score) to `ts_rank` (non-parametric ranking)
- **Invalid fields** that cause errors: `earnings`, `net_income` — use `sales`, `income`, `assets`, `close`, `volume`, `returns` instead
- **Invalid operator**: `ts_max` does not exist — use `ts_rank` instead
