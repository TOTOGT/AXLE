# Duplicate Provisioning Survey (DPS-1)
## Measuring the cost of the missing gauge

**Instrument v0.1 · pre-registration draft · G6 LLC · Newark, NJ**
**Supports:** WP-36 *No Gauge on the Tank* · parent WP-32, doi:10.5281/zenodo.21561819
**Licence:** CC BY 4.0 — reuse and replication encouraged, attribution required

---

## 0 · The one number this exists to produce

> **DPS** — the share of professional users of metered AI subscriptions who hold
> **more than one subscription to substitutable services primarily because they
> cannot observe remaining capacity**, and the incremental annual spend that
> behaviour represents.

Everything below is designed so that this number survives a hostile reviewer.

### The attack we must survive

An advocacy survey that asks *"did the missing meter force you to buy more?"*
gets the answer it wants and is correctly discarded. Three defences are built in:

1. **Behaviour before attribution.** Counts and spend are collected *before* the
   respondent is told what the survey is about. Attribution questions come last.
2. **Competing explanations are offered as equals.** Duplicate subscriptions have
   several legitimate causes — different model capabilities, employer provision,
   evaluation, redundancy. These are listed alongside, not beneath, the
   capacity-visibility reason.
3. **A revealed-preference tradeoff.** A forced-choice item that is costly to
   answer strategically (§4) provides an estimate independent of stated reasons.
   **If the stated and revealed estimates diverge, we report both and lead with
   the lower.** `[VALUE PREMISE]`

---

## 1 · Pre-registration (publish before collecting)

| Item | Commitment |
|---|---|
| Primary outcome | DPS prevalence (§3) |
| Secondary | Incremental annual spend; interruption frequency; revealed-preference share |
| Population | Adults who personally pay for, or personally choose, ≥1 metered AI subscription used for work |
| Exclusions | Respondents whose subscriptions are entirely employer-selected without their input |
| Analysis | Fixed in `analyze.py`, published with the instrument, before data collection |
| Stopping rule | Fixed collection window (no peeking-and-extending) |
| Null result | Published regardless of direction |
| Conflict | Author advocates for metering disclosure. Stated on the landing page, not buried. |

**Pre-register at OSF (free) before the first response.** A survey behind a
policy proposal that was not pre-registered will be assumed to have been tuned.

---

## 2 · Screening & context (asked first, purpose not yet disclosed)

**S1.** In the past 12 months, have you paid for, or personally chosen, any
subscription to an AI assistant, coding assistant, or similar service used for
work? ☐ Yes ☐ No *(No → terminate)*

**S2.** Which best describes you?
☐ Sole proprietor / freelancer ☐ Employee of a firm <50 people
☐ Employee of a firm 50–999 ☐ Employee of a firm 1000+
☐ Student ☐ Public-sector employee ☐ Other

**S3.** Primary use: ☐ Software ☐ Writing/editing ☐ Research/analysis
☐ Design ☐ Teaching ☐ Legal/finance ☐ Operations/admin ☐ Other ___

**S4.** Roughly how many hours per week do you use these services for work?
☐ <2 ☐ 2–5 ☐ 6–10 ☐ 11–20 ☐ 21–40 ☐ >40

---

## 3 · Behaviour (still no framing)

**B1.** How many *separate paid subscriptions* to AI assistant services do you
currently hold — including multiple accounts with the same provider?
`___` (integer)

**B2.** *If B1 ≥ 2:* Do any two of them provide **substantially the same
capability** for your main use? ☐ Yes ☐ No ☐ Unsure

**B3.** Total monthly spend across these subscriptions, in USD:
☐ <$20 ☐ $20–49 ☐ $50–99 ☐ $100–199 ☐ $200–499 ☐ $500–999 ☐ ≥$1000

**B4.** In the last 30 days, how many times did a service stop, slow, or refuse
work because you reached a usage limit? `___`

**B5.** *If B4 ≥ 1:* Did any of those occur in the middle of a task you then had
to abandon, redo, or move elsewhere? ☐ Yes, more than once ☐ Yes, once ☐ No

**B6.** Before it happened, could you see how much of your allowance remained?
☐ Yes, a clear number ☐ Only a vague indicator ☐ No ☐ Don't know

**B7.** Estimated time lost to the most recent such interruption (recovering
context, re-running work, switching accounts):
☐ <5 min ☐ 5–15 ☐ 16–30 ☐ 31–60 ☐ 1–3 h ☐ >3 h ☐ Not applicable

---

## 4 · Revealed preference (the hard-to-fake item)

*This is the estimate that does not depend on the respondent's theory of their
own behaviour.*

**R1.** Suppose you must choose **one** plan, same price:

- **Plan A** — a *larger* allowance, but you cannot see how much remains and get
  no warning before it runs out.
- **Plan B** — an allowance **30% smaller**, with a live usage display and a
  warning before you reach the limit.

☐ Plan A ☐ Plan B ☐ No preference

**R2.** *Randomised follow-up, shown only to Plan-B choosers:* Same choice, but
Plan B's allowance is **50% smaller**. ☐ Plan A ☐ Plan B ☐ No preference

> A respondent who gives up 30–50% of capacity to obtain a gauge is telling us
> the gauge has substantial value to them, without ever being asked to
> introspect on why they hold two subscriptions. This is the primary
> defensible estimate. `[MODEL]`

**R3.** If your main service showed remaining capacity clearly and warned you
before cutoff, would you cancel any other subscription you currently hold?
☐ Yes, definitely ☐ Probably ☐ Probably not ☐ No ☐ N/A (only one)

---

## 5 · Attribution (purpose now disclosed)

> *This study examines how usage limits are disclosed in subscription AI
> services. There are no right answers; we are equally interested in
> respondents for whom this is a non-issue.*

**A1.** *If B1 ≥ 2:* Why do you hold more than one? **Select all that apply**,
then rank your top reason.

☐ Different services are better at different tasks
☐ My employer provides one; I pay for another
☐ Evaluating or comparing services
☐ **To keep working when one hits its limit**
☐ **Because I cannot tell how much capacity I have left on one**
☐ Redundancy against outages
☐ Team or family sharing
☐ Different pricing for different features
☐ Other ___

Top reason: `___`

**A2.** *If either bolded option selected:* If you could see your remaining
capacity in real time on a single service, how likely would you be to reduce to
one subscription? ☐ Very likely ☐ Somewhat ☐ Not very ☐ Not at all

**A3.** Which are currently available to you? (select all)
☐ A number showing usage this period ☐ The limit itself, as a number
☐ Time until reset ☐ A warning before the limit ☐ A usage API
☐ A record I could use to check a bill ☐ None of these

**A4.** Free text (optional): describe one occasion when not knowing your
remaining capacity affected your work or spending. `___`

---

## 6 · Public-sector module (asked if S2 = public sector)

**P1.** Does your agency hold multiple subscriptions to substitutable AI
services? ☐ Yes ☐ No ☐ Don't know
**P2.** Does your agency's contract require the vendor to disclose usage?
☐ Yes ☐ No ☐ Don't know
**P3.** Has your unit purchased additional capacity or accounts because usage was
not visible? ☐ Yes ☐ No ☐ Don't know

*(This module is what makes the procurement argument in WP-36 evidentiary rather
than rhetorical.)*

---

## 7 · Sampling — and its honest limits

**The weak point of this study, stated plainly.** Any convenience sample of AI
power users **over-represents heavy users**, who are exactly the people most
likely to hit limits and hold duplicates. An uncorrected headline prevalence
from such a sample is not a population estimate and must not be presented as
one. `[OPEN]`

Mitigations, in ascending cost:

1. **Triangulate frames.** Collect through ≥3 unlike channels (a professional
   association, a general small-business list, a developer community) and
   **report each separately.** Convergence across unlike frames is evidence;
   a single pooled number is not.
2. **Report by intensity.** Always stratify by S4 (hours/week). The honest
   headline is *"among professionals using these tools >10 h/week, X%"* — a
   claim the data can support.
3. **Anchor to a probability panel** if funding permits. A short 3-item version
   (B1, B2, R1) fielded on an established panel calibrates the convenience
   sample. This is the single highest-value upgrade. `[OPEN]`
4. **Publish the raw distribution**, not just point estimates.

**Target n:** 400 minimum for stratified reporting; 1,000 preferred.
**Field window:** fixed, published in advance, not extended.

---

## 8 · Estimator

```
DPS_stated   = share with B1≥2 AND B2=Yes AND (A1 includes a bolded option)
DPS_revealed = share choosing Plan B at the 30% penalty (R1)
Transfer_hi  = DPS_stated   × mean(incremental spend) × population
Transfer_lo  = DPS_revealed × mean(incremental spend) × population   [if lower]
```

**Reporting rule, fixed in advance:** publish both; **lead with the lower**;
state the population base used and its source; give confidence intervals; and
report the by-frame spread rather than concealing it in a pooled mean.
`[VALUE PREMISE]`

Incremental spend is computed as the reported total (B3, midpoint) minus the
cost of a single subscription at the respondent's stated tier — not the full
multi-subscription spend, which would overstate.

---

## 9 · Ethics & admin

- No PII collected; no account credentials; no employer identification.
- Consent screen states purpose after §4, and permits withdrawal.
- Free-text is reviewed for inadvertent identifiers before publication.
- Author's advocacy interest is disclosed on the landing page.
- Data published as anonymised microdata with the analysis code, so the
  headline number can be recomputed by anyone who distrusts it.
- No IRB is required for a private working paper, but any university
  collaboration will require one — obtain it *before* fielding, not after.
  `[OPEN]`

---

## 10 · What would falsify the premise

State this before collecting, so the result means something either way:

- If **DPS_revealed is low** (most respondents take Plan A — more capacity,
  no gauge), the gauge is worth less than claimed and WP-36's economic argument
  weakens substantially, whatever the stated-reason data says.
- If duplicates are **overwhelmingly explained by capability differences**
  rather than capacity visibility, the duplicate-provisioning harm is not the
  right lead for the policy and the disclosure case must rest on
  interruption cost alone.
- If **most respondents already have a usable gauge** (A3), the problem is
  narrower than described and the proposal should be scoped to the providers
  that lack one.

Any of these outcomes gets published. `[VALUE PREMISE]`

---

*CC BY 4.0 · © 2026 Pablo Nogueira Grossi — G6 LLC · Newark, NJ ·
g6llc@proton.me · ORCID 0009-0000-6496-2186 · Series DOI 10.5281/zenodo.19117399*
