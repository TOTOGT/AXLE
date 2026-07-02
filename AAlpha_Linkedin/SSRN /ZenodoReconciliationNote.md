SSRN / Zenodo Reconciliation Note
==================================
For: ssrn.com/abstract=6439626 ("Principia Orthogona, Volume Two:
Contact Realization of Generative Transitions," with Volume One
bundled as companion content in the same PDF)

WHAT'S CURRENTLY LIVE AND WHERE
---------------------------------
SSRN (abstract=6439626): Volume Two + an early-era Volume One (no fifth
  operator E, no seven-proof appendix, no Analytical-Invariants
  renumbering — this is the same content stage as Zenodo's original
  V1/V2 deposit, March-May 2026).

Zenodo (10.5281/zenodo.19117399, concept DOI -> resolves to latest):
  Volume One has since reached V5 (July 2026): adds the fifth operator
  E, a seven-proof template for four major theorems, a corrected
  Gronwall-radius derivation, and large-print/figure updates. Volume
  Two on Zenodo has not been independently re-versioned to match — it
  still reflects the same content as the SSRN copy.

THE PROBLEM
------------
A reader who finds the SSRN copy and the Zenodo V5 copy independently
will see two documents both titled "Principia Orthogona, Volume One,"
different in real substantive content (operator count, proof
completeness, Gronwall radius derivation), with no cross-reference
connecting them. Without a note, this reads as either an unresolved
duplicate or an unexplained revision — worth fixing regardless of the
math questions underneath either version.

RECOMMENDED FIX (minimal, does not require re-deriving anything)
-------------------------------------------------------------------
Add this notice to the SSRN abstract page and as a first-page note in
the PDF itself, for both the Volume One and Volume Two content:

  "This SSRN posting reflects an earlier stage of the Principia
  Orthogona series (equivalent to Zenodo v1-v2, March-May 2026). The
  current version of Volume One (v5, July 2026) is maintained at
  Zenodo: https://doi.org/10.5281/zenodo.19117399 (concept DOI,
  resolves to latest). Volume Two is scheduled for a matching update;
  until then, readers should treat statements in this SSRN posting
  that depend on Volume One's Invariant 7.5 ("Injectivity Before
  Threshold") as provisional -- see the open-item note below."

OPEN ITEM TO FLAG IN THE SAME NOTICE (from this session's audit)
---------------------------------------------------------------------
Volume Two's Theorem 3.4 (used to prove Theorem B, Threshold
Equivalence) depends on Volume One's Invariant 7.5, which is stated
without proof in every version of Volume One (V1 through the current
Zenodo V5). A direct numerical check of the paper's own canonical
toy-model system (r_dot = r(1-r^2)+2(r-1)e^{-z}, starting at z=0, i.e.
exactly the "before threshold" regime Invariant 7.5 covers) shows
trajectories at r0=0.68 and r0=0.75 -- both satisfying |kappa|<kappa*
-- escape rather than remain injective/stable. This is a concrete
counterexample to Invariant 7.5 as literally stated, not yet resolved
in any version. Recommend flagging Theorem B as conditional on this
open item in both the SSRN and Zenodo postings until Invariant 7.5 is
either proved with the necessary added hypothesis, or restricted in
scope to the z->infinity regime where the paper's separate Gronwall-
radius derivation (Section 22 in Zenodo V5) already lives.

WHAT I HAVE NOT DONE
----------------------
I have not edited either PDF, the SSRN listing, or the Zenodo record.
This is a draft notice for your review and for you to post/edit
directly, since I don't have write access to either platform.
