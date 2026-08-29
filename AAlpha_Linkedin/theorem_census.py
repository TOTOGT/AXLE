#!/usr/bin/env python3
"""theorem_census.py — the per-file basis behind any corpus-wide theorem count.

Opened as a TODO in CLAUDE.md on 2026-08-18: "the theorem registry undercounts
the repo … the task is reconciliation, not recounting." This is the tool that
does the reconciliation, so that a published number has a basis a reader can
regenerate instead of a number a reader must trust.

    python3 tools/theorem_census.py --corpus --tracked   # the published corpus
    python3 tools/theorem_census.py ~/Desktop/geometry ~/Desktop/AXLE
    python3 tools/theorem_census.py --table ...     # per-file table
    python3 tools/theorem_census.py --json  ...
    python3 tools/theorem_census.py --selftest

SCOPE, which is half the number. A corpus figure is undefined until the root set
is. --corpus reads tools/corpus_roots.txt: one checkout per distinct git remote,
with the excluded paths listed there and the reason for each. --tracked restricts
to `git ls-files` output, because an untracked file is a draft, not a publication.
Without both flags this tool counts whatever tree you point it at, second
checkouts and ~/Downloads copies included, and the total means nothing.

METHOD, stated because the number is worthless without it.

  · Block comments (/- -/, /-- -/) and line comments (--) are stripped BEFORE
    matching. A `theorem` named in a docstring or a summary table is prose.
  · Counted: `theorem`, `lemma`. NOT counted: `example` (anonymous, cannot be
    cited), `def`, `instance`, `abbrev`.
  · A declaration is ADMITTED if `sorry` appears anywhere between its own header
    and the next declaration header. Admitted declarations are reported, never
    silently dropped: disclosure is the point.
  · `axiom` declarations are counted separately. An `axiom` is not a proof.
  · VERSION DUPLICATES: files whose names differ only by a version suffix
    (_v2, _v5_1, _v6, Main_v6 vs AXLE_v6) are grouped. Their declarations are
    reported both raw and de-duplicated, because a versioned copy of the same
    material double-counts a corpus total.
  · Files outside every lakefile target are NOT distinguished here. That is a
    real gap — an uncompiled declaration is not a checked one — and it needs the
    lakefile parsed, which this tool does not do.

WHAT THIS TOOL CANNOT TELL YOU. A declaration with no `sorry` is not thereby
proved. `theorem X : True := by trivial` is sorry-free and vacuous; a
biconditional proved from assumptions on both sides is sorry-free and empty.
Only `#print axioms` on a named declaration reports what the kernel actually
used, and only a human reading the statement can say whether it says anything.
Report this census as "declarations written" and "declarations sorry-free" —
never as "theorems proved".

Exit 0 clean, 2 if a root has no .lean files (a silent zero is how a count
quietly stops counting).
"""
import os, re, sys, json, hashlib, subprocess
from collections import defaultdict

SKIP_DIRS = {'.lake', 'lake-packages', '.git', 'node_modules', '__pycache__'}
DECL = re.compile(
    r'^[ \t]*(?:@\[[^\]]*\][ \t]*)*'
    r'(?:private[ \t]+|protected[ \t]+|noncomputable[ \t]+|nonrec[ \t]+)*'
    r'(theorem|lemma)[ \t]+([A-Za-z_À-￿][^\s:({\[]*)', re.M)
AXIOM = re.compile(r'^[ \t]*(?:private[ \t]+|protected[ \t]+)*axiom[ \t]+(\S+)', re.M)
VERSUF = re.compile(r'(_v\d+(?:_\d+)*|_V\d+)+$')


def strip_comments(s):
    """Remove /- -/ (nesting), /-- -/ and -- to end of line. Preserves offsets."""
    out = []
    d = i = 0
    n = len(s)
    while i < n:
        if s.startswith('/-', i):
            d += 1
            i += 3 if s.startswith('/--', i) else 2
            out.append('  ')
            continue
        if d and s.startswith('-/', i):
            d -= 1
            i += 2
            out.append('  ')
            continue
        if d:
            out.append('\n' if s[i] == '\n' else ' ')
            i += 1
            continue
        if s.startswith('--', i):
            j = s.find('\n', i)
            j = n if j < 0 else j
            out.append(' ' * (j - i))
            i = j
            continue
        out.append(s[i])
        i += 1
    return ''.join(out)


def scan_text(s):
    """(total, admitted, admitted_names, axiom_count) for one stripped source."""
    ms = list(DECL.finditer(s))
    admitted = []
    for k, m in enumerate(ms):
        end = ms[k + 1].start() if k + 1 < len(ms) else len(s)
        if re.search(r'\bsorry\b', s[m.start():end]):
            admitted.append(m.group(2))
    return len(ms), len(admitted), admitted, len(AXIOM.findall(s))


def looks_like_module(head):
    """True only if the text OPENS as a Lean module.

    Containing `import Mathlib` is not enough: MAYA/1 is a markdown article with
    Lean in fenced code blocks, and a substring test calls it a source file. So
    walk from the top, skip comments and blank lines, and require the first real
    line to be a module-head keyword. A file that opens with '##' or '<' is prose.
    """
    depth = 0
    for line in head.splitlines():
        t = line.strip()
        if not t:
            continue
        if depth:
            depth += t.count('/-') - t.count('-/')
            if depth < 0:
                depth = 0
            continue
        if t.startswith('/-'):
            if '-/' not in t[2:]:
                depth = 1
            continue
        if t.startswith('--'):
            continue
        return bool(re.match(r'(import|namespace|open|set_option|universe|section|'
                             r'noncomputable|private|protected|theorem|lemma|def|'
                             r'abbrev|structure|inductive|instance|axiom)\b', t))
    return False


BINARY_EXT = {'.pdf','.png','.jpg','.jpeg','.zip','.gz','.pyc','.olean','.ilean',
              '.trace','.hash','.svg','.ico','.woff','.woff2','.ttf','.mp4',
              # other languages whose files also open with `import`
              '.py','.js','.jsx','.ts','.tsx','.java','.scala','.kt','.go',
              '.html','.htm','.md','.txt','.json','.toml','.yml','.yaml','.css'}
BACKUP_MARK = ('.bak', '.pre-', '.orig', '~')


def stray_lean(root):
    """Lean source NOT named *.lean — invisible to lake, to this census, and to
    decl_resolve. Found because AXLE/main/axle_v8.1 is Lean source with a version
    number where the extension should be: `lake` cannot build it, no tool counts
    it, and a paper citing it as `AXLE_v8.1.lean` resolves to nothing. Reported
    separately rather than folded into the totals, because a file the toolchain
    cannot see should be fixed, not quietly counted."""
    out = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS and d != 'to_delete']
        for f in fns:
            if f.endswith('.lean'):
                continue
            if os.path.splitext(f)[1].lower() in BINARY_EXT:
                continue
            if any(m in f for m in BACKUP_MARK):
                continue
            p = os.path.join(dp, f)
            try:
                if os.path.getsize(p) > 400_000:
                    continue
                with open(p, encoding='utf-8', errors='strict') as fh:
                    head = fh.read(4000)
            except (OSError, UnicodeDecodeError):
                continue
            if looks_like_module(head) and re.search(r'^import Mathlib', head, re.M):
                body = strip_comments(open(p, encoding='utf-8', errors='replace').read())
                tot, adm, _, ax = scan_text(body)
                out.append({'path': os.path.relpath(p, root), 'decls': tot,
                            'admitted': adm, 'axioms': ax})
    return out


def stem_key(path):
    """Version-duplicate group key: basename with any _vN suffix removed."""
    b = os.path.splitext(os.path.basename(path))[0]
    return VERSUF.sub('', b).lower()


def tracked_lean(root):
    """git-tracked .lean paths under root, or None if root is not a git repo."""
    r = subprocess.run(['git', '-C', root, 'ls-files', '*.lean'],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    return set(r.stdout.split())


def read_roots_file(path):
    """One path per line, ~ expanded, # comments and blanks ignored."""
    out = []
    for line in open(path, encoding='utf-8'):
        line = line.split('#', 1)[0].strip()
        if line:
            out.append(os.path.expanduser(line))
    return out


def census(roots, tracked=False):
    rows = []
    for root in roots:
        root = os.path.abspath(os.path.expanduser(root))
        label = os.path.basename(root.rstrip('/'))
        keep = tracked_lean(root) if tracked else None
        if tracked and keep is None:
            print(f'warning: {root} is not a git repo — skipped under --tracked',
                  file=sys.stderr)
            continue
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if d not in SKIP_DIRS]
            for f in sorted(fns):
                if not f.endswith('.lean'):
                    continue
                p = os.path.join(dp, f)
                if keep is not None and os.path.relpath(p, root) not in keep:
                    continue
                raw = open(p, encoding='utf-8', errors='replace').read()
                s = strip_comments(raw)
                tot, adm, names, ax = scan_text(s)
                rows.append({
                    'repo': label,
                    'path': os.path.relpath(p, root),
                    'decls': tot,
                    'admitted': adm,
                    'admitted_names': names,
                    'axioms': ax,
                    'stem': stem_key(p),
                    'sha': hashlib.sha256(s.encode()).hexdigest()[:12],
                })
    return rows


def summarize(rows):
    groups = defaultdict(list)
    for r in rows:
        groups[(r['repo'], r['stem'])].append(r)
    dup_groups = {k: v for k, v in groups.items() if len(v) > 1}
    # de-duplicated total: from each version group keep the largest member only
    dedup = dedup_adm = 0
    for k, v in groups.items():
        m = max(v, key=lambda x: x['decls'])
        dedup += m['decls']
        dedup_adm += m['admitted']
    return {
        'files': len(rows),
        'decls_raw': sum(r['decls'] for r in rows),
        'decls_dedup_version_groups': dedup,
        'admitted': sum(r['admitted'] for r in rows),
        'sorry_free': sum(r['decls'] - r['admitted'] for r in rows),
        'admitted_grouped': dedup_adm,
        'sorry_free_grouped': dedup - dedup_adm,
        'axiom_decls': sum(r['axioms'] for r in rows),
        'version_dup_groups': {'/'.join(k): sorted(x['path'] for x in v)
                               for k, v in sorted(dup_groups.items())},
    }


CASES = [
    ("theorem a : True := trivial\n", 1, 0, 0, "one plain theorem"),
    ("lemma b : True := by sorry\n", 1, 1, 0, "sorry is admitted, still counted"),
    ("-- theorem c : True := trivial\n", 0, 0, 0, "line comment is prose"),
    ("/-- theorem d in a docstring -/\ntheorem e : True := trivial\n", 1, 0, 0,
     "docstring mention does not count; the real decl does"),
    ("/- theorem f\n   theorem g -/\n", 0, 0, 0, "block comment is prose"),
    ("axiom h : True\ntheorem i : True := trivial\n", 1, 0, 1, "axiom counted apart"),
    ("@[simp]\nprivate theorem j : True := trivial\n", 1, 0, 0, "attribute + modifier"),
    ("example : True := by sorry\n", 0, 0, 0, "example is anonymous, not counted"),
    ("theorem k : True := by\n  sorry\ntheorem l : True := trivial\n", 2, 1, 0,
     "sorry attaches to its own decl, not the next"),
]


MODULE_CASES = [
    ("import Mathlib\ntheorem a : True := trivial\n", True, "opens with import"),
    ("-- header\n/- block -/\nimport Mathlib\n", True, "comments before import"),
    ("## An article\n\n```lean\nimport Mathlib\n```\n", False,
     "markdown containing Lean is not a module (the MAYA/1 case)"),
    ("<html>\nimport Mathlib\n", False, "html is not a module"),
    ("namespace Foo\n", True, "namespace also opens a module"),
    ("", False, "empty is not a module"),
]


def selftest():
    bad = 0
    for text, want, why in MODULE_CASES:
        got = looks_like_module(text)
        ok = got == want
        bad += not ok
        print(f'  {"ok  " if ok else "FAIL"}  module-head {want!s:<5} == {got!s:<5}  {why}')
    for text, wt, wa, wx, why in CASES:
        t, a, _, x = scan_text(strip_comments(text))
        ok = (t, a, x) == (wt, wa, wx)
        bad += not ok
        print(f'  {"ok  " if ok else "FAIL"}  decls {wt}=={t}  adm {wa}=={a}  ax {wx}=={x}  {why}')
    return bad


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        bad = selftest()
        print('selftest clean' if not bad else f'{bad} case(s) failed')
        sys.exit(1 if bad else 0)

    TRACKED = '--tracked' in sys.argv
    roots = [a for a in sys.argv[1:] if not a.startswith('--')]
    if '--corpus' in sys.argv:
        rf = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corpus_roots.txt')
        if not os.path.exists(rf):
            print(f'--corpus needs {rf}', file=sys.stderr); sys.exit(2)
        roots = read_roots_file(rf) + roots
    roots = roots or ['.']
    rows = census(roots, tracked=TRACKED)
    if not rows:
        print('no .lean files found — nothing counted')
        sys.exit(2)
    S = summarize(rows)

    if '--json' in sys.argv:
        print(json.dumps({'summary': S, 'rows': rows}, indent=1)); sys.exit(0)

    if '--table' in sys.argv:
        print(f'{"decls":>6} {"adm":>4} {"ax":>3}  path')
        for r in sorted(rows, key=lambda r: (-r['decls'], r['repo'], r['path'])):
            if r['decls'] or r['axioms']:
                print(f'{r["decls"]:6d} {r["admitted"]:4d} {r["axioms"]:3d}  {r["repo"]}/{r["path"]}')
        print()

    print(f'roots            : {", ".join(roots)}')
    print(f'scope            : {"git-tracked .lean only" if TRACKED else "every .lean on disk under each root"}')
    print(f'.lean files      : {S["files"]}')
    print()
    print(f'{"":<14} {"raw":>8} {"grouped":>8}   (grouped = version-suffixed copies collapsed)')
    print(f'{"declarations":<14} {S["decls_raw"]:>8} {S["decls_dedup_version_groups"]:>8}')
    print(f'{"sorry-free":<14} {S["sorry_free"]:>8} {S["sorry_free_grouped"]:>8}   <- NOT the same as proved; see header')
    print(f'{"admitted":<14} {S["admitted"]:>8} {S["admitted_grouped"]:>8}   (sorry in the proof body)')
    print()
    print(f'axiom decls      : {S["axiom_decls"]}   (an axiom is not a proof)')
    print('Read down one column. A raw figure and a grouped figure are not comparable.')
    strays = []
    for r in roots:
        strays += stray_lean(os.path.abspath(os.path.expanduser(r)))
    if strays:
        print(f'\nLEAN SOURCE NOT NAMED *.lean ({len(strays)}) — invisible to lake,')
        print('to this census, and to decl_resolve. Not included in the totals above:')
        for x in strays:
            print(f'  {x["path"]}  decls={x["decls"]} admitted={x["admitted"]} axioms={x["axioms"]}')

    if S['version_dup_groups']:
        print(f'\nversion-duplicate groups ({len(S["version_dup_groups"])}):')
        for k, v in list(S['version_dup_groups'].items())[:12]:
            print(f'  {k}: {", ".join(os.path.basename(p) for p in v)}')
        if len(S['version_dup_groups']) > 12:
            print(f'  … {len(S["version_dup_groups"]) - 12} more (use --json)')
    sys.exit(0)
