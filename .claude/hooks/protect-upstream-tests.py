#!/usr/bin/env python3
"""PreToolUse hook: block agent edits to upstream Pintos tests.

Obligation: an agent does not change a test that came with the week's
baseline. Protected = a file under pintos/tests/ that exists in the repo's
root commit. New test files are allowed. Make.tests is allowed, because a new
test must be registered there.
Blind spots: shell edits (sed -i, >), and human edits. jungle-close checks
`git diff --stat <root> -- pintos/tests` for both.
Decided 2026-10-31 (docs/dialectic/2026-10-31-rules-barriers/JUDGMENT.md).
"""
import json
import os
import subprocess
import sys

EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}


def git(cwd, *args):
    return subprocess.run(["git", "-C", cwd, *args],
                          capture_output=True, text=True)


def main():
    event = json.load(sys.stdin)
    if event.get("tool_name") not in EDIT_TOOLS:
        return 0
    inp = event.get("tool_input", {})
    path = inp.get("file_path") or inp.get("notebook_path")
    if not path:
        return 0
    path = os.path.realpath(os.path.join(event.get("cwd", "."), path))

    # A new file's directory may not exist yet: ask git from its nearest parent.
    probe = os.path.dirname(path)
    while probe != "/" and not os.path.isdir(probe):
        probe = os.path.dirname(probe)
    top = git(probe, "rev-parse", "--show-toplevel")
    if top.returncode != 0:
        return 0
    rel = os.path.relpath(path, top.stdout.strip())
    if not rel.startswith("pintos/tests/") or os.path.basename(rel) == "Make.tests":
        return 0

    roots = git(probe, "rev-list", "--max-parents=0", "HEAD").stdout.split()
    for root in roots:
        if git(probe, "cat-file", "-e", f"{root}:{rel}").returncode == 0:
            print(f"Blocked: {rel} is an upstream test (in root commit "
                  f"{root[:7]}). Do not edit it. Add a new test file instead, "
                  f"and register it in Make.tests.", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
