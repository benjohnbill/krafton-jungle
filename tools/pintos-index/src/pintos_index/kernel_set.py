"""Kernel translation units by the build rule (FINAL C13).

The set is `KERNEL_SUBDIRS` from `vm/Make.vars` and each dir's `<dir>_SRC`
lines, which live in `<dir>/targets.mk` or, for test dirs, `<dir>/Make.tests`.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class KernelSet:
    c_files: list[str]
    asm_files: list[str]
    make_lines: list[str]
    db: dict[str, dict]


class KernelSetError(Exception):
    pass


def _assignments(path: Path, var: str) -> list[tuple[int, str, list[str]]]:
    out = []
    pat = re.compile(rf"^{re.escape(var)}\s*\+?=\s*(.*)$")
    for n, raw in enumerate(path.read_text().splitlines(), 1):
        m = pat.match(raw.split("#", 1)[0].rstrip())
        if m:
            out.append((n, raw.rstrip(), m.group(1).split()))
    return out


def load(root: Path) -> KernelSet:
    make_vars = root / "vm/Make.vars"
    make_lines = []
    subdirs: list[str] = []
    for n, raw, words in _assignments(make_vars, "KERNEL_SUBDIRS"):
        make_lines.append(f"vm/Make.vars:{n}: {raw}")
        subdirs += words
    if not subdirs:
        raise KernelSetError("vm/Make.vars has no KERNEL_SUBDIRS")

    sources: list[str] = []
    for d in subdirs:
        found = False
        for mk in (root / d / "targets.mk", root / d / "Make.tests"):
            if not mk.exists():
                continue
            for n, raw, words in _assignments(mk, f"{d}_SRC"):
                found = True
                make_lines.append(f"{mk.relative_to(root)}:{n}: {raw}")
                sources += words
        if not found:
            make_lines.append(f"{d}: no {d}_SRC")

    db_raw = json.loads((root / "compile_commands.json").read_text())
    db = {}
    for e in db_raw:
        rel = str((Path(e["directory"]) / e["file"]).resolve().relative_to(root.resolve()))
        db[rel] = e

    c_files = [s for s in sources if s.endswith(".c")]
    asm_files = [s for s in sources if s.endswith(".S")]
    missing = [s for s in c_files if s not in db]
    if missing:
        raise KernelSetError(f"kernel .c files missing from compile_commands.json: {missing}")
    missing_asm = [s for s in asm_files if not (root / s).exists()]
    if missing_asm:
        raise KernelSetError(f"kernel .S files missing on disk: {missing_asm}")
    return KernelSet(c_files, asm_files, make_lines, {f: db[f] for f in c_files})
