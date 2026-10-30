#!/usr/bin/env python3
# Builds Journal/vol16.html from vol15.html (head, script, tail) + new pages.
import re, os, sys
J = os.path.expanduser('~/mnt/Desktop/AXLE/Journal')
LIT = os.path.expanduser('~/mnt/Desktop/b3s/assignments/literature')
src = open(f'{J}/vol15.html', encoding='utf8').read().split('\n')
head = '\n'.join(src[:106])           # through <section open? no: lines 1-106 end before page 1
assert src[106].strip().startswith('<section class="pg is-active">'), src[106]
# end of pages = line index of '</div>' after last </section> ; find the nav div
i_nav = next(i for i, l in enumerate(src) if l.startswith('<div class="nav">'))
tail = '\n'.join(src[i_nav - 1:])      # blank line + '</div>' closing pgs? checked below
# head fixes
head = re.sub(r'<title>.*?</title>', '<title>Imaginary Origin — The Generative Science Journal — Vol. Ω No. 16 — Dimensions Between the Integers</title>', head)
head = re.sub(r'<meta name="description" content="[^"]*">',
 '<meta name="description" content="Vol. &#937; No. 16, 7 November 2026. Three new chapters of Book 4 on dimension: a curve of dimension exactly 4/3 whose pieces touch but do not cross, strange attractors with their computed Lyapunov exponents and what the checks changed, and a set of dimension &#960;. Page 6: The Reading Room, Part 11.">', head)
assert 'No. 16' in head

def J_(n, t): return f'<span class="jump" data-goto="{n}" style="text-decoration:underline;cursor:pointer;">{t}</span>'
CONT = lambda t: f'<span class="kick">{t}</span>'
def RH(n, t): return f'<div class="runhead"><span>Imaginary Origin · Vol. Ω No. 16</span><span>Page {n} &#183; {t}</span></div>'
def HD(t, sub): return (f'<div class="hd" style="font-size:clamp(20px,3.2vw,26px);">{t}</div>\n'
  f'    <div style="font-size:12px;color:#3a3a40;font-style:italic;margin:4px 0 10px;">{sub}</div>')
def BOX(title, *ps, last_grey=True):
    out = f'<div style="border:1px solid #16161a;background:#fbfbf8;padding:10px 13px;margin:12px 0 4px;">\n      <div class="kick" style="margin-bottom:5px;">{title}</div>'
    for k, p in enumerate(ps):
        g = ' color:#3a3a40;' if (last_grey and k == len(ps) - 1 and len(ps) > 1) else ''
        mb = '0' if k == len(ps) - 1 else '0 0 6px'
        out += f'\n      <p style="font-size:11.5px;margin:{mb};{g}">{p}</p>'
    return out + '\n    </div>'

# ---------------- page 1 : fractals ----------------
p1 = f'''  <section class="pg is-active">
    <div style="display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:10px;padding-bottom:6px;">
      <div style="border:1px solid #16161a;padding:5px 8px;font-size:9px;max-width:158px;"><b style="font-size:8px;">THE MOTTO</b><br><span style="font-style:italic;">&#8220;i, the rotation; o, the point it turns about.&#8221;</span></div>
      <div style="text-align:center;" class="kick">Vol. &#937; &#183; No. 16<br>The Generative Science Journal</div>
      <div style="text-align:right;" class="kick">Newark, N.J.<br>Free &#183; CC BY 4.0<br><a href="vol15.html" style="color:#16161a;">&#8592; No. 15</a> &#183; <a href="vol16.html" style="color:#16161a;">No. 16 &#8594;</a></div>
    </div>
    <div style="text-align:center;border-top:1px solid #16161a;border-bottom:1px solid #16161a;padding:8px 0 6px;"><div style="font-family:'UnifrakturMaguntia',serif;font-size:clamp(34px,7vw,60px);line-height:1;">Imaginary Origin</div></div>
    <div style="display:flex;justify-content:space-between;align-items:center;font-size:9.5px;text-transform:uppercase;letter-spacing:.06em;color:#3a3a40;border-bottom:1px solid #16161a;padding:4px 1px;"><span>Saturday, November 7, 2026</span><span style="text-transform:none;font-size:12px;">emblem: <span class="emblem">$g^{{16}}$</span></span><span>Morning Edition</span></div>
    <div class="lead" style="display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-top:14px;">
      <div style="border-right:1px solid #d0d0c8;padding-right:16px;">
        <div class="hd" style="font-size:clamp(22px,3.6vw,30px);">Dimensions Between the Integers</div>
        <div style="font-size:12px;color:#3a3a40;font-style:italic;margin:5px 0 9px;padding-bottom:8px;border-bottom:1px solid #d0d0c8;">Three new chapters of Book 4 ask what it means for an object to have a dimension that is not a whole number. A curve at exactly 4/3, attractors thinner than a solid, and a set of dimension &#960;.</div>
        <p>A line has dimension 1 and a filled square has dimension 2. Replace an object by N copies of itself, each scaled by a ratio r, and its similarity dimension is log N / log(1/r). Chapter 1&#189; builds a curve from four pieces at ratio 2<sup>&#8722;3/2</sup>, which gives d = 4/3 exactly. It is not the Koch curve, whose dimension is 1.2619. {J_(1, 'Page 2')} and {J_(2, 'Page 3')} move one step up, to chaotic flows in three variables. {J_(3, 'Page 4')} builds a set of dimension &#960; and says what must be true of the space around it.</p>
        <p>The curve was checked in exact integer arithmetic. No two pieces cross at any level tried, but from level 3 on pieces touch: 12, 70, 316 touching pairs at levels 3 to 5, and 5,544,270 at level 12. Touching is compatible with the open-set condition that the dimension formula needs, and that condition has <b>not</b> been proved.</p>
        <div class="pull">The algebra is exact. Whether the limit curve has dimension 4/3 rests on a condition that is checked at finite levels and not proved.</div>
        <p>A floating-point version of the crossing test gave false crossings at level 5, exactly at the touch points, and its counts were dropped. {J_(4, 'Page 5')} lists what was withdrawn and what is open.</p>
        <p style="font-size:11.5px;color:#3a3a40;">The Reading Room, {J_(5, 'Page 6')}, carries Part 11 of the serial, set from its source.</p>
      </div>
      <div>
        <div class="kick" style="border-bottom:1px solid #16161a;padding-bottom:3px;margin-bottom:7px;">The one number to carry</div>
        <p style="font-size:11.5px;">0.3305. Touching pairs per piece on the tent curve at levels 9 to 12 run 0.3299, 0.3302, 0.3304, 0.3305, rising ever more slowly. That is below 1/3, so an earlier suggestion that the value tends to 1/3 is not supported. The extrapolation assumes the differences shrink geometrically, which is itself unproved.</p>
        <div class="stat" style="margin-top:9px;">
          <span class="kick">This issue</span>
          <div style="font-family:'Courier New',monospace;font-size:11.5px;line-height:1.55;">chapters added &#160;&#160;&#160;&#160;&#160;&#160;3<br>Lean files, clean &#160;&#160;&#160;&#160;3<br>proper crossings &#160;&#160;&#160;&#160;&#160;0<br>serial part &#160;&#160;&#160;&#160;&#160;&#160;&#160;11 of 18</div>
          <span class="kick">Lean runs are the author&#8217;s</span>
        </div>
        <div class="stat" style="margin-top:9px;">
          <span class="kick">An invitation</span>
          <div style="font-size:11.5px;line-height:1.5;margin-top:3px;">A math study group meets online, in the library. Everyone is welcome. {J_(4, 'Page 5')} says how to join.</div>
        </div>
        <p style="font-size:11px;color:#3a3a40;margin-top:9px;">Figures from Book 4, Chapter 1&#189;: <code>book4/fractals.html</code>, with the verifier <code>fractals-verify.py</code> and the touch counters beside it.</p>
      </div>
    </div>
    <span class="kick">Continued on Page 2 &#183; Strange Attractors</span>
  </section>'''

# ---------------- page 2 : attractors computed ----------------
p2 = f'''  <section class="pg is-right">
    {RH(2, 'Strange Attractors')}
    {HD('Between Two and Three Dimensions', 'Chapter 2&#189; &#183; What was computed, and what the checks changed')}
    <p>A chaotic flow in three variables contracts volume, so its attractor is thinner than a solid, yet it never settles into a curve. For each system the verifier integrates the equations with a fourth-order Runge&#8211;Kutta step, discards a transient, and computes the full Lyapunov spectrum by the Benettin method (QR renormalization, tangent map carried alongside the orbit). The Kaplan&#8211;Yorke dimension is then read off the spectrum. It is a conjectured estimate, not a proved value, and any exponent within 0.01 of zero is counted as zero.</p>
    <p>Two checks guard the code. For systems whose divergence is constant, the exponents must add up to it exactly. The Burke&#8211;Shaw field must be unchanged by the half-turn (x, y, z) &#8594; (&#8722;x, &#8722;y, z). All constant-divergence rows pass the sum check to four decimals, and both symmetry tests pass at 200 random points each. For Lorenz, &#955;<sub>1</sub> = 0.909 and the Kaplan&#8211;Yorke dimension is 2.062, consistent with the usual values (about 0.906 and 2.06), which are quoted from memory of the literature and were not checked against a source for this chapter.</p>
    <div class="kick" style="margin:12px 0 4px;">What the checks changed</div>
    <table class="led"><tr><th style="width:24%;">System</th><th>Common belief</th><th>In this run</th></tr>
      <tr><td>Halvorsen, a = 1.89</td><td>Drawn everywhere as a chaotic attractor.</td><td>&#955;<sub>1</sub> = +0.0015, indistinguishable from zero, the others negative: a limit cycle. At a = 1.4 the largest exponent is 0.673 and the system is chaotic. Both are on the plate.</td></tr>
      <tr><td>Aizawa</td><td>One set of parameters, one attractor.</td><td>Same parameters, two starts. One gave &#955;<sub>1</sub> = 0.096, chaotic. The other, the one many write-ups use, gave exponents (0, &#8722;, &#8722;): a limit cycle. A single parameter set can hold more than one attractor.</td></tr>
      <tr><td>Thomas, b = 0.208186</td><td>Chaotic.</td><td>&#955;<sub>1</sub> = +0.0023 here, not distinguishable from zero. At b = 0.18 it is 0.030 and the system is chaotic. It sits at the edge.</td></tr>
      <tr><td>Sprott&#8217;s case A</td><td>A strange attractor.</td><td>Exponents sum to about zero (&#8722;0.0039). It is conservative, so it has no attractor: a chaotic sea among regular orbits that does not contract. On the plate as a contrast.</td></tr></table>
    {BOX('Limits of the numbers', 'Each exponent is a finite-time estimate from one orbit. Where two starts were tried they agree to about two decimals, and no more precision is claimed. This is not a proof of chaos for any system.', 'The chapter does not claim the systems share an invariant. They share a form, three variables and a smooth nonlinear flow, and each has its own computed numbers.')}
    {CONT('Continued on Page 3 &#183; Sources and the Neighbour Audit')}
  </section>'''

# ---------------- page 3 : sources + audit ----------------
p3 = f'''  <section class="pg is-right">
    {RH(3, 'Sources and the Neighbour Audit')}
    {HD('Where Each Equation Came From', 'And what the neighbouring pages of Book 4 turned out to be good for, audited in full on 29 October 2026')}
    <table class="led"><tr><th style="width:30%;">Item</th><th>Source, and its limit</th></tr>
      <tr><td>Lorenz, Chen and L&#252; equations and classical parameters</td><td>Read from arXiv 1409.8649. The constant divergences, &#8722;10 and &#8722;19, are the desk&#8217;s arithmetic from the paper&#8217;s formula, and the verifier reproduces them.</td></tr>
      <tr><td>Aizawa</td><td>From a web write-up that is internally inconsistent about the parameter e: it is listed but missing from the written z-equation. The form with the e term was used, as the write-up&#8217;s own code does.</td></tr>
      <tr><td>Burke&#8211;Shaw</td><td>Parameters s = 10, v = 4.272 and the half-turn symmetry are from Paul Bourke&#8217;s page, which gives the equations only as an image. The equations used are the standard form written from memory. The symmetry check agrees with his statement and does not prove the form is the published one.</td></tr>
      <tr><td>Sprott&#8217;s case A</td><td>From a course page.</td></tr>
      <tr><td>R&#246;ssler, Halvorsen, Thomas</td><td>Standard forms from memory, not fetched for this chapter.</td></tr></table>
    <div class="kick" style="margin:12px 0 4px;">The neighbour audit</div>
    <table class="led"><tr><th style="width:30%;">Page</th><th>What it is good for, and what to read with care</th></tr>
      <tr><td>Lorenz &#183; Chaos Theory and dm&#179;</td><td>The equations, fixed points, exponents (+0.906, 0, &#8722;14.572) and Kaplan&#8211;Yorke dimension 2.06 agree with this chapter&#8217;s run (+0.9086 and 2.062). Its claim that the Lorenz flow sits in a contact manifold as a Reeb flow is <b>not supported</b>: a Reeb flow preserves volume, and Lorenz contracts it, with divergence &#8722;13.667, the same number the verifier reproduces.</td></tr>
      <tr><td>&#956; &#183; The Lyapunov Operator, F &#183; Catastrophe Theory and Disaster Theory</td><td>Readable accounts of the exponent and of Thom&#8217;s catastrophes, each now carrying a corrections box listing statements that do not hold: fold location, catastrophe labels, the n-bonacci rate, the Reeb divergence. Nothing in them is a computed result about the systems on this chapter&#8217;s plate.</td></tr>
      <tr><td>The Banking Butterfly</td><td>A settlement-arithmetic paper that borrows the Lorenz picture as an analogy. It says itself that the mechanism is not chaotic, and it does not use catastrophe theory.</td></tr></table>
    <div class="pull">A Reeb flow preserves volume. Lorenz contracts it. The two cannot be the same flow.</div>
    <p>This chapter&#8217;s role is narrower than those pages: it adds the other systems and a computed check for each.</p>
    {CONT('Continued on Page 4 &#183; Pi')}
  </section>'''

# ---------------- page 4 : pi ----------------
p4 = f'''  <section class="pg is-right">
    {RH(4, 'Pi')}
    {HD('A Set Whose Dimension Is 3.14159&#8230;', 'Chapter 3&#189; &#183; A vector space cannot have it; a set can')}
    <p>A vector space has a whole-number dimension. A set has other dimensions that measure how it fills space, and they take any real value from 0 up to the dimension of the space it sits in. A set of dimension 3.14159&#8230; needs at least four dimensions around it, and four is enough.</p>
    <table class="led"><tr><th style="width:26%;">Step</th><th>Derivation</th></tr>
      <tr><td>The Cantor set</td><td>Let s = &#960; &#8722; 3 = 0.14159&#8230; Two pieces, each a copy of the whole scaled by r, one at each end of [0, 1]. The similarity equation 2&#183;r<sup>s</sup> = 1 gives r = 2<sup>&#8722;1/s</sup> = 0.0074812&#8230;, so 1/r = 133.67&#8230; Since r &lt; 1/2 the pieces do not touch.</td></tr>
      <tr><td>Times a solid</td><td>Take C &#215; [0,1]<sup>3</sup> in R<sup>4</sup>. At scale &#949; = r<sup>k</sup> the count is N(&#949;) = 2<sup>k</sup>&#183;(r<sup>&#8722;k</sup>)<sup>3</sup> = &#949;<sup>&#8722;(3+s)</sup> = &#949;<sup>&#8722;&#960;</sup>, using 2 = r<sup>&#8722;s</sup>.</td></tr>
      <tr><td>What is quoted</td><td>That the Hausdorff dimension of the dust is s (open set condition; Moran, Hutchinson) and that the product with R<sup>3</sup> adds the dimensions (Falconer) are standard theorems, <b>quoted, not derived</b>.</td></tr></table>
    <p>The verifier&#8217;s output matches: log 2 / log(1/r) = 0.141592653590 = s, and 2&#183;r<sup>s</sup> = 1.000000000000. At the level-aligned scales the exact count gives s at every level checked, 1 to 6. A straight fit across ten decades gave 0.158 against the true 0.142, which is what box counting does on a very sparse set, and the reason to prefer the exact level count.</p>
    {BOX('The lattice trap', 'The grid constructions of Chapter 1&#189; give dimensions ln N / ln m for whole numbers N and m. In the unit 4-cube N can be as large as m<super style="display:none"></super><sup>4</sup>. The verifier found m = 37 with N = 84,460 giving 3.141593, an error near 4&#215;10<sup>&#8722;8</sup>. It does not give &#960; exactly: that would need m<sup>&#960;</sup> to be a whole number, and this check does not settle whether it can. The non-lattice ratio, 1/r = 133.67&#8230;, sidesteps the question.', 'Proposition, proved on paper: lattice dimensions are dense in (0, 4], with 0 &#8804; d &#8722; ln N / ln m &#8804; ln 2 / ln m. This is elementary and may well be known; no literature search was made.')}
    <div class="kick" style="margin:12px 0 4px;">Can m<sup>&#960;</sup> be a whole number? Every route tried</div>
    <table class="led"><tr><th style="width:26%;">Route</th><th>What it gives</th></tr>
      <tr><td>Certified bracketing</td><td>m<sup>&#960;</sup> lies strictly between two consecutive integers for every m from 2 to 1,000,000, by interval arithmetic. Nearest miss: 2.9&#215;10<sup>&#8722;7</sup>, at m = 973,492. Nothing beyond the limit.</td></tr>
      <tr><td>Six exponentials theorem</td><td>At most two primes p can have p<sup>&#960;</sup> algebraic. Says nothing directly about composite m.</td></tr>
      <tr><td>Gelfond&#8211;Schneider, Baker</td><td>Do not apply: &#960; is neither an algebraic exponent nor an algebraic coefficient.</td></tr>
      <tr><td>Schanuel&#8217;s conjecture</td><td>Would, as far as the author knows, settle it. Conditional on an unproved conjecture; the implication is not derived.</td></tr>
      <tr><td>Heuristic</td><td>Fractional parts of m<sup>&#960;</sup> behave like random numbers. Evidence, not proof.</td></tr></table>
    <p style="font-size:11.5px;color:#3a3a40;">Machine-checked, by the author on Lean v4.32.0 with only the standard axioms: the algebra of the construction (<code>PiDimension.lean</code>) and the density statement with the crude bound (<code>LatticeDensity.lean</code>). Neither proves a Hausdorff dimension. The certificates for m<sup>&#960;</sup> are computed, not Lean-checked.</p>
    <p style="font-size:11.5px;color:#3a3a40;">This is a construction, not a natural object. &#960; is not special: the same recipe gives e, 3.2 or 3.9. No four-variable flow was computed, so the chapter makes no claim about any natural set near &#960;.</p>
    {CONT('Continued on Page 5 &#183; Corrections and the Open Desk')}
  </section>'''
p4 = p4.replace('<super style="display:none"></super>', '')

# ---------------- page 5 : corrections + open desk ----------------
p5 = f'''  <section class="pg is-right">
    {RH(5, 'Corrections and the Open Desk')}
    {HD('What Was Withdrawn, and What Is Still Unchecked', 'Corrections go inside the page, at the section they change, with a date; each open item is named so none can be mistaken for done')}
    <div class="kick" style="margin:6px 0 4px;">Withdrawn or superseded</div>
    <table class="led"><tr><th style="width:34%;">Where</th><th>What changed</th></tr>
      <tr><td>Ch 1&#189; &#183; floating-point crossing scan</td><td>Superseded by an exact integer scan at nine rational-tangent angles. The floating-point test gave nonzero crossings at level 5, exactly at the touch points where rounding flips the answer. Its counts are not to be quoted.</td></tr>
      <tr><td>Ch 1&#189; &#183; touching pairs per piece &#8594; 1/3</td><td>Not supported. Levels 9 to 12 give 0.3299 to 0.3305, below 1/3.</td></tr>
      <tr><td>Ch 1&#189; &#183; lattice alignment makes 45&#176; special</td><td>Tested and dropped. Every rational tangent gives lattice vertices and those angles still cross. What differs is that at 45&#176; the segment directions close up into a finite set.</td></tr>
      <tr><td>Lorenz &#183; Chaos Theory and dm&#179;</td><td>The claim that the Lorenz flow is a Reeb flow is not supported, because a Reeb flow preserves volume and Lorenz does not.</td></tr>
      <tr><td>&#956;, F, Catastrophe and Disaster pages</td><td>Corrections boxes added on 29 October 2026 listing the statements that do not hold.</td></tr>
      <tr><td>Ch 2&#189; &#183; Halvorsen at 1.89, Sprott&#8217;s case A</td><td>Shown as a limit cycle and as a conservative system respectively, not as strange attractors.</td></tr></table>
    <div class="kick" style="margin:12px 0 4px;">The open desk</div>
    <table class="led"><tr><th style="width:34%;">Item</th><th>State</th></tr>
      <tr><td>Open-set condition for the 4/3 tent curve</td><td>Checked numerically to level 5 and by touch counts to level 12. Not proved, so d = 4/3 is the similarity dimension and not a proved Hausdorff dimension. <span class="open">open</span></td></tr>
      <tr><td>Touch counts beyond level 8</td><td>The fast vertex counter agrees with the slow one at levels 3 to 8 and is assumed to agree beyond. <span class="open">open</span></td></tr>
      <tr><td>Odd-level half of the grid lemma</td><td><code>FractalGridLemma.lean</code> covers the even levels only. The tent argument for odd levels, and the identification of the two-step generator with two refinements, are by hand. <span class="open">open</span></td></tr>
      <tr><td>Hausdorff dimension of the &#960; set</td><td>Rests on two quoted theorems. The sharp lattice bound is on paper only. <span class="open">open</span></td></tr>
      <tr><td>m<sup>&#960;</sup> a whole number?</td><td>Open as far as the author knows. Proved only for m up to 10<sup>6</sup>. <span class="open">open</span></td></tr>
      <tr><td>Attractor equations from memory</td><td>R&#246;ssler, Halvorsen, Thomas and the Burke&#8211;Shaw form are not checked against a source. <span class="open">open</span></td></tr>
      <tr><td>A four-variable flow with dimension between 3 and 4</td><td>None computed. <span class="open">open</span></td></tr>
      <tr><td><code>book5/ExistenceBanach.lean</code></td><td>Written this week; <b>not yet compiled</b>. Nothing is claimed for it until it has been run and its output read. <span class="open">open</span></td></tr></table>
    {BOX('An invitation &#183; Math study group', 'You are invited to join a math study group that meets online, in the library. Everyone is welcome.', 'To join, or to ask when it meets, write to <b>g6llc@proton.me</b>.')}
    <div class="pull">An open item stays on this page until the check it names has been run and the result written beside it.</div>
    <p style="font-size:11.5px;color:#3a3a40;">The Reading Room follows on Page 6.</p>
    {CONT('Continued on Page 6 &#183; The Reading Room')}
  </section>'''
p5 = p5.replace('style="font-size:11.5px;margin:0 0 6px;"', 'style="font-size:12px;margin:0 0 6px;"', 1) if False else p5

# ---------------- page 6 : reading room, verbatim from the_ceiling.md ----------------
def esc(t):
    t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    t = t.replace('—', '&#8212;')
    t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
    return t
raw = open(f'{LIT}/the_ceiling.md', encoding='utf8').read().split('\n')
title = raw[0].lstrip('# ').strip(); assert title == 'The Ceiling'
kicker = raw[2].strip()
blocks = [l for l in raw[3:] if l.strip()]
PSTY = 'font-size:12.5px;text-align:justify;margin:0 0 8px;'
body = ''
first = True
for l in blocks:
    if l.strip() == '---':
        body += '    <div style="border-top:1px solid #c9b9a0;margin:12px 0 10px;"></div>\n'; continue
    e = esc(l.strip())
    if first:
        ch, rest = e[0], e[1:]
        body += f'    <p style="{PSTY}"><span style="float:left;font-family:Georgia,serif;font-size:34px;line-height:.8;padding:2px 6px 0 0;">{ch}</span>{rest}</p>\n'; first = False
    else:
        body += f'    <p style="{PSTY}">{e}</p>\n'
p6 = f'''  <section class="pg is-right" style="background:#f0e6d2;">
  <div class="runhead" style="padding:6px 18px 0;"><span>Imaginary Origin &#183; The Reading Room</span><span>Page 6</span></div>

  <div style="display:flex;align-items:flex-end;justify-content:space-between;gap:10px;padding:12px 18px 0;">
    <div style="font-family:Georgia,'Iowan Old Style',serif;line-height:.86;color:#221a14;">
      <span style="font-size:12px;letter-spacing:.02em;">The</span>
      <span style="font-size:30px;letter-spacing:-.02em;">Reading Room</span>
    </div>
    <div style="font-family:Georgia,serif;font-size:10px;color:#b5321f;text-align:right;letter-spacing:.04em;padding-bottom:3px;white-space:nowrap;">
      A Serial in 18 Parts &#183; Part 11<br>Week of November 7, 2026
    </div>
  </div>
  <div style="padding:0 18px;"><div aria-hidden="true" style="border-top:2px solid #221a14;border-bottom:1px solid #221a14;height:3px;margin:0 0 10px;"></div></div>

  <div style="padding:0 18px 16px;">
    <div style="font-family:Georgia,serif;font-size:10px;color:#b5321f;letter-spacing:.06em;text-transform:uppercase;margin-bottom:2px;">{esc(kicker)}</div>
    <div style="font-family:Georgia,'Iowan Old Style',serif;font-size:26px;line-height:1.1;color:#221a14;margin-bottom:2px;">No.&#8202;11&#8194;{esc(title)}</div>
    <div style="font-family:Georgia,serif;font-style:italic;font-size:12.5px;color:#3a3a40;margin-bottom:10px;">
      Pierre et Mademoiselle, by Pablo Nogueira Grossi &#8194;&#183;&#8194;
      <span style="font-size:11px;">See the note on fact &amp; fiction, below</span></div>

{body}
    <div style="border-top:1px solid #c9b9a0;margin:12px 0 8px;"></div>
    <p style="font-size:10.5px;color:#3a3a40;font-style:italic;margin:0 0 10px;">Part 11 of 18 &#8194;&#183;&#8194; Fiction, drawn from the documented world; the ledger below says which is which. Set from its source file, as written.</p>
    <p style="font-size:10.5px;color:#8a2f2f;margin:0 0 10px;border:1px solid #c9b9a0;background:#fdf6e8;padding:7px 9px;">
    <b>Rights notice.</b> <i>Pierre et Mademoiselle</i> is <b>not</b> covered by this issue&#8217;s
    CC&nbsp;BY&nbsp;4.0 licence. The serial and the work it belongs to &#8212; a limited series in
    development &#8212; are <b>&#169; 2026 Pablo Nogueira Grossi / G6 LLC, all rights reserved</b>.
    No licence to reproduce, adapt, translate or perform it is granted here.</p>

    <div style="border:1px solid #c9b9a0;background:#f7f0e2;padding:10px 12px;">
      <div style="font-family:Georgia,serif;font-size:10px;color:#b5321f;letter-spacing:.06em;text-transform:uppercase;margin-bottom:6px;">Fact &amp; Fiction &#183; the ledger for No.&#8202;11</div>
      <p style="font-size:11px;margin:0 0 7px;"><b>Documented</b>: nothing in the series ledger (FACT_AND_FICTION.md) bears on this part. It has no entry for the smoke, the children, the officer or the gates, and this part names no place, so it asserts nothing documented about any.</p>
      <p style="font-size:11px;margin:0;"><b>Invented</b>: the three children and their running ahead; Marie&#8217;s collapse and Fermat&#8217;s counting aloud to her; the soldiers at the gates, the officer who crosses himself, and the account of himself as a shipwrecked merchant. Marie is the series ledger&#8217;s item 2 and the voyage its item 5; both are invented, and the buffalo is the relocation recorded for No.&#8202;8.</p>
    </div>
  </div>
  </section>'''

tail = tail.replace('No. 15', 'No. 16').replace('vol15.html" style', 'vol16.html" style')
tail = re.sub(r'<a href="vol14\.html">.*?<a href="https://totogt\.github\.io/AXLE/">&#8592; AXLE home</a>',
  '<a href="vol15.html">&#8592; No. 15</a> &#183; <span style="font-style:italic;color:#3a3a40;">Three Tests That Could Have Failed</span> &#183; <a href="vol16.html">No. 16 &#8594;</a> &#183; <span style="font-style:italic;color:#3a3a40;">Dimensions Between the Integers</span> &#183; <span style="font-style:italic;color:#3a3a40;">Latest issue &#183; the full run is listed on</span> <a href="index.html">No. 2</a> &#183; <a href="https://totogt.github.io/AXLE/">&#8592; AXLE home</a>',
  tail, flags=re.S)
assert 'vol15.html">&#8592; No. 15' in tail, 'colophon not replaced'
out = head + '\n' + '\n'.join([p1, p2, p3, p4, p5, p6]) + '\n\n' + tail
open(f'{J}/vol16.html', 'w', encoding='utf8').write(out)
print('written', len(out))
