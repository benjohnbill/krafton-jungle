---
role: Critique by c-problem (lens: problem definition) of CASE.md
truth: Snapshot of one critic's view on 2026-10-31. Not a decision
born: 2026-10-31
status: Open
---

# Critique c-problem: the question itself

Paths: `K` = `/home/benjohnbill/dev/krafton-jungle`, `W9` = `K/week09`.

## 1. The frame asks about enforcement. His problem is control of shape.

**Claim**: "Real barrier or rule that only sounds good" asks how documents
constrain the agent, but his recurring question is how he decides, sees, and
compares code shape.

**Evidence**: The handoff names the pattern: "how can a human keep control of
the code shape when an agent writes the lines?"
(`K/docs/handoffs/2026-10-30-clean-code-interest-evidence.md:52-55`). The
article itself splits the work: "CRAP and DRY keep the shape; tidying and
systemic refactoring make it" (`CASE.md:35`). Control has three parts: the
intended shape, the actual shape, and a comparison. The case frame covers only
the blocking half of the comparison.

**Change**: rewrite the core question for the grilling: "For each moment
(before a hunk, at a PR, when he analyzes a codebase), which artifact holds
the intended shape, which shows the actual shape, and what tells him that the
two differ?"

**Test**: The grilling result names an artifact for each moment and part, or
marks it empty on purpose. A result that lists only lint checks means the old
frame won.

## 2. He already owns both halves of shape control. Only the comparison is missing.

**Claim**: The stage sheet already holds his intended shape, `pintos-index`
already extracts the actual shape, and nothing compares the two.

**Evidence**: The mmap sheet gives each function the fields 호출자, 역할,
인자, 인자의 사용·변화, 반환값
(`W9/notes/sheets/mmap/memory-mapped-files.md:9-32`). The template has only a
name line (`K/docs/templates/stage-sheet.md:5-7`), so he added these fields
himself in the latest stage. The `pintos-index` card answers the same fields:
callers, calls, argument changes, return (`K/tools/pintos-index/README.md:4-6`).
`grep -rn sheet K/tools/pintos-index/src` finds only "stylesheet"
(`views.py:138`). No link exists.

**Change**: wire, at no code cost. Add one line to
`K/docs/transcription-mode.md` loop step 5 (Close): compare the function's
sheet row with its `pintos-index` card. A difference is a D-row candidate or a
review comment. A script that diffs the two comes later, only if the manual
step finds differences.

**Test**: Count the close steps in the next stage where a row and its card
differ. If the count is zero, retire the step.

## 3. The article's premise does not hold for his present mode.

**Claim**: The article assumes the human no longer reads the lines, but his
mode requires that he types and explains every line, so he is the barrier for
each hunk today.

**Evidence**: Article: "let go of syntax" (`CASE.md:25`). Transcription mode:
"Done for a unit: he can explain why each line exists ... He types every line
himself" (`K/docs/transcription-mode.md:26-29`). He catches prompt-rule drift
when he types the hunk. Unread code enters only through teammate PRs
(`K/docs/transcription-mode.md:106-108`).

**Change**: rewrite the question in two parts. Now: a one-week repo where he
reads every line. Later (question 4): code that nobody reads line by line.
Build the article's barrier list only for later.

**Test**: No week repo gains a barrier whose only reason is "the agent drops
prompt rules" while transcription mode is on.

## 4. Question 4 is a reading problem. Class C is the asset that transfers.

**Claim**: Rules for writing do not transfer to a codebase he analyzes, but
review questions and instruments do, so the judgment questions are the core
output and not the leftover class.

**Evidence**: Question 4 is "manage future codebases that he will analyze"
(`CASE.md:43`). The five judgment questions are already reading questions:
"Can a reader understand the function without opening another file?", "When
you search a new name with `grep`, do the results show one concept only?"
(`K/docs/code-principles.md:68-82`). P1 treats C as the residue for prose.
For question 4, C is the main output.

**Change**: rewrite: make the five questions an analysis checklist that names
no Pintos symbol. Keep Pintos examples local (P2, with a new reason:
portability to foreign code).

**Test**: Apply the checklist to code he did not write (a teammate PR or
Pintos base code) in 30 minutes. Each question must give a yes, a no with a
`file:line`, or "cannot answer here". A "cannot answer" marks a local rule.

## 5. P1 sorts on three different axes at once.

**Claim**: P1 mixes a property of the rule (can a tool check it), a property
of the repo (is a tool wired), and a property of the proxy (does the check
match the intent).

**Evidence**: judgment, plus one inner contradiction. A rule moves from B to A
by a config change, so A and B are states, not classes. D is defined as "a
tool enforces a proxy", but its third example is "a lint that always fails and
blocks nothing" (`CASE.md:96-98`). Nothing enforces that lint. It is class B
with a broken baseline.

**Change**: rewrite P1 as two axes. Checker: exact tool, proxy tool, or human
question. State: wired, unwired, or claimed but absent.

**Test**: Every reviewed rule lands in one cell without debate, the
always-failing `make lint` and `code-principles.md:20-21` included.

## 6. P1 omits the worst kind: false assurance.

**Claim**: The rule that "only sounds good" in the harmful sense is a document
that claims a barrier which does not exist, because the claim switches off the
reader's own attention.

**Evidence**: `K/docs/code-principles.md:20-21` says `clang-format` and
`clang-tidy` "already cover those cases". `W9/.clang-tidy` enables two checks
that touch none of its rules (`CASE.md:69-76`). Compare
`W9/CONVENTION.md:178`: "도구가 못 잡는 부분이다." That line is an honest
unwired rule. It keeps the reviewer alert.

**Change**: fix `code-principles.md:20-21`: state which rules a tool checks
(none today) and which rules he checks at review.

**Test**: For each claim of coverage in the rule documents ("cover", "catch",
"enforce", "잡"), a reader can run the named command and see it fail on a
planted violation. A claim with no command is deleted.

## 7. P3 makes a converse error. Replace "barrier" with "named detector".

**Claim**: P3 inverts the user's own gate, and its demotion changes what
"absolute" means but leaves the real gap, detection, open.

**Evidence**: `code-principles.md:19-21`: a mechanical check is accepted only
when no exception exists (check implies no exception). P3 says no exception
implies a check. "Absolute" in `code-principles.md:25` is a review decision:
"A violation is fixed, not justified", so no `[CJG]` exception is allowed.
Demotion makes a justified lying name legal. The real gap: no rule says who
finds a violation, and when. Detectors exist already. `pintos-index` records member writes through
parameters (`K/tools/pintos-index/src/pintos_index/model.py:21-22`,
`cards.py:137-140`). A query-named function with member writes is a rule-1
candidate. For rule 2, the course leak test `multi-oom` ("If you seriously
think there is no memory leak", `multi-oom.c:17`) is in the userprog test set
(`W9/pintos/userprog/Make.vars:6`) but not in the VM set
(`W9/pintos/vm/Make.vars:6`). The inherited barrier disappeared at P3.

**Change**: rewrite P3: "An absolute rule names its detector: a tool, a
test, or a fixed review moment (transcription close step). Prove a tool
detector by mutation." Keep the word "absolute".

**Test**: Each absolute rule has one named detector. One planted violation for
each rule, in a `lab/` probe, is flagged by that detector.

Verdict on the core question: The frame is wrong; ask not whether a rule is a barrier but which artifact holds his intended shape, which shows the actual shape, and when he compares them, because he already has both artifacts and lacks only the comparison.
