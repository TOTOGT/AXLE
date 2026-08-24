# CS — contributions to and from computer science

Organised by domain. The domain list is open — add a file when a domain
actually produces something, not in advance. Each domain file has two sections:

- **↑ Domain → CS.** What working in that domain produced that is a
  contribution to computer science: an instrument, a failure class, a method.
- **↓ CS → Domain.** What computer-science methods bring to that domain, and
  what they cannot.

A rule this folder keeps, because the corpus has been bitten by not keeping
it: an entry is written only when there is a recorded artifact behind it.
Everything else is listed as a **candidate** and marked unexamined. An empty
section is information; a plausible-sounding section with nothing behind it is
the failure this folder exists to document.

| domain | ↑ filled | ↓ filled |
|---|---|---|
| [maths.md](maths.md) | 1 | 0 |
| [architecture.md](architecture.md) | 1 | 0 |
| [physics.md](physics.md) | 0 | 0 |
| [chem.md](chem.md) | 0 | 0 |
| [bio.md](bio.md) | 0 | 0 |

## Method

- **[ROUTINE.md](ROUTINE.md)** — the seven-step routine, each step traced to the
  defect that earned it, marked mechanisable or not, plus the trigger problem
  and the counterweight.

## Instruments

- **[verify-stamp/](verify-stamp/)** — binds a verification claim to the
  triple *(artifact, toolchain, library)* and separates MISMATCH, STALE and
  FAIL. 24 tests including self-application, wired into CI as a gating step, self-stamped. Write-up:
  `book6/wp73-the-stamp-and-the-triple.html`.

## Copies

This folder exists in `geometry` and in `AXLE`. `geometry` is canonical.
The copies are not kept in sync by hand — `verify_stamp.py` carries its own
stamp, so drift between the two is detectable by running

    python3 CS/verify-stamp/verify_stamp.py check CS/verify-stamp/verify_stamp.py

in either repo. A folder duplicated across repositories without a mechanism
for detecting divergence is precisely the defect catalogued in maths.md.
