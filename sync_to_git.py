#!/usr/bin/env python3
"""
Sync Thai IPA cache to git repo and push to GitHub.

This script is run by cron. It:
1. Copies the current lookup files from /opt/data/scripts/
2. Commits if changed
3. Pushes to GitHub
"""

import subprocess
import shutil
import sys
from pathlib import Path
from datetime import datetime, timezone

REPO_DIR = Path("/opt/data/thai-ipa-cache")
SOURCE_DIR = Path("/opt/data/scripts")

FILES = [
    "thai_ipa_lookup.json",
    "thai_ipa_lookup.csv",
]


def run(cmd: list[str], cwd: Path = REPO_DIR) -> tuple[int, str, str]:
    """Run a command, return (exit_code, stdout, stderr)."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def main():
    changed = False

    # Copy files from source
    for fname in FILES:
        src = SOURCE_DIR / fname
        dst = REPO_DIR / fname
        if src.exists():
            old_hash = None
            if dst.exists():
                old_hash = dst.read_bytes()
            new_data = src.read_bytes()
            if old_hash != new_data:
                dst.write_bytes(new_data)
                changed = True
                print(f"  Updated: {fname}")

    if not changed:
        print("No changes.")
        return

    # Stage and commit
    run(["git", "add"] + FILES)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    run(["git", "commit", "-m", f"Update IPA cache — {ts}"])

    # Push
    code, out, err = run(["git", "push", "origin", "master"])
    if code != 0:
        print(f"Push failed: {err}", file=sys.stderr)
        sys.exit(1)
    print(f"Push OK: {out}")


if __name__ == "__main__":
    main()
