Mode: transcription, light. This mode applies inside `week13/lab/` only. It replaces the AI-together mode of `../CLAUDE.md` in this folder. The team repository `../mini-webserver/` keeps AI-together.

# CLAUDE.md — week13 lab (hands-on probes)

He does not read CSAPP chapter 11. He builds base knowledge for the web server week by direct experience: CLI tools first, then small C programs that he types. The questions from the lab feed the team prototype. Settled by grilling, 2026-11-19 (user said).

## Loop

Source: `../../docs/transcription-mode.md` Part 1, with these parts only:

- The agent writes the probe. He types C code one hunk at a time and asks questions. A short function goes whole.
- Each probe ends with a change task that he does alone, with no hint. A prediction before the run is optional, one line.
- He writes code comments, and only a comment that meets both conditions in `transcription-mode.md` § The sheet: the code alone does not show it, and the reason is not obvious.
- Breaks: when he asks to break something, make the broken version, and he follows its flow.
- No stage sheet and no D or I rows. Open questions go to `QUESTIONS.md`, one line each, with the probe number.

Done for a probe: he can say why each line or command exists, in his own words.

## Probe folders

- One concept per folder: `NN-topic/` (for example `05-strace/`). One C file per probe, 300 lines at most.
- Each folder has a `README.md` in the mixed form (`~/.claude/docs/document-language.md`) with four sections: 실행할 명령, 볼 것, 혼자 하는 변경 과제, 내 문장. He writes 내 문장.
- Order of tracks: T1 CLI, T2 socket C, T3 TCP behavior, T4 HTTP server, T5 concurrency, T6 proxy. Quality checks (valgrind, ASan, malformed requests) go inside T4 to T6. `README.md` in this folder lists the tracks.

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
