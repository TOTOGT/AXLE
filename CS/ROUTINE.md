# The routine

Exposition is a second implementation of the claim, in a different language.
Two independent implementations of one thing disagree somewhere, and the
disagreement localises a defect. That is differential testing, with prose as
the second implementation — which is why writing the chapter keeps finding
things, and why it should not be run last.

Each step below earned its place by catching something on 2026-08-21. The
provenance is recorded so the routine can be pruned when a step stops paying.

---

## 1 · State the claim as a full sentence, with every argument named

Not a token. `KERNEL-VERIFIED` is one word; written out for a reader it becomes
*this artifact, under this toolchain, against this library, on this date*. If
you cannot name what the claim is true **of**, you do not have a claim.

> Caught: the triple. It came out of writing §2, not out of the audit.

**Mechanisable in part** — a claim in prose that quotes a command or an output
can be checked against a recorded run.

## 2 · Write it for someone with no access to your machine

Every implicit referent must be named. Directory names, tree names, "the
build", "the other copy" — each one is a place where a load-bearing fact can
hide behind a phrase.

> Caught: "the orthogenesis tree" was doing decisive work in a header while
> being unspecified, unversioned, and different from the tree that was checked.

**Not mechanisable.**

## 3 · Order the facts causally, not chronologically

A narrative forces a causal sequence. Facts that were adjacent in time but not
causally joined stop fitting, and the misfit is the finding.

> Caught: the 22:28 / 22:29 minute. Both timestamps sat inert in a manifest
> until §1 required an explanation of *why* the two copies differed.

**Not mechanisable.**

## 4 · Write the limits section before the results section

The section header is the instrument. Having to fill "what this does not
establish" produces defects that no test suite reaches, because tests check
what you built and this checks what you claimed.

> Caught: that a stamp can launder a weak check — the tool's net-negative case,
> found by nothing but an empty heading.

**Not mechanisable.**

## 5 · Write usage examples as executable commands, then run them

Documentation that cannot be executed is prose about software. Documentation
that can be is a test.

> Caught: self-application corrupting the tool's own source. Writing the
> README's usage block is what made me run the tool on itself.

**Mechanisable** — extract commands from the document and execute them in CI.

## 6 · Record defects found in the instrument; do not repair them silently

A verification tool with an undisclosed defect history asks for exactly the
trust it exists to withhold.

> Three defects in `verify-stamp` are in its README rather than in its git
> history alone.

**Not mechanisable.**

## 7 · Someone must doubt the auditor

No mechanism produces this, and the failure it prevents is the worst
available, because a wrong correction arrives carrying more authority than the
error it replaces.

> Caught: the two-stage verdict. It was wrong for two of three theorems, it was
> written into a source retraction and a manuscript, and it was corrected only
> because the author said half of it was not true.

**Not mechanisable. Irreducible.**

---

## The trigger problem

Steps 1 and 5 can be automated, but note *when* they must run.

**MISMATCH** and **FAIL** are caused by a change, so a push trigger finds them.
**STALE is not.** Decay happens when a toolchain or library moves under a claim
that nobody is touching — the commit that would fire CI never arrives. The
July defect stood for a month for exactly this reason: no relevant push
occurred, so no check ran, so nothing was wrong as far as any layer could tell.

A push-triggered pipeline is structurally blind to decay. `verify-proofs.yml`
now carries `schedule: cron '17 6 * * 1'` alongside `on: push`, so a dormant
repository is still asked, weekly, whether its claims still hold.

---

## The counterweight

Exposition also **manufactures** structure. Prose wants three classes, an arc,
a clean table. The three-class taxonomy in `maths.md` reads well partly because
it reads well — and two of its three classes have exactly one instance each,
from one file, on one afternoon.

Ask of every find: did writing **reveal** this, or **produce** it? The triple
survives the question. Whether the taxonomy is three real classes, or two
observed failure modes plus one inferred, is still open and is recorded as
open.

---

## Not yet built

**A document linter.** A chapter asserts things like *"five theorems report
`[propext, Classical.choice, Quot.sound]`"*. That is a claim with a recorded
run behind it, sitting in prose where nothing checks it. `verify-stamp` binds a
claim to an artifact; the sibling instrument would bind a **document's quoted
claims** to the stamps of the artifacts they describe, and fail when a paper
outruns its evidence. Every false claim in this corpus so far has travelled
through prose, and prose is the one layer with no checker at all.
