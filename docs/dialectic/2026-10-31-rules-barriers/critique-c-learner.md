---
role: Critique for the rules-and-barriers panel, from critic c-learner
truth: Read-only review of local documents on 2026-10-31. Recommendations are judgments, not decisions. No live GitHub settings or checks were verified.
scope: Learner cost, one-week repository lifetime, team ownership, and YAGNI
status: Proposed
---

# Learner cost and YAGNI

Paths are relative to the workspace root. Claims are ranked, strongest first.

## 1. P5 makes automation the default before establishing a need

**Claim:** For this learner, “default for B: wire” spends scarce exercise time on an unproved tooling requirement.

**Evidence:** Judgment, given the one-week lifetime and team ownership in `CASE.md`, “Constraints.” `skills/jungle-team-merge/SKILL.md:57-65` already specifies baseline comparisons for lint and tests. `week09/README.md:189` leaves CI for later. Neither fact proves that CI is unnecessary, but the case supplies no measured frequency or cost of missed checks to justify replacing the existing practice now.

**Change — rewrite:** In P5, make the default “none until a concrete risk justifies a change.” Wire an existing check when expected avoided rework during the remaining week exceeds setup, baseline repair, team agreement, and maintenance costs. Reuse across weeks can count only when someone owns that reuse. A repeated omission or one costly integration failure can justify wiring immediately. Do not require repeated damage for a serious risk.

**Test:** At week close, compare setup and repair effort with actual checks run and failures caught before integration. If no actionable result arrived before the repo closed, do not automatically carry the gate forward.

## 2. The central learning test is a code judgment, not a barrier inventory

**Claim:** The panel should first ask whether he can judge code shape and explain a failure, rather than whether every rule has enforcement.

**Evidence:** Judgment. `docs/code-principles.md:12-15` makes his reading the priority. `docs/transcription-mode.md:23-29` defines completion through explanation. The same mode records a failed documentation experiment: about 60 questions, none answered by the existing rows (`:78-82`). More recorded structure did not establish useful understanding in that trial.

**Change — rewrite:** Change the panel's leading question to: “Which decision can he make more accurately on the next PR?” Use one existing, in-scope function to practice tracing calls, identifying ownership, and explaining whether a helper earns its place. Use the current sheet, not another assessment document. Respect the selected mode: let him make the judgment before the tutor supplies feedback. Do not give an exercise solution or corrective patch as an assessment answer.

**Test:** On the next unfamiliar function, he explains a relevant state transition and defends a structural choice before seeing the agent's judgment. A green check alone does not pass this test.

## 3. P3 confuses the strength of an obligation with the reach of a checker

**Claim:** Requiring a tool for every absolute rule either creates an expensive verification project or weakens an important obligation through relabeling.

**Evidence:** Judgment. `docs/code-principles.md:32-35` covers memory, frames, mappings, locks, and files. `week09/.clang-tidy:5` enables naming and brace checks only. A test that detects one deliberately broken cleanup path cannot establish that every resource is released on every failure path. Transcription mode also makes deliberate breaks optional (`docs/transcription-mode.md:113-118`).

**Change — rewrite:** Separate “required behavior” from “verification available.” Keep cleanup required. State which paths existing tests cover and which paths need review. Use a targeted failure demonstration when it serves the current exercise. Defer a generic leak framework, Gherkin layer, mutation suite, and shape metrics unless a concrete current problem earns their cost. Do not introduce mandatory exercise mutations through a policy review.

**Test:** For one path he has studied, he predicts the resource state after failure and identifies what the selected test cannot prove. Calling that test universal enforcement fails the review.

## 4. P4 assigns too much reading by document type and too little by decision

**Claim:** Human ownership should mean authority over consequential decisions, not compulsory reading of every spec, ADR, glossary, and convention or categorical blindness to agent notes.

**Evidence:** Judgment. `docs/transcription-mode.md:72-73` deliberately limits reading to the current sheet. `docs/tutor-spine.md`, “Re-entry,” uses progress to avoid repeating confirmed work. `skills/jungle-team-merge/SKILL.md:80-81` leaves human-only judgments for him. Thus an agent-managed file can affect his learning path even when he need not maintain that file.

**Change — rewrite:** In P4, require him to read the current requirement, changed interface, relevant ownership rule, and evidence needed for his approval. Let agents maintain routine records. When a handoff or progress claim changes what the tutor skips, expose the relevant claim for correction. Do not add blanket review of memory files.

**Test:** Before approval or re-entry, he can explain the current requirement and correct a false assumption about what he already understands without reading the whole document stack.

## 5. Truth repairs pay back sooner than reorganizing the rule hierarchy

**Claim:** Correcting misleading operational statements has immediate value, while promoting universal principles or restructuring all documents has no demonstrated payoff this week.

**Evidence:** `docs/code-principles.md:19-21` overstates existing checks, while `week09/CONVENTION.md:178` explicitly reserves semantic naming for review. `skills/jungle-close/SKILL.md:38-52` prescribes a different commit form from `week09/README.md:194-215`. The principles already declare a draft trial and a revision point after mmap (`docs/code-principles.md:5`).

**Change — fix:** Propose a narrow correction to the checker claim and an explicit team-format override in the close workflow. Put live-ruleset discrepancies on the existing team agenda before editing shared policy. **None:** defer global promotion and a document-wide A–D catalog until the stated trial produces evidence.

**Test:** The next generated commit follows the team format, and the learner can distinguish what lint checks from what he must review. No new parallel principles file appears.

## 6. A failing lint report can remain useful without becoming a blocking gate

**Claim:** P1's class D example mistakes nonblocking detection for useless enforcement and could discard a cheap review aid.

**Evidence:** `skills/jungle-team-merge/SKILL.md:60-65` explicitly compares new lint findings against an already failing base. `week09/README.md:376` likewise distinguishes expected unfinished behavior from regressions. Judgment: the actionable question is whether a report changes a decision, not whether every report blocks a commit.

**Change — rewrite:** Call lint an advisory detector until the team makes it required. Retain the existing baseline comparison. Do not clean unrelated scaffolding or add an absolute full-suite gate merely to obtain green status.

**Test:** On the next PR, inherited findings and new findings are distinguished, and new actionable findings receive a response. If reviewers repeatedly ignore both, reconsider the report or its trigger with the team.

Verdict on the core question: Build his ability to judge code and verification limits first, fix misleading guidance now, and add only team-approved barriers whose benefit can arrive within the remaining project or a demonstrated reuse path.
