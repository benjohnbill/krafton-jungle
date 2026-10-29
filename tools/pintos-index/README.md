# pintos-index

An exact code index of the Pintos kernel, built from libclang. It answers
"what to read": for a function, where it is called, what it calls (direct,
through function pointers, from asm), how its arguments change, and what it
returns, each with `file:line`. Readers are the user (HTML views) and the
Aside agent (Markdown cards). Design: `~/.claude/plans/pintos-clangd-index/FINAL.md`.

## Commands

```sh
cd ~/dev/krafton-jungle/tools/pintos-index
uv run pintos-index            # build week09/.code-index (about 3 s)
uv run pintos-index-verify     # gate: freshness, kernel set, diagnostics, clangd oracle, golden, run time
uv run pintos-index-mutate     # proof that verify fails when a fact disappears
```

`--pintos PATH` and `--out PATH` point at another tree. `verify --no-oracle`
skips clangd. The tool never writes inside the pintos tree; the output dir is
excluded in week09's `.git/info/exclude`.

## Output (`week09/.code-index/`)

| Path | For |
|---|---|
| `INDEX.md` | Symbol to card to `file:line`, grouped by file. Start here. |
| `symbols/<name>.md` | One card per function and function-like macro in the card scope (`views.toml` `[cards]`). A name used twice gets `<name>@<path-with-dashes>.md`. |
| `views/*.html` | Views from `views.toml`, re-rendered every run. Kinds: `flow` (call tree from a root) and `structs` (fields in declaration order, field types linked within the view, functions whose signature names the struct). |
| `index.json` | The fact store. Scripts only. |

## Data shape (`model.py`)

- `Symbol {usr, name, kind, file, line, signature, comment, ...}`, keyed by
  clang USR. Kinds: function, struct, typedef, macro, field. Functions also
  carry params (writes, member writes, calls that receive them) and return
  statements.
- `Edge {kind, src, dst | candidates[], ev, col, attrs}`. Kinds are a closed
  registry, `EDGE_KINDS`: calls, dispatches, asm_calls, registers, expands,
  includes, field_of, refs_type. Each entry says how it is extracted, whether
  flow views walk it, and which card section shows it.
- `refs`: every reference to a function, with its container. The clangd
  oracle compares against it.

Cards, `INDEX.md`, and views read only `index.json`.

## Rules worth knowing

- Kernel set = `vm/Make.vars` `KERNEL_SUBDIRS` plus each dir's `<dir>_SRC`,
  intersected with `compile_commands.json`. A missing file fails the build.
- One extra flag, `-Wno-error=int-conversion`, for `threads/mmu.c:189`
  (clang 16+ rejects what gcc accepts). Any other error diagnostic aborts.
- Indirect call candidates (`dispatch.py`): rule `a` field, `a'` global or
  array, `b` local or parameter traced to its stores, `+fwd` reached through
  parameter forwarding, `c` type-match fallback when a trace meets a value it
  cannot follow. The rule is printed next to every candidate.
- `asm_calls` come from regexes over kernel `.S` files and carry the label
  `asm (not clang)`.
- clangd's call hierarchy counts every reference inside a function as a call
  (a function passed as an argument included). The oracle therefore compares
  it with all contained references and reports how many of those are not
  calls.
- Compiler builtins (`__builtin_va_start`, ...) have no source declaration
  and are not indexed; the stamp lists them.

## Stamp

`index.json` `stamp`: week09 HEAD, dirty flag, sha256 of every file read,
kernel set with the Make lines it came from, libclang and clangd versions,
the extra flag, and build timing. Each card lists the hashes of the files it
cites. `verify` fails when any hash no longer matches.

## Rollback

Delete this directory and `week09/.code-index/`, then remove the
`/.code-index/` line from `week09/.git/info/exclude`.
