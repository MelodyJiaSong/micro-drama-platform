/* t13 各场景共用的构件：旋钮、齿轮、两层小网络。数据来自 scenes/data.json（data.py 算出）；颜色一律取设计规范变量（tokens.css）。
   旋钮是第 1 季统一画法（s1_bible「画面」）：圆盘、一根指针、下面标读数（照 t10 的样子，本期自己画一份）。
   颜色含义：正着算（数往前走）= 琥珀；错误、往回传的责任 = 红；对上了 / 更准了 = 绿。 */
const D = EDU.S.data;
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const SVGNS = "http://www.w3.org/2000/svg";
const A0 = -135, A1 = 135;
const pol = (cx, cy, r, deg) => [cx + r * Math.sin(deg * Math.PI / 180), cy - r * Math.cos(deg * Math.PI / 180)];
function arcPath(cx, cy, r, a, b) {
  if (b - a < 0.01) b = a + 0.01;
  const [x0, y0] = pol(cx, cy, r, a), [x1, y1] = pol(cx, cy, r, b);
  return `M${x0},${y0} A${r},${r} 0 ${b - a > 180 ? 1 : 0} 1 ${x1},${y1}`;
}

/* 旋钮：opt = size、min、max、value、fmt、left / top（中心点，相对 parent）、readingSize */
function knob(parent, opt = {}) {
  const o = Object.assign({ size: 110, min: 0, max: 10, value: 0, fmt: v => v.toFixed(1), left: 0, top: 0, ticks: 11, readingSize: null }, opt);
  const host = typeof parent === "string" ? document.querySelector(parent) : parent;
  const el = document.createElement("div");
  el.className = "knob";
  const S = o.size, c = S / 2, rDisc = S * 0.40, rArc = S * 0.47, w = Math.max(3, S * 0.035);
  Object.assign(el.style, { position: "absolute", left: (o.left - S / 2) + "px", top: (o.top - S / 2) + "px", width: S + "px",
                            display: "flex", flexDirection: "column", alignItems: "center" });
  const svg = document.createElementNS(SVGNS, "svg");
  svg.setAttribute("width", S); svg.setAttribute("height", S); svg.style.overflow = "visible";
  const fid = "ks" + Math.round(Math.random() * 1e9);
  svg.innerHTML = `
    <defs><filter id="${fid}" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="${S * 0.03}" stdDeviation="${S * 0.04}" flood-color="#1D1D1F" flood-opacity=".12"/></filter></defs>
    <path d="${arcPath(c, c, rArc, A0, A1)}" fill="none" stroke="${css("--hair")}" stroke-width="${w}" stroke-linecap="round"/>
    <path class="k-fill" fill="none" stroke="${css("--accent")}" stroke-width="${w}" stroke-linecap="round"/>
    <g class="k-ticks"></g>
    <circle cx="${c}" cy="${c}" r="${rDisc}" fill="${css("--surface")}" stroke="${css("--hair")}" stroke-width="${Math.max(1.5, S * 0.008)}" filter="url(#${fid})"/>
    <g class="k-ptr"><line x1="${c}" y1="${c}" x2="${c}" y2="${c - rDisc * 0.78}" stroke="${css("--ink")}" stroke-width="${Math.max(4, S * 0.05)}" stroke-linecap="round"/></g>
    <circle cx="${c}" cy="${c}" r="${Math.max(4, S * 0.05)}" fill="${css("--accent")}"/>`;
  const tg = svg.querySelector(".k-ticks");
  for (let i = 0; i < o.ticks; i++) {
    const a = A0 + (A1 - A0) * i / (o.ticks - 1), [x0, y0] = pol(c, c, rDisc * 0.86, a), [x1, y1] = pol(c, c, rDisc * (i % 5 === 0 ? 0.70 : 0.76), a);
    const t = document.createElementNS(SVGNS, "line");
    Object.entries({ x1: x0, y1: y0, x2: x1, y2: y1, stroke: css("--faint"), "stroke-width": Math.max(1.5, S * 0.012), "stroke-linecap": "round" })
      .forEach(([k, v]) => t.setAttribute(k, v));
    tg.appendChild(t);
  }
  const ptr = svg.querySelector(".k-ptr"), fill = svg.querySelector(".k-fill");
  const rd = document.createElement("div");
  rd.className = "knob-reading";
  Object.assign(rd.style, { fontSize: (o.readingSize || Math.max(28, S * 0.26)) + "px", fontWeight: 700, color: "var(--ink)", whiteSpace: "nowrap",
                            marginTop: S * 0.02 + "px", fontVariantNumeric: "tabular-nums" });
  el.append(svg, rd);
  host.appendChild(el);
  const api = {
    el, svg, reading: rd, value: o.value,
    set(v) {
      api.value = v;
      const k = Math.max(0, Math.min(1, (v - o.min) / (o.max - o.min))), a = A0 + (A1 - A0) * k;
      ptr.setAttribute("transform", `rotate(${a} ${c} ${c})`);
      fill.setAttribute("d", arcPath(c, c, rArc, A0, a));
      fill.style.opacity = k < 0.004 ? 0 : 1;
      rd.textContent = o.fmt(v);
    },
    turn(at, from, to, d = 1.2, then = null) {
      const s = { v: from };
      return EDU.tl.fromTo(s, { v: from }, { v: to, duration: d, ease: "power2.inOut", immediateRender: false,
        onUpdate: () => { api.set(s.v); if (then) then(s.v); } }, at);
    },
    /* 轻轻来回拧一下（试拧） */
    wiggle(at, amp = 0.6, d = 0.5) {
      const s = { v: api.value }, v0 = api.value;
      return EDU.tl.to(s, { keyframes: [{ v: v0 + amp, duration: d / 2 }, { v: v0, duration: d / 2 }], ease: "power1.inOut",
        onUpdate: () => { const keep = api.value; api.set(s.v); rd.textContent = o.fmt(keep); api.value = keep; } }, at);
    },
  };
  api.set(o.value);
  return api;
}

/* 齿轮外形：中心 (0,0)、半径 r、齿数 n */
function gearPath(r, n, depth = 14) {
  const pts = [], ro = r + depth / 2, ri = r - depth / 2;
  for (let i = 0; i < n; i++) {
    const a = (i / n) * 2 * Math.PI, s = (2 * Math.PI / n);
    [[ri, a], [ro, a + s * 0.12], [ro, a + s * 0.45], [ri, a + s * 0.57]].forEach(([rr, aa]) => pts.push([rr * Math.cos(aa), rr * Math.sin(aa)]));
  }
  return "M" + pts.map(p => p.map(v => v.toFixed(1)).join(",")).join("L") + "Z";
}

/* 数字从 from 滚到 to；fmt 缺省整数或去掉末尾 0 */
const trim2 = v => v.toFixed(2).replace(/\.?0+$/, "");
function countTo(el, at, from, to, d = .8, fmt = trim2) {
  const o = { v: from };
  return EDU.tl.fromTo(o, { v: from }, { v: to, duration: d, ease: "power2.out", immediateRender: false, onUpdate: () => { el.textContent = fmt(o.v); } }, at);
}

/* 小红牌：某个旋钮分到的责任 */
function pill(parent, text, left, top, cls = "pill") {
  const el = document.createElement("div");
  el.className = cls; el.textContent = text;
  Object.assign(el.style, { position: "absolute", left: left + "px", top: top + "px", transform: "translateX(-50%)" });
  (typeof parent === "string" ? document.querySelector(parent) : parent).appendChild(el);
  return el;
}
