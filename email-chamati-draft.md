# Draft — Email to Prof. Dr. Hassan Chamati
**To:** (via MDPI author page / issp.bas.bg contact)  
**Subject:** Inquiry: Operator-Order Framework for Iron Oxide Surface Selectivity — Special Issue Fit?

---

Dear Prof. Dr. Chamati,

I am writing to ask whether a submission on formal operator-order mathematics applied to iron oxide surface selectivity would be appropriate for your Special Issue on Theoretical and Computational Studies of Condensed-Matter Systems in *Molecules*.

A brief disclosure before the science: I am a self-taught researcher, not currently affiliated with an institution, and my graduate studies are incomplete. I want to be upfront about that. The work is serious, and the proofs are machine-verified, but you should know the academic context.

The paper I am developing applies a framework called GTCT (Generative Topological Contact Theory) to the (111) versus (110) surface facet selectivity in iron oxides. Your recent review with Dr. Ivanova (Molecules 2026, 31(10), 1629) is the direct empirical ground: the compact (111) plane and the open (110) plane behave as what the framework calls a **K operator** — a geometric gate that determines which molecules are admitted to the fold (the F operator, the recursive interaction step). The non-commutativity K∘F ≠ F∘K, which governs whether the gate is applied before or after the molecular interaction, turns out to be the structural explanation for why hematite's (111) and (110) planes yield such different adsorption and catalytic outcomes.

The operator algebra behind this has been kernel-checked in Lean 4. The proof repository is public at [totogt.github.io/io](https://totogt.github.io/io). The specific file relevant to materials science is `zeolite_operator_order/ZeoliteCommutation.lean`, which establishes — with no `sorry` axioms — that a gate acting on a pointwise map commutes exactly (no boundary term), while a gate acting on a coupling operator (one that moves amplitude between sites) genuinely does not. The (111)/(110) distinction is precisely the coupling case: the open facet allows lateral site-to-site interaction the compact facet suppresses.

My question is specific: **would you be willing to look at a draft of this paper and give your honest assessment of whether it makes a genuine contribution?** I am not asking for a formal referee report, only your view on whether the argument is sound from a condensed-matter perspective and whether the framing fits the special issue — or, if not, where it might better belong.

I understand this is an unusual request from a non-standard academic position. I am grateful either way.

Sincerely,  
Pablo Grossi  
brodananda@gmail.com  
[totogt.github.io/geometry](https://totogt.github.io/geometry)

---

*Notes for Pablo before sending:*
- Find Chamati's direct email at [https://issp.bas.bg/en/department-17-napravlenie-teoriia](https://issp.bas.bg/en/department-17-napravlenie-teoriia) or via the MDPI [E-Mail] link on the special issue page
- The Lean file path to cite: `ZeoliteCommutation.lean` in the io repo — confirm the file is publicly viewable before sending
- If you want to include a 1-page outline of the paper, attach it; the email is strong enough on its own without one
- "Points you made" that can go into the paper: (1) gate + pointwise fold commutes exactly — the δ does NOT exist; (2) gate + coupling operator (lateral site interaction) genuinely does not commute; (3) the (111) plane suppresses lateral coupling → commuting case → homogeneous surface; (4) the (110) plane permits it → non-commuting case → selectivity emerges at the gate
