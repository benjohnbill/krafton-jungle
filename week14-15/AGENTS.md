Mode: team project (AI 이해하기, two team repositories). Transcription mode (`../docs/transcription-mode.md`), nearly settled (user said 2026-11-26).

# week14-15 (AI 이해하기)

Two team assignments over two weeks. First `mnist`: a two-layer MNIST classifier in NumPy only. Then `LLM-from-scratch`: a small GPT in plain PyTorch modules, trained on NSMC, with a sentiment-classification head. What must remain: he can explain Forward → Loss → Backward → Update with formulas and array shapes, and text → token → Dataset → attention → GPT → loss and classification, in his own words. Accuracy and fluent generation are not goals.

This file is the personal layer. It sits above the team repositories, so no teammate's clone has it.

## Mode

Course words (LMS `learning/1325`, read 2026-11-26): "AI는 개념 이해, PyTorch API 확인, 자신이 작성한 코드의 오류 메시지 해석에 사용할 수 있습니다. TODO 함수 전체 구현이나 테스트 정답 코드를 생성해 붙여 넣는 용도로는 사용하지 않습니다. 받은 설명은 작은 tensor나 테스트로 직접 검증하고 REPORT.md의 "참고와 AI 사용"에 기록합니다."

- The mode does not meet that wording: his questions start from agent-generated code. His reading (2026-11-26): typing the code and asking questions teaches faster than writing it alone; the failure to prevent is copy-paste. The AI use goes into `REPORT.md` § "참고와 AI 사용".
- `mnist`: the TODOs are short NumPy formulas that the statement already gives. Whether he writes a formula first or types generated code is decided per function, as he goes (user said 2026-11-26).
- `LLM-from-scratch`: generate, then transcribe.
- AI-generated code goes on his personal branch `CJG` and may be pushed. `main` takes changes only through a team-reviewed PR. Never push to `main` directly (course rule).
- Course team rules: each member implements every core TODO on their own branch (no split by file); the team reviews in core time and merges one chosen implementation; the merged branch holds only code that passes the tests.
- His commits and PRs carry no Claude trace: no `Co-Authored-By: Claude` trailer, no "Generated with Claude Code" line.

## Statement and spoilers

- Week guide: `statement-1327.md` (LMS `learning/1327`): schedule, presentations, submissions.
- `mnist`: `statement-1326.md` (LMS `learning/1326`) and the template README. Book: 『밑바닥부터 시작하는 딥러닝』 chapters 1–6.
- `LLM-from-scratch`: `statement-1325.md` (LMS `learning/1325`), the template README and `HINTS.md`. Book: 『밑바닥부터 만들면서 배우는 LLM』, source https://github.com/rickiepark/llm-from-scratch.
- Spoiler list: none. Quote the statements, `HINTS.md`, and the book source freely (user said 2026-11-26).
- Sheets: `notes/sheets/<project>/<stage>.md`, one stage per Day group. Glossary: `GLOSSARY.md` in this directory. Term, problem, and requirement definitions come before code; he spends most time there (user said 2026-11-26).

## Environment

- Repositories (submodules of the workspace root): `mnist/` (`origin` `jonggeonyu/mnist`, template `krafton-jungle/mnist-lab-v2`) and `LLM-from-scratch/` (`origin` `jonggeonyu/LLM-from-scratch`, template `krafton-jungle/gpt-lab-v2`). A teammate (종건) uploads the templates.
- Python 3.12 in a `uv` venv, not conda. conda is not installed on this machine (user said 2026-11-26: keep `uv`). `week14-15/.venv` serves `mnist` and `lab/dlfs-course/`: `uv venv --python 3.12 .venv`, then `uv pip install --python .venv/bin/python -r mnist/requirements.txt`. `LLM-from-scratch` gets its own venv when that work starts. The template README's conda commands give the same packages. `mnist` code he writes uses numpy, math, random, time, matplotlib, and pytest only.
- Data, checkpoints, tokens, and personal environment files are never committed (course rule).

Verify, in order: (1) the terms and requirements for the stage are in `GLOSSARY.md` and the sheet; (2) agent-generated tests in his own test files, separate from the template `tests/`; (3) `pytest` for the current Day and every earlier Day; (4) `python tools/selfcheck.py --day N` (`LLM-from-scratch`); gradient check and a falling loss (`mnist`).

Board: none (team board, owned by the team)

## Do not touch

- Template-provided code. `mnist`: `src/data.py`, `download_mnist.py`, `src/network.py`, the provided parts of `src/training.py` and `src/optimizers.py` (Adam), BatchNorm and Dropout in `src/layers.py`, `tests/`. `LLM-from-scratch`: `tests/`, `tools/selfcheck.py`, `download_data.py`, the data files, and the non-TODO code in `src/`.
- The team's repository settings and team-tracked config. Change them only when he asks.
