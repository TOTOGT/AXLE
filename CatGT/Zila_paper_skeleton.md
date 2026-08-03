# Operator Firing Order in Ethanol-to-Hydrocarbon Selectivity over ZSM-5 and MCM-22 Zeolites: In Situ DRIFTS Evidence for Contact-Geometric Pore Topology Control

**Prepared for:** Zila — bench-ready skeleton in *Catalysis Today* house style
**Date:** June 2026
**Status:** working draft — paragraphs marked `[FILL]` for narrative; experimental section is bench-protocol ready.

---

## Authors

Zila Sousa<sup>a,*</sup>, Pablo Nogueira Grossi<sup>b</sup>, [additional co-authors]<sup>a,c</sup>

<sup>a</sup> [Zila's affiliation]
<sup>b</sup> G6 LLC, Newark, NJ 07104, USA. ORCID 0009-0000-6496-2186
<sup>c</sup> [other affiliations]

*Corresponding author: [Zila's email]

---

## Abstract `[FILL — 200 words]`

`[FILL]` HZSM-5 and HMCM-22 produce markedly different product distributions and coke-deposition profiles in ethanol-to-hydrocarbon conversion despite nominally identical Brønsted acidity. We show — by combining time-resolved in situ DRIFTS, fixed-bed activity tests, SEM/EDX coke mapping and structural ablation — that this difference is governed not by pore size but by the **firing order of the catalytic operators** (pore-mouth constraint **K**, intra-cage folding **F**) imposed by the topology of each zeolite. ZSM-5 fires **C → K → F → U** (constraint before folding), trapping the ethoxy intermediate before branching can occur; MCM-22 fires **C → F → K → U** (folding before constraint), allowing diethyl ether and aromatic C₆–C₈ intermediates to form in the open supercage and then trap as coke at the 10-ring exit. Three falsifiable contact-time DRIFTS predictions are derived and tested. The non-commutativity [K, F] ≠ 0 is the previously missing mechanistic principle for pore-topology control in zeolite catalysis.

**Keywords:** ZSM-5; MCM-22; ethanol-to-hydrocarbon; in situ DRIFTS; pore topology; operator order; coke deposition; contact geometry; Topographical Orthogenetic Theory

---

## 1. Introduction `[FILL — 1.5 pages]`

Suggested paragraph spine (one paragraph each):

1. The industrial relevance of ethanol-to-hydrocarbon over zeolites; reference to MTO, MTH lines. Position ZSM-5 and MCM-22 as the two best-characterised contrasting topologies.
2. The empirical puzzle in Sousa 2014 and 2023: identical Brønsted acidity, different product distribution and deactivation. Restate that pore-mouth diameter alone cannot explain it — both are 10-ring.
3. Brief review of the operando DRIFTS work on H-ZSM-5 (Kadam & Shamzhy 2018; Zhou 2019) showing ethoxy precedence; and on MCM-22 (MTH 2022; ACS Interfaces 2024) showing aromatic precedence.
4. State the hypothesis: pore topology imposes a firing order on the catalytic operators. ZSM-5 constrains before folding; MCM-22 folds before constraining. The two orders are non-equivalent because [K, F] ≠ 0.
5. State what this paper adds: three falsifiable contact-time DRIFTS predictions, the spatial coke-mapping test, and the structural-ablation test that reorders MCM-22 toward ZSM-5 behaviour.
6. Outline of the paper.

---

## 2. Experimental

### 2.1. Materials

| Reagent / catalyst precursor | Source | Purity / spec |
|---|---|---|
| NH₄-ZSM-5 (CBV 3024E) | Zeolyst International | Si/Al = 15 (nominal) |
| Boron-MCM-22 precursor (B-MWW-P) | synthesised in-house, see §2.2.2 | Si/Al = 15 (target) |
| MCM-22 precursor (MWW-P) | synthesised in-house | Si/Al = 15 |
| Hexamethyleneimine (HMI) | Sigma-Aldrich | ≥99 % |
| NaOH, NH₄NO₃ | Sigma-Aldrich | ≥99 % |
| Ethanol (anhydrous) | Merck | ≥99.8 %, dried over 4 Å sieves |
| N₂, dry air, He | Linde | 99.999 % |
| SiC diluent | Sigma-Aldrich | 400 mesh |

### 2.2. Catalyst preparation

#### 2.2.1. H-ZSM-5

**Bench steps:**

1. Weigh ~5 g of NH₄-ZSM-5 (CBV 3024E) into a porcelain calcination boat.
2. Place boat in tube furnace under flowing dry air (50 mL min⁻¹).
3. Ramp at 1 K min⁻¹ from 298 K to 823 K. Hold at 823 K for 4 h.
4. Cool to room temperature under flowing dry air.
5. Transfer to dry glass vial. Store in desiccator.

**Recorded:** initial and final mass (to compute loss on calcination).

#### 2.2.2. H-MCM-22

**Synthesis of MCM-22 precursor (MWW-P):**

1. Prepare reagent gel with molar composition `1 SiO₂ : 0.033 Al₂O₃ : 0.18 Na₂O : 0.5 HMI : 45 H₂O`.
2. Stir for 60 min at room temperature in a PTFE-lined autoclave.
3. Crystallise at 423 K for 7 days under rotation (60 rpm).
4. Recover solid by filtration; wash with deionised water to pH 8.
5. Dry at 373 K, overnight.

**Conversion to H-form:**

6. Calcine the MWW-P at 823 K, 6 h, dry air, ramp 1 K min⁻¹ (this opens the MWW interlayer and removes HMI template).
7. Ion-exchange in 1 M NH₄NO₃ (10 mL g⁻¹ catalyst), 353 K, 4 h, stir; repeat 3 times.
8. Filter, wash, dry at 373 K overnight.
9. Final calcination at 823 K, 4 h, dry air, ramp 1 K min⁻¹ to obtain H-MCM-22.

**Recorded:** XRD at each step to confirm phase purity.

#### 2.2.3. Boron-regulated MCM-22 (B-MCM-22, structural ablation series)

Repeat §2.2.2 substituting H₃BO₃ for Al₂O₃ source to achieve nominal B/(Al+B) ratios of 0.25, 0.50, 0.75. This series tests the prediction that moving Brønsted sites into the 10-ring channels (away from the 12-ring supercage) suppresses coke. Document each member.

#### 2.2.4. Pelletisation

All H-form catalysts are pressed without binder (200 MPa, 1 min), crushed, sieved to 250–425 μm. Discard fines.

### 2.3. Catalyst characterisation

For every catalyst in the series, run the **full** characterisation panel before any reaction test.

#### 2.3.1. Powder XRD

1. Pack ~50 mg in a zero-background holder.
2. Cu Kα radiation, 40 kV, 40 mA. 2θ range 5–50°, step 0.02°, count time 1 s per step.
3. Compare against ICDD reference patterns: MFI (44-0003) for ZSM-5, MWW (49-0386) for MCM-22.
4. Compute crystallinity index relative to a reference high-crystallinity sample.

**Recorded:** diffractogram, crystallinity index, any peak shifts indicating dealumination.

#### 2.3.2. N₂ physisorption (textural)

1. Degas ~100 mg at 573 K, overnight, in vacuum.
2. Run N₂ isotherm at 77 K (Micromeritics ASAP 2020 or equivalent).
3. Compute BET surface area (P/P₀ = 0.05–0.30); micropore volume by t-plot (Harkins–Jura); external surface area by t-plot subtraction; mesopore volume from BJH on the desorption branch.

**Recorded:** isotherm, S_BET, V_micro, V_meso, S_ext.

#### 2.3.3. NH₃-TPD (total acidity)

1. Load 50 mg on quartz wool plug.
2. Pretreat at 773 K, 1 h, flowing He (30 mL min⁻¹).
3. Cool to 373 K. Saturate with 10 % NH₃/He, 30 min.
4. Purge in He, 1 h at 373 K to remove physisorbed NH₃.
5. Ramp at 10 K min⁻¹ to 1073 K. Detect desorbing NH₃ by TCD.
6. Calibrate signal against pulses of known NH₃ volume.
7. Deconvolute into weak (< 573 K), medium (573–773 K), strong (> 773 K) acid populations.

**Recorded:** total acid density (mmol NH₃ g⁻¹), distribution across strength bins.

#### 2.3.4. FTIR of adsorbed pyridine (Brønsted / Lewis discrimination)

1. Press ~15 mg into a self-supporting wafer (Ø 13 mm).
2. Mount in vacuum IR cell. Activate at 723 K, 2 h, < 10⁻⁴ Pa.
3. Background spectrum at 423 K.
4. Dose pyridine (saturated vapour over liquid) for 30 min at 423 K.
5. Evacuate at 423 K, then 523 K, then 623 K for 30 min each; collect spectra after each evacuation.
6. Integrate bands at 1545 cm⁻¹ (Brønsted-pyridinium) and 1455 cm⁻¹ (Lewis-pyridine coordinated). Use ε_B = 1.67 cm μmol⁻¹, ε_L = 2.22 cm μmol⁻¹ (Emeis 1993).

**Recorded:** Brønsted and Lewis acid-site densities (μmol g⁻¹) at each evacuation temperature.

#### 2.3.5. ²⁷Al / ²⁹Si MAS NMR

1. Pack hydrated samples (equilibrate over saturated NH₄Cl for 48 h) into 4 mm ZrO₂ rotor.
2. ²⁷Al: 9.4 T, MAS 10 kHz, π/12 pulse, recycle delay 0.5 s, 10 000 scans.
3. ²⁹Si: same field, MAS 10 kHz, π/4 pulse, recycle delay 30 s, 2000 scans.
4. Reference ²⁷Al to 1 M Al(NO₃)₃ at 0 ppm; ²⁹Si to TMS at 0 ppm.

**Recorded:** ²⁷Al spectrum to confirm tetrahedral (50–65 ppm) vs. extra-framework octahedral (0 ppm) Al; ²⁹Si Q⁴(nAl) decomposition.

#### 2.3.6. SEM / EDX (crystal habit)

1. Sputter-coat with Au/Pd (5 nm).
2. SEM at 5–10 kV. Capture representative micrographs at 5 000×, 20 000×, 50 000×.
3. EDX at 15–20 kV. Quantify external Si/Al at five spots per particle, 10 particles per sample.

**Recorded:** crystal size distribution; external vs. bulk Si/Al ratio.

### 2.4. Catalytic activity tests (fixed-bed reactor)

#### 2.4.1. Reactor configuration

Continuous-flow fixed-bed quartz microreactor, i.d. 8 mm, length 30 cm, with K-type thermocouple in the catalyst bed. Reactor is housed in a three-zone tubular furnace. Atmospheric pressure operation. Bed dilution with SiC keeps the bed isothermal and prevents channelling.

#### 2.4.2. Bench protocol

1. Load 100 mg catalyst (250–425 μm) between two quartz-wool plugs; dilute with 300 mg SiC.
2. Pretreat in flowing dry N₂ (50 mL min⁻¹) at 773 K, 1 h. Ramp at 5 K min⁻¹.
3. Cool to reaction temperature (typically 623 K; vary 573–773 K in the temperature series).
4. Feed ethanol via syringe pump (0.05–0.20 mL min⁻¹ liquid) through a vaporiser at 423 K, mixed with N₂ (10–40 mL min⁻¹) to give ethanol partial pressures of 5–15 kPa and WHSV in the range 1–10 h⁻¹.
5. Wait 30 min steady-state before first sample.
6. Sample reactor effluent on-line at 30 min intervals for at least 8 h (or until deactivation > 50 %).
7. After run, switch to N₂ purge, cool to 373 K, recover spent catalyst for §2.6.

#### 2.4.3. Analytical: on-line GC

GC with two channels in parallel:
- **FID** with HP-PLOT/Q (30 m × 0.32 mm × 20 μm) for C₁–C₈ hydrocarbons and oxygenates.
- **TCD** with Carboxen-1010 PLOT (30 m × 0.53 mm × 50 μm) for water, CO, CO₂, H₂.

Temperature programme: 313 K (5 min) → 10 K min⁻¹ → 523 K (10 min).
Carrier: He, 25 mL min⁻¹.
Calibration: response factors from at least three reference mixtures spanning 0.1–10 % each species.

#### 2.4.4. Reported quantities

- Ethanol conversion (X), defined on a carbon basis.
- Product selectivity (S_i), carbon basis: ethylene, diethyl ether, C₃–C₅ olefins, BTX aromatics, C₉⁺ aromatics, methane, CO_x, water.
- Carbon balance: target ±3 %, mandatory ±5 % for inclusion.
- Time-on-stream deactivation curves.

### 2.5. In situ (operando) DRIFTS

This is the **central experiment** of the paper. Pulse and steady-state modes both used.

#### 2.5.1. Equipment

- Bruker Vertex 70 FTIR (or Thermo Nicolet iS50) with liquid-N₂-cooled MCT-A detector.
- Harrick Praying Mantis diffuse reflectance accessory with high-temperature/high-pressure reaction chamber (HVC-DRP), ZnSe windows.
- Vaporiser identical to §2.4.2 piped into the DRIFTS chamber.
- Six-port pulse valve (VICI) for contact-time experiments.
- DRIFTS chamber effluent piped to the on-line GC of §2.4.3 (so spectra and product distribution are time-aligned).

#### 2.5.2. Bench protocol — steady-state in situ DRIFTS

1. Load 25 mg of sieved catalyst (250–425 μm) into the sample cup. Tap to level surface.
2. Pretreat in N₂ (50 mL min⁻¹) at 773 K, 1 h.
3. Cool to reaction temperature (matching §2.4.2).
4. Acquire background spectrum in flowing N₂: 4 cm⁻¹ resolution, 256 scans, 4000–1000 cm⁻¹.
5. Switch to ethanol/N₂ stream (same conditions as §2.4.2).
6. Acquire spectra every 60 s for 60 min: 4 cm⁻¹ resolution, 64 scans (~30 s acquisition time), Kubelka–Munk treatment, background-subtracted.
7. After 60 min, switch back to N₂ purge; continue recording for 30 min to follow desorption.
8. Cool under N₂, recover spent sample.

#### 2.5.3. Bench protocol — contact-time DRIFTS (P1 test)

1. Pretreat and reach reaction temperature as in §2.5.2 steps 1–3.
2. Establish steady N₂ flow at the chosen total flow.
3. Inject a 100 μL ethanol pulse through the six-port valve.
4. Trigger IR acquisition: collect single spectra (32 scans, ~15 s each) at t = 0.1, 0.5, 1.0, 5.0, 10.0, 30.0 and 60.0 s after injection.
5. Wait until spectrum returns to baseline (5–10 min).
6. Repeat with 5 successive pulses per condition for averaging.
7. Repeat at three temperatures: 573, 623, 673 K.
8. Repeat for each catalyst in the series (H-ZSM-5, H-MCM-22, three B-MCM-22 boron-regulated samples).

#### 2.5.4. Band assignments (literature)

| Band (cm⁻¹) | Assignment | Reference |
|---|---|---|
| 3650 | bridged Si(OH)Al | Sousa 2014 |
| 2980, 2900, 1080 | ν(OH) and ν(CO) of adsorbed ethanol | Kadam & Shamzhy 2018 |
| 2975, 2930, 2870, 1450, 1390 | ν, δ(CH) of ethoxy | Zhou 2019 |
| 2980, 2870, 1390, 1115 | ν(CH), ν(COC) of DEE | Sousa 2023 |
| 3050, 1600, 1500 | aromatic ν(CH), ν(C=C) | Bjørgen et al. 2007 |
| 1580–1620 (broad) | polyaromatic coke | Bjørgen et al. 2008 |

#### 2.5.5. Data treatment

1. Convert reflectance to Kubelka–Munk units.
2. Subtract the inert N₂ background at the reaction temperature.
3. Integrate each diagnostic band over a fixed 30 cm⁻¹ window. Plot integrated intensity vs. time.
4. **For P1 testing:** define order-of-appearance of bands by the time at which integrated intensity crosses a 10 % threshold of its maximum.
5. **For P2 testing (coke):** track the 1580–1620 cm⁻¹ broad band over the full 60 min run; fit to a Hill-type growth curve.

### 2.6. Post-mortem coke analysis (P2 test)

#### 2.6.1. Thermogravimetric coke quantification

1. Mettler TGA/DSC 3+ or equivalent.
2. ~20 mg of spent catalyst; ramp 10 K min⁻¹ in synthetic air (50 mL min⁻¹) to 1073 K.
3. Coke = mass loss in 573–1073 K window (after dehydration up to 573 K).

#### 2.6.2. SEM/EDX coke mapping (spatial distribution — central P2 test)

1. Embed spent catalyst pellet in epoxy. Polish cross-section.
2. SEM imaging at 5–10 kV; EDX carbon mapping at 15 kV across the entire cross-section.
3. **Quantify:** carbon signal in the supercage / external-pocket regions vs. the sinusoidal-channel regions for MCM-22; for ZSM-5 compare pore-mouth vs. interior.

#### 2.6.3. Soluble coke (chemical identity)

1. Dissolve 100 mg spent catalyst in 5 mL 40 % HF (CAREFUL — fume hood, PPE) for 24 h to liberate trapped organics.
2. Extract three times with 5 mL CH₂Cl₂.
3. Concentrate, analyse by GC–MS (Agilent 5977A or equivalent) on HP-5MS column.
4. Identify aromatics, polyaromatics, retained intermediates.

#### 2.6.4. Raman (graphitisation state)

1. Spent catalyst on glass slide.
2. 514 nm excitation, 1 mW power, 10 s × 5 accumulations.
3. Fit D (~1350 cm⁻¹) and G (~1580 cm⁻¹) bands; report D/G intensity ratio.

### 2.7. Structural ablation (P3 test — boron regulation)

For each member of the B-MCM-22 series (B/(Al+B) = 0, 0.25, 0.50, 0.75):

1. Run the full §2.3, §2.4, §2.5.2 panel.
2. Compute the operator-order index *O* = (time of DEE appearance) / (time of ethoxy appearance) in the DRIFTS contact-time data.
3. **Prediction:** *O* approaches 1 as boron fraction → 1 (operator order C→F→K→U → C→K→F→U).
4. Plot coke yield vs. *O* across the series.

---

## 3. Results and Discussion `[FILL — built around the figures below]`

Suggested figure list (Zila to produce):

| Fig | Content | Source data |
|---|---|---|
| 1 | XRD patterns of all catalysts | §2.3.1 |
| 2 | N₂ isotherms + textural table | §2.3.2 |
| 3 | Acid-site densities (NH₃-TPD + pyridine FTIR) | §2.3.3, §2.3.4 |
| 4 | Steady-state conversion / selectivity vs T-on-S, ZSM-5 vs MCM-22 | §2.4 |
| 5 | Contact-time DRIFTS series: H-ZSM-5 (a) and H-MCM-22 (b) | §2.5.3 |
| 6 | Order-of-appearance diagram: ethoxy → DEE → aromatics → coke, both catalysts | §2.5.3 + §2.5.5 |
| 7 | SEM/EDX carbon maps of spent MCM-22 (supercage vs channel) and spent ZSM-5 | §2.6.2 |
| 8 | B-MCM-22 series: operator-order index *O* vs. boron fraction; coke yield vs. *O* | §2.7 |
| 9 | Schematic: C→K→F→U vs C→F→K→U operator chains overlaid on pore topology | conceptual |

Suggested discussion structure (one subsection each):

- **3.1** Catalyst characterisation: equivalent acidity is established (this defends the central claim).
- **3.2** Activity tests confirm the Sousa 2014/2023 selectivity contrast and locate it in time-on-stream.
- **3.3** Steady-state DRIFTS: surface-species inventory differs at constant chemistry.
- **3.4** **Contact-time DRIFTS (P1):** order-of-appearance differs — ethoxy precedence on ZSM-5, DEE/aromatic precedence on MCM-22. *This is the central result of the paper.*
- **3.5** Coke mapping (P2): supercage-localised on MCM-22, pore-mouth-localised on ZSM-5.
- **3.6** Structural ablation (P3): boron regulation tunes *O* continuously, with coke yield tracking *O*. The smooth dependence falsifies any binary "topology" explanation in favour of operator order.
- **3.7** Mechanistic synthesis: why [K, F] ≠ 0 is necessary and sufficient. (Reference the Grossi 2026 contact-geometric framework only briefly here; theory belongs in supplementary.)

---

## 4. Conclusions `[FILL — 5 bullet points]`

`[FILL]` Sample:

1. HZSM-5 and HMCM-22 show identical Brønsted acidity but different product distributions and coke profiles.
2. Time-resolved DRIFTS resolves the difference as a difference in the **order in which catalytic operators fire**: constraint before folding on ZSM-5, folding before constraint on MCM-22.
3. The order can be tuned continuously by boron regulation of MCM-22; coke yield tracks the order index *O* monotonically.
4. The non-commutativity [K, F] ≠ 0 is the previously missing mechanistic principle for pore-topology control in zeolite catalysis.
5. The operator-order analysis generalises to any pore-topology-controlled zeolite system; tested predictions and protocols are catalysed-system-independent.

---

## Acknowledgements `[FILL]`

---

## References `[starter list — Zila to expand]`

1. Z. Sousa et al., *Microporous Mesoporous Mater.* (2014) — empirical ZSM-5 vs MCM-22 selectivity.
2. Z. Sousa et al., *Catal. Today* (2023) — dealuminated / delaminated variants.
3. P. N. R. Kadam, M. Shamzhy, *J. Catal.* 365 (2018) — operando DRIFTS H-ZSM-5 ethanol.
4. Y. Zhou et al., *ACS Catal.* 9 (2019) — ethoxy precedence on ZSM-5.
5. M. Bjørgen et al., *J. Catal.* 249 (2007) — aromatic intermediates in MTH on ZSM-5.
6. M. Bjørgen et al., *J. Catal.* 259 (2008) — coke types and Raman D/G.
7. J. M. Lawton et al., *Microporous Mesoporous Mater.* 23 (1998) — MCM-22 12-ring external pockets.
8. C. A. Emeis, *J. Catal.* 141 (1993) — pyridine FTIR extinction coefficients.
9. P. N. Grossi, *Zenodo* 10.5281/zenodo.20563363 (2026) — operator-firing-order theory, this study's framework.
10. P. N. Grossi, *Principia Orthogona Vol. I* (Zenodo 10.5281/zenodo.20784030, 2026).

---

## Supplementary information (separate file)

- S1: Algebraic proofs of the seven theorems from Grossi 2026 (cite, do not reproduce; link to AXLE repository).
- S2: Full DRIFTS spectra series (every time point, every catalyst).
- S3: TGA traces of all spent catalysts.
- S4: Raman spectra.
- S5: Lean 4 source `CatGT_Main.lean`.

---

## Bench timeline for Zila (suggested)

| Week | Task |
|---|---|
| 1 | §2.2 catalyst preparation (all members of B-MCM-22 series) |
| 2 | §2.3 characterisation panel |
| 3 | §2.4 fixed-bed activity tests, ZSM-5 + MCM-22 baseline |
| 4 | §2.5.2 steady-state DRIFTS, both baseline catalysts |
| 5 | §2.5.3 contact-time DRIFTS (P1 test) — central data |
| 6 | §2.6 post-mortem coke analysis (P2 test) — SEM/EDX mapping |
| 7 | §2.7 structural ablation B-MCM-22 series (P3 test) |
| 8 | Data analysis, figure generation |
| 9 | Manuscript draft |
| 10 | Internal review + submission |

---

*Skeleton prepared for Zila Sousa, June 2026. All protocols traceable to the operator-firing-order analysis of Grossi 2026 (Zenodo DOI 10.5281/zenodo.20563363). Bench-level questions: g6llc@proton.me.*
