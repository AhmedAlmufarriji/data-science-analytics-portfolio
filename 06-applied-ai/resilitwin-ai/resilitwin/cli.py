"""Reproducible command-line workflow."""
import argparse
import json
from pathlib import Path
from .scenarios import Scenario, engine, evaluate
from .simulation import generate_history


def main():
    parser = argparse.ArgumentParser(description="ResiliTwin AI reproducible simulation and scenario analysis")
    parser.add_argument("command", choices=["generate", "train", "scenario"])
    parser.add_argument("--out", default="artifacts", help="Output directory")
    parser.add_argument("--outage", action="append", default=[], help="Supplier code to disrupt; repeatable")
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    if args.command == "generate":
        path = out / "synthetic_demand.csv"
        generate_history().to_csv(path, index=False)
        print(f"Wrote {path}")
    elif args.command == "train":
        path = out / "model_card.json"
        path.write_text(json.dumps(engine().score, indent=2), encoding="utf-8")
        print(f"Wrote {path}")
    elif args.command == "scenario":
        path = out / "scenario.json"
        path.write_text(json.dumps(evaluate(Scenario(outages=args.outage)), indent=2), encoding="utf-8")
        print(f"Wrote {path}")

if __name__ == "__main__":
    main()
