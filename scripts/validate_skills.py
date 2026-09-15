#!/usr/bin/env python3
"""Check local links/Python syntax; optionally execute allowlisted offline examples."""

import argparse
import ast
from pathlib import Path
import re
import runpy
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
CORE_EXAMPLES = ("quickstart", "circuits", "simulation", "compilation",
                 "mitigation", "visualization")
ASSET_EXAMPLES = ("cqlib-pulse/assets/pulse_timeline.py", "cqlib-qaoa/assets/maxcut.py",
                  "cqlib-vqe/assets/minimal_vqe.py")


def python_blocks(text):
    return re.findall(r"^```python\s*\n(.*?)^```\s*$", text, flags=re.M | re.S)


def check_static():
    markdown = [*sorted(ROOT.glob("README*.md")), ROOT / "SKILL.md",
                *sorted((ROOT / "skills").rglob("*.md"))]
    block_count = 0
    for path in markdown:
        text = path.read_text(encoding="utf-8")
        # Only actual inline Markdown links, not examples inside code fences.
        prose = re.sub(r"^```[^\n]*\n.*?^```\s*$", "", text, flags=re.M | re.S)
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", prose):
            parsed = urlsplit(link.strip("<>"))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(ROOT) or not destination.exists():
                raise ValueError(f"Missing or out-of-repository link in {path}: {link}")
        for index, block in enumerate(python_blocks(text), 1):
            ast.parse(block, filename=f"{path}:python-block-{index}")
            block_count += 1
    python_files = [*sorted((ROOT / "scripts").glob("*.py")),
                    *sorted((ROOT / "tests").glob("*.py")),
                    *sorted((ROOT / "skills").rglob("*.py"))]
    for path in python_files:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    print(f"Static checks passed: {len(markdown)} Markdown files, "
          f"{block_count} Python blocks, {len(python_files)} Python files")


def check_offline_examples():
    # Intentionally exclude cloud, chemistry and arbitrary shell/Rust/C snippets.
    for name in CORE_EXAMPLES:
        path = ROOT / "skills/cqlib/references/python" / (name + ".md")
        namespace = {"__name__": "__skill_example__"}
        for index, block in enumerate(python_blocks(path.read_text(encoding="utf-8")), 1):
            exec(compile(block, f"{path}:python-block-{index}", "exec"), namespace)
        print(f"PASS core/{name}")
    for relative in ASSET_EXAMPLES:
        runpy.run_path(str(ROOT / "skills" / relative), run_name="__main__")
        print(f"PASS {relative}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline-examples", action="store_true",
                        help="Also run local numerical examples; needs source-built SDKs and dependencies")
    args = parser.parse_args()
    check_static()
    if args.offline_examples:
        check_offline_examples()


if __name__ == "__main__":
    main()
