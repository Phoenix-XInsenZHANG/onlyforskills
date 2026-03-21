#!/usr/bin/env python3
"""P0: Structure validation — zero cost, runs first."""
import re, sys, json, argparse
from pathlib import Path

ALLOWED_KEYS = {"name", "description", "license", "allowed-tools",
                "metadata", "compatibility", "user-invocable", "hooks"}
NAME_RE = re.compile(r"^[a-z0-9-]+$")

def validate(skill_dir: Path) -> list[str]:
    errors = []
    md = skill_dir / "SKILL.md"
    if not md.exists():
        return [f"SKILL.md missing"]
    content = md.read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return ["No YAML frontmatter"]
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return ["Malformed frontmatter delimiters"]
    try:
        import yaml
        fm = yaml.safe_load(m.group(1))
    except Exception as e:
        return [f"YAML parse error: {e}"]
    if not isinstance(fm, dict):
        return ["Frontmatter not a mapping"]
    extra = set(fm.keys()) - ALLOWED_KEYS
    if extra:
        errors.append(f"Unexpected keys: {extra}")
    name = fm.get("name")
    if not name:
        errors.append("Missing 'name'")
    elif not isinstance(name, str):
        errors.append("'name' must be string")
    else:
        name = name.strip()
        if not NAME_RE.match(name):
            errors.append(f"'name' not kebab-case: {name!r}")
        if name.startswith("-") or name.endswith("-") or "--" in name:
            errors.append(f"'name' invalid hyphens: {name!r}")
        if len(name) > 64:
            errors.append(f"'name' too long ({len(name)} chars)")
    desc = fm.get("description")
    if not desc:
        errors.append("Missing 'description'")
    elif not isinstance(desc, str):
        errors.append("'description' must be string")
    else:
        if "<" in desc or ">" in desc:
            errors.append("'description' contains < or >")
        if len(desc) > 1024:
            errors.append(f"'description' too long ({len(desc)} chars)")
    return errors

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--skills-dir", default=".claude/skills")
    p.add_argument("--output", default=".skill-test-results/p0.json")
    args = p.parse_args()

    skills_dir = Path(args.skills_dir)
    results = {}
    for d in sorted(skills_dir.iterdir()):
        if d.is_dir():
            errs = validate(d)
            results[d.name] = {"errors": errs, "passed": len(errs) == 0}

    total = len(results)
    passed = sum(1 for v in results.values() if v["passed"])
    overall = passed == total

    out = {
        "phase": "P0",
        "total": total, "passed": passed, "failed": total - passed,
        "score": f"{passed}/{total}",
        "overall_passed": overall,
        "threshold": "100%",
        "cost_usd": 0.0,
        "skills": results
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(out, indent=2, ensure_ascii=False))

    # Print summary
    print(f"P0 Validation: {passed}/{total} passed", "✅" if overall else "❌")
    for name, r in results.items():
        if not r["passed"]:
            for e in r["errors"]:
                print(f"  ✗ {name}: {e}")
    sys.exit(0 if overall else 1)

if __name__ == "__main__":
    main()
