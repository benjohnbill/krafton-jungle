---
role: AI-together mode — the course period "AI 함께하기", where the agent may generate all code and the learning goal moves from writing code to understanding frameworks, AI workflow, and team structure
truth: This file, for the generic rules. The week file names the course words, the repositories, and the core logic of each project
born: 2026-11-05 at week 11-12 init (user said). Rules under "Rules" are the agent's draft from his goals
status: Trial. First run: week 11-12. He decides on changes after the first project
edits: The agent may update this file (Tier 2). Mark trial findings with their date
---

# AI-together mode

Read when the week file's `Mode:` line names AI-together, before the first
reply.

## Goals

The three headings are the learning objects as he heard them from the course.
The bullets are his own purpose and principles (user said 2026-11-05).

**The content of the framework**

- Why that framework? Why do people use it?
- What problems do the framework solve?
- Why are those functionalities in that framework?

**How to work with AI**

- Investigate existing skill workflows (for example matt-pocock-skills, pstack
  poteto-mode, CBM).
- Read Claude and OpenAI documents.
- Read recent issues about AI workflow.

**How to do team**

- Do functional and structural thinking about the codebase, with Clean Code
  instructions to the AI.
- Graph engineering (for example Graphify, CBM).
- Conventions for AI, like the items above.

## Rules

- **Code.** The agent may generate all code and push it, on the branches that
  the week file names. He types only the code that the study cycle below
  selects. The sentence "do not hand it to him" at the top of the spine does
  not apply in this mode.
- **Spoilers.** Spoilers are welcome. Give a well-defined spoiler when it helps
  him understand a concept or start a new useful activity (user said
  2026-11-05). The spoiler boundary is the week file's list only.
- **Framework reasons.** When generated code implements a framework feature,
  say which problem that feature solves in the real framework, and how this
  implementation differs from the real one. Cite the framework's own documents
  or source.
- **Workflow before work.** Before you start a new kind of task, check whether
  an existing skill or workflow covers it, then use it. Name the skill or
  workflow, and the document or issue behind it, in the reply. Verify that an
  external tool works in this environment before you recommend it.
- **Structure before generation.** Before you generate a module, state its
  function, its interface, and its place in the codebase. Then generate it.
  Keep the Clean Code instructions and other conventions for AI in one file.
  Changes to that file go through a PR and one approval, the same as code
  (user said 2026-11-06).
- **Graph.** Index each project repository with `codebase-memory-mcp` before
  structural exploration, and use the graph for structure questions.
- **Done.** The course's condition: he can explain how the core logic works, in
  his own words. When he asks for a check, ask him to explain one core-logic
  item, and name the gaps. The week file lists the items.

## Study cycle

Trial (user said 2026-11-06, first run: `mini-react`). The order goes from
concrete to abstract. A week file names the study plan of each project.

1. He types a small code block. A change task that he does alone, with no hint,
   is required. Discomfort appears when he changes code, not when he copies it.
2. He uses a before and after page. The agent builds the page shell. The logic
   in the page is the code that he typed.
3. He reads a short passage. The agent names the location.
4. He writes one sentence in his own words. The agent names the gaps.

- One app goes in order: vanilla, the real framework, then the mini version.
  This order passes once through the plan, not once for each concept.
- Each step has three levels (Min, Mid, Best). He changes the level of a step at
  any time. Do not plan in minutes.
- He asks about syntax, functions, and errors at once. He batches "why"
  questions to the end of a block. The count of questions is not a goal.
- A correct prediction, a finished change task, and the sentence are the pass
  signal. If one fails, stop at that block.
- Record a dated observation after one cycle. One cycle does not prove the
  method, so do not promote it to a rule.

## From the other modes

The spine stays in force, except the sentence named above. No section of
`docs/tutor-mode.md`, `docs/concept-tutor-mode.md`, or
`docs/transcription-mode.md` applies.
