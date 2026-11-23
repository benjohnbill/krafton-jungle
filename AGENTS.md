---
scope: This workspace and its descendants during Krafton Jungle
role: Entry point for every agent CLI (Claude Code reads it through the CLAUDE.md shim); routes to shared and repository-specific instructions
truth: Referenced policies define behavior; source and build files define current implementation
updated: 2026-11-24
---

# Krafton Jungle workspace

This is the user's main workbench during Krafton Jungle. Most `weekNN/`
directories here are their own git repository: one week of Krafton Jungle.
This directory is a repository too, and holds what is the same across weeks:
the tutor spine, the local skills under `skills/`, and the issue scripts. It
also holds a blog and learning experiments.

## Load the relevant instructions

Paths in this file are relative to this workspace root unless stated otherwise.
Read each source once per session, then reread it only if it changes or the task
changes scope.

@docs/tutor-spine.md

1. Read [docs/tutor-spine.md](docs/tutor-spine.md). Claude Code loads it
   through the import line above. Other agents must open it explicitly:
   `@` imports do not run in Codex.
2. Before work in a child directory, read its applicable `AGENTS.md` (or its
   `CLAUDE.md` if it has no `AGENTS.md`) and task-relevant `.claude/rules/`
   files. Read from the workspace toward the target. Local instructions refine
   the shared policy. A week's `Mode:` declaration controls whether that week
   uses tutor or project mode.
3. Codex follows the global OS in `~/.codex/AGENTS.md`; Claude Code loads
   `~/.claude/CLAUDE.md` itself. Read the relevant `~/.claude/rules/` when
   their topic applies. Before writing documents, read
   `~/.claude/docs/document-language.md`.

Current user instructions take precedence over project policy. More specific
project instructions take precedence over shared defaults. Keep common rules
in their source files; this file is a router, not a second tutor manual.
Treat undated documents as snapshots. Confirm paths, tools, targets, and
environment claims in the actual repository before using them.

## Choose the working mode

Inside `week*/`, use the tutor spine and that week's `AGENTS.md`. Classify the
request before acting: exercise guidance, concept exploration, or a direct
language/tool question. Preserve the learner's work and spoiler boundaries.
Tool setup and language facts get direct answers. Explicit user direction and
the week's declared mode take precedence over the default tutoring behavior.

Outside the week repositories (the blog, the scripts), perform the requested
work normally. The spine's user signals and session routines still apply. Do
not impose the exercise question loop on scripts, blog work, or workspace
maintenance.

Use Korean 해요체 and address the user as 오라버니 in conversation. Keep code,
commits, and documents in a neutral professional voice for their reader.

## Respect repository boundaries

The nested repositories are git submodules; `.gitmodules` lists them.
`function_visualizer/` and `issue-template/` are course repositories this
account can only read; the root `.gitignore` excludes them. `week11-12/` and
`week13/` are plain root directories that hold submodules. Inspect new
directories rather than assuming ownership.

- Before edits or Git operations, resolve the target with
  `git -C <directory> rev-parse --show-toplevel` and inspect its status.
- Run builds and Git commands in the owning repository. A root commit records
  only a submodule's pointer, not its content: commit and push in the child
  first, then `git add <path>` in the root to move the pointer.
- Preserve existing changes and untracked learner files. Stage only the paths
  for the requested task; do not combine repositories into one commit.
- Read the week's fixed-scaffolding and upstream restrictions before edits.
  Put requested probe programs in its `lab/` or designated scratch directory.
- Each independent child repository keeps its instructions in its own
  `AGENTS.md`, with a `CLAUDE.md` shim that is an exact copy of
  `~/dev/study/CLAUDE.md`. Add both when setting up a new repository here.
- Before touching the study site (`benjohnbill.github.io/`), read its
  `AGENTS.md`, section "Site rules": page paths, copies of originals, card
  attributes, week headings.

## Use the existing workflows

Read the matching local skill before executing its workflow, even if it is not
listed in the agent's installed skill catalog:

| Request | Source |
| --- | --- |
| Close the day, commit/push, update progress or the board | [skills/jungle-close/SKILL.md](skills/jungle-close/SKILL.md) |
| Set up a new week | [skills/jungle-week-init/SKILL.md](skills/jungle-week-init/SKILL.md) |
| Team week: verify a PR or a broken base branch before the user merges | [skills/jungle-team-merge/SKILL.md](skills/jungle-team-merge/SKILL.md) |
| Build, resume, or publish the weekly 2-minute 발표 slides | [skills/jungle-deck/SKILL.md](skills/jungle-deck/SKILL.md) |

The skills define the steps and completion criteria. Respect the scope the
user requested. Do not treat workspace initialization as a request to run
any workflow or publish changes.

Before you create or change a week's GitHub Project board, read
[docs/gh-project-setup.md](docs/gh-project-setup.md).

Agents other than Claude Code do not have Claude memory loaded. For week
re-entry or close, locate the memory directory using `jungle-close` step 0.
Read `MEMORY.md` and `progress.md` if present. Missing memory is not evidence
of completed work. Use the existing progress memo rather than creating a
competing copy. File permissions and the active sandbox still govern access to
that location.

## Verify in the owning project

There is no workspace-wide build or test command. Read the target repository's
README, build files, and `Verify:` declaration. Run checks for the changed
paths. A planted crash in an unfinished exercise is not a regression to fix.

Inspect wrappers before trusting their exit status: a recipe such as
`program || echo ...` can return success after a crash. Check the program's
actual result and the required host/container runs before reporting a solve.
Consult the week's tool guides before explaining custom debugger commands.

For root issue scripts, inspect their constants and use `--dry-run` to review
generated content before an authorized live run. Live runs create GitHub issues.
For documentation-only changes, check references, scope, and the diff; do not
run the exercise suite. Codex: use `rg` for discovery, `apply_patch` for edits,
and `rtk` for noisy commands per `~/.codex/RTK.md`.

Claude hooks, settings, permissions, and auto-memory do not become Codex
configuration through this file. Codex uses its active tools and approval
rules.
