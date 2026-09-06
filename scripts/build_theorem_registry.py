#!/usr/bin/env python3
"""Regenerate theorem-registry.html from the live .lean files.
Honest text-scan (same heuristic as theorem_tracker.py; NOT a kernel check).
Core = top-level files (trusted). Extended = subfolders (hold known duplicates/orphans)."""
import re, os, sys, glob, html, datetime
from pathlib import Path

# ONE scan method for the whole corpus. This script used to carry its own regex,
# which matched only line-initial `^(theorem|lemma)` -- missing `private theorem`
# and anything under an `@[simp]` -- and did not strip comments, so a declaration
# named in a docstring counted as a declaration. Two errors in opposite directions,
# which is why its totals never reconciled with tools/theorem_census.py. It now
# delegates, so there is one method and one place to fix it.
_CENSUS = os.environ.get('GEOMETRY_TOOLS',
                         os.path.expanduser('~/Desktop/geometry/tools'))
sys.path.insert(0, _CENSUS)
try:
    import theorem_census as TC
    import axiom_gate as AG
except ImportError:
    sys.exit(f'theorem_census.py not found under {_CENSUS}. '
             'Set GEOMETRY_TOOLS to the geometry repo tools directory.')

AX = re.compile(r"^\s*axiom\s+[A-Za-z_]", re.M)
root = Path('.')


def files(rec):
    return (sorted(p for p in root.rglob('*.lean') if '.lake' not in p.parts)
            if rec else sorted(root.glob('*.lean')))


def scan(fs):
    """(entries, axiom_count) using theorem_census's comment-stripped method."""
    ents = []
    ax = 0
    for f in fs:
        src = TC.strip_comments(f.read_text(errors='ignore'))
        ax += len(AX.findall(src))
        ms = list(TC.DECL.finditer(src))
        for i, m in enumerate(ms):
            end = ms[i + 1].start() if i + 1 < len(ms) else len(src)
            st = 'sorry' if re.search(r'\bsorry\b', src[m.start():end]) else 'proved'
            ents.append((str(f).lstrip('./'), m.group(2), st))
    return ents, ax


def _corpus_roots():
    """The same root set every other published number uses.

    Reads geometry/tools/corpus_roots.txt rather than carrying its own list,
    because two lists of roots is two corpora and only one of them gets updated.
    """
    f = os.path.join(os.path.dirname(_CENSUS), 'tools', 'corpus_roots.txt')
    roots = []
    if os.path.exists(f):
        for line in open(f, encoding='utf-8'):
            line = line.split('#')[0].strip()
            if line:
                roots.append(os.path.expanduser(line))
    here = os.path.abspath('.')
    if here not in roots:
        roots.append(here)
    return roots


def kernel_tier():
    """Tier 1: declarations a gate actually ran `#print axioms` on.

    Read out of the axioms.txt files the gates write, so this number cannot be
    typed -- it exists only if a probe produced it. A declaration whose report
    line contains sorryAx contributes nothing: admitted is disclosed, not audited.

    UNDERCOUNT FIXED 2026-09-06. This used to glob two hardcoded shapes -- the
    cwd's own tools/verify-*/ and geometry's. That missed every gate report
    living anywhere else in the corpus, most importantly vol1-proofs/tools/
    axioms.txt, which alone holds 82 audited declarations. Tier 1 read 32 when
    the true figure was 133: a four-fold undercount, and it was in this glob,
    not in the Lean. It now sweeps every corpus root.

    Deposit copies under docs/ml-evidence/ and anything under a to_delete path
    are excluded on purpose: a deposit copy is evidence, not a source, and
    counting it would double a report already counted at its origin.
    """
    seen, sources = {}, []
    shapes = ['tools/verify-*/axioms*.txt', 'tools/axioms*.txt',
              'CS/verify-stamp/axioms*.txt',
              # dated per-file reports from `leancheck.sh --audit`
              'tools/verify-audit/*/*.axioms.txt']
    skip = re.compile(r'(^|/)(_?to_delete|ml-evidence|\.lake)(/|$)')
    reports = []
    for root in _corpus_roots():
        for shape in shapes:
            reports += glob.glob(os.path.join(root, shape))
    for rep in sorted(set(os.path.realpath(r) for r in reports)):
        if skip.search(rep):
            continue
        txt = open(rep, encoding='utf-8', errors='replace').read()
        # Parsed by tools/axiom_gate.py, never by a local regex. It rejoins
        # Lean's wrapped pretty-printer output, reads BOTH forms (a proof
        # resting on nothing reports `does not depend on any axioms`, and that
        # is the strongest result there is), and holds the allowlist. The
        # previous filter here was a sorryAx grep -- the forbidden-list shape
        # WP-73 §6 rejects, which cannot see Lean.ofReduceBool or a
        # native_decide axiom and would credit a declaration the kernel never
        # checked. Permitted three in, everything else out.
        recs, _unparsed = AG.parse(txt)
        allowed = set(AG.DEFAULT_ALLOWED)
        clean = [n for n, ax in recs if set(ax) <= allowed]
        if not clean:
            continue
        for n in clean:
            seen.setdefault(n, rep)
        mt = datetime.date.fromtimestamp(os.path.getmtime(rep))
        label = os.path.relpath(rep, os.path.dirname(os.path.dirname(_CENSUS)))
        sources.append((label, len(clean), mt.isoformat()))
    return sorted(seen), sources

cf = files(False)
rf = files(True)
core, cax = scan(cf)
rec, rax = scan(rf)
cpaths = {str(f).lstrip('./') for f in cf}
ext = [e for e in rec if e[0] not in cpaths]


def c(es):
    return sum(e[2] == 'proved' for e in es), sum(e[2] == 'sorry' for e in es)


cp, cs = c(core)
rp, rs = c(rec)
ep, es = c(ext)

k_names, k_sources = kernel_tier()
kn = len(k_names)
# was datetime.date(2026,7,16) -- a hardcoded literal, so every regeneration
# restamped the same July date and the page looked stale whenever it was not.
today=datetime.date.today().strftime('%B %-d, %Y')
def rows(ents):
    out=[]; last=None
    for path,name,st in sorted(ents):
        if path!=last: out.append(f'<div class="file">{html.escape(path)}</div>'); last=path
        b='✓' if st=='proved' else '⚠'
        out.append(f'<div class="thm" data-st="{st}"><span class="b b-{st}">{b}</span>{html.escape(name)}</div>')
    return '\n'.join(out)
H=f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AXLE Theorem Registry — Imaginary Origin</title>
<meta name="description" content="Honest, live-scanned theorem registry for the AXLE / Principia Orthogona Lean 4 corpus. Text-scan heuristic, not a kernel check. Core (top-level) and extended (subfolder) tiers reported separately.">
<style>
:root{{--navy:#1a2744;--gold:#c9a84c;--cream:#faf7f0;--smoke:#f0ece4;--ink:#1c1c1c;--muted:#6b6757;--green:#2d5a27;--red:#8b1a1a;--rule:#d9d3c4;}}
*{{box-sizing:border-box;}}body{{margin:0;background:var(--cream);color:var(--ink);font-family:Georgia,serif;line-height:1.5;}}
header{{background:var(--navy);color:#fff;padding:2rem 1.4rem 1.6rem;}}
.wrap{{max-width:960px;margin:0 auto;padding:0 1.2rem;}}
h1{{font-size:1.5rem;margin:0 0 .2rem;color:var(--gold);}}
.sub{{font-size:.85rem;color:#cfd6e4;}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule);margin:1.4rem auto;max-width:960px;}}
.card{{background:#fff;padding:.9rem 1rem;text-align:center;}}
.card .n{{font-family:'Courier New',monospace;font-size:1.5rem;color:var(--navy);display:block;}}
.card .l{{font-family:'Courier New',monospace;font-size:.58rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);}}
.note{{max-width:960px;margin:1rem auto;padding:.9rem 1.1rem;background:var(--smoke);border-left:3px solid var(--gold);font-size:.84rem;}}
.caveat{{border-left-color:var(--red);}}
.controls{{max-width:960px;margin:1.2rem auto .6rem;display:flex;gap:.5rem;flex-wrap:wrap;}}
.controls button{{font-family:'Courier New',monospace;font-size:.7rem;text-transform:uppercase;letter-spacing:.05em;padding:.35rem .8rem;border:1px solid var(--navy);background:#fff;color:var(--navy);cursor:pointer;}}
.controls button.on{{background:var(--navy);color:var(--gold);}}
h2{{max-width:960px;margin:2rem auto .4rem;font-size:1.05rem;color:var(--navy);border-bottom:2px solid var(--gold);padding-bottom:.2rem;}}
.list{{max-width:960px;margin:0 auto;}}
.file{{font-family:'Courier New',monospace;font-size:.74rem;color:var(--gold);background:var(--navy);padding:.35rem .7rem;margin-top:.5rem;}}
.thm{{font-family:'Courier New',monospace;font-size:.78rem;padding:.2rem .7rem;border-bottom:1px solid var(--rule);display:flex;align-items:center;gap:.5rem;}}
.b{{display:inline-block;width:1.1em;text-align:center;font-weight:bold;}}.b-proved{{color:var(--green);}}.b-sorry{{color:var(--red);}}
footer{{max-width:960px;margin:2rem auto;padding:1.2rem;border-top:1px solid var(--rule);font-size:.72rem;color:var(--muted);text-align:center;}}
footer a{{color:var(--gold);}}
</style></head><body>
<header><div class="wrap"><h1>AXLE Theorem Registry</h1>
<div class="sub">Principia Orthogona · Lean 4 / Mathlib4 · live text-scan, regenerated {today} · <a href="index.html" style="color:var(--gold);">Imaginary Origin ↩</a></div></div></header>

<div class="cards">
  <div class="card"><span class="n">{cp}</span><span class="l">Core proved</span></div>
  <div class="card"><span class="n">{cs}</span><span class="l">Core sorry (open)</span></div>
  <div class="card"><span class="n">{cax}</span><span class="l">Core axioms</span></div>
  <div class="card"><span class="n">{len(cf)}</span><span class="l">Core files</span></div>
</div>
<div class="note"><b>Tier 1 &mdash; kernel-audited: {kn}.</b> Not a scan. These are the declarations a
gate actually ran <code>#print axioms</code> on, read out of the <code>axioms.txt</code> each
<code>tools/verify-*/run.sh</code> writes, so the figure cannot be typed &mdash; it exists only if a
probe produced it. An admitted declaration contributes nothing here: <code>sorryAx</code> means
disclosed, not audited. Sources: {" &middot; ".join(f"{p} ({n}, {d})" for p,n,d in k_sources) or "none yet"}.
<br><br>
<b>Tiers 2 and 3 are text-scan, reported honestly.</b> The <b>core</b> figures above are the {len(cf)} top-level Lean files the tracker trusts: <b>{cp} proved · {cs} open <code>sorry</code> · {cax} explicit axioms beyond Mathlib4</b>. The full <b>recursive</b> scan over every folder reports <b>{rp} proved · {rs} sorry</b> ({rax} axiom declarations), but includes the subfolders&#8217; unresolved duplicate/orphan copies — so the extended list below is shown separately and should not be read as {rp} distinct results.</div>
<div class="note caveat"><b>Not a kernel check.</b> This registry is a text/regex scan (the same heuristic as <code>scripts/theorem_tracker.py</code>): it classifies a declaration as open when its body contains the <code>sorry</code> tactic. It does not run Lean and cannot certify that a file compiles. Treat it as an honest inventory, not a proof of verification.</div>

<div class="controls">
  <button data-f="all" class="on">All</button>
  <button data-f="proved">Proved ✓</button>
  <button data-f="sorry">Open ⚠</button>
</div>

<h2>Core — top-level files ({cp} proved · {cs} sorry)</h2>
<div class="list" id="core">
{rows(core)}
</div>

<h2>Extended — subfolders ({ep} proved · {es} sorry · includes duplicates/orphans)</h2>
<div class="list" id="ext">
{rows(ext)}
</div>

<footer>© 2026 Pablo Nogueira Grossi · G6 LLC · Newark, NJ · ORCID 0009-0000-6496-2186 · <a href="https://doi.org/10.5281/zenodo.19117399">DOI 10.5281/zenodo.19117399</a> · CC BY-NC-ND 4.0<br>
Regenerate: <code>python3 scripts/build_theorem_registry.py</code></footer>
<script>
var btns=document.querySelectorAll('.controls button');
btns.forEach(function(b){{b.addEventListener('click',function(){{
  btns.forEach(function(x){{x.classList.remove('on');}});b.classList.add('on');
  var f=b.getAttribute('data-f');
  document.querySelectorAll('.thm').forEach(function(t){{t.style.display=(f==='all'||t.dataset.st===f)?'flex':'none';}});
}});}});
</script></body></html>"""
Path('theorem-registry.html').write_text(H,encoding='utf-8')
print(f"core: {cp} proved / {cs} sorry / {cax} ax / {len(cf)} files")
print(f"recursive: {rp} proved / {rs} sorry / {rax} ax")
print(f"extended-only: {ep} proved / {es} sorry")
print(f"wrote theorem-registry.html ({Path('theorem-registry.html').stat().st_size} bytes)")
