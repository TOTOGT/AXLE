#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
axle_rag.handoff — the mandatory empty-tank protocol
====================================================
G6 LLC · Principia Orthogona · AXLE-RAG · MIT License

The scheduled audit knows COMMITTED state. It cannot see what the session in
front of you is holding: the half-finished edit, the decision just made, the
thing deliberately NOT done. That is exactly what is lost when an account hits
its limit mid-task — and it is why the next session "is always fixing something."

So the rule is: **write the handoff before you need it.** This tool makes that
cost about sixty seconds, because a protocol that costs more will not be run
when the tank is empty.

    python3 handoff.py start   -m "repairing r* drift across GTCT + site"
    python3 handoff.py note    -m "ch03 still shows 0.8 — deliberate, awaiting ruling"
    python3 handoff.py decide  -m "series DOI is 19117399" --because "resolves to latest"
    python3 handoff.py blocked -m "need Chain_updated.lean from AXLE NASA path"
    python3 handoff.py end                       # writes SESSION.md, prints the paste-block

`end` also runs when you are nearly out: it snapshots git state (branch, dirty
files, last commits) so the next session inherits the working tree, not just the
repo. Nothing here needs the network.

Exit code of `check` is 1 if a session is open with no `end` — wire it into a
pre-push hook and the handoff becomes structurally mandatory:

    .git/hooks/pre-push:  python3 handoff.py check || exit 1
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

STATE = Path(os.environ.get("AXLE_SESSION_STATE", ".axle_session.json"))
OUT   = Path(os.environ.get("AXLE_SESSION_OUT", "SESSION.md"))


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def sh(*cmd: str) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=15).stdout.strip()
    except Exception:
        return ""


def git_snapshot() -> dict:
    return {
        "branch": sh("git", "rev-parse", "--abbrev-ref", "HEAD"),
        "head": sh("git", "rev-parse", "--short", "HEAD"),
        "dirty": [l for l in sh("git", "status", "--porcelain").splitlines() if l.strip()],
        "recent": sh("git", "log", "--oneline", "-5").splitlines(),
    }


def load() -> dict:
    if STATE.exists():
        try:
            return json.loads(STATE.read_text())
        except Exception:
            pass
    return {}


def save(d: dict) -> None:
    STATE.write_text(json.dumps(d, indent=2, ensure_ascii=False))


def cmd_start(a) -> int:
    s = load()
    if s.get("open"):
        print(f"session already open since {s['started']}: {s.get('goal','')}")
        print("use `note` / `decide` / `blocked`, or `end` to close it.")
        return 0
    save({"open": True, "started": now(), "goal": a.message,
          "account": a.account or os.environ.get("AXLE_ACCOUNT", "unknown"),
          "notes": [], "decisions": [], "blocked": [], "git_start": git_snapshot()})
    print(f"session open — {a.message}")
    return 0


def _append(kind: str, a) -> int:
    s = load()
    if not s.get("open"):
        print("no open session; run `start` first (or this note will be lost).")
        return 1
    item = {"t": now(), "text": a.message}
    if kind == "decisions" and getattr(a, "because", None):
        item["because"] = a.because
    s[kind].append(item)
    save(s)
    print(f"{kind[:-1]} recorded ({len(s[kind])} total)")
    return 0


def cmd_end(a) -> int:
    s = load()
    if not s.get("open"):
        print("no open session to close.")
        return 0
    g0, g1 = s.get("git_start", {}), git_snapshot()
    started, ended = s.get("started", "?"), now()

    L = [f"# SESSION HANDOFF — {ended}", "",
         f"**Account:** `{s.get('account','unknown')}`  ",
         f"**Window:** {started} → {ended}  ",
         f"**Goal:** {s.get('goal','—')}", "",
         "> Written before the tank ran out. The next session starts at "
         "**Next actions**, not at the beginning.", ""]

    if s["decisions"]:
        L += ["## Decisions made (do not re-litigate)", ""]
        for d in s["decisions"]:
            L.append(f"- **{d['text']}**" + (f" — _{d['because']}_" if d.get("because") else ""))
        L.append("")

    if s["notes"]:
        L += ["## What happened", ""] + [f"- {n['text']}" for n in s["notes"]] + [""]

    if s["blocked"]:
        L += ["## Blocked / needs the human", ""] + [f"- ⛔ {b['text']}" for b in s["blocked"]] + [""]

    L += ["## Working tree at handoff", "",
          f"- branch `{g1.get('branch','?')}` @ `{g1.get('head','?')}`"
          + (f" (was `{g0.get('head','?')}`)" if g0.get("head") != g1.get("head") else " (no commits this session)"),
          ""]
    if g1.get("dirty"):
        L += ["**Uncommitted — this is the in-flight work:**", "", "```"] \
             + g1["dirty"][:40] + ["```", ""]
    else:
        L += ["_Working tree clean._", ""]
    if g1.get("recent"):
        L += ["<details><summary>recent commits</summary>", "", "```"] \
             + g1["recent"] + ["```", "</details>", ""]

    L += ["## Next actions", "",
          "1. Read `HANDOFF.md` (corpus state — regenerated by the scheduled audit).",
          "2. Resolve anything under **Blocked** above first.",
          "3. Before editing a constant or a DOI, run the closure:",
          "   ```bash",
          "   python3 flow.py chunks.jsonl --change \"const:<name>\" --order",
          "   ```",
          "4. Do not 'tidy' a hedge; a caveat is removed only by the edit that verifies it.",
          "5. Start your own session: `python3 handoff.py start -m \"<goal>\"`.", ""]

    OUT.write_text("\n".join(L), encoding="utf-8")
    s["open"] = False
    s["ended"] = ended
    save(s)

    print(f"handoff written → {OUT}\n")
    print("─" * 62)
    print("PASTE THIS INTO THE NEXT SESSION:")
    print("─" * 62)
    print(f"Continuing work on: {s.get('goal','—')}")
    if s["blocked"]:
        print("Blocked on: " + "; ".join(b["text"] for b in s["blocked"]))
    if s["decisions"]:
        print("Already decided: " + "; ".join(d["text"] for d in s["decisions"]))
    print(f"Read {OUT} and HANDOFF.md first. Do not redo settled decisions.")
    print("─" * 62)
    return 0


def cmd_check(a) -> int:
    s = load()
    if s.get("open"):
        n = len(s["notes"]) + len(s["decisions"]) + len(s["blocked"])
        print(f"⛔ session open since {s['started']} ({n} entries) — run `handoff.py end` first.")
        return 1
    print("no open session.")
    return 0


def cmd_status(a) -> int:
    s = load()
    if not s.get("open"):
        print("no open session." + (f" last ended {s['ended']}." if s.get("ended") else ""))
        return 0
    print(f"open since {s['started']} · {s.get('account')}\ngoal: {s.get('goal')}")
    for k, sym in (("decisions", "✔"), ("notes", "·"), ("blocked", "⛔")):
        for i in s[k]:
            print(f"  {sym} {i['text']}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Mandatory session handoff protocol.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("start"); p.add_argument("-m", "--message", required=True)
    p.add_argument("--account", help="which Claude account is driving")
    p.set_defaults(fn=cmd_start)

    for name, kind in (("note", "notes"), ("blocked", "blocked")):
        p = sub.add_parser(name); p.add_argument("-m", "--message", required=True)
        p.set_defaults(fn=lambda a, k=kind: _append(k, a))

    p = sub.add_parser("decide"); p.add_argument("-m", "--message", required=True)
    p.add_argument("--because", help="the reason, so it is not re-litigated")
    p.set_defaults(fn=lambda a: _append("decisions", a))

    for name, fn in (("end", cmd_end), ("check", cmd_check), ("status", cmd_status)):
        sub.add_parser(name).set_defaults(fn=fn)

    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
