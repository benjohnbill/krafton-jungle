"""`pintos-index`: kernel set -> libclang facts -> index.json -> cards, INDEX.md, views."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import time
from pathlib import Path

from clang import cindex as ci

from . import asm, cards, clangloc, dispatch, kernel_set, views
from .extract import EXTRA_FLAG, Walker
from .model import Edge, Index

DEFAULT_PINTOS = Path.home() / "dev/krafton-jungle/week09/pintos"
TOOL_DIR = Path(__file__).resolve().parents[2]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True).stdout.strip()


def clangd_version() -> str | None:
    try:
        out = subprocess.run(["clangd", "--version"], capture_output=True, text=True).stdout
    except FileNotFoundError:
        return None
    return out.splitlines()[0] if out else None


def extract(root: Path) -> Index:
    ks = kernel_set.load(root)
    walker = Walker(root)
    index = ci.Index.create()
    for f in ks.c_files:
        walker.parse(index, ks.db[f])
    facts = walker.facts
    if facts.errors:
        raise SystemExit("error diagnostics in the kernel set:\n  " + "\n  ".join(sorted(set(facts.errors))))

    expands = []
    for (f, off), (macro, line, col) in sorted(facts.instantiations.items()):
        fn = next((u for s, e, u in facts.fn_extents.get(f, []) if s <= off < e), None)
        if fn and macro in facts.macros:
            expands.append(("expands", fn, f"{f}:{line}", macro, col))
    used = {m for *_, m, _ in expands}
    symbols = {**facts.symbols, **{u: s for u, s in facts.macros.items() if u in used}}


    # Compiler builtins (__builtin_va_start, ...) are declared implicitly at
    # their first use, never by a source declaration, so they have no symbol.
    implicit = sorted({r["usr"] for r in facts.refs if r["usr"] not in symbols})
    facts.refs = [r for r in facts.refs if r["usr"] in symbols]
    facts.edges = [e for e in facts.edges if not (e.kind == "calls" and e.dst not in symbols)]
    for usr, refs in facts.decl_type_refs.items():
        if not facts.symbols[usr].defined:
            facts.edges += refs
    edges = facts.edges + dispatch.resolve(facts)
    edges += [Edge(k, s, ev, d, col=c) for k, s, ev, d, c in expands]
    edges += asm.extract(root, ks.asm_files, symbols)
    edges.sort(key=lambda e: (e.kind, e.ev, e.col, e.src, e.dst or ""))

    files_read = sorted(facts.files_read | set(ks.asm_files) | {l.split(":", 1)[0] for l in ks.make_lines if ":" in l} | {"compile_commands.json"})
    files_read = [f for f in files_read if (root / f).is_file()]
    repo = Path(git(root, "rev-parse", "--show-toplevel") or root)
    stamp: dict = {
        "root": str(root),
        "head": git(root, "rev-parse", "HEAD"),
        "dirty": bool(git(root, "status", "--porcelain", "--untracked-files=no")),
        "repo": str(repo),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "kernel_set": {"c": ks.c_files, "asm": ks.asm_files, "make_lines": ks.make_lines},
        "extra_flag": EXTRA_FLAG,
        "libclang": clangloc.clang_version(),
        "clangd": clangd_version(),
        "error_diagnostics": [],
        "implicit_callees_not_indexed": implicit,
        "file_hashes": {f: sha(root / f) for f in files_read},
    }
    return Index(stamp, symbols, edges, sorted(facts.refs, key=lambda r: (r["at"], r["usr"])))


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pintos", type=Path, default=DEFAULT_PINTOS, help="pintos source root")
    ap.add_argument("--out", type=Path, help="output dir (default: <pintos>/../.code-index)")
    ap.add_argument("--views", type=Path, default=TOOL_DIR / "views.toml")
    a = ap.parse_args(argv)
    root = a.pintos.resolve()
    out = (a.out or root.parent / ".code-index").resolve()

    t0 = time.perf_counter()
    idx = extract(root)
    t1 = time.perf_counter()
    staging = out.with_name(out.name + ".tmp")
    shutil.rmtree(staging, ignore_errors=True)
    staging.mkdir(parents=True)
    idx.save(staging / "index.json")
    n_views = views.render(idx, staging, a.views)
    n_cards = cards.render(idx, staging, a.views)
    t2 = time.perf_counter()
    idx.stamp["timing_s"] = {"extract": round(t1 - t0, 2), "render": round(t2 - t1, 2), "total": round(t2 - t0, 2)}
    idx.save(staging / "index.json")
    shutil.rmtree(out, ignore_errors=True)
    staging.rename(out)
    by_kind: dict[str, int] = {}
    for e in idx.edges:
        by_kind[e.kind] = by_kind.get(e.kind, 0) + 1
    print(
        f"pintos-index: {len(idx.stamp['kernel_set']['c'])} TUs, {len(idx.symbols)} symbols, "
        f"edges {by_kind}, {n_cards} cards, {n_views} views -> {out} in {t2 - t0:.2f}s",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
