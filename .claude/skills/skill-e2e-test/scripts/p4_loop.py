#!/usr/bin/env python3
"""P4: Loop / deadlock detection.

A loop is when the same skill appears twice in one session.
Deadlock is when stop=error_max_turns (session exhausted turn budget).
"""
import json, os, subprocess, sys, argparse, time
from pathlib import Path
from collections import Counter

TIMEOUT = 180


def call_claude_detect(prompt: str, max_turns: int) -> dict:
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


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--loop-file",
                   default=".claude/skills/skill-e2e-test/evals/loop_tests.json")
    p.add_argument("--output", default=".skill-test-results/p4.json")
    p.add_argument("--max-turns", type=int, default=20)
    args = p.parse_args()

    loop_path = Path(args.loop_file)
    if not loop_path.exists():
        print(f"ERROR: {loop_path} not found.")
        sys.exit(1)

    tests = json.loads(loop_path.read_text())
    test_results = []
    total_loops = 0

    for test in tests:
        name = test["name"]
        prompt = test["prompt"]
        print(f"  Loop test: {name}...")

        raw = call_claude_detect(prompt, args.max_turns)
        skills = raw["skills"]
        counts = Counter(skills)
        loops = {k: v for k, v in counts.items() if v > 1}
        deadlocked = raw["stop"] == "error_max_turns"

        issues = []
        if loops:
            issues.append(f"repeated skills: {loops}")
        if deadlocked:
            issues.append(f"hit max_turns={args.max_turns} (deadlock)")

        passed = not loops and not deadlocked
        total_loops += len(loops)

        result = {
            "test": name,
            "passed": passed,
            "skill_sequence": skills,
            "turns": raw["turns"],
            "stop": raw["stop"],
            "loops_detected": loops,
            "deadlocked": deadlocked,
            "issues": issues,
        }
        test_results.append(result)
        status = "✅" if passed else "❌"
        print(f"    {status} {name}: sequence={skills} stop={raw['stop']}")
        if issues:
            for issue in issues:
                print(f"       ⚠ {issue}")
        time.sleep(1)

    overall_passed = total_loops == 0 and all(r["passed"] for r in test_results)
    out = {
        "phase": "P4",
        "overall_passed": overall_passed,
        "total_loops_detected": total_loops,
        "tests": test_results,
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(out, indent=2, ensure_ascii=False))

    status = "✅ PASS" if overall_passed else "❌ FAIL"
    print(f"\nP4 Loop Detection: {total_loops} loops found {status}")
    sys.exit(0 if overall_passed else 1)


if __name__ == "__main__":
    main()
