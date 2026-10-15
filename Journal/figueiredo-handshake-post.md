# Handshake post — for Carolina Figueiredo

Publish only after: (1) `git push` in the geometry repo lands book7/ch-figueiredo.html,
so the link in this post resolves; (2) confirm the 2026-08-30 corpus-audit numbers
below are still the last full scan — if a newer one exists, cite that instead. Not
yet assigned a Journal issue number; this can run as a Notices-page item in the next
issue, or stand alone, the way the Axiom Math piece ran in Vol. Ω No. 10 before it
had a page of its own.

Same move as that one, aimed differently: last time it was a job posting, read as a
specification and resolved at an address rather than asserted. This time there is no
posting. The occasion is a prize, and the specification is closer to a stated
temperament than a list of requirements — so this post checks whether that
temperament is actually the same one, rather than just claiming it is.

---

## Main post

**Carolina Figueiredo won the 2026 Vera Rubin New Frontiers Prize for showing that
three quantum field theories with nothing obviously in common — gluons, pions, and a
toy model with no physical counterpart — forbid exactly the same particle
collisions, because all three are curves drawn on the same surfaces.** No spacetime
in the description. No sum over diagrams. The geometry does the work a page of
Feynman-diagram bookkeeping used to do.

We didn't just admire that from a distance. We wrote a chapter about it —
sourced to the Princeton announcement, the Breakthrough Prize citation, the
Daily Princetonian, and the primary paper (arXiv:2408.11891) — and gave it the
same treatment every chapter in this corpus gets: a script that checks the page
still says what its sources said, because a page that used to be true and
silently drifted is a page nobody re-reads. It's here:
https://totogt.github.io/geometry/book7/ch-figueiredo.html

Here's the actual reason for writing this post, though. "Let the object's own
structure carry the claim, instead of asserting it and hoping" is also the
whole idea behind the Lean 4 work this desk does, and we hold ourselves to it
literally, not as a slogan. The verdict on any theorem here is never "it
compiled" — a false axiom compiles just fine and proves everything downstream,
silently. The verdict is `#print axioms`, checked by hand against an allowed
list of exactly three (`propext`, `Classical.choice`, `Quot.sound` — Lean's own
classical foundation), with anything else — an admitted `sorry`, a
`native_decide` that asked the kernel to trust a compiled evaluation, or a
declared axiom nobody has read — printed and looked at, not waved through by a
green checkmark.

**What resolved, on 2026-08-30:** a corpus-wide sweep, cheap and mechanical —
no compute, just comparing each file's own prose claim to its own body — over
206 tracked `.lean` files (158 unique by content hash) across this repo and its
neighbors. 79 files claim some form of verification in their prose. 21 of those
carry a `sorry`, a `native_decide`, or a bare axiom. Most of the 21 are honest
about it — they say "not machine-checked" or scope the claim to where it
actually holds, and that's the pattern kept. One was not honest: a file whose
header claimed zero sorry, zero axioms beyond Mathlib, fully proved. It had
zero imports, so nothing in it had ever compiled; it declared nine axioms, not
zero; and three of those were false as stated, which makes the file
inconsistent — `False` follows from it, checked by instantiating at a
two-element type, which means every "theorem" downstream of it was true for
free, proving nothing. **A false axiom is strictly worse than a `sorry`.** A
`sorry` fails loudly. A false axiom passes silently and certifies anything you
ask it to. Found, printed, fixed the same day, with the counterexample kept in
the repo rather than quietly removed.

**What did not resolve, and isn't claimed here:** nothing in this corpus's own
contact-geometric machinery has been shown to connect to surfaceology's
kinematic-space geometry, and this post doesn't try to manufacture that
connection. Both talk about physics "as geometry instead of dynamics" — that's
a shared description, not a shared derivation, and the chapter linked above
says so explicitly rather than leaving a reader to assume more. Nor has this
desk attempted to formalize anything from surfaceology itself — no curve, no
surface, no amplitude identity, not yet. That's the honest gap, not a
hedge: if there's a small, real, checkable piece of that structure worth
stating in Lean as a first test, that's a concrete thing to try, not a
promise made in the abstract.

The temperament match is real. Whether it's worth more than that is a
question for a conversation, not a blog post.

---

## Short version, if the field is tight

Carolina Figueiredo's Vera Rubin New Frontiers Prize work replaces a page of
Feynman-diagram bookkeeping with curves on a surface — the geometry carries the
claim instead of a derivation asserting it. That's also the standard this desk
holds its own Lean 4 work to: the verdict is never "it compiled," it's
`#print axioms` checked against an allowed list of three, printed in full, with
a caught-and-fixed example (a false axiom that made a whole file trivially
true) to show the check isn't decorative.

No claim that the two geometries are related — that's not shown and this post
doesn't pretend it is. What's offered is the same temperament applied to a
different kind of object, and an actual first thing to try if that's of
interest: https://totogt.github.io/geometry/book7/ch-figueiredo.html

---

## One line, for a comment or repost

Wrote a sourced, self-checking chapter on Carolina Figueiredo's Vera Rubin
Prize work (curves on surfaces standing in for Feynman diagrams), then pointed
out the same "let the object's structure carry the claim" instinct is what our
own Lean 4 axiom-gate does — verdict by `#print axioms`, not by compiling —
including the false axiom it caught in our own house and fixed the same day:
https://totogt.github.io/geometry/book7/ch-figueiredo.html
