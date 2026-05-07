# Paper v3 — deliverables

This folder contains the v3 revision of the Zenodo paper, the four new figures, and a compiled draft PDF.

## Files

**Paper source and compiled draft**

- `paper_v3.tex` — LaTeX source. Compiles cleanly with `pdflatex` (no bibtex needed; uses `thebibliography` inline).
- `paper_v3.pdf` — compiled draft (15 pages). The fig1–fig5 placements currently use **placeholder boxes**; replace with the original v2 figures before submission (see "Figures" below).

**New figures (v3 additions)**

- `fig6_d2_natural.{pdf,png}` — D₂ scaling at natural Rauzy lengths (Section 4.3). Two-panel: clean Fibonacci fit with D₂=0.65 ± 0.11; tribonacci plateau-and-drop pattern with caveat annotations.
- `fig7_fss_T1e4.{pdf,png}` — FSS at T=10⁴ (Section 4.4). Grouped bars by λ × N showing the differential ratio trib/fib.
- `fig8_ratio_collapse.{pdf,png}` — Ratio collapse from T=10⁴ to T=10⁵ at λ=1.5 (Section 4.5). Bar pairs at N=500/1000/2000.
- `fig9_T1e6_saturation.{pdf,png}` — Long-time evolution at N=1000, λ=1.5 to T=10⁶ (Section 4.5). Anchor points from direct measurements at T=10⁴, 10⁵, 3×10⁵, 10⁶ with the saturation band.

**Generators**

- `generate_figures_v3.py` — self-contained matplotlib script that produces fig6–fig9 from embedded data tables. No CSV dependencies. Re-run with `python3 generate_figures_v3.py`.
- `make_placeholder_figs.py` — creates the placeholder PDFs for fig1–fig5. Used only to verify the v3 LaTeX compiles. Replace with actual figures before submission.

## Compile instructions

```bash
# 1. Place the original fig1–fig5 PDFs into figures/
#    (regenerate from the v2 generate_figures.py output, or copy from your
#     Zenodo v2 deposit alongside fig6–fig9 which are already in figures/)
cp /path/to/v2/fig1_chain_structure.pdf   figures/
cp /path/to/v2/fig2_eigenstates.pdf       figures/
cp /path/to/v2/fig3_ipr_vs_lambda.pdf     figures/
cp /path/to/v2/fig4_ipr_ratio.pdf         figures/
cp /path/to/v2/fig5_substitution_tree.pdf figures/

# 2. Compile twice for cross-references
pdflatex paper_v3.tex
pdflatex paper_v3.tex
```

## What changed from v2

Substantive additions (with section locations):

- **Abstract** rewritten to incorporate FSS, long-time saturation, pre-saturation α, and D₂ extraction.
- **Section 3.3** (numerical implementation): added DOP853 + tighter tolerances for long-time runs; added run-to-run reproducibility note (~5% on absolute ratios at T≥10⁵).
- **Section 4.3** (new): multifractal dimension D₂ at natural substitution lengths. Quotes D₂_fib = 0.65 ± 0.11 (clean); documents the tribonacci plateau-and-drop anomaly and defers numerical D₂_trib to future work.
- **Section 4.4** (new): finite-size scaling at T=10⁴ across N ∈ {500, 1000, 2000}. The differential generally grows with N. Notes the non-monotone λ=1.5 row and forward-references its resolution at T=10⁵.
- **Section 4.5** (new): long-time evolution and ratio collapse. The T=10⁴ peak at N=1000 (4.18×) collapses to 1.20× at T=10⁵; saturation at T~3×10⁵ at N=1000 with ratio settling to 1.04 ± 0.04.
- **Section 4.6** (new): pre-saturation spreading rates table at N=2000, T=10⁵, t > 10⁴ window. α_trib > α_fib uniformly across λ ∈ [0.5, 2.0]. Explicit reinterpretation of α as a finite-N rate of approach to saturation, not an asymptotic exponent.
- **Section 6** (rewritten): five v1 open questions revisited; three closed (with reinterpretation note on the spreading-exponent item), two still open, one new (D₂_trib state-isolation).
- **Conclusion** (rewritten): preserves the original headline, adds the long-time and FSS findings, frames the corrected narrative.
- **Bibliography**: added the Atratores repo entry for code and data.

What did *not* change: Sections 1, 2, 3.1–3.2 (Introduction, n-bonacci recurrence, substitution chains, DNLS model formulation), and Sections 4.1–4.2 (linear baseline and T=50 differential). The v1 results stand as reported.

## Source data

All long-time runs, raw IPR time-series CSVs, and analysis scripts are in:

- `grossi-ops/Atratores` — main code repository.
  - `data/ipr_lambda1p5_T1e4.csv` — FSS at T=10⁴ (Section 4.4)
  - `data/ipr_lambda1p5_N1000_T1e5.csv` and `data/ipr_lambda1p5_N2000_T1e5.csv` — T=10⁵ (Section 4.5)
  - `data/ipr_lambda1p5_N1000_T1e6.csv` — T=10⁶ (Section 4.5)
  - `data/ipr_N2000_T1e5.csv` — α-fits (Section 4.6)
  - Brief 3 D₂ data in `data/d2_natural_lengths.csv`

The figures here can be regenerated from the embedded data tables in `generate_figures_v3.py` without needing the CSVs.

## Reviewer-relevant notes

Three caveats are worth flagging before any peer review:

1. **D₂_trib is not numerically extracted.** The plateau-and-drop pattern in tribonacci IPR(N) at natural Rauzy lengths is documented honestly in Section 4.3; a clean extraction requires either an eigenmode tracker via spatial-profile overlap or a different multifractal observable (open question 6).

2. **α at λ=0.5 fibonacci has R²=0.33.** Quoted in Table 2 for completeness; explicitly noted in Section 4.6 as not supporting a power-law interpretation.

3. **Absolute ratio values at T≥10⁵ have ~5% relative uncertainty.** Independent runs at the same nominal tolerances disagree at the 4–5% level; this is documented in Section 3.3. Quoted ratios should be read with this uncertainty in mind.

These are honest about the residual unknowns and preempt likely referee questions.
