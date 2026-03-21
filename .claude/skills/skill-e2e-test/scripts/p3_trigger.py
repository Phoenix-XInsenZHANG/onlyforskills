#!/usr/bin/env python3
"""P3: Leaf-node trigger rate evaluation.

Calls claude -p for each query in trigger_evals.json, parses stream-json
for Skill tool_use blocks, majority-votes across repeats.

Confirmed format from live output:
  {"type":"tool_use","name":"Skill","input":{"skill":"<name>","args":"..."}}
"""
import json, os, subprocess, sys, argparse, time
from pathlib import Path
from collections import Counter

TIMEOUT = 60  # seconds per claude -p call


def call_claude(prompt: str, max_turns: int = 3) -> list[str]:
    """Run claude -p, return list of skill names invoked."""
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    cmd = ["claude", "-p",
           "--output-format", "stream-json",
           "--verbose",
           "--max-turns", str(max_turns)]
    try:
        result = subprocess.run(
            cmd, input=prompt, capture_output=True,
            text=True, env=env, timeout=TIMEOUT
        )
        skills = []
        for line in result.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
                if msg.get("type") == "assistant":
                    for block in msg.get("message", {}).get("content", []):
                        if (block.get("type") == "tool_use"
                                and block.get("name") == "Skill"):
                            s = block.get("input", {}).get("skill", "")
                            if s:
                                skills.append(s)
            except Exception:
                pass
        return skills
    except subprocess.TimeoutExpired:
        return []
    except Exception:
        return []


def evaluate_skill(skill_name: str, queries: list[dict],
                   repeats: int, max_turns: int) -> dict:
    results = []
    total_cost = 0.0

    for q in queries:
        prompt = q["query"]
        should_trigger = q["should_trigger"]
        runs = []

        for _ in range(repeats):
            skills_seen = call_claude(prompt, max_turns)
            triggered = skill_name in skills_seen
            correct = triggered == should_trigger
            runs.append({"triggered": triggered, "correct": correct})
            time.sleep(0.5)  # rate limit courtesy

        correct_count = sum(1 for r in runs if r["correct"])
        passed = correct_count > repeats / 2  # majority vote

        results.append({
            "query": prompt,
            "should_trigger": should_trigger,
            "passed": passed,
            "correct_rate": correct_count / repeats,
        })

    total = len(results)
    passed_count = sum(1 for r in results if r["passed"])
    trigger_rate = passed_count / total if total else 0

    return {
        "skill": skill_name,
        "trigger_rate": trigger_rate,
        "passed": passed_count,
        "total": total,
        "queries": results,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--skills-dir", default=".claude/skills")
    p.add_argument("--evals-file",
                   default=".claude/skills/skill-e2e-test/evals/trigger_evals.json")
    p.add_argument("--output", default=".skill-test-results/p3.json")
    p.add_argument("--max-turns", type=int, default=3)
    p.add_argument("--repeats", type=int, default=3)
    p.add_argument("--threshold", type=float, default=0.75)
    p.add_argument("--skill", help="Test a single skill only")
    args = p.parse_args()

    evals_path = Path(args.evals_file)
    if not evals_path.exists():
        print(f"ERROR: {evals_path} not found. Create trigger_evals.json first.")
        sys.exit(1)

    evals = json.loads(evals_path.read_text())
    skill_results = []

    for entry in evals:
        skill_name = entry["skill"]
        if args.skill and skill_name != args.skill:
            continue
        print(f"  Testing trigger: {skill_name} ({len(entry['queries'])} queries × {args.repeats} repeats)...")
        result = evaluate_skill(
            skill_name, entry["queries"], args.repeats, args.max_turns
        )
        skill_results.append(result)
        status = "✅" if result["trigger_rate"] >= args.threshold else "❌"
        print(f"    {status} {skill_name}: {result['trigger_rate']:.0%} "
              f"({result['passed']}/{result['total']})")

    if not skill_results:
        print("No skills tested.")
        sys.exit(0)

    overall_rate = sum(r["trigger_rate"] for r in skill_results) / len(skill_results)
    failing = [r for r in skill_results if r["trigger_rate"] < args.threshold]
    overall_passed = len(failing) == 0 and overall_rate >= 0.80

    out = {
        "phase": "P3",
        "threshold": args.threshold,
        "overall_rate": overall_rate,
        "overall_passed": overall_passed,
        "skills_tested": len(skill_results),
        "skills_failing": len(failing),
        "score": f"{overall_rate:.0%}",
        "skills": skill_results,
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(out, indent=2, ensure_ascii=False))

    status = "✅ PASS" if overall_passed else "❌ FAIL"
    print(f"\nP3 Trigger Rate: {overall_rate:.0%} overall {status}")
    for r in failing:
        print(f"  ✗ {r['skill']}: {r['trigger_rate']:.0%} < {args.threshold:.0%}")
    sys.exit(0 if overall_passed else 1)


if __name__ == "__main__":
    main()
