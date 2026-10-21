#!/usr/bin/env python3
"""Extract "His signals" audit candidates from Claude Code transcripts.

Design: ~/.claude/plans/signals-audit/FINAL.md. The script only extracts and
counts; a judging subagent decides each case (jungle-close step 9).

  signals-audit.py scan [--force] [--root DIR] [--since YYYY-MM-DD]
      Gate on signals/state.json, then write candidates to stdout as JSON.
      Prints {"skip": days} when the last report is < 14 days old.
  signals-audit.py record DATE COUNTS_JSON
      After the report is written: set last_report, append the counts.
"""
import datetime as dt, glob, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(REPO, 'signals', 'state.json')
ROOT = os.path.expanduser('~/.claude/projects')
GLOB = '-home-benjohnbill-dev-krafton-jungle*/*.jsonl'
MIN_GAP, WARN_GAP, RETIRE_DAYS, SAMPLE = 14, 25, 60, 120
SIGNALS = ('numbered', 'stall', 'walkthrough', 'probe')

SKIP_PREFIX = ('<command-', '<local-command', '<system-reminder', 'Caveat:',
               '<bash-', '<task-notification', 'Base directory for this skill',
               'This session is being continued', '[Request interrupted',
               'Another Claude session sent a message')
AGENT_PROMPT = re.compile(r'^(Read \S*BRIEF\.md|Designer answer:)')
STALL = re.compile(r'솔직히.{0,20}(이해|모르)|이해(를|가)?\s*(못\s*했|안\s*(돼|되|가))|고민했는데|감이 안')
WALK = re.compile(r'한\s*줄씩|line by line|따라가면서|검증받|순서를 내가|내가 말할\s*테니|여기까지 맞')
LIST_ITEM = re.compile(r'^\s*(?:[-*]\s*)?\**(\d{1,2})[.)]\**\s')
NOT_EXERCISE = re.compile(r'/(lab|notes|docs|\.claude|signals|scripts|skills|tests)/')
CODE_FILE = re.compile(r'\.(c|h|S|cpp|py|js|ts)$')


def load_state():
    try:
        with open(STATE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {'last_report': None, 'history': [], 'rows': []}


def human_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        if any(isinstance(b, dict) and b.get('type') == 'tool_result' for b in content):
            return None
        return '\n'.join(b.get('text', '') for b in content
                         if isinstance(b, dict) and b.get('type') == 'text')
    return None


def sessions(root, since):
    """Yield (session id, ordered events) per transcript file."""
    for path in glob.glob(os.path.join(root, GLOB)):
        if os.path.getmtime(path) < since.timestamp():
            continue
        events, seen = [], set()
        for line in open(path, errors='ignore'):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get('isSidechain') or d.get('isMeta') or d.get('isCompactSummary'):
                continue
            ts = d.get('timestamp', '')
            if ts < since.strftime('%Y-%m-%dT%H:%M'):
                continue
            meta = {'ts': ts[:16], 'sid': (d.get('sessionId') or '')[:8],
                    'cwd': d.get('cwd'), 'branch': d.get('gitBranch')}
            msg = d.get('message') or {}
            if d.get('type') == 'user':
                text = (human_text(msg.get('content')) or '').strip()
                if not text or text.startswith(SKIP_PREFIX):
                    continue
                ev = dict(meta, kind='U', text=text)
            elif d.get('type') == 'assistant':
                for b in msg.get('content') or []:
                    if not isinstance(b, dict):
                        continue
                    if b.get('type') == 'text' and b.get('text', '').strip():
                        ev = dict(meta, kind='A', text=b['text'])
                    elif b.get('type') == 'tool_use' and b.get('name') in ('Write', 'Edit', 'MultiEdit'):
                        ev = dict(meta, kind='W', text=str((b.get('input') or {}).get('file_path')))
                    else:
                        continue
                    key = (ev['ts'], ev['kind'], ev['text'][:300])
                    if key not in seen:
                        seen.add(key)
                        events.append(ev)
                continue
            else:
                continue
            key = (ev['ts'], ev['kind'], ev['text'][:300])
            if key not in seen:
                seen.add(key)
                events.append(ev)
        humans = [e for e in events if e['kind'] == 'U']
        if humans and AGENT_PROMPT.match(humans[0]['text']):
            continue
        if humans:
            yield events


def clip(text, n):
    text = ' '.join(text.split())
    return text if len(text) <= n else text[:n] + '…'


def numbering_collision(text):
    """True when one reply holds two numbered lists that reuse a number."""
    runs, last = [], None
    for line in text.splitlines():
        m = LIST_ITEM.match(line)
        if not m:
            continue
        n = int(m.group(1))
        if n == 1 and last is not None:
            runs.append(last)
        last = n
    return bool(runs)


def scan(root, since):
    cand = {s: [] for s in SIGNALS}
    humans = []
    n_human = 0
    for events in sessions(root, since):
        for i, e in enumerate(events):
            ref = {k: e[k] for k in ('ts', 'sid', 'cwd', 'branch')}
            if e['kind'] == 'A' and numbering_collision(e['text']):
                cand['numbered'].append(dict(ref, reply=clip(e['text'], 1500)))
            if e['kind'] == 'W' and e['text'].startswith(os.path.expanduser('~/dev/krafton-jungle/')) \
                    and CODE_FILE.search(e['text']) and not NOT_EXERCISE.search(e['text']):
                before = [x['text'] for x in events[:i] if x['kind'] == 'U'][-3:]
                cand['probe'].append(dict(ref, path=e['text'],
                                          prior=[clip(t, 300) for t in before]))
            if e['kind'] != 'U' or '<pasted_content' in e['text']:
                continue
            n_human += 1
            humans.append(dict(ref, human=clip(e['text'], 200)))
            nxt = [x['text'] for x in events[i + 1:i + 6] if x['kind'] == 'A'][:1]
            pair = dict(ref, human=clip(e['text'], 400), reply=clip(nxt[0], 800) if nxt else '')
            if STALL.search(e['text']):
                cand['stall'].append(pair)
            if WALK.search(e['text']):
                after = [dict(human=clip(x['text'], 300)) if x['kind'] == 'U'
                         else dict(reply=clip(x['text'], 500))
                         for x in events[i + 1:i + 12] if x['kind'] in 'UA']
                cand['walkthrough'].append(dict(pair, follow=after))
    # New-habit raw material: an even sample of his messages for the subagent.
    step = max(1, len(humans) // SAMPLE)
    return cand, humans[::step][:SAMPLE], n_human


def retirement(state):
    """Signals with zero candidates across reports spanning >= RETIRE_DAYS."""
    hist = state['history']
    if not hist:
        return []
    newest = dt.date.fromisoformat(hist[-1]['date'])
    window = [h for h in hist if (newest - dt.date.fromisoformat(h['date'])).days < RETIRE_DAYS + MIN_GAP]
    span = (newest - dt.date.fromisoformat(window[0]['date'])).days + MIN_GAP
    if span < RETIRE_DAYS:
        return []
    return [s for s in SIGNALS if all(h['counts'].get(s, 0) == 0 for h in window)]


def main(argv):
    state = load_state()
    if argv[:1] == ['record']:
        state['last_report'] = argv[1]
        state['history'].append({'date': argv[1], 'counts': json.loads(argv[2])})
        os.makedirs(os.path.dirname(STATE), exist_ok=True)
        with open(STATE, 'w') as f:
            json.dump(state, f, ensure_ascii=False, indent=1)
        return
    force = '--force' in argv
    root = argv[argv.index('--root') + 1] if '--root' in argv else ROOT
    today = dt.date.today()
    last = dt.date.fromisoformat(state['last_report']) if state['last_report'] else None
    gap = (today - last).days if last else None
    if gap is not None and gap < MIN_GAP and not force:
        print(json.dumps({'skip': gap}))
        return
    if '--since' in argv:
        since = dt.datetime.fromisoformat(argv[argv.index('--since') + 1])
    else:
        since = dt.datetime.combine(last or today - dt.timedelta(days=30), dt.time())
    cand, sample, n_human = scan(root, since)
    print(json.dumps({
        'since': since.date().isoformat(), 'gap_days': gap,
        'gap_warning': gap is not None and gap > WARN_GAP,
        'human_messages': n_human,
        'counts': {s: len(v) for s, v in cand.items()},
        'candidates': cand, 'message_sample': sample,
        'retirement': retirement(state),
        'pending_rows': [r for r in state['rows'] if r.get('status') == 'pending'],
        'declined_rows': [r for r in state['rows'] if r.get('status') == 'declined'],
    }, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main(sys.argv[1:])
