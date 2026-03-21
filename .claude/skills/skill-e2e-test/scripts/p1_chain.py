#!/usr/bin/env python3
"""P1: Hub node chain propagation test.

Key insight from live testing:
- brainstorming requires interactive approval to proceed to writing-plans
- Prompt must explicitly say "auto-proceed, no approval needed"
- Skill format: {"type":"tool_use","name":"Skill","input":{"skill":"<n>"}}
"""
import json, os, subprocess, sys, argparse, time
from pathlib import Path

TIMEOUT = 600  # chain tests take longer (10 min for long chains)


def call_claude_chain(prompt: str, max_turns: int) -> dict:
    """Run claude -p, return skill sequence and stop reason."""
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    cmd = ["claude", "-p",
           "--output-format", "stream-json",
           "--verbose"]
    # Only add --max-turns if it's > 0 (0 means unlimited, so omit the flag)
    if max_turns > 0:
        cmd.extend(["--max-turns", str(max_turns)])
    try:
        result = subprocess.run(
            cmd, input=prompt, capture_output=True,
            text=True, env=env, timeout=TIMEOUT
        )
        skills = []
        turns = 0
        stop = None
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
                if msg.get("type") == "result":
                    turns = msg.get("num_turns", 0)
                    stop = msg.get("subtype", msg.get("stop_reason"))
            except Exception:
                pass
        return {"skills": skills, "turns": turns, "stop": stop}
    except subprocess.TimeoutExpired:
        return {"skills": [], "turns": 0, "stop": "timeout"}
    except Exception as e:
        return {"skills": [], "turns": 0, "stop": f"error:{e}"}


def score_chain(skills_seen: list[str], expected_chain: list[str]) -> dict:
    """Score how far through the expected chain we got."""
    completed = 0
    for expected in expected_chain:
        if expected in skills_seen:
            completed += 1
    return {
        "completed": completed,
        "total": len(expected_chain),
        "rate": completed / len(expected_chain) if expected_chain else 0,
        "expected": expected_chain,
        "actual": skills_seen,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--chains-file",
                   default=".claude/skills/skill-e2e-test/evals/chains.json")
    p.add_argument("--output", default=".skill-test-results/p1.json")
    p.add_argument("--max-turns", type=int, default=30)
    p.add_argument("--repeats", type=int, default=2)
    p.add_argument("--threshold", type=float, default=0.60)
    args = p.parse_args()

    chains_path = Path(args.chains_file)
    if not chains_path.exists():
        print(f"ERROR: {chains_path} not found.")
        sys.exit(1)

    chains = json.loads(chains_path.read_text())
    chain_results = []

    for chain in chains:
        name = chain["name"]
        prompt = chain["prompt"]
        expected = chain["expected_skills"]
        print(f"  Testing chain: {name} (expected: {' → '.join(expected)})...")

        run_scores = []
        for run_i in range(args.repeats):
            raw = call_claude_chain(prompt, args.max_turns)
            score = score_chain(raw["skills"], expected)
            run_scores.append({
                "run": run_i,
                "score": score,
                "turns": raw["turns"],
                "stop": raw["stop"],
            })
            print(f"    run {run_i+1}: {score['completed']}/{score['total']} "
                  f"skills hit | actual={raw['skills']} | stop={raw['stop']}")
            time.sleep(1)

        avg_rate = sum(r["score"]["rate"] for r in run_scores) / len(run_scores)
        passed = avg_rate >= args.threshold

        chain_results.append({
            "chain": name,
            "expected": expected,
            "avg_completion_rate": avg_rate,
            "passed": passed,
            "runs": run_scores,
        })
        status = "✅" if passed else "❌"
        print(f"    {status} {name}: {avg_rate:.0%} avg completion")

    overall_passed = all(r["passed"] for r in chain_results)
    out = {
        "phase": "P1",
        "threshold": args.threshold,
        "overall_passed": overall_passed,
        "chains": chain_results,
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(out, indent=2, ensure_ascii=False))

    status = "✅ PASS" if overall_passed else "❌ FAIL"
    print(f"\nP1 Chain Propagation: {status}")
    sys.exit(0 if overall_passed else 1)


if __name__ == "__main__":
    main()
