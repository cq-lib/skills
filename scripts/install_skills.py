#!/usr/bin/env python3
"""Install selected bundled skills to an explicit directory; no SDK/network work."""

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import sys
import tempfile
from uuid import uuid4


REPOSITORY = Path(__file__).resolve().parents[1]
SKILLS = ("cqlib", "cqlib-tianyan", "cqlib-pulse", "cqlib-qaoa", "cqlib-vqe")


def install(target, names, *, replace=False, dry_run=False, repository=REPOSITORY):
    """Preflight all destinations, stage copies, and retain backups on replacement."""
    target = Path(target).expanduser().resolve()
    repository = Path(repository).resolve()
    names = tuple(dict.fromkeys(names))
    if not names or any(name not in SKILLS for name in names):
        raise ValueError("Select at least one known skill")
    if target in (Path(target.anchor), Path.home().resolve(), repository):
        raise ValueError("Choose a dedicated skills directory, not a root/home/repository")
    if target.is_relative_to(repository / "skills"):
        raise ValueError("Destination cannot be inside the bundled source skills")
    destinations = {name: target / name for name in names}
    for name, destination in destinations.items():
        if not (repository / "skills" / name / "SKILL.md").is_file():
            raise ValueError(f"Missing source SKILL.md: {name}")
        if os.path.lexists(destination) and not replace:
            raise FileExistsError(f"Already exists: {destination}; use --replace to back it up")
    for name, destination in destinations.items():
        action = "back up and replace" if os.path.lexists(destination) else "install"
        print(f"{'Would ' if dry_run else 'Will '}{action}: {name} -> {destination}")
    if dry_run:
        return None

    target.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
    # Backups live outside the discovery directory, so old skills are not loaded.
    backup_root = target.parent / (target.name + "-backups") / stamp
    backed_up = []
    published = []
    with tempfile.TemporaryDirectory(prefix=".cqlib-install-", dir=target.parent) as temporary:
        stage = Path(temporary)
        for name in names:
            shutil.copytree(repository / "skills" / name, stage / name,
                            symlinks=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
        try:
            for name, destination in destinations.items():
                if os.path.lexists(destination):
                    if not replace:
                        raise FileExistsError(f"Destination appeared during install: {destination}")
                    backup_root.mkdir(parents=True, exist_ok=True)
                    destination.rename(backup_root / name)
                    backed_up.append(name)
                (stage / name).rename(destination)
                published.append(name)
        except BaseException:
            # Move only our newly published copies back to the owned staging area.
            for name in reversed(published):
                destinations[name].rename(stage / name)
            for name in reversed(backed_up):
                (backup_root / name).rename(destinations[name])
            raise
    if backed_up:
        print(f"Previous installations preserved at: {backup_root}")
    legacy = [name for name in ("cqlib-python", "cqlib-rust", "cqlib-c")
              if os.path.lexists(target / name)]
    if legacy:
        print("Legacy skills left unchanged: " + ", ".join(legacy)
              + ". Move them outside the discovery directory after reviewing the merged cqlib skill.")
    print(f"Installed {len(names)} skill(s). SDKs and agent configuration were not changed.")
    return backup_root if backed_up else None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, help="Agent's skills directory (required unless --list)")
    parser.add_argument("--skill", action="append", choices=SKILLS,
                        help="Install only this skill; repeat to select several (default: all five)")
    parser.add_argument("--list", action="store_true", help="List bundled skills without writing")
    parser.add_argument("--dry-run", action="store_true", help="Validate and preview without writing")
    parser.add_argument("--replace", action="store_true", help="Back up existing destinations before replacing")
    args = parser.parse_args(argv)
    if args.list:
        print("\n".join(SKILLS))
        return 0
    if args.target is None:
        parser.error("--target is required; no agent installation is selected implicitly")
    try:
        install(args.target, args.skill or SKILLS, replace=args.replace, dry_run=args.dry_run)
    except (OSError, ValueError) as error:
        print(f"Installation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
