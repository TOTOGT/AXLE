namespace Orthogenesis

structure GrowthParams where
  g      : ℝ
  stages : ℕ
  target : ℝ
  rel    : Prop
deriving Repr

def R (P : GrowthParams) (n : ℕ) : ℝ :=
  P.g ^ (n : ℝ)

end Orthogenesis
