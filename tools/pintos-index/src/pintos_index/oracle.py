"""Full comparison of the libclang walker against clangd (FINAL C1, C16).

For every defined kernel function, clangd answers incoming calls, outgoing
calls, and references. Each answer is compared, as a set of source
positions, with what index.json says. clangd reads a filtered
compile_commands.json (the kernel set plus the one extra flag) in a scratch
dir outside the repo.
"""

from __future__ import annotations

import json
import os
import queue
import re
import shutil
import subprocess
import threading
from pathlib import Path
from urllib.parse import unquote, urlparse

from .extract import compile_args
from .model import Index

SCRATCH = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "pintos-index/oracle"


class Lsp:
    def __init__(self, cmd: list[str]):
        self.p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.next_id = 0
        self.waiting: dict[int, queue.Queue] = {}
        self.indexed = threading.Event()
        threading.Thread(target=self._read, daemon=True).start()

    def _send(self, msg: dict) -> None:
        body = json.dumps(msg).encode()
        self.p.stdin.write(b"Content-Length: %d\r\n\r\n" % len(body) + body)
        self.p.stdin.flush()

    def _read(self) -> None:
        out = self.p.stdout
        while True:
            length = 0
            while (line := out.readline()) not in (b"\r\n", b""):
                if line.lower().startswith(b"content-length:"):
                    length = int(line.split(b":")[1])
            if not line:
                return
            msg = json.loads(out.read(length))
            if "id" in msg and "method" in msg:
                self._send({"jsonrpc": "2.0", "id": msg["id"], "result": None})
            elif "id" in msg:
                self.waiting.pop(msg["id"]).put(msg)
            elif msg.get("method") == "$/progress":
                p = msg["params"]
                if p.get("token") == "backgroundIndexProgress" and p["value"].get("kind") == "end":
                    self.indexed.set()

    def request(self, method: str, params: dict, timeout: float = 120):
        self.next_id += 1
        q: queue.Queue = queue.Queue()
        self.waiting[self.next_id] = q
        self._send({"jsonrpc": "2.0", "id": self.next_id, "method": method, "params": params})
        msg = q.get(timeout=timeout)
        if "error" in msg:
            raise RuntimeError(f"{method}: {msg['error']}")
        return msg["result"]

    def notify(self, method: str, params: dict) -> None:
        self._send({"jsonrpc": "2.0", "method": method, "params": params})

    def close(self) -> None:
        try:
            self.request("shutdown", {}, timeout=10)
            self.notify("exit", {})
        finally:
            self.p.kill()


def filtered_db(idx: Index, root: Path, scratch: Path) -> None:
    db = json.loads((root / "compile_commands.json").read_text())
    keep = set(idx.stamp["kernel_set"]["c"])
    out = []
    for e in db:
        rel = str((Path(e["directory"]) / e["file"]).resolve().relative_to(root))
        if rel in keep:
            out.append({"directory": e["directory"], "file": e["file"], "arguments": [e["arguments"][0], *compile_args(e), e["file"]]})
    shutil.rmtree(scratch, ignore_errors=True)
    scratch.mkdir(parents=True)
    (scratch / "compile_commands.json").write_text(json.dumps(out, indent=1))


def compare(idx: Index, root: Path, scratch: Path = SCRATCH) -> dict:
    """Returns {"checked": {...counts}, "mismatches": [...]} ; empty mismatches = pass."""
    root = root.resolve()
    filtered_db(idx, root, scratch)
    lsp = Lsp(["clangd", f"--compile-commands-dir={scratch}", "--background-index", "-j=8", "--log=error", "--pch-storage=memory"])
    uri = lambda f: (root / f).as_uri()
    lsp.request("initialize", {
        "processId": os.getpid(),
        "rootUri": root.as_uri(),
        "capabilities": {
            "window": {"workDoneProgress": True},
            "general": {"positionEncodings": ["utf-8"]},
            "textDocument": {"callHierarchy": {}, "references": {}},
        },
    })
    lsp.notify("initialized", {})
    for f in idx.stamp["kernel_set"]["c"][:1]:
        lsp.notify("textDocument/didOpen", {"textDocument": {"uri": uri(f), "languageId": "c", "version": 1, "text": (root / f).read_text()}})
    if not lsp.indexed.wait(600):
        lsp.close()
        raise RuntimeError("clangd background index did not finish in 600 s")

    def rel(u: str) -> str:
        return os.path.relpath(unquote(urlparse(u).path), root)

    def pos(r: dict) -> tuple[str, int, int]:
        return (r[0], r[1]["start"]["line"] + 1, r[1]["start"]["character"] + 1)

    syms = idx.symbols
    fns = sorted((s for s in syms.values() if s.kind == "function" and s.defined), key=lambda s: (s.file, s.line))
    mismatches: list[dict] = []
    checked = {"functions": 0, "incoming": 0, "outgoing": 0, "references": 0}
    opened: set[str] = set()
    # clangd builds its call hierarchy from every reference contained in a
    # function body, so a function passed as an argument counts as a "call"
    # there. The walker side is therefore all contained references; the
    # count of those that are not calls is reported, not dropped. A reference
    # in a global initializer has that variable as its container.
    contained = [r for r in idx.refs if r["in"] is not None or r["in_var"] is not None]
    checked_noncall = sum(1 for r in contained if r["ctx"] != "call")
    for s in fns:
        if s.file not in opened:
            lsp.notify("textDocument/didOpen", {"textDocument": {"uri": uri(s.file), "languageId": "c", "version": 1, "text": (root / s.file).read_text()}})
            opened.add(s.file)
        line_text = (root / s.file).read_bytes().splitlines()[s.line - 1].decode(errors="replace")
        m = re.search(rf"\b{re.escape(s.name)}\s*\(", line_text)
        if not m:
            mismatches.append({"fn": s.name, "kind": "locate", "detail": f"name not found at {s.file}:{s.line}"})
            continue
        col = len(line_text[: m.start()].encode())
        tdp = {"textDocument": {"uri": uri(s.file)}, "position": {"line": s.line - 1, "character": col}}
        items = lsp.request("textDocument/prepareCallHierarchy", tdp) or []
        if not items:
            mismatches.append({"fn": s.name, "kind": "locate", "detail": "clangd has no call hierarchy item"})
            continue
        item = items[0]
        checked["functions"] += 1

        got_in = {
            (c["from"]["name"], *pos((rel(c["from"]["uri"]), r)))
            for c in lsp.request("callHierarchy/incomingCalls", {"item": item}) or []
            for r in c["fromRanges"]
        }
        want_in = {(syms[r["in"]].name if r["in"] else r["in_var"], *_split(r["at"])) for r in contained if r["usr"] == s.usr}
        got_out = {
            (c["to"]["name"], *pos((s.file, r)))
            for c in lsp.request("callHierarchy/outgoingCalls", {"item": item}) or []
            for r in c["fromRanges"]
        }
        want_out = {(syms[r["usr"]].name, *_split(r["at"])) for r in contained if r["in"] == s.usr}
        got_ref = {
            pos((rel(r["uri"]), r["range"]))
            for r in lsp.request("textDocument/references", {**tdp, "context": {"includeDeclaration": False}}) or []
        }
        want_ref = {_split(r["at"]) for r in idx.refs if r["usr"] == s.usr}
        for kind, got, want in (("incoming", got_in, want_in), ("outgoing", got_out, want_out), ("references", got_ref, want_ref)):
            checked[kind] += len(want)
            for x in sorted(want - got):
                mismatches.append({"fn": s.name, "kind": kind, "side": "walker only", "at": x})
            for x in sorted(got - want):
                mismatches.append({"fn": s.name, "kind": kind, "side": "clangd only", "at": x})
    lsp.close()
    checked["hierarchy_entries_that_are_not_calls"] = checked_noncall
    checked["calls_edges"] = sum(1 for e in idx.edges if e.kind == "calls")
    return {"checked": checked, "mismatches": mismatches}


def _split(at: str) -> tuple[str, int, int]:
    f, line, col = at.rsplit(":", 2)
    return (f, int(line), int(col))
