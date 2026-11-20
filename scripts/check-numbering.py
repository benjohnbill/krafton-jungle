#!/usr/bin/env python3
"""Stop hook: block a reply that has two numbered lists.

Rule: docs/tutor-spine.md, "Numbered negotiation" (one number sequence per
reply; numbered bold headings count as a list). Signals audit row
numbered-headings-still-numbered, accepted 2026-11-21.

Input: the Stop hook JSON on stdin. Acts only when cwd is under
~/dev/krafton-jungle. Output: {"decision": "block", "reason": ...} when the
last reply has more than one top-level number sequence; nothing otherwise.

Self-test: check-numbering.py --test
"""
import json
import os
import re
import sys

ROOT = os.path.expanduser("~/dev/krafton-jungle")

# Top-level numbered line: "1. x", "**1. x**", "## 1. x". Indented lines are
# sub-lists inside an item and do not start a new sequence.
NUMBERED = re.compile(r"^(?:#{1,6}\s+)?(?:\*\*)?(\d+)[.)]\s")
FENCE = re.compile(r"^\s*(```|~~~)")


def find_sequences(text):
    """Return a list of number sequences found outside code fences."""
    sequences = []
    in_fence = False
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = NUMBERED.match(line)
        if not match:
            continue
        number = int(match.group(1))
        if not sequences or number <= sequences[-1][-1]:
            sequences.append([number])
        else:
            sequences[-1].append(number)
    return sequences


def is_real_prompt(entry):
    """A user entry typed by him, not a tool result."""
    if entry.get("type") != "user" or entry.get("isMeta"):
        return False
    content = entry.get("message", {}).get("content")
    if isinstance(content, str):
        return True
    return any(part.get("type") == "text" for part in content or [])


def get_last_reply(transcript_path):
    """Join the assistant text written since his last prompt."""
    entries = []
    with open(transcript_path, encoding="utf-8") as transcript:
        for line in transcript:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    texts = []
    for entry in reversed(entries):
        if is_real_prompt(entry):
            break
        if entry.get("type") != "assistant" or entry.get("isSidechain"):
            continue
        for part in entry.get("message", {}).get("content") or []:
            if part.get("type") == "text":
                texts.append(part["text"])
    return "\n".join(reversed(texts))


def main():
    hook_input = json.load(sys.stdin)
    if hook_input.get("stop_hook_active"):
        return
    cwd = os.path.realpath(hook_input.get("cwd") or os.getcwd())
    if not (cwd + "/").startswith(ROOT + "/"):
        return
    reply = hook_input.get("last_assistant_message")
    if not isinstance(reply, str):
        path = hook_input.get("transcript_path")
        if not path or not os.path.exists(path):
            return
        reply = get_last_reply(path)
    sequences = find_sequences(reply)
    if len(sequences) < 2:
        return
    shown = " / ".join(",".join(map(str, s)) for s in sequences)
    print(json.dumps({
        "decision": "block",
        "reason": (
            f"Your last reply has {len(sequences)} numbered lists ({shown}). "
            "tutor-spine Numbered negotiation: one number sequence per reply. "
            "Only the decision list keeps numbers; findings, steps, and "
            "headings use bullets or a bold word. Send the reply again, "
            "corrected, and say in one line that it replaces the last one."
        ),
    }, ensure_ascii=False))


def self_test():
    cases = [
        ("1. a\n2. b\n", 1),
        ("1. a\n2. b\n\ntext\n\n1. c\n", 2),
        ("**1. title**\nx\n**2. title**\n1. pick\n2. pick\n", 2),
        ("1. a\n   1. sub\n   2. sub\n2. b\n", 1),
        ("```\n1. code\n```\n1. a\n2. b\n", 1),
        ("- a\n- b\n", 0),
        ("1. a\n2. b\n3. c\n4. d\n5. e\n6. f\n", 1),
    ]
    for text, expected in cases:
        got = len(find_sequences(text))
        assert got == expected, (text, got, expected)
    print("self-test ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--test"]:
        self_test()
    else:
        main()
