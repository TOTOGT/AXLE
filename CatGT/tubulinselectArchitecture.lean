import Mathlib.Topology.Basic
import Mathlib.Data.Set.Basic
import Mathlib.Analysis.InnerProductSpace.Basic  -- for vector-like curvature/energy

/-!
# dm³ Operator — selectArchitecture with Contact-Normal Parameters

This implements the **grammar function** `selectArchitecture` using the **contact normal form** you reference in the AXLE/TOGT framework.

### Model
Each architecture is selected by a tuple of parameters that encode the geometric/energetic "signature" of the tubulin lattice:

- `μ_max` : maximum contact normal strength (longitudinal + lateral bonds)
- `ω`     : angular / curvature frequency (protofilament twist or sheet closure)
- `β`     : lateral bond angle / chirality bias parameter
- Additional helpers: average curvature `κ_avg`, energy threshold `ε`, polarity `polarity`

The function evaluates a **score** for each of the 15 architectures and picks the one with the highest score (or the first that exceeds a stability threshold). This is deterministic under the dm³ pipeline but can be made stochastic later.

This directly supports **Morphology is Computation**: the parameters flowing through C → K → F determine the executable geometry.
-/

-- Extend Configuration with parameter context (for realism)
structure ContactParams where
  μ_max : ℝ   -- max contact normal (bond strength)
  ω     : ℝ   -- curvature / twist frequency
  β     : ℝ   -- lateral angle / chirality bias
  κ_avg : ℝ   -- average sensed curvature
  ε     : ℝ   -- local energy / GTP-cap level
  polarity : Bool  -- + / - end dominance

structure Configuration (α β : Type) where
  monomers     : Set (TubulinMonomer)
  curvatureMap : α → ℝ
  energyMap    : α → ℝ
  topology     : Architecture
  params       : ContactParams   -- injected from K phase

-- The 15 architectures (unchanged)
inductive Architecture : Type
  | theWave      | theEngine    | theDivider | theBus      | theStrut
  | theTemplate  | theDrill     | theRod     | theArchitect| theSculptor
  | theMouth     | theCage      | theSpring  | theLattice  | theBreaker

-- Score function for each architecture based on contact-normal parameters
def architectureScore (arch : Architecture) (p : ContactParams) : ℝ :=
  match arch with
  | .theWave      =>  p.ω * 10.0 + p.κ_avg * 5.0 - |p.β| * 2.0          -- oscillatory, high frequency
  | .theEngine    =>  p.μ_max * 8.0 + if p.polarity then 5.0 else 0.0   -- symmetric 9+2
  | .theDivider   =>  p.κ_avg * (-8.0) + p.ε * 12.0                     -- catastrophe-prone bipolar
  | .theBus       =>  if p.polarity then p.μ_max * 7.0 else 0.0         -- anti-parallel transport
  | .theStrut     =>  p.μ_max * 9.0 - p.κ_avg * 3.0                     -- high stiffness, low curvature
  | .theTemplate  =>  p.μ_max * 6.0 + if p.ω ≈ 9 then 20.0 else 0.0     -- nine-fold symmetry
  | .theDrill     =>  p.β * 15.0 + p.ω * 4.0                            -- helical chiral
  | .theRod       =>  p.μ_max * 10.0 - p.κ_avg                          -- straight crystalline
  | .theArchitect =>  p.κ_avg * 6.0 + p.ω * 8.0                         -- geodesic / spatial
  | .theSculptor  =>  p.ε * 10.0 - |p.β|                                -- transient morphogenetic
  | .theMouth     =>  p.κ_avg * (-12.0) + p.μ_max * 5.0                 -- convergent funnel
  | .theCage      =>  p.μ_max * 7.0 + if !p.polarity then 6.0 else 0.0  -- cortical compression
  | .theSpring    =>  p.ω * 12.0 - p.κ_avg * 2.0                        -- elastic reversible
  | .theLattice   =>  p.μ_max * 11.0 - p.ω * 3.0                        -- hexagonal crystal
  | .theBreaker   =>  p.β * 20.0 + p.κ_avg * 3.0                        -- strong chirality break (LR asymmetry)

-- Threshold for stability (tunable)
def stabilityThreshold : ℝ := 25.0

-- The grammar: select the architecture with the highest score above threshold
def selectArchitecture (cfg : Configuration α β) : Architecture :=
  let scores := [
    (Architecture.theWave,      architectureScore .theWave      cfg.params),
    (Architecture.theEngine,    architectureScore .theEngine    cfg.params),
    (Architecture.theDivider,   architectureScore .theDivider   cfg.params),
    (Architecture.theBus,       architectureScore .theBus       cfg.params),
    (Architecture.theStrut,     architectureScore .theStrut     cfg.params),
    (Architecture.theTemplate,  architectureScore .theTemplate  cfg.params),
    (Architecture.theDrill,     architectureScore .theDrill     cfg.params),
    (Architecture.theRod,       architectureScore .theRod       cfg.params),
    (Architecture.theArchitect, architectureScore .theArchitect cfg.params),
    (Architecture.theSculptor,  architectureScore .theSculptor  cfg.params),
    (Architecture.theMouth,     architectureScore .theMouth     cfg.params),
    (Architecture.theCage,      architectureScore .theCage      cfg.params),
    (Architecture.theSpring,    architectureScore .theSpring    cfg.params),
    (Architecture.theLattice,   architectureScore .theLattice   cfg.params),
    (Architecture.theBreaker,   architectureScore .theBreaker   cfg.params)
  ]
  let best := scores.argmax (fun (_, s) => s)  -- or fold to find max
  match best with
  | some (arch, score) => if score > stabilityThreshold then arch else cfg.topology  -- fallback to current if unstable
  | none => cfg.topology

-- Updated dm³ phases (now using the parameterized selector)
def Fold (cfg : Configuration α β) : Configuration α β :=
  { cfg with
    topology := selectArchitecture cfg
  }

def dm3 (cfg : Configuration α β) : Configuration α β :=
  Unfold (Fold (CurvatureThreshold (Compression cfg)))

/-!
## Key Properties (ready for proofs)

- `selectArchitecture` is total and returns one of the 15 constructors.
- It encodes your **contact normal form**: higher `μ_max` favors rigid structures (Strut, Lattice, Rod); high `|β|` favors chiral ones (Drill, Breaker); high `ω` favors oscillatory/wavy ones.
- The K phase (CurvatureThreshold) populates `curvatureMap` and `energyMap`, which feed into `params` for F.
- Fixed-point condition now depends explicitly on parameters:
  `dm3 x = x` when the selected architecture reproduces parameters consistent with its own signature.

## Example Instantiation

```lean4
def exampleBreakerParams : ContactParams :=
  { μ_max := 30.0, ω := 2.5, β := 45.0, κ_avg := 0.8, ε := 15.0, polarity := false }

def testCfg : Configuration Unit Unit := { ... params := exampleBreakerParams, topology := .theBreaker, ... }

#eval selectArchitecture testCfg  -- should return .theBreaker with high probability
