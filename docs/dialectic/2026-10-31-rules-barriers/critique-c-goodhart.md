---
role: Critic c-goodhart — class D and barrier verification
truth: Read-only observations on 2026-10-31; proposed mutations were not applied
scope: K = workspace root; W9 = week09; costs are judgment estimates
---

# Ranked claims

## 1. P3 makes detector availability decide whether a requirement is unconditional

**Claim:** An absolute obligation and complete automated detection are independent properties; killing one mutant cannot connect them.

**Evidence:** `CASE.md` P3 demands a tool or demotion. `K/docs/code-principles.md:25–39` combines ownership safety with semantic naming and comments. Judgment: finite tests support bounded claims, and an already-red command “kills” every mutant without detecting anything new.

**Change — rewrite:** Replace P3 with a record of obligation, checked scope, blind spots, and blocking trigger. Keep ownership obligations unconditional despite incomplete evidence. Require an original passing baseline, a violating mutant failing for the intended reason, restoration passing, and a legitimate neighboring example passing. Verify the actual trigger separately.

**Test:** A pre-existing compiler error must make a mutation experiment inconclusive. A harmless edit must pass. Record survivors rather than weakening the obligation to obtain green checks. Cost: minutes per selected fixture; exhaustive mutation is inappropriate for this week.

## 2. The current lint report misclassifies a compiler error and can discard tool failure

**Claim:** Wiring the existing report unchanged would enforce an unreliable diagnostic proxy.

**Evidence:** On branch CJG, HEAD `3c39884`, with an existing modified `pintos/include/vm/file.h`, `rtk proxy make lint` exited **2**:

```text
pintos/vm/file.c:143:45: naming: use of undeclared identifier 'lazy_load_file' [clang-diagnostic-error]
모양 22줄: make format 으로 자동 수정 | 이름·중괄호 1건: 직접 수정 (CONVENTION.md)
make: *** [Makefile:15: lint] Error 1
```

This differs from CASE's earlier HEAD. Installed format/tidy versions matched the documented pins. Twenty layout lines concern disk comments. `W9/scripts/convention.py:63–87,97–105,129–132` discards subprocess status and labels every non-brace diagnostic “naming.” A read-only `runpy` probe with mocked subprocess results returned `layout_count: 0` for formatter exit 2 with `fatal: invalid option`, and `naming_count: 0` for silent tidy exit 2.

**Change — fix:** Preserve tool failures separately from convention findings before proposing a team-owned gate. Cost: small script repair. The present report has useful style locations and a real parse failure, but measures neither ownership safety nor code clarity.

**Test:** Both simulated failures must produce infrastructure failure, never a clean result; compiler errors must retain their category.

## 3. Absolute rule 1 contradicts the project's own accepted allocation vocabulary

**Claim:** Enforcing query prefixes as purity would penalize honest Pintos names.

**Evidence:** `K/docs/code-principles.md:27–29` forbids state changes under `get`; `W9/CONVENTION.md:190–194` explicitly approves `palloc_get_page`. Its implementation reaches `bitmap_scan_and_flip` and takes a lock (`W9/pintos/threads/palloc.c:266–303`). Current snake-case checks do not inspect effects (`W9/.clang-tidy:5–7`).

**Change — rewrite:** Specify advertised observable effects and preserve upstream APIs (`W9/README.md:231`). Review new names against contracts. A bounded test can snapshot named state around a selected query; no ASan, Valgrind, or stock analyzer check establishes name honesty. Snapshots miss unlisted state. Cost: minutes of review, hours for a useful state fixture; whole-program effect modeling exceeds this week's budget (judgment).

**Test:** A selected query's hidden persistent write must fail its contract test while legitimate allocation passes. Renaming the query to evade a prefix matcher must not erase the contract.

## 4. Absolute rule 2 admits useful bounded barriers, not universal leak certification

**Claim:** Failure injection plus ownership observations can detect real cleanup defects without pretending to cover every failure path.

**Evidence:** The rule spans memory, frames, mappings, locks, and files (`K/docs/code-principles.md:32–35`). Real acquisition and rollback cross allocation and page-table layers (`W9/pintos/threads/mmu.c:33–94`). Judgment: “acquired here” must distinguish local ownership from permitted ownership transfer.

**Change — rewrite and wire:** State “discharge every locally owned obligation on failure.” For one selected VM operation, fail each acquisition site and relevant occurrence. Observe resource identities, mappings, file ownership, and lock availability after quiescence. Use an approved scratch harness, preserving upstream tests. Cost: hours with existing seams; days to add broad instrumentation (judgment). Team agreement precedes shared tooling.

**Test:** Independently omit a release, retain a mapping, or leave a lock held; each must fail the corresponding observation. A balanced total alone is insufficient: one leak and one wrongful release can cancel. Uninjected success and legitimate transfers must pass. Unvisited paths remain explicitly unverified.

## 5. “Add a sanitizer” can measure the emulator or a substitute allocator

**Claim:** These tools require different adaptations, so rule 2 is not merely class B awaiting a CI command.

**Evidence:** Pintos uses its own arena allocator (`W9/pintos/threads/malloc.c:12–29`) and kernel toolchain (`W9/pintos/Make.config:8–24`). [ASan](https://clang.llvm.org/docs/AddressSanitizer.html) requires instrumentation and runtime support; leak detection is a separate facility. [Memcheck](https://valgrind.org/docs/manual/mc-manual.html#mc-manual.mempools) requires descriptions of custom pools. [Clang annotations](https://clang.llvm.org/docs/analyzer/user-docs/Annotations.html) model custom allocation and ownership transfer.

**Change — rewrite:** Offer explicit choices: host-extracted C with ASan/LSan or Valgrind costs hours to days but loses kernel integration; a kernel sanitizer port is a separate multiday project. Valgrind around [QEMU](https://www.qemu.org/docs/master/system/index.html) observes the host emulator, not Pintos ownership (inference). Clang static analysis needs correct build flags, allocator/transfer models, and further treatment of Pintos locks and files. Model work costs hours to days and can hide defects through incorrect annotations (judgment). Prefer claim 4's narrow guest test this week.

**Test:** Seed a guest ownership defect and a separate harness defect; record which tool detects which. A clean emulator or replacement allocator must never certify the guest.

## 6. Absolute rule 3 has no faithful runtime barrier

**Claim:** Comment similarity enforcement would reward deletion and paraphrase rather than useful explanation.

**Evidence:** `K/docs/transcription-mode.md:49–56` defines usefulness semantically. `W9/pintos/vm/vm.c:165–175` supplies concrete comments for review. Judgment: runtime tests, sanitizers, and static memory analysis cannot determine whether prose adds necessary knowledge; token overlap also rejects valid ownership explanations.

**Change — rewrite:** Keep a review question: “What necessary fact does this comment add?” Cost: minutes per hunk. Retire any proposed comment-count or similarity gate.

**Test:** Review a restatement, an overlapping but useful ownership explanation, and a misleading paraphrase. Removing all three must not earn automatic approval.

## 7. Exact lint-line comparison can turn an unrelated edit into a new violation

**Claim:** Baseline comparison needs stable diagnostic identity, not output-line equality.

**Evidence:** `K/skills/jungle-team-merge/SKILL.md:60–65,77` compares lint lines and reports counts. Output embeds line numbers and source excerpts (`W9/scripts/convention.py:84–86`). Judgment: adding a blank line shifts an inherited warning without introducing a defect.

**Change — fix:** Compare normalized rule, file, symbol, and message; retain raw locations for inspection. Cost: a small parser change. Require explicit review where identity is ambiguous.

**Test:** A preceding blank line must not create a new finding; a second genuine violation must appear even if another disappears and totals remain equal.

## 8. Equal test results do not establish behavior-preserving refactoring

**Claim:** Bin 1's verification can reward changes that merely escape the suite.

**Evidence:** `K/docs/code-principles.md:101,114–115` uses unchanged `make dfast` results and moves undemonstrated fixes elsewhere. Judgment: unchanged results leave unexercised failure behavior unconstrained.

**Change — rewrite:** Label equality a regression observation. Keep intended behavior fixes out of bin 1 even without a reproducer; record uncertainty or defer. Add one relevant ownership observation when warranted, not a coverage quota.

**Test:** A cleanup omission on an unexercised failure path must remain a verification gap despite identical suite results. Cost: explicit classification plus one targeted check.

Verdict on the core question: Preserve the obligations, repair misleading measurements, and prove narrowly scoped barriers rather than equating green tools with sound rules.
