// The four lanes of one request: client app, client kernel, server kernel,
// server app. Every lesson uses this element, so all lessons draw the same
// picture.
//
// <flow-lanes active="c-app c-kern s-kern" loopback>
//   <step from="c-app" to="c-kern">connect()</step>
//   <step from="c-kern" to="s-kern">SYN</step>
// </flow-lanes>
//
// active   lanes that act in this lesson; the others are dim
// loopback both kernel lanes are one kernel (localhost); drawn dashed
// blank  lane names hidden, for the recall drill at the start of a lesson
// <step>   one arrow, in time order; from/to = c-app c-kern s-kern s-app dns
const LANES = [
  ["c-app", "client 앱", "app"],
  ["c-kern", "client 커널", "kernel"],
  ["s-kern", "서버 커널", "kernel"],
  ["s-app", "서버 앱", "app"],
];

const LANE_NAME = Object.fromEntries(LANES.map(([id, name]) => [id, name]));
LANE_NAME.dns = "DNS";

class FlowLanes extends HTMLElement {
  connectedCallback() {
    if (this.dataset.drawn) return;
    this.dataset.drawn = "1";
    const active = (this.getAttribute("active") || "").split(/\s+/);
    const loopback = this.hasAttribute("loopback");
    const blank = this.hasAttribute("blank");
    const steps = [...this.querySelectorAll("step")].map((s) => ({
      from: s.getAttribute("from"),
      to: s.getAttribute("to"),
      html: s.innerHTML,
    }));

    const lanes = LANES.map(([id, name, kind]) => {
      const cls = ["ln", kind];
      if (active.includes(id)) cls.push("on");
      if (loopback && kind === "kernel") cls.push("one");
      return `<div class="${cls.join(" ")}"><b>${blank ? "?" : name}</b></div>`;
    }).join("");

    const rows = steps
      .map(
        (s, n) =>
          `<li><span class="n">${n + 1}</span>${LANE_NAME[s.from] || s.from} → ` +
          `${LANE_NAME[s.to] || s.to}: ${s.html}</li>`,
      )
      .join("");

    const note = loopback
      ? `<p class="note">점선 = localhost(lo)라서 두 커널 칸이 같은 커널 하나다.</p>`
      : "";

    this.innerHTML =
      `<div class="fl-row">${lanes}</div>` +
      `<div class="fl-bd"><span>│ syscall</span><span></span><span></span><span>syscall │</span></div>` +
      (rows ? `<ol class="fl-steps">${rows}</ol>` : "") +
      note;
  }
}

if (!document.getElementById("flow-lanes-css")) {
  const s = document.createElement("style");
  s.id = "flow-lanes-css";
  s.textContent = `
    flow-lanes { display: block; margin: 1.2rem 0; }
    flow-lanes .fl-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: .5rem; }
    flow-lanes .ln { border: 1.5px solid var(--rule); border-radius: 6px; padding: .5rem .3rem; text-align: center; color: var(--muted); }
    flow-lanes .ln.on { border-color: var(--write); color: var(--ink); background: var(--write-soft, #fbf1ee); }
    flow-lanes .ln.one { border-style: dashed; }
    flow-lanes .fl-bd { display: grid; grid-template-columns: repeat(4, 1fr); font-size: .8rem; color: var(--muted); margin-top: .2rem; }
    flow-lanes .fl-bd span:last-child { text-align: right; }
    flow-lanes .fl-steps { list-style: none; padding: 0; margin: .8rem 0 0; border-top: 1px solid var(--rule); padding-top: .5rem; }
    flow-lanes .fl-steps li { padding: .15rem 0; }
    flow-lanes .n { display: inline-block; width: 1.4rem; color: var(--write); font-weight: 600; }
    flow-lanes .note { font-size: .9rem; color: var(--muted); margin: .5rem 0 0; }
  `;
  document.head.append(s);
}

customElements.define("flow-lanes", FlowLanes);
