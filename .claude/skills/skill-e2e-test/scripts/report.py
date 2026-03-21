#!/usr/bin/env python3
"""Aggregate results from all phases and print final report."""
import json, sys, argparse
from pathlib import Path


def load(path: Path) -> dict | None:
    if path.exists():
        return json.loads(path.read_text())
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--results-dir", default=".skill-test-results")
    p.add_argument("--output", default=".skill-test-results/report.json")
    args = p.parse_args()

    d = Path(args.results_dir)
    p0 = load(d / "p0.json")
    p1 = load(d / "p1.json")
    p3 = load(d / "p3.json")
    p4 = load(d / "p4.json")
    p2 = load(d / "p2.json")

    rows = []
    total_cost = 0.0

    def row(phase, score, threshold, passed, cost):
        nonlocal total_cost
        total_cost += cost
        rows.append((phase, score, threshold,
                     "✅ PASS" if passed else "❌ FAIL",
                     f"${cost:.2f}"))

    if p0:
        row("P0 Valid", p0["score"], "100%", p0["overall_passed"],
            p0.get("cost_usd", 0.0))
    if p3:
        row("P3 Trig ", p3["score"], "75%", p3["overall_passed"],
            p3.get("cost_usd", 0.0))
    if p1:
        chains = p1.get("chains", [])
        avg = (sum(c["avg_completion_rate"] for c in chains) / len(chains)
               if chains else 0)
        row("P1 Chain", f"{avg:.0%}", "60%", p1["overall_passed"],
            p1.get("cost_usd", 0.0))
    if p4:
        loops = p4["total_loops_detected"]
        row("P4 Loop ", f"{loops} loops", "0", p4["overall_passed"],
            p4.get("cost_usd", 0.0))
    if p2:
        row("P2 Biz  ", "see detail", "60%", p2["overall_passed"],
            p2.get("cost_usd", 0.0))

    # CI gate: P0 + P3 must pass
    ci_passed = (
        (p0 is None or p0["overall_passed"]) and
        (p3 is None or p3["overall_passed"])
    )

    # Print table
    w = 54
    print("╔" + "═" * w + "╗")
    print(f"║{'Skill E2E Test Report':^{w}}║")
    print("╠══════════╦═══════════╦══════════╦════════╦══════════╣")
    print(f"║{'Phase':<10}║{'Score':<11}║{'Threshold':<10}║{'Status':<8}║{'Cost':<10}║")
    print("╠══════════╬═══════════╬══════════╬════════╬══════════╣")
    for phase, score, threshold, status, cost in rows:
        print(f"║{phase:<10}║{score:<11}║{threshold:<10}║{status:<8}║{cost:<10}║")
    print("╠══════════╬═══════════╬══════════╬════════╬══════════╣")
    overall_status = "✅ PASS" if ci_passed else "❌ FAIL"
    print(f"║{'OVERALL':<10}║{'':11}║{'':10}║{overall_status:<8}║${total_cost:<9.2f}║")
    print("╚══════════╩═══════════╩══════════╩════════╩══════════╝")
    print(f"\nCI gate (P0+P3): {'PASS ✅' if ci_passed else 'FAIL ❌'}")
    if not ci_passed:
        print("  Fix P0/P3 failures before merging.")

    report = {
        "ci_passed": ci_passed,
        "total_cost_usd": total_cost,
        "phases": {"p0": p0, "p1": p1, "p2": p2, "p3": p3, "p4": p4},
    }
    Path(args.output).write_text(json.dumps(report, indent=2, ensure_ascii=False))
    sys.exit(0 if ci_passed else 1)


if __name__ == "__main__":
    main()
