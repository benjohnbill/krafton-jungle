// Reusable state stepper.
// mountStepper(root, { fields: [{key, label, scope}], steps: [{phase, title, code, note, state, predict}] })
// Each step's `state` holds every field value as a string. Changed fields are highlighted.
// Optional `predict: { key, q, options: [..] }` hides that field as "?" until the learner picks.
// The right option is the step's own state[key].
function mountStepper(root, spec) {
  const css = `
    .stepper { border: 1px solid var(--rule); border-radius: 6px; padding: 1rem 1.2rem; margin: 1rem 0; background: transparent; }
    .stepper .head { display: flex; flex-wrap: wrap; gap: .6rem; align-items: center; }
    .stepper .title { font-weight: 600; }
    .stepper .count { margin-left: auto; color: var(--muted); font: .85rem var(--mono); }
    .stepper pre { margin: .6rem 0; }
    .stepper .note { margin: .4rem 0 .8rem; }
    .stepper .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr)); gap: 1rem; }
    .stepper .grid > * { min-width: 0; }
    .stepper .box h4 { margin: 0 0 .3rem; font-size: .85rem; color: var(--muted); font-weight: 600; }
    .stepper .row { display: flex; justify-content: space-between; gap: 1rem; padding: .15rem .4rem; border-radius: 3px; font: .9rem var(--mono); }
    .stepper .row span { min-width: 0; overflow-wrap: anywhere; }
    .stepper .row.changed { background: var(--hi); }
    .stepper .controls { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1rem; }
    .stepper button { font: inherit; padding: .3rem .9rem; border: 1px solid var(--rule); background: var(--paper); border-radius: 4px; cursor: pointer; }
    .stepper button:disabled { opacity: .4; cursor: default; }
    .stepper .predict { border: 1px dashed var(--read); border-radius: 4px; padding: .5rem .8rem; margin: .4rem 0 .8rem; }
    .stepper .predict .opts { display: flex; gap: .5rem; flex-wrap: wrap; margin-top: .4rem; }
    .stepper .predict .opts button { font-family: var(--mono); }
    .stepper .predict .fb { margin-top: .4rem; font-weight: 600; }
    .stepper .predict .fb.ok { color: var(--read); }
    .stepper .predict .fb.no { color: var(--write); }
    .stepper .row.hidden span:last-child { color: var(--read); font-weight: 700; }
  `;
  if (!document.getElementById("stepper-css")) {
    const s = document.createElement("style");
    s.id = "stepper-css";
    s.textContent = css;
    document.head.append(s);
  }
  let i = 0;
  const picked = {};
  root.classList.add("stepper");
  const scopes = [...new Set(spec.fields.map((f) => f.scope))];
  function render() {
    const step = spec.steps[i];
    const prev = i > 0 ? spec.steps[i - 1].state : null;
    const p = step.predict;
    const waiting = p && picked[i] === undefined;
    const boxes = scopes
      .map((scope) => {
        const rows = spec.fields
          .filter((f) => f.scope === scope)
          .map((f) => {
            const hide = waiting && f.key === p.key;
            const v = hide ? "?" : step.state[f.key];
            const changed = !hide && prev && prev[f.key] !== step.state[f.key];
            const cls = `row${changed ? " changed" : ""}${hide ? " hidden" : ""}`;
            return `<div class="${cls}"><span>${f.label}</span><span>${v}</span></div>`;
          })
          .join("");
        return `<div class="box"><h4>${scope}</h4>${rows}</div>`;
      })
      .join("");
    let predictHtml = "";
    if (p) {
      const answer = step.state[p.key];
      const opts = p.options
        .map((o) => `<button data-pick="${o}" ${waiting ? "" : "disabled"}>${o}</button>`)
        .join("");
      const fb = waiting
        ? ""
        : picked[i] === answer
          ? `<div class="fb ok">맞았어요: ${answer}</div>`
          : `<div class="fb no">고른 값 ${picked[i]} · 실제 값 ${answer}</div>`;
      predictHtml = `<div class="predict"><div>예측: ${p.q}</div><div class="opts">${opts}</div>${fb}</div>`;
    }
    root.innerHTML = `
      <div class="head">
        <span class="tag ${step.phase.toLowerCase()}">${step.phase}</span>
        <span class="title">${step.title}</span>
        <span class="count">${i + 1} / ${spec.steps.length}</span>
      </div>
      ${step.code ? `<pre>${step.code}</pre>` : ""}
      ${predictHtml}
      ${waiting ? "" : `<div class="note">${step.note}</div>`}
      <div class="grid">${boxes}</div>
      <div class="controls">
        <button data-d="-1" ${i === 0 ? "disabled" : ""}>← 이전</button>
        <button data-d="1" ${i === spec.steps.length - 1 ? "disabled" : ""}>다음 →</button>
        <button data-d="0">처음으로</button>
      </div>`;
    root.querySelectorAll("button[data-pick]").forEach((b) =>
      b.addEventListener("click", () => {
        picked[i] = b.dataset.pick;
        render();
      }),
    );
    root.querySelectorAll("button[data-d]").forEach((b) =>
      b.addEventListener("click", () => {
        const d = Number(b.dataset.d);
        i = d === 0 ? 0 : i + d;
        render();
      }),
    );
  }
  render();
  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight" && i < spec.steps.length - 1) { i++; render(); }
    if (e.key === "ArrowLeft" && i > 0) { i--; render(); }
  });
}
