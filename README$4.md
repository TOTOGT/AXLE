Language Specification: The Unified Generative Framework
TOGT + GCM + dm³_disc
Discrete Generative Contact Mechanics (dm³_disc)
A Formal Lift of the dm³ Category to Arithmetic Dynamical Systems
Pablo Nogueira Grossi (Independent Researcher)
v1.0 — April 2026 - Accompanies DiscreteDm3.lean attached to Lean Folder on the ROOT for the AXLE REPO: 
This note provides the precise “language-first” specification requested by the Collatz supplement (TOGT Report, pp. 108–109). It synthesizes:
the continuous dm³ framework of the GCM Manifesto (§2.2), both documents can be found attached to the ROOT of the AXLE REPO. 
the Topographical Orthogonal Generative Theory (TOGT) operator algebra (G = U \circ F \circ K \circ C),
the discrete lift dm³_disc formalized in Lean 4 (DiscreteDm3.lean v1.5).
The result is a single higher-order category in which both smooth contact flows and piecewise-linear arithmetic maps (such as the Collatz map) are objects. The Collatz conjecture is thereby reduced to a pure membership problem inside this category.
1. Continuous dm³ (GCM Recap)
A continuous dm³-system is a tuple (M, X, \alpha, V, \Phi, \Gamma) where:
(M) is a Riemannian manifold,
(X) is a C^2 vector field generating a flow,
\alpha is a contact form (maximally non-integrable hyperplane field),
(V) is a Lyapunov function with average descent outside the limit cycle,
\Phi is the contact Hamiltonian,
\Gamma is a hyperbolic structured limit cycle.
Morphisms are contactomorphisms f: M \to M' such that:
(f) commutes with the flows,
|\Phi'(f(x)) - \Phi(x)| \le C_\Phi,
V'(f(x)) \le V(x) + C_V.
The framework admits four main theorems (GCM Manifesto §2.2):
Existence and stability of \Gamma.
Categorical closure of the generative pipeline.
Contact normal form.
Structural stability under contact-preserving perturbations.
2. Discrete Lift: dm³_disc
A discrete dm³-system is a tuple (X, T, V, \Phi, \Gamma, \mathcal{G}) (exactly as in DiscreteDm3System v1.5) satisfying the eight axioms below.
State space:
X = \mathbb{N}_{\ge 1} (or any countable discrete space) with the 2-adic metric d_2(m,n) = 2^{-v_2(m-n)}.
Generative map: T: X \to X (piecewise-linear).
Discrete contact form:
Axiom (contactForm): \forall n odd, v_2(3n+1) \ge 1 (proved for Collatz).
Discrete contact Hamiltonian: \Phi: X \to \mathbb{R}_{\ge 0}.
Lyapunov function: V: X \to \mathbb{R}_{\ge 0}.
Structured limit cycle: \Gamma finite and attracting.
Mean contraction:
Axiom (meanContraction): \exists \kappa < 1, N_0 \in \mathbb{N} (monster threshold g_6 = 33) such that
\forall n \ge N_0,\quad \log(T^2(n)) - \log n \le \log \kappa.
(Classical 3/4 heuristic; analytic target.)
Operator grammar (TOGT):
Axiom (operatorDecomposition): T = G = U \circ F \circ K \circ C (proved for Collatz).
Categorical closure: The system belongs to \mathbf{dm}^3_{\mathrm{disc}}.
Morphisms \mathrm{Hom}(A,B) in \mathbf{dm}^3_{\mathrm{disc}} (exactly as in DiscreteDm3Hom v1.5) are maps f: A.X \to B.X such that:
f \circ T_A = T_B \circ f,
|\Phi_B(f(x)) - \Phi_A(x)| \le C_\Phi,
V_B(f(x)) \le V_A(x) + C_V,
the grammar is respected at the object level.
Composition and identities are defined and satisfy the category axioms (proved in Lean v1.5).
3. Collatz as a Canonical Object
The standard Collatz map is the normalized macro-step
T(n) =
\begin{cases}
n/2 & n \text{ even}, \\
(3n+1)/2^{v_2(3n+1)} & n \text{ odd}.
\end{cases}
It defines the concrete discrete dm³-system \mathrm{CollatzDm3Candidate} with:
X = \mathbb{N}, T = collatz,
\Phi(n) = v_2(n), V(n) = \log_2(n+1),
\Gamma = \{1,2,4\},
grammar \{C,K,F,U\} exactly as in the Lean file.
Proved axioms (structural):
operatorDecomposition (TOGT grammar (G)).
contactForm (2-adic valuation forces structured dissipation on odd branch).
Analytic targets (open in Lean):
meanContraction (3/4 factor above g_6 = 33).
lyapunovDescent (average \Delta V < 0).
hasStructuredCycle (every orbit reaches \Gamma).
4. AXLE Target 5 = Membership Problem
The Collatz conjecture is equivalent to the statement
\text{Collatz map } T \text{ is an object of } \mathbf{dm}^3_{\mathrm{disc}}.
i.e., the three open fields of CollatzDm3Candidate are satisfied. Once they are filled (or reduced to finitely-checkable inequalities), the categorical closure theorems of dm³_disc immediately imply that every orbit enters the unique structured cycle \Gamma = \{1,2,4\}.
In the Lean companion file DiscreteDm3.lean v1.5 this is literally the statement
lean
theorem collatz_converges (n : ℕ) :
  ∃ k, (Function.iterate collatz k n) ∈ collatzCycle
which reduces to membership of CollatzDm3Candidate in the category.
References
GCM Manifesto §2.2 (continuous dm³).
TOGT Report, pp. 108–109 (Collatz as corollary of crystal geometry).
DiscreteDm3.lean v1.5 (formal companion, AXLE repository).
This specification completes the “language-first” directive. The proof is now a membership problem inside a rigorously defined category. The only remaining work is the analytic verification of the three open fields — precisely where the Collatz supplement said the framework would land.
(End of specification — 3 pages when typeset.)
