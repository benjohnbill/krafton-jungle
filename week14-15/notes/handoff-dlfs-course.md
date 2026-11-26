# HANDOFF: hands-on course on 『밑바닥부터 시작하는 딥러닝』 chapters 1 to 6 (week14-15)

Date: 2026-11-26. Reply voice: per `~/.claude/CLAUDE.md` (Lotte, 해요체, closing block).
Workspace: `/home/benjohnbill/dev/learning/krafton-jungle/week14-15` (plain directory in the root repo, not a team repo).
Course map (read it first): `lab/dlfs-course/README.md`.

## First action of the next session

1. Read `lab/dlfs-course/README.md` in full.
2. Open stage 1 with one short paragraph: the stage question, and what the user will type first. Then give the first script (NumPy `shape` and broadcasting) and ask for his prediction before he runs it.
3. Ask him to confirm the book section numbers against the book's table of contents. The numbers come from agent memory.

## What the user decided (user said, 2026-11-26)

- Goal: "이 책의 내용 기반을 실전적으로 직접 체험하면서 익힐 수 있는 코스". The core concepts of chapters 1 to 6 come first, not the LMS Day table.
- Order: "내 체험과 질의응답이 먼저". The book is "그 실습 뒤에 읽을 내용".
- Book timing: "일단 다 끝나고 읽는다 생각하면 될 듯". The agent gives section numbers per stage. He reads them at the end of the day.
- Glossary: "GLOSSARY.md는 너하고 치밀하게 단어를 깎아나가는 과정이 필요하긴 할 듯". Use the glossary where it helps the TODOs or deep learning.
- Time: "가용 시간은 6시간 정도긴 한데. 음.. 일단. 해보고 생각하자."
- Every other item in the course map: "모두 동의할게." and "응, 추천대로 진행해줘".

The agreed items, in short:

- Five stages: ch1-2, ch3, ch4, ch5, ch6. One toy network grows through all five stages.
- Course files live in `lab/dlfs-course/`. Use toy data only. Do not write code for the `mnist` TODOs.
- One unit of practice: the agent gives a short script, the user types it, predicts the output, runs it, compares, and explains it in his own words.
- Tools: plain `.py` scripts, plots saved as PNG. No Jupyter.
- After each stage: about 10 minutes of glossary work (see the course map), then fill the stage sheet.
- Time check at the end of stage 2 (chapter 3). If the course is late, cut stage 5 to the optimizer comparison. Never cut stage 4.

## Do not

- Do not ask him to read the book before a stage.
- Do not pre-write the scripts of later stages. Write each script when the stage needs it, so it can follow his predictions and questions.
- Do not write or complete code in `mnist/` or `LLM-from-scratch/`. The LMS forbids AI-generated code for a whole TODO function.
- Do not define a glossary term for him. He writes the definition first. The agent attacks it with counterexamples.
- Do not add a Claude trailer or attribution to his commits.

## State (verified by the agent, 2026-11-26)

- Python environment: `week14-15/.venv`, made with `uv` (Python 3.12.13, numpy 2.5.5, matplotlib 3.11.2, pytest 9.2.0, from `mnist/requirements.txt`). A PNG save works with the `Agg` backend. Root `.gitignore` line 8 ignores `.venv/`.
- conda is not installed on this machine. The user chose to keep the `uv` venv.
- Stage sheets exist and are empty: `notes/sheets/mnist/dlfs-1-perceptron.md` to `dlfs-5-training-techniques.md`.
- `GLOSSARY.md` has empty sections `신경망 (mnist)` and `LLM (LLM-from-scratch)`. Its format contract is the `domain-modeling` skill file `GLOSSARY-FORMAT.md`. Load that skill before the first glossary entry.
- No course script exists yet.

## Settled at the end of the preparation session (user said "1, 2번 추천대로 진행해줘.", 2026-11-26)

- Python environment: keep the `uv` venv. Do not install conda. `AGENTS.md` § Environment now says so.
- Glossary language: a `GLOSSARY.md` entry holds his Korean definition as he wrote it, then one English line under it. This is an exception to the English-only document rule, for this file only.

## After the course

Tomorrow the user starts the `mnist` TODOs (Day 1 to Day 3 in `statement-1326.md`) on his branch `CJG`. The stage sheets and `GLOSSARY.md` are his input for that work.
