"""Run the whole pipeline end to end:  python run_all.py

generate raw data -> clean + load SQLite -> SQL analysis -> models -> charts -> README numbers -> tests
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STEPS = [
    ("Generate synthetic raw data", ["src/generate_data.py"]),
    ("Clean data and load SQLite", ["src/clean_data.py"]),
    ("Run SQL analysis queries", ["src/run_sql.py"]),
    ("Fit statistical models", ["src/analysis.py"]),
    ("Render charts", ["src/charts.py"]),
    ("Fill README numbers from outputs", ["src/build_readme.py"]),
    ("Run tests", ["-m", "pytest", "-q"]),
]


def main() -> int:
    for i, (label, args) in enumerate(STEPS, start=1):
        print(f"\n[{i}/{len(STEPS)}] {label}", flush=True)
        t0 = time.time()
        result = subprocess.run([sys.executable, *args], cwd=ROOT)
        if result.returncode != 0:
            print(f"\nFAILED at step {i}: {label}")
            return result.returncode
        print(f"    done in {time.time() - t0:.1f}s")
    print("\nPipeline complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
