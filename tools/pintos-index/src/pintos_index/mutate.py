"""`pintos-index-mutate`: proof that verify fails when a fact disappears (FINAL § 4 item 5).

Each source mutation runs on a scratch copy of pintos outside the repo:
copy, delete one line, build, verify. A mutation passes when verify exits
non-zero and names the golden fact the deleted line carried. One more case
deletes a single reference from a correct index.json and expects the clangd
oracle, not the golden fixture, to catch it.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from .build import DEFAULT_PINTOS

SCRATCH = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "pintos-index/mutation"

MUTATIONS = [
    {
        "name": "drop-swap_in-registration",
        "file": "vm/anon.c",
        "line": "    .swap_in = anon_swap_in,",
        "expect": "kind=registers fn=anon_swap_in",
    },
    {
        "name": "drop-direct-call",
        "file": "userprog/exception.c",
        "line": '    intr_register_int(14, 0, INTR_OFF, page_fault, "#PF Page-Fault Exception");',
        "expect": "kind=calls src=exception_init dst=intr_register_int",
    },
]


def copy_tree(src: Path, dst: Path) -> None:
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".cache", "graphify-out", "*.o", "build"), symlinks=True)
    db = json.loads((dst / "compile_commands.json").read_text())
    for e in db:
        e["directory"] = e["directory"].replace(str(src), str(dst))
    (dst / "compile_commands.json").write_text(json.dumps(db))


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pintos", type=Path, default=DEFAULT_PINTOS)
    a = ap.parse_args(argv)
    src = a.pintos.resolve()
    exe = Path(sys.executable).parent
    ok_all = True
    for m in MUTATIONS:
        work = SCRATCH / m["name"]
        root = work / "pintos"
        copy_tree(src, root)
        path = root / m["file"]
        lines = path.read_text().splitlines(keepends=True)
        hits = [i for i, l in enumerate(lines) if l.rstrip("\n") == m["line"]]
        if len(hits) != 1:
            print(f"FAIL  {m['name']}: line to delete found {len(hits)} times in {m['file']}")
            ok_all = False
            continue
        del lines[hits[0]]
        path.write_text("".join(lines))
        out = work / ".code-index"
        b = run([str(exe / "pintos-index"), "--pintos", str(root), "--out", str(out)])
        v = run([str(exe / "pintos-index-verify"), "--pintos", str(root), "--out", str(out)]) if b.returncode == 0 else b
        caught = v.returncode != 0 and m["expect"] in v.stdout
        ok_all &= caught
        print(f"{'PASS' if caught else 'FAIL'}  {m['name']}: deleted {m['file']}:{hits[0] + 1}, "
              f"build exit {b.returncode}, verify exit {v.returncode}, golden miss reported: {m['expect'] in v.stdout}")
        for line in v.stdout.splitlines():
            if line.startswith("FAIL") or "MISS" in line:
                print(f"      {line.strip()}")

    work = SCRATCH / "drop-one-reference"
    out = work / ".code-index"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    b = run([str(exe / "pintos-index"), "--pintos", str(src), "--out", str(out)])
    idx = json.loads((out / "index.json").read_text())
    victim = next(r for r in idx["refs"] if r["ctx"] == "call" and r["at"].startswith("vm/"))
    idx["refs"].remove(victim)
    (out / "index.json").write_text(json.dumps(idx))
    v = run([str(exe / "pintos-index-verify"), "--pintos", str(src), "--out", str(out)])
    oracle_line = next((l for l in v.stdout.splitlines() if "3 oracle" in l), "")
    caught = b.returncode == 0 and v.returncode != 0 and oracle_line.startswith("FAIL")
    ok_all &= caught
    print(f"{'PASS' if caught else 'FAIL'}  drop-one-reference: removed ref at {victim['at']} from index.json, "
          f"verify exit {v.returncode}; {oracle_line.strip()[:160]}")
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
