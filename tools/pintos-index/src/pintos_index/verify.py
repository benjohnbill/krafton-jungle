"""`pintos-index-verify`: the first-slice gate (FINAL § 4 items 1-3, 4, 6) over a built index."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import tomllib
from pathlib import Path

from clang import cindex as ci

from . import kernel_set, oracle
from .build import DEFAULT_PINTOS, TOOL_DIR, sha
from .extract import compile_args
from .graph import Graph
from .model import Index

RUN_TIME_TARGET_S = 10.0


class Golden:
    """One checker per golden fact kind. Each returns None on a match or a reason."""

    def __init__(self, idx: Index):
        self.idx = idx
        self.g = Graph(idx)

    def names(self, node: str | None) -> str:
        return self.g.name(node)

    def edges(self, kind: str):
        return [e for e in self.idx.edges if e.kind == kind]

    def registers(self, f: dict) -> str | None:
        hits = [e for e in self.edges("registers") if self.names(e.dst) == f["fn"] and e.ev == f["ev"]]
        if not hits:
            return "no registers edge"
        return None if any(e.attrs.get("into") == f["into"] for e in hits) else f"into {[e.attrs.get('into') for e in hits]}"

    def calls(self, f: dict) -> str | None:
        ok = any(self.names(e.src) == f["src"] and self.names(e.dst) == f["dst"] and e.ev == f["ev"] for e in self.edges("calls"))
        return None if ok else "no calls edge"

    def asm_calls(self, f: dict) -> str | None:
        ok = any(self.names(e.src) == f["src"] and self.names(e.dst) == f["dst"] and e.ev == f["ev"] for e in self.edges("asm_calls"))
        return None if ok else "no asm_calls edge"

    def includes(self, f: dict) -> str | None:
        ok = any(e.src == f"file:{f['src']}" and e.dst == f"file:{f['dst']}" and e.ev == f["ev"] for e in self.edges("includes"))
        return None if ok else "no includes edge"

    def dispatches(self, f: dict) -> str | None:
        hits = [e for e in self.edges("dispatches") if self.names(e.src) == f["src"] and e.ev == f["ev"]]
        if not hits:
            return "no dispatch site"
        e = hits[0]
        for key in ("via", "via_macro"):
            if key in f and e.attrs.get(key) != f[key]:
                return f"{key} = {e.attrs.get(key)!r}"
        if "rule" in f and e.attrs.get("rule") != f["rule"]:
            return f"rule = {e.attrs.get('rule')!r}"
        have = {(self.names(c.usr), c.ev) for c in e.candidates}
        missing = [c for c in f.get("candidates", []) if (c["fn"], c["ev"]) not in have]
        return f"candidates missing {missing}" if missing else None

    def fields(self, f: dict) -> str | None:
        structs = [s for s in self.idx.symbols.values() if s.kind == "struct" and s.name == f["struct"]]
        s = next((s for s in structs if f"{s.file}:{s.line}" == f["at"]), None)
        if s is None:
            return f"no struct at {f['at']}"
        got = [self.names(e.src) for e in sorted(self.edges("field_of"), key=lambda e: (e.ev.rsplit(":", 1)[0], int(e.ev.rsplit(":", 1)[1]), e.col)) if e.dst == s.usr]
        return None if got == f["fields"] else f"fields {got}"

    def check(self, f: dict) -> str | None:
        return getattr(self, f["kind"])(f)


def describe(f: dict) -> str:
    return " ".join(f"{k}={v}" for k, v in f.items() if k != "candidates") + (f" candidates={[c['fn'] for c in f['candidates']]}" if "candidates" in f else "")


def parse_errors(root: Path, ks: kernel_set.KernelSet) -> list[str]:
    index = ci.Index.create()
    errs = []
    cwd = os.getcwd()
    for f in ks.c_files:
        e = ks.db[f]
        os.chdir(e["directory"])
        tu = index.parse(e["file"], args=compile_args(e))
        errs += [f"{d.location.file}:{d.location.line}: {d.spelling}" for d in tu.diagnostics if d.severity >= ci.Diagnostic.Error]
    os.chdir(cwd)
    return errs


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pintos", type=Path, default=DEFAULT_PINTOS)
    ap.add_argument("--out", type=Path, help="index dir (default: <pintos>/../.code-index)")
    ap.add_argument("--golden", type=Path, default=TOOL_DIR / "golden.toml")
    ap.add_argument("--no-oracle", action="store_true", help="skip the clangd comparison")
    ap.add_argument("--report", type=Path, help="write the full result as JSON here")
    a = ap.parse_args(argv)
    root = a.pintos.resolve()
    out = (a.out or root.parent / ".code-index").resolve()
    idx = Index.load(out / "index.json")
    golden = tomllib.loads(a.golden.read_text())
    results: dict[str, dict] = {}

    stale = [f for f, h in idx.stamp["file_hashes"].items() if not (root / f).is_file() or sha(root / f) != h]
    results["fresh"] = {"ok": not stale, "detail": f"{len(stale)} files changed since the build: {stale[:5]}" if stale else "every cited file hash matches"}

    ks = kernel_set.load(root)
    n = len(ks.c_files)
    ok = n == golden["kernel_tus"] and ks.c_files == idx.stamp["kernel_set"]["c"]
    results["1 kernel set"] = {"ok": ok, "detail": f"{n} TUs from the build rule, golden {golden['kernel_tus']}, index {len(idx.stamp['kernel_set']['c'])}"}

    errs = parse_errors(root, ks)
    results["2 diagnostics"] = {"ok": not errs, "detail": f"{len(errs)} error diagnostics with {idx.stamp['extra_flag']}" + (f": {errs[:5]}" if errs else "")}

    if a.no_oracle:
        results["3 oracle"] = {"ok": True, "detail": "skipped (--no-oracle)"}
    else:
        t = time.perf_counter()
        r = oracle.compare(idx, root)
        mm = r["mismatches"]
        results["3 oracle"] = {
            "ok": not mm,
            "detail": f"{r['checked']}, {len(mm)} mismatches, {time.perf_counter() - t:.1f}s",
            "mismatches": mm[:50],
        }

    g = Golden(idx)
    failed = [(describe(f), why) for f in golden["fact"] if (why := g.check(f)) is not None]
    results["4 golden"] = {
        "ok": not failed,
        "detail": f"{len(golden['fact']) - len(failed)}/{len(golden['fact'])} facts" + "".join(f"\n      MISS {d}: {w}" for d, w in failed),
        "failed": [d for d, _ in failed],
    }

    total = idx.stamp.get("timing_s", {}).get("total")
    results["6 run time"] = {"ok": total is not None and total < RUN_TIME_TARGET_S, "detail": f"build {idx.stamp.get('timing_s')} s, target < {RUN_TIME_TARGET_S} s"}

    for name, r in results.items():
        print(f"{'PASS' if r['ok'] else 'FAIL'}  {name}: {r['detail']}")
    if a.report:
        a.report.write_text(json.dumps(results, indent=1, default=str))
    sys.exit(0 if all(r["ok"] for r in results.values()) else 1)


if __name__ == "__main__":
    main()
