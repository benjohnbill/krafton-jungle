---
role: Critic c-universal — universal versus local principles
truth: Cross-language critique of P2, not adopted policy or installed barriers
date: 2026-10-31
---

`K` = workspace root; `W9` = `K/week09`; `G` = `~/.claude/rules/agent-operating-model.md`. Barriers below are proposed mechanisms, not claims about installed checks.

1. **Claim:** A second language can falsify a universal prescription but cannot prove universality (judgment).

   **Evidence:** The new Scope (`CASE.md:39`) is a useful comparison method, not an induction proof. Hunt and Thomas explicitly defend techniques that cross code, documentation, and organizations ([preface, p. v](https://media.pragprog.com/titles/tpp20/preface2.pdf)). Their claim supports testing stable intents beyond C without establishing exception-free implementation rules.

   **Change:** **rewrite** P2 around the four conditional universal intents below. Separate rationale from mechanisms and recorded counterexamples.

   **Test:** Each intent survives the four translations below. A semantic counterexample triggers revision, not another unexplained exception.

2. **Claim:** Resource responsibility survives language changes, while acquiring-function cleanup does not (judgment).

   **Intent:** Every resource retained during work has a responsible owner until valid release or explicit transfer, including failure.

   **Evidence:** `K/docs/code-principles.md:32` overstates cleanup. A robust mutex can return `EOWNERDEAD` while transferring ownership for recovery ([Oracle](https://docs.oracle.com/cd/E19455-01/806-5257/sync-45513/index.html)).

   | Language | Barrier and limit |
   |---|---|
   | Python | [`with`](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement) calls `__exit__` after successful entry; the manager must implement correct release. |
   | TypeScript | `try/finally`, or [`using`/`await using`](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-2.html) with supported compiler/runtime and disposers. |
   | Go | Register [`defer`](https://go.dev/ref/spec#Defer_statements) after successful acquisition; cleanup is function-scoped, and close errors need handling. |
   | Rust | Ownership and [`Drop`](https://doc.rust-lang.org/std/ops/trait.Drop.html) automate scoped cleanup; safe [`forget`](https://doc.rust-lang.org/std/mem/fn.forget.html) shows that memory safety does not guarantee release. |

   Abrupt termination is outside these structured-cleanup guarantees. Garbage collection does not generally close external resources.

   **C-only evidence sufficient?** No; manual allocation reveals neither automatic cleanup nor its limits.

   **Change:** **rewrite** rule 2 around responsibility and transfer.

   **Test:** Inject failure after acquisition; assert valid release or transfer, including wrapper cleanup.

3. **Claim:** Predictable public contracts are universal; particular verbs and documentation styles are not (judgment).

   **Intent:** A user can determine accepted inputs, observable effects, and outcomes without reconstructing hidden implementation.

   **Evidence:** The purity rule (`K/docs/code-principles.md:27`) conflicts with allocating `palloc_get_page()` (`W9/pintos/threads/palloc.c:270`, `:301`).

   | Language | Partial barrier |
   |---|---|
   | Python | Optional static checker; [annotations alone have no runtime enforcement](https://docs.python.org/3/library/typing.html). |
   | TypeScript | `tsc --noEmit --strict`; [erased types](https://www.typescriptlang.org/docs/handbook/2/basic-types.html#erased-types) do not validate incoming data. |
   | Go | Compiler checks [interfaces and signatures](https://go.dev/ref/spec#Interface_types), not promised business behavior. |
   | Rust | Types and [`Result`](https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html) expose alternatives, not every effect or semantic condition. |

   All four still need boundary validation, contract tests, and human review for name honesty and undocumented effects.

   **C-only evidence sufficient?** No; one vocabulary cannot establish expectations across ecosystems.

   **Change:** **rewrite** name honesty and explicit-state questions around contracts. Admit useful contract comments even when their rationale is obvious.

   **Test:** A caller predicts failure behavior and side effects without opening the body.

4. **Claim:** Containing the effects of private decisions is universal; physical adjacency is not (judgment).

   **Intent:** Changing an internal decision while preserving its public agreement does not require unrelated users to change.

   **Evidence:** [Parnas](https://www.cs.lafayette.edu/~gexia/cs301/resources/parnas.html) hides design decisions; [Martin's SRP](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html) relates change boundaries to responsible people. Hunt and Thomas distinguish [duplicated knowledge from identical text](https://media.pragprog.com/titles/tpp20/dry.pdf). These converge on change coupling, not a particular file arrangement (inference).

   | Language | Partial barrier |
   |---|---|
   | Python | [Privacy is convention](https://docs.python.org/3/tutorial/classes.html#private-variables); add executable import restrictions where needed. |
   | TypeScript | [Module exports](https://www.typescriptlang.org/docs/handbook/2/modules.html) control visibility; separate import restrictions enforce allowed dependency directions. |
   | Go | Unexported names and [`internal/`](https://pkg.go.dev/cmd/go) restrict access and imports. |
   | Rust | [Private items and restricted `pub`](https://doc.rust-lang.org/reference/visibility-and-privacy.html) enforce declared access boundaries. |

   **C-only evidence sufficient?** No; other module systems expose different boundary failures.

   **Change:** **rewrite** locality and mixing questions around representation independence.

   **Test:** Reject a forbidden import, then change private storage without changing clients. Access checks alone cannot prove good boundaries.

5. **Claim:** Correctness claims need relevant, falsifiable evidence in every language (judgment).

   **Intent:** Confidence must match what the observation could detect in the actual working environment.

   **Evidence:** `G:45` and `G:59` distinguish environment validity and missing observations.

   | Language | Proposed executable check |
   |---|---|
   | Python | [`python -m unittest discover`](https://docs.python.org/3/library/unittest.html) with behavioral assertions. |
   | TypeScript | Separate type-check and configured behavioral-test commands. |
   | Go | [`go test ./...`](https://pkg.go.dev/cmd/go). |
   | Rust | [`cargo test`](https://doc.rust-lang.org/cargo/commands/cargo-test.html). |

   **C-only evidence sufficient?** No; discovery, runtime assumptions, and failure reporting differ.

   **Change:** **wire** selected checks into required CI after team agreement; compilation alone is insufficient.

   **Test:** A known behavioral defect fails the relevant assertion and blocks the required check. Report actual coverage limits.

6. **Claim:** The remaining shape rules are optional heuristics, not additional universals (judgment).

   **Evidence:** `K/docs/code-principles.md:48`–`:82` supplies caller counts, abstraction mixing, adjacency, explicit parameters, and grep uniqueness. Namespaced methods undermine lexical uniqueness; C-family `static` adjacency and Pintos `thread_current()` are contextual. Ousterhout and Martin agree on modularity but dispute [function decomposition](https://github.com/johnousterhout/aposd-vs-clean-code#method-length-summary) and [commenting](https://github.com/johnousterhout/aposd-vs-clean-code#comments-summary). Ousterhout favors keeping entangled reasoning together; Martin favors smaller named steps. Ousterhout relies more on interface comments; Martin more often prefers code and names. Neither establishes the transcription comment gate (`K/docs/transcription-mode.md:49`).

   **Change:** **rewrite** these as aids to intents 3–4. Keep snake_case, 80 columns, and branch tags team-local.

   **Test:** Accept a qualified duplicate name or useful interface comment when the contract remains clear.

7. **Claim:** Global defaults express ownership and preferences, not scientific universality (judgment).

   **Evidence:** `G:9`, `:15`, `:23`, `:29`, and `:119` prescribe roles, one glossary, refactoring cadence, reuse order, and permissions. Voice is personal. A critical scaffolding ban stays local (`W9/CLAUDE.md:20`); importance cannot determine scope.

   **Change:** **rewrite** `G` to label methods as defaults. **retire** `G:138`'s technical-versus-behavioral placement shortcut. Preserve verification intent without mandating one glossary or cadence.

   **Test:** Another project overrides the method without weakening its evidence requirements.

8. **Claim:** Three reading layers work only when language bindings and authority are explicit (judgment).

   **Evidence:** `CASE.md:114` omits language bindings; `:144` reserves team authority. Beck makes [tidying an economic choice](https://newsletter.kentbeck.com/p/options-versus-cash-flows), supporting cost-sensitive adoption rather than global promotion after one week (inference).

   **Change:** **rewrite** placement as follows; **none** to global files during this critique.

   | Layer | Proposed disk home |
   |---|---|
   | Adopted intents | `~/.claude/docs/code-principles.md`; `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` contain task-triggered pointers. |
   | Contextual policies | On-demand language guides under `~/.claude/docs/`, added as needed; learner bindings in `K/docs/code-principles.md`; team rules and tool configurations in their owning repository. |
   | Cases | Contracts beside declarations; personal `W9/notes/sheets/`; shared decisions in tracked `W9/docs/adr/`. |

   **Test:** A fresh clone contains every team obligation. Try the draft on one non-C task before promotion; record benefit, exception, and upkeep. More cases increase confidence, never prove universality.

Verdict on the core question: Universal intents can survive language changes while barriers differ; one C project proves none, and importance alone determines neither global placement nor automatic loading.
