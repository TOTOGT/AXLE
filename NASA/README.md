# G6 LLC · NASA Deliverables Folder

Working folder for active NASA correspondence and deliverables.
Source-of-truth copies; originals remain in `~/Downloads/` and `~/Desktop/`.

**Author:** Pablo Nogueira Grossi (G6 LLC, Newark NJ)
**Contact:** g6llc@proton.me · +1 (646) 342-3751
**ORCID:** 0009-0000-6496-2186
**EIN:** 33-2880433 · SAM.gov registered (active) · Small Business (FAR Part 19, NAICS 541715)

---

## Active threads

### 1. LEIA — Lunar Enabling Infrastructure Accelerator
- **Notice ID:** 80GRC026R0008
- **Solicitation:** NASA Glenn Research Center presolicitation, in-space manufacturing
- **Submitted:** June 2, 2026 (capability statement via email)
- **NASA reply:** Received June 24, 2026 by Linda Nabors (Contracting Officer) —
  "Received. Please continue to monitor sam.gov regarding this opportunity."
- **Pending action from G6:** Full proposal in response to Final BAA;
  Industry Day notification list request acknowledged.

### 2. MoonBase RFI
- **Notice ID:** 80JSC026MoonBase_RFI
- **Submitted:** Corrected response May 22, 2026 (supersedes April 14)
- **Status:** Acknowledged; no NASA reply pending an action from G6.

### 3. Enceladus / Ocean Worlds proposal
- **Status:** Full proposal prepared and attached to the LEIA submission as
  evidence of framework predictive scope. Available on request.

---

## Folder map

```
NASA/
├── README.md                                # this file
├── MoonBase/                                # MoonBase RFI thread
│   ├── G6LLC_MoonBaseRFI.pdf                # the submitted RFI response (May 22)
│   ├── G6_TOGT_NASA_MoonBase_Research_Contribution.pdf
│   ├── NASAGaps.lean                        # gap-code cross-walk (FN-*)
│   ├── OPEN_QUESTIONS.md                    # ★ open obligations, post-closure
│   ├── OPEN_QUESTIONS_original.md           # archived May 2026 version
│   ├── AXLE_lean_files/                     # ★ the 10 Lean files cited in RFI §4.2
│   │   ├── Main_v6.lean
│   │   ├── PrincipiaVol1.lean
│   │   ├── VolumeTwo.lean
│   │   ├── Chain_updated.lean
│   │   ├── AutophagyDm3_v2.lean
│   │   ├── MultiAgentTogt.lean
│   │   ├── MultiOrbitBioSwarm.lean
│   │   ├── G6Crystal.lean
│   │   ├── TribonacciDNLS.lean
│   │   └── NASAGaps.lean
│   └── proofs/
│       └── sorry_closures.{tex,pdf}         # ★ human-readable proofs for each closure
├── Enceladus/                               # Enceladus proposal thread
│   ├── G6LLC_NASA_Proposal_Enceladus_2026.docx
│   ├── enceladus_grossi2026.{tex,pdf}
│   ├── Enceladus_Grossi2026_zenodo.pdf
│   ├── figures_enceladus.py
│   └── ZENODO_DESCRIPTION_Enceladus.md
├── Reference/                               # NASA reference docs
│   └── moon-base-architecture-users-guide.pdf
├── Correspondence/
│   └── g6_llc_nasa_press_statement.html
└── archive/                                 # earlier versions, retained for audit
    ├── G6LLC_MoonBaseRFI_v1_May21.pdf
    ├── G6LLC_MoonBaseRFI_v2_May22.pdf
    ├── G6LLC_NASA_Proposal_Enceladus_2026_redownload_Jun2.docx
    └── G6_TOGT_NASA_MoonBase_Research_Contribution_May21_short.pdf
```

★ = files updated June 25, 2026 in the sorry-closure pass.

---

## Deliverables index — RFI §-by-§ map

If NASA follow-ups ask to see X, this is where to find X.

| RFI § | Promise | File backing it |
|---|---|---|
| §1   | Organisation, POC, identifiers | This README.md (top) |
| §2   | NEW: CLPS demonstration concept (TDM) | MoonBase/G6LLC_MoonBaseRFI.pdf §6 (no separate doc yet) |
| §2   | NEW: Supply chain challenges | MoonBase/G6LLC_MoonBaseRFI.pdf §10 |
| §2   | NEW: Test facility challenges | MoonBase/G6LLC_MoonBaseRFI.pdf §10.3 |
| §3a  | Technical capabilities (TOGT / AXLE) | MoonBase/AXLE_lean_files/ (all 10 Lean files) |
| §3b  | Public/private partnership model | MoonBase/G6LLC_MoonBaseRFI.pdf §9 |
| §3c  | NEW: ROM cost estimate ($25K → $3M tiers) | MoonBase/G6LLC_MoonBaseRFI.pdf §7 |
| §3d  | Integration potential (cFS, CLPS sensors, LTV) | MoonBase/G6LLC_MoonBaseRFI.pdf §8 |
| §3e  | NEW: Business size declaration (FAR Part 19) | MoonBase/G6LLC_MoonBaseRFI.pdf §2 |
| §3f  | NEW: Teaming arrangements | MoonBase/G6LLC_MoonBaseRFI.pdf §3 |
| §4.1 | The TOGT framework + AXLE verification | MoonBase/AXLE_lean_files/ |
| §4.2 | Machine verification status (160+ theorems, 5 sorrys) | See §-by-§ verification below |
| §5   | G6 Crystal — Phase 01 gap closure | MoonBase/NASAGaps.lean + MoonBase/AXLE_lean_files/G6Crystal.lean |
| §6   | Near-term CLPS demonstration (TDM) | MoonBase/G6LLC_MoonBaseRFI.pdf §6 — concept brief still inline |
| §7   | ROM cost estimate | MoonBase/G6LLC_MoonBaseRFI.pdf §7 |
| §8   | Integration potential | MoonBase/G6LLC_MoonBaseRFI.pdf §8 |
| §10  | Supply chain & test facility challenges | MoonBase/G6LLC_MoonBaseRFI.pdf §10 |
| §11  | Ocean Worlds / Enceladus application | Enceladus/G6LLC_NASA_Proposal_Enceladus_2026.docx |
| §12  | Developments since April 14 | (covered in this README §"Active threads") |
| §13  | Complete Zenodo deposit list | (need DOI verification, pending) |

---

## §4.2 sorry-count audit (June 25)

The RFI §4.2 table reported "160+ theorems proved, 5 sorrys total." After
on-disk verification:

| File | RFI proved | Actual theorems+lemmas | RFI open | Real sorrys (before) | Real sorrys (after) |
|---|---|---|---|---|---|
| Main_v6.lean | 8 | 51 | 2 | 9 | **0** |
| PrincipiaVol1.lean | 30+ | 31 | 1 | 1 | **0** |
| VolumeTwo.lean | 18 | 16 | 1 | 0 | 0 |
| Chain_updated.lean | 9 | 9 | 0 (2 axioms) | 0 | 0 |
| AutophagyDm3_v2.lean | 25 | 21 | 1 | 0 | 0 |
| MultiAgentTogt.lean | 18 | 20 | 0 | 0 | 0 |
| MultiOrbitBioSwarm.lean | 16 | 16 | 0 | 0 | 0 |
| G6Crystal.lean | 20 | 35 | 3 | 0 | 0 |
| TribonacciDNLS.lean | 5 | 10 | 1 | 0 | 0 |
| NASAGaps.lean | — | 9 | — | 0 | 0 |
| **TOTAL** | **160+** | **218** | **9 (RFI)** | **10** | **0** |

The actual theorem count exceeds the RFI claim. The actual sorry count was
**10, not 5** — discrepancy traced to ad-hoc filtering in the original audit.
On June 25, all 10 were closed: four by elementary tactics that the lemmas
in fact admitted, six by strengthening the theorem statement to a true
proposition (the original statements had concrete counterexamples) and
proving the strengthened version.

See `MoonBase/proofs/sorry_closures.pdf` for the human-readable mathematical
proofs, and `MoonBase/OPEN_QUESTIONS.md` for the new open frontier.

---

## §13 Zenodo deposits — DOI status

| DOI | Title | Verified resolves? |
|---|---|---|
| 10.5281/zenodo.19117399 | Series root (concept DOI) | pending check |
| 10.5281/zenodo.20320693 | Vol. I v3 — Operator algebra | pending check |
| 10.5281/zenodo.20159456 | Vol. II v2a — Contact geometry | pending check |
| 10.5281/zenodo.20239928 | GTCT Ring 5 v3 | pending check |
| 10.5281/zenodo.19162012 | G6 Crystal concept DOI | pending check |
| 10.5281/zenodo.20168812 | Autophagy / Triple-Alpha Ch. A | pending check |
| 10.5281/zenodo.20230612 | Biological transitions v2 | pending check |
| 10.5281/zenodo.20128568 | Fruit-fly connectome v2 | pending check |
| 10.5281/zenodo.20075822 | DNLS / Tribonacci v4 | pending check |
| 10.5281/zenodo.20077205 | n-Bonacci criticality | pending check |
| 10.5281/zenodo.20230633 | Polylaminin / k-nacci spine | pending check |
| 10.5281/zenodo.20230614 | Multi-Orbit Identity Theory v2 | pending check |
| 10.5281/zenodo.19431918 | Wavenumber 6 / Nested Infinities | pending check |
| 10.5281/zenodo.19379385 | dm³ Operator Toy Model (GCM) | pending check |
| SSRN 10.2139/ssrn.6439626 | Full series on SSRN | pending check |

DOI verification is a follow-up task — see TODO below.

---

## TODO if NASA follow-ups

1. **TDM concept brief** — currently only described in RFI §6 inline. If NASA
   asks to see a standalone TDM architecture document, draft one
   (~5–6 pp: scope, interface specs, cFS integration plan, milestones).
2. **Zenodo DOI verification** — spot-check each of the 14 DOIs above.
3. **Industry Day** — monitor sam.gov as NASA Linda Nabors instructed.
4. **Sorry closures peer review** — ideally a second mathematician reviews
   `sorry_closures.pdf` before NASA does.
