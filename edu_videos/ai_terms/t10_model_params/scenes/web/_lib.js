/* t10 各场景共用的构件：旋钮、机器、打车散点图。数据来自 scenes/data.json（data.py 算出）；颜色一律取设计规范变量（tokens.css）。
   旋钮是第 1 季统一画法（s1_bible「画面」）：圆盘、一根指针、下面标读数。
     - 圆盘：白底（--surface）、细边（--hair）、柔和投影；刻度弧 270°（左下 −135° 到右下 +135°），11 根刻度。
     - 已拧过的那段弧用琥珀（--accent），没拧到的留浅灰（--hair）；指针墨黑（--ink）圆头，圆心琥珀小圆点。
     - 名字在圆盘上方（小号灰字），读数在圆盘下方（大号、等宽数字、可带单位）。
   颜色含义：数据点 = 墨黑，模型直线 = 琥珀，「差多少」的竖线 = 猜少了红 / 猜多了紫（--d-valid），拧到合适 = 绿。 */
const D = EDU.S.data;
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const SVGNS = "http://www.w3.org/2000/svg";
const A0 = -135, A1 = 135;             // 刻度弧的起止角（度，0 = 正上方，顺时针为正）

/* 极坐标 → 平面（角度 0 朝上、顺时针） */
const pol = (cx, cy, r, deg) => [cx + r * Math.sin(deg * Math.PI / 180), cy - r * Math.cos(deg * Math.PI / 180)];
function arcPath(cx, cy, r, a, b) {
  if (b - a < 0.01) b = a + 0.01;
  const [x0, y0] = pol(cx, cy, r, a), [x1, y1] = pol(cx, cy, r, b);
  return `M${x0},${y0} A${r},${r} 0 ${b - a > 180 ? 1 : 0} 1 ${x1},${y1}`;
}

/* 在 parent（元素或选择器）里放一个旋钮。
   opt：size（圆盘直径 px）、min / max、value、label（HTML，已按语言取好）、unit（读数后的小字）、fmt（读数格式）、
        left / top（绝对定位，相对 parent）、showLabel / showReading（缺省都显示）、ticks（刻度数，缺省 11）。
   返回 api：el（外层 div）、set(v) 立即设、turn(at, from, to, d) 在时间线上拧、value。 */
function knob(parent, opt = {}) {
  const o = Object.assign({ size: 220, min: 0, max: 10, value: 0, label: "", unit: "", fmt: v => v.toFixed(1),
                            left: 0, top: 0, showLabel: true, showReading: true, ticks: 11, readingSize: null }, opt);
  const host = typeof parent === "string" ? document.querySelector(parent) : parent;
  const el = document.createElement("div");
  el.className = "knob";
  Object.assign(el.style, { position: "absolute", left: o.left + "px", top: o.top + "px", width: o.size + "px",
                            display: "flex", flexDirection: "column", alignItems: "center" });
  const S = o.size, c = S / 2, rDisc = S * 0.40, rArc = S * 0.47, w = Math.max(3, S * 0.035);
  const lab = document.createElement("div");
  lab.className = "knob-label"; lab.innerHTML = o.label;
  Object.assign(lab.style, { fontSize: Math.max(22, S * 0.13) + "px", fontWeight: 600, color: "var(--sub)", whiteSpace: "nowrap",
                             marginBottom: S * 0.04 + "px", display: o.showLabel && o.label ? "block" : "none" });
  const svg = document.createElementNS(SVGNS, "svg");
  svg.setAttribute("width", S); svg.setAttribute("height", S);
  svg.style.overflow = "visible";
  svg.innerHTML = `
    <defs><filter id="ks${Math.round(Math.random() * 1e9)}" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="${S * 0.03}" stdDeviation="${S * 0.04}" flood-color="#1D1D1F" flood-opacity=".12"/></filter></defs>
    <path class="k-track" d="${arcPath(c, c, rArc, A0, A1)}" fill="none" stroke="${css("--hair")}" stroke-width="${w}" stroke-linecap="round"/>
    <path class="k-fill" fill="none" stroke="${css("--accent")}" stroke-width="${w}" stroke-linecap="round"/>
    <g class="k-ticks"></g>
    <circle class="k-disc" cx="${c}" cy="${c}" r="${rDisc}" fill="${css("--surface")}" stroke="${css("--hair")}" stroke-width="${Math.max(1.5, S * 0.008)}"/>
    <g class="k-ptr"><line x1="${c}" y1="${c}" x2="${c}" y2="${c - rDisc * 0.78}" stroke="${css("--ink")}" stroke-width="${Math.max(4, S * 0.05)}" stroke-linecap="round"/></g>
    <circle cx="${c}" cy="${c}" r="${Math.max(4, S * 0.05)}" fill="${css("--accent")}"/>`;
  const filt = svg.querySelector("filter");
  svg.querySelector(".k-disc").setAttribute("filter", `url(#${filt.id})`);
  const tg = svg.querySelector(".k-ticks");
  for (let i = 0; i < o.ticks; i++) {
    const a = A0 + (A1 - A0) * i / (o.ticks - 1), [x0, y0] = pol(c, c, rDisc * 0.86, a), [x1, y1] = pol(c, c, rDisc * (i % 5 === 0 ? 0.70 : 0.76), a);
    const t = document.createElementNS(SVGNS, "line");
    t.setAttribute("x1", x0); t.setAttribute("y1", y0); t.setAttribute("x2", x1); t.setAttribute("y2", y1);
    t.setAttribute("stroke", css("--faint")); t.setAttribute("stroke-width", Math.max(1.5, S * 0.012)); t.setAttribute("stroke-linecap", "round");
    tg.appendChild(t);
  }
  const ptr = svg.querySelector(".k-ptr"), fill = svg.querySelector(".k-fill");
  const rd = document.createElement("div");
  rd.className = "knob-reading";
  Object.assign(rd.style, { fontSize: (o.readingSize || Math.max(28, S * 0.22)) + "px", fontWeight: 700, color: "var(--ink)", whiteSpace: "nowrap",
                            marginTop: S * 0.02 + "px", fontVariantNumeric: "tabular-nums", display: o.showReading ? "block" : "none" });
  rd.innerHTML = `<span class="v"></span><span class="u" style="font-size:.5em;font-weight:500;color:var(--sub);margin-left:.18em">${o.unit}</span>`;
  const rv = rd.querySelector(".v");
  el.append(lab, svg, rd);
  host.appendChild(el);
  const api = {
    el, svg, label: lab, reading: rd, value: o.value,
    set(v) {
      api.value = v;
      const k = Math.max(0, Math.min(1, (v - o.min) / (o.max - o.min))), a = A0 + (A1 - A0) * k;
      ptr.setAttribute("transform", `rotate(${a} ${c} ${c})`);
      fill.setAttribute("d", arcPath(c, c, rArc, A0, a));
      fill.style.opacity = k < 0.004 ? 0 : 1;
      rv.textContent = o.fmt(v);
    },
    /* 在时间线上把旋钮从 from 拧到 to（onUpdate 同时调 then(v)，好让图跟着动） */
    turn(at, from, to, d = 1.2, then = null) {
      const s = { v: from };
      return EDU.tl.fromTo(s, { v: from }, { v: to, duration: d, ease: "power2.inOut", immediateRender: false,
        onUpdate: () => { api.set(s.v); if (then) then(s.v); } }, at);
    },
  };
  api.set(o.value);
  return api;
}

/* 打车散点图：横轴公里、纵轴车费；模型直线（琥珀）、每趟一根「差多少」竖线。
   draw(base, perKm) 按当前两个读数重画直线与竖线。 */
function fareChart(sel, { W = 1000, H = 640, dom = D.domain } = {}) {
  const m = { l: 96, r: 30, t: 30, b: 86 };
  const svg = d3.select(sel).attr("width", W).attr("height", H);
  const x = d3.scaleLinear(dom.km, [m.l, W - m.r]), y = d3.scaleLinear(dom.fare, [H - m.b, m.t]);
  const g = svg.append("g");
  g.append("line").attr("class", "axis-base").attr("x1", m.l).attr("x2", W - m.r).attr("y1", y(0)).attr("y2", y(0));
  g.append("line").attr("class", "axis-base").attr("x1", m.l).attr("x2", m.l).attr("y1", y(0)).attr("y2", m.t);
  const tick = (t, xx, yy, anchor) => g.append("text").attr("x", xx).attr("y", yy).attr("text-anchor", anchor)
    .attr("font-size", 24).attr("fill", css("--sub")).text(t);
  [0, 4, 8, 12].forEach(k => tick(k, x(k), y(0) + 36, "middle"));
  [0, 20, 40].forEach(f => tick(f, m.l - 18, y(f) + 8, "end"));
  const axX = g.append("text").attr("x", W - m.r).attr("y", y(0) + 76).attr("text-anchor", "end").attr("font-size", 28)
    .attr("font-weight", 600).attr("fill", css("--ink2")).text(EDU.tr("距离（公里）", "Distance (km)")).node();
  const axY = g.append("text").attr("x", m.l - 6).attr("y", m.t - 6).attr("text-anchor", "start").attr("font-size", 28)
    .attr("font-weight", 600).attr("fill", css("--ink2")).attr("transform", `translate(${18},0)`).text(EDU.tr("车费（元）", "Fare ($)")).node();
  const cid = "clip" + sel.replace(/[^a-z0-9]/gi, "");
  svg.append("defs").append("clipPath").attr("id", cid).append("rect").attr("x", m.l).attr("y", m.t).attr("width", W - m.r - m.l).attr("height", y(0) - m.t);
  const gapG = svg.append("g").attr("clip-path", `url(#${cid})`), lineG = svg.append("g").attr("clip-path", `url(#${cid})`),
        dotG = svg.append("g"), over = svg.append("g");
  const gaps = D.rides.map(r => gapG.append("line").attr("x1", x(r.km)).attr("x2", x(r.km)).attr("stroke-width", 5)
    .attr("stroke-linecap", "round").node());
  const line = lineG.append("line").attr("stroke", css("--accent")).attr("stroke-width", 8).attr("stroke-linecap", "round").node();
  const dots = D.rides.map(r => dotG.append("circle").attr("cx", x(r.km)).attr("cy", y(r.fare)).attr("r", 12)
    .attr("fill", css("--ink")).attr("stroke", css("--bg")).attr("stroke-width", 4).node());
  const api = {
    svg, x, y, W, H, m, gaps, line, dots, over, axX, axY, gapG,
    good: 3.5,                                      // 竖线短于这个（元）就算「贴着」，画绿
    draw(base, k) {
      const x0 = dom.km[0], x1 = dom.km[1];
      line.setAttribute("x1", x(x0)); line.setAttribute("y1", y(base + k * x0));
      line.setAttribute("x2", x(x1)); line.setAttribute("y2", y(base + k * x1));
      D.rides.forEach((r, i) => {
        const p = base + k * r.km, e = gaps[i];
        e.setAttribute("y1", y(r.fare)); e.setAttribute("y2", y(p));
        e.setAttribute("stroke", css(p < r.fare ? "--d-bad" : "--d-valid"));
      });
    },
  };
  return api;
}

/* 把 GSAP 时间线上的一段「两个旋钮一起拧」接到图上：from / to 是 {base, per_km}，s 是共享状态 */
function turnBoth(K1, K2, chart, s, at, from, to, d = 1.4) {
  return EDU.tl.fromTo(s, { base: from.base, per_km: from.per_km }, { base: to.base, per_km: to.per_km, duration: d, ease: "power2.inOut",
    immediateRender: false, onUpdate: () => { K1.set(s.base); K2.set(s.per_km); if (chart) chart.draw(s.base, s.per_km); } }, at);
}

/* 数字从 from 滚到 to（EDU.count 只能从 0 起） */
function countTo(el, at, from, to, d = .8, fmt = v => v.toFixed(1)) {
  const o = { v: from };
  return EDU.tl.fromTo(o, { v: from }, { v: to, duration: d, ease: "power2.out", immediateRender: false, onUpdate: () => { el.textContent = fmt(o.v); } }, at);
}

/* 在时间线 at 处把 el 的文字换成 text（可来回 seek：之前显示上一个文字）。按建时间线的先后记住每个元素的上一个文字。 */
function setText(el, at, text, html = false) {
  const e = typeof el === "string" ? document.querySelector(el) : el;
  const prev = e.__last ?? (html ? e.innerHTML : e.textContent);
  e.__last = text;
  const o = { p: 0 };
  return EDU.tl.fromTo(o, { p: 0 }, { p: 1, duration: 0.01, immediateRender: false,
    onUpdate: () => { const v = o.p > 0 ? text : prev; if (html) e.innerHTML = v; else e.textContent = v; } }, at);
}
