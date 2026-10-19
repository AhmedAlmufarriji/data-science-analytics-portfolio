"""Generate shareable synthetic demo telemetry, never real sensitive utility data."""
from __future__ import annotations

import argparse
from pathlib import Path

from aquasentinel.simulator import get_demo_frame


def main() -> None:
    parser = argparse.ArgumentParser(description="Export deterministic AquaSentinel demo CSV")
    parser.add_argument("--output", default="data/synthetic_telemetry.csv")
    args = parser.parse_args()
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    get_demo_frame().to_csv(path, index=False)
    print(f"Wrote synthetic telemetry to {path}")


if __name__ == "__main__":
    main()
