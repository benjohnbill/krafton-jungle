Mode: transcription, light. This mode applies inside `week13/lab/` only. It replaces the AI-together mode of `../AGENTS.md` in this folder. The team repository `../mini-webserver/` keeps AI-together.

`teach/` is the `/teach` workspace for the request-flow lessons (L1 to L4). The `/teach` skill rules apply there, not transcription mode. Each lesson sits right before the track it predicts.

`teach-bot/` is a second `/teach` workspace, for the defense layers of `rproxy` (lessons L1 to L5, settled 2026-11-24). The `/teach` skill rules apply there too. Its lessons do not explain concepts: the crawler notes 00 to 04 hold the knowledge, and a lesson links them. Read `teach-bot/NOTES.md` before work there.

# week13 lab (hands-on probes)

He does not read CSAPP chapter 11. He builds base knowledge for the web server week by direct experience: CLI tools first, then small C programs that he types. The questions from the lab feed the team prototype. Settled by grilling, 2026-11-19 (user said).

## Loop

Source: `../../docs/transcription-mode.md` Part 1, with these parts only:

- The agent writes the probe. He types C code one hunk at a time and asks questions. A short function goes whole.
- Each probe ends with a change task that he does alone, with no hint.
- If he pastes a lesson copy block (from `teach/`), write its predictions and wrong quiz picks into the probe README, section 볼 것. Before the run, ask him each one. After the run, compare with the output. Do not give the answer first. With no block, a prediction before the run is optional, one line.
- He writes code comments, and only a comment that meets both conditions in `transcription-mode.md` § The sheet: the code alone does not show it, and the reason is not obvious.
- Breaks: when he asks to break something, make the broken version, and he follows its flow.
- No stage sheet and no D or I rows. Open questions go to `QUESTIONS.md`, one line each, with the probe number.

Done for a probe: he can say why each line or command exists, in his own words.

## Probe folders

- One concept per folder: `NN-topic/` (for example `05-strace/`). One C file per probe, 300 lines at most.
- Each folder has a `README.md` in the mixed form (`~/.claude/docs/document-language.md`) with four sections: 실행할 명령, 볼 것, 혼자 하는 변경 과제, 확인 질문. In 확인 질문 the agent writes one question on the core of the probe. He answers it in the conversation. His answer does not go in the README (user said 2026-11-20; this replaces 내 문장, kept in 01 to 05).
- Order of tracks: T1 CLI, T2 socket C, T3 TCP behavior, T4 HTTP server, T5 concurrency, T6 proxy. Quality checks (valgrind, ASan, malformed requests) go inside T4 to T6. `README.md` in this folder lists the tracks.
- He reads long command output through `bat`. When a command ends by itself and its output is long, give it as `<command> 2>&1 | bat -l <syntax>` (for example `http`, `log`). Do not pipe an interactive or long-running command (`nc -l`, `telnet`, `strace` on a server) into `bat` (user said, 2026-11-19).
- When T6 ends, tell him to stop nginx with `sudo systemctl disable --now nginx`. He installed nginx on 2026-11-19 for probes 02, 03, and T6. The service starts at each boot (user said, 2026-11-19).

## Code conventions

Source: `../../week09/CONVENTION.md` (Pintos). Rules A, B, C2, C3, C5, and C6 apply. C1 does not apply to a one-file probe. Formatting: `.clang-format` and `.editorconfig` in this folder, copied from week09. No `make lint`; the format on save is enough.

C4 for this week. Use these names:

| Concept | Name | Do not use |
|---|---|---|
| Listening socket | `listen_fd` | `listenfd`, `sock`, `s` |
| Connected socket | `conn_fd` | `connfd`, `cfd` |
| Client-side socket | `client_fd` | `clientfd`, `fd` |
| Buffer and its length | `buffer`, `length` | `buf`, `n` |
| Address and its length | `addr`, `addr_len` | `sa`, `len` |

- Standard C and POSIX only. No `csapp.c`, no wrappers from the book.
- Build with the `Makefile` in this folder: `make NN-topic/name` builds `NN-topic/name.c`.
