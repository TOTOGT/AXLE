# Setting up the watchtower

**Repo to create: `TOTOGT/axle-monitor`** (public). It watches the corpus
repos; it does not contain them.

```
axle-monitor/
├── ingest.py  retrieve.py  audit.py  flow.py  handoff.py
├── README.md
├── HANDOFF.md          ← generated daily, committed. THE shared state.
├── ROOTS.md            ← generated: every constant/DOI/lean node + blast radius
├── findings.json       ← generated
└── .github/workflows/
    ├── corpus-audit.yml   (scheduled + push + manual)
    └── work-order.yml     (manual: "what does changing X break?")
```

## 1 · Create it

```bash
gh repo create TOTOGT/axle-monitor --public --clone
cd axle-monitor
cp -r /path/to/axle_rag/* .
git add . && git commit -m "AXLE-RAG: corpus watchtower" && git push
```

Actions permissions: **Settings → Actions → General → Workflow permissions →
Read and write**, and tick *Allow GitHub Actions to create and approve pull
requests*. Without this the workflow cannot commit `HANDOFF.md` or open issues.

Private corpus repos? Add a fine-grained PAT as secret `CORPUS_TOKEN` and change
the clone URL in the workflow to
`https://x-access-token:${{ secrets.CORPUS_TOKEN }}@github.com/$1.git`.

## 2 · What runs when

| trigger | what happens |
|---|---|
| daily 11:00 UTC (≈06:00 Newark) | re-ingest → audit → commit `HANDOFF.md` → issue on HIGH → red badge |
| push to `main` | same, immediately |
| manual (`workflow_dispatch`) | same, with a severity you choose |
| manual **work order** | `--change const:r*` → full closure as an issue checklist |

Badge for the corpus README:

```markdown
![corpus audit](https://github.com/TOTOGT/axle-monitor/actions/workflows/corpus-audit.yml/badge.svg)
```

Red badge = the corpus currently contradicts itself. That is the signal you can
see from any account without opening anything.

## 3 · The empty-tank rule

The scheduled job knows **committed** state. It cannot know what the live
session is holding. So:

> **When the tank looks low, `handoff.py end` is mandatory — before the last
> useful message, not after.**

```bash
python3 handoff.py start  -m "repairing r* drift" --account claude-A
python3 handoff.py decide -m "series DOI is 19117399" --because "resolves to latest"
python3 handoff.py note   -m "GTCT tex + 4 figures done; ch10 synced ×3"
python3 handoff.py blocked -m "book4/ch03.html still shows 0.8"
python3 handoff.py end            # writes SESSION.md + a paste-block
```

`end` prints a short block. Paste it as the **first message** of the next
session, on any account. It contains the goal, the blockers, and the settled
decisions — so session B does not re-litigate what session A already decided.

Make it structural, not a habit:

```bash
cat > .git/hooks/pre-push <<'EOF'
#!/bin/sh
python3 handoff.py check || {
  echo "Open session — run: python3 handoff.py end"; exit 1; }
EOF
chmod +x .git/hooks/pre-push
```

Now you cannot push with an unclosed session.

## 4 · The two files that matter

- **`HANDOFF.md`** — corpus state. Machine-generated, always current, committed.
  Claim inventory, contested constants, open claims, inherited rules.
- **`SESSION.md`** — human/session state. What was decided and what is in flight.

A fresh session reads both, in that order, and starts at *Next actions*.

## 5 · First run will be noisy

The first audit over the full corpus will surface real drift — several `r*`
values, DOI collisions (19117399 vs 19117400), κ symbol reuse, prose/Lean
mismatches. That is the point. Triage HIGH first, and use the work order so each
fix propagates completely instead of leaving the next session something to
"discover."

## 6 · Limits

- Actions cron is best-effort; GitHub may delay a scheduled run.
- Scheduled workflows are disabled automatically after 60 days of repo
  inactivity — the daily commit of `HANDOFF.md` keeps the repo active, so this
  is self-sustaining as long as findings change. If the corpus goes fully quiet,
  re-enable manually.
- Everything here is lexical/structural. It catches contradiction and drift.
  It does not check whether a claim is *true* — only whether the corpus agrees
  with itself and with its own labels.
