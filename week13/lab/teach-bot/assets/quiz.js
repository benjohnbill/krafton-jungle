// Reusable quiz with immediate feedback, plus predictions and one copy block.
// Base: week11-12/lab/teach/assets/quiz.js.
//
// mountQuiz(root, items, lesson?)
//   items:  [{ q, options: [..], answer: index, why }]
//   lesson: { id, title, next, record, predictions: [question, ..] }
// With `lesson`, the page keeps picks and prediction text in this browser
// (localStorage) and shows a button that copies them as markdown for a
// Claude session. The first pick locks a question.
// window.QUIZ_SEED[lesson.id] = { picks, notes, date }: answers the published
// copy shows when this browser has none of its own (publish/build.py adds it).
function mountQuiz(root, items, lesson) {
  if (!document.getElementById("quiz-css")) {
    const s = document.createElement("style");
    s.id = "quiz-css";
    s.textContent = `
      .quiz .item { margin: 1.2rem 0; }
      .quiz .q { font-weight: 600; margin-bottom: .4rem; }
      .quiz button.opt { display: block; width: 100%; text-align: left; font: inherit; margin: .25rem 0; padding: .4rem .8rem; border: 1px solid var(--rule); background: transparent; color: inherit; border-radius: 4px; cursor: pointer; }
      .quiz button.right { border-color: var(--read); background: var(--read-soft, #e8f3f6); }
      .quiz button.wrong { border-color: var(--write); background: var(--write-soft, #fbf1ee); }
      .quiz .why { color: var(--muted); font-size: .95rem; margin-top: .3rem; }
      .quiz .score { font-weight: 600; margin-top: 1rem; }
      .quiz .seed { font-weight: 600; }
      .quiz textarea { display: block; width: 100%; box-sizing: border-box; min-height: 3.2rem; font: inherit; padding: .4rem .6rem; border: 1px solid var(--rule); border-radius: 4px; background: transparent; color: inherit; }
      .quiz .copy { margin-top: 1.2rem; text-align: right; }
      .quiz .copy button { font: inherit; font-weight: 600; padding: .45rem 1rem; border-radius: 6px; border: 1px solid var(--ink); background: var(--ink); color: var(--paper); cursor: pointer; }
      .quiz .copy small { color: var(--muted); margin-right: .6rem; }
      .quiz .copy textarea { margin-top: .6rem; }
    `;
    document.head.append(s);
  }

  const key = lesson ? "teach:" + lesson.id : null;
  const seed = lesson && window.QUIZ_SEED ? window.QUIZ_SEED[lesson.id] : null;
  let seeded = false;
  const state = load();

  function load() {
    const empty = { picks: {}, notes: {} };
    if (!key) return empty;
    let stored = null;
    try {
      stored = JSON.parse(localStorage.getItem(key));
    } catch {}
    if (stored) return stored;
    if (seed) {
      seeded = true;
      return { picks: { ...seed.picks }, notes: { ...seed.notes } };
    }
    return empty;
  }

  function save() {
    if (!key) return;
    try {
      localStorage.setItem(key, JSON.stringify(state));
    } catch {}
  }

  root.classList.add("quiz");
  if (seeded) {
    const from = document.createElement("p");
    from.className = "seed";
    from.textContent = `아래 선택과 주관식 답은 ${seed.date}에 직접 고르고 쓴 답이다.`;
    root.append(from);
  }
  let done = 0;
  let right = 0;
  const score = document.createElement("div");
  score.className = "score";

  function showScore() {
    if (done === items.length) score.textContent = `${items.length}문제 중 ${right}개 맞음`;
  }

  items.forEach((it, n) => {
    const box = document.createElement("div");
    box.className = "item";
    box.innerHTML = `<div class="q">${n + 1}. ${it.q}</div>`;
    const why = document.createElement("div");
    why.className = "why";
    const buttons = [];

    function pick(k, restoring) {
      if (box.dataset.done) return;
      box.dataset.done = "1";
      done++;
      if (k === it.answer) right++;
      buttons[k].classList.add(k === it.answer ? "right" : "wrong");
      buttons[it.answer].classList.add("right");
      why.innerHTML = it.why;
      if (!restoring) {
        state.picks[n] = k;
        save();
      }
      showScore();
    }

    it.options.forEach((opt, k) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "opt";
      b.innerHTML = opt;
      b.addEventListener("click", () => pick(k, false));
      buttons.push(b);
      box.append(b);
    });
    box.append(why);
    root.append(box);
    if (state.picks[n] !== undefined) pick(state.picks[n], true);
  });
  root.append(score);

  if (!lesson) return;

  (lesson.predictions || []).forEach((q, n) => {
    const box = document.createElement("div");
    box.className = "item";
    box.innerHTML = `<div class="q">주관식 ${n + 1}. ${q}</div>`;
    const ta = document.createElement("textarea");
    ta.value = state.notes[n] || "";
    ta.addEventListener("input", () => {
      state.notes[n] = ta.value;
      save();
    });
    box.append(ta);
    root.append(box);
  });

  const bar = document.createElement("div");
  bar.className = "copy";
  const msg = document.createElement("small");
  const btn = document.createElement("button");
  btn.type = "button";
  btn.textContent = "답안 복사";
  btn.addEventListener("click", async () => {
    const md = toMarkdown();
    try {
      await navigator.clipboard.writeText(md);
      msg.textContent = "복사했어요. Claude 세션에 붙여 넣으세요.";
    } catch {
      // Fallback: show the text so it can be selected and copied by hand.
      let ta = bar.querySelector("textarea");
      if (!ta) {
        ta = document.createElement("textarea");
        ta.readOnly = true;
        bar.append(ta);
      }
      ta.value = md;
      ta.style.minHeight = "12rem";
      ta.select();
      msg.textContent = "자동 복사가 막혔어요. 아래 글을 직접 복사하세요.";
    }
  });
  bar.prepend(msg, btn);
  root.append(bar);

  function plain(html) {
    const d = document.createElement("div");
    d.innerHTML = html;
    return d.textContent.trim();
  }

  function toMarkdown() {
    const lines = [`# ${lesson.title || lesson.id} · 답안`];
    if (lesson.next) lines.push(`- 다음 probe: ${lesson.next}`);
    if (lesson.record) lines.push(`- 문답 정리: ${lesson.record}`);
    lines.push("", "## 퀴즈");
    items.forEach((it, n) => {
      const k = state.picks[n];
      const q = `${n + 1}. ${plain(it.q)} → `;
      if (k === undefined) lines.push(q + "(안 풂)");
      else if (k === it.answer) lines.push(q + `${plain(it.options[k])} ✓`);
      else lines.push(q + `${plain(it.options[k])} ✗ (정답: ${plain(it.options[it.answer])})`);
    });
    if ((lesson.predictions || []).length) {
      lines.push("", "## 주관식");
      lesson.predictions.forEach((q, n) => {
        const a = (state.notes[n] || "").trim() || "(비어 있음)";
        lines.push(`${n + 1}. ${plain(q)} → ${a}`);
      });
    }
    return lines.join("\n") + "\n";
  }
}
