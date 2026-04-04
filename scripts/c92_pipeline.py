"""
AXLE — C9.2 Pipeline Runner
scripts/c92_pipeline.py

Runs the canonical C9.2 pipeline end-to-end:
  Step 1 — c92_sampler.py : graded drift observable, dyadic window [N, 2N]
  Step 2 — c92_fourier.py : mean-centered sparsity Fourier analysis

Modes
-----
  --test    Test run  : N=10000, M=8   (fast smoke-test)
  --golden  Golden run: N=100000, M=12 | M=14 | M=16
  --N / --M Custom single run

Artifacts per run
-----------------
  outputs/c92_sample_N{N}_M{M}.csv
  outputs/c92_summary_N{N}_M{M}.json
  outputs/c92_fourier_N{N}_M{M}.json

Usage:
  python c92_pipeline.py --test
  python c92_pipeline.py --golden
  python c92_pipeline.py --N 10000 --M 8 --out my_outputs/

G6 LLC · Pablo Nogueira Grossi · Newark NJ · 2026
MIT License
"""

import argparse
import sys
from pathlib import Path

# Allow running from the scripts/ directory directly
_SCRIPTS_DIR = Path(__file__).parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from c92_sampler import sample_dyadic_window      # noqa: E402
from c92_fourier import run_fourier_analysis       # noqa: E402


# ── PIPELINE CONFIGURATION ────────────────────────────────────────────────────

TEST_N = 10_000
TEST_M = 8

GOLDEN_N = 100_000
GOLDEN_M_VALUES = [12, 14, 16]


# ── PIPELINE ──────────────────────────────────────────────────────────────────

def run_single(N: int, M: int, out_dir: Path) -> None:
    """Run sampler + Fourier analysis for a single (N, M) configuration."""
    print(f"\n{'='*60}")
    print(f"C9.2 Pipeline — N={N}, M={M}")
    print(f"{'='*60}")

    sample_dyadic_window(N, M, out_dir)
    run_fourier_analysis(N, M, out_dir, out_dir)

    print(f"\n[C9.2 Pipeline] Run complete — artifacts:")
    print(f"  {out_dir / f'c92_sample_N{N}_M{M}.csv'}")
    print(f"  {out_dir / f'c92_summary_N{N}_M{M}.json'}")
    print(f"  {out_dir / f'c92_fourier_N{N}_M{M}.json'}")


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="C9.2 Pipeline Runner — Collatz graded drift + Fourier",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--test", action="store_true",
        help=f"Test run: N={TEST_N}, M={TEST_M}",
    )
    mode.add_argument(
        "--golden", action="store_true",
        help=f"Golden runs: N={GOLDEN_N}, M={GOLDEN_M_VALUES}",
    )
    parser.add_argument("--N", type=int,
                        help="Custom N (lower bound of dyadic window)")
    parser.add_argument("--M", type=int,
                        help="Custom M (odd residue class count)")
    parser.add_argument("--out", type=str, default="outputs",
                        help="Output directory for all artifacts")
    args = parser.parse_args()

    out_dir = Path(args.out)

    if args.test:
        run_single(TEST_N, TEST_M, out_dir)

    elif args.golden:
        for M in GOLDEN_M_VALUES:
            run_single(GOLDEN_N, M, out_dir)

    elif args.N and args.M:
        run_single(args.N, args.M, out_dir)

    else:
        print("C9.2 Pipeline — AXLE Collatz Golden Run System")
        print()
        print(f"  Test run  : python c92_pipeline.py --test")
        print(f"              (N={TEST_N}, M={TEST_M})")
        print()
        print(f"  Golden run: python c92_pipeline.py --golden")
        print(f"              (N={GOLDEN_N}, M=12 / 14 / 16)")
        print()
        print(f"  Custom    : python c92_pipeline.py --N <N> --M <M>")
        print()
        parser.print_help()
