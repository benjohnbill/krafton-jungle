# Brief for each critic

You are one of five critics. Read `CASE.md` in this folder first, then the
documents it names. Your lens is given in your prompt. Other critics cover
other lenses; stay in yours, go deep.

## Rules

- Read-only on everything except your own output file
  `critique-<your-name>.md` in this folder. Do not edit, commit, or run
  commands that change state. Read-only commands (`cat`, `rg`, `git log`,
  `make -n`) are fine. `make lint` is fine; it changes nothing.
- Attack the case. Agreement is allowed only with a new reason the case does
  not already give.
- You may attack the question itself. If the user asks the wrong question,
  say what the right question is and why.
- No advice that only sounds good. Each claim needs:
  1. **Claim**: one sentence.
  2. **Evidence**: `file:line`, a command and its output, or a named source
     (book, paper, public practice of a named team or tool). Mark a claim
     from your own judgment as "judgment".
  3. **Change**: the concrete change in a file, a tool, or a practice. Name
     the verb: wire, fix, rewrite, retire, or "none".
  4. **Test**: how anyone can tell later if the change worked or failed.
- Weigh cost. The user is a learner; a week repo lives about one week.
- At most 8 claims. Rank them, strongest first. At most 1200 words.
- End with one line: `Verdict on the core question: <your answer in one
  sentence>`.

When you finish, reply only with the path of your file.
