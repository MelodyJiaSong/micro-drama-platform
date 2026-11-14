/* t01 美国全国停飞：各场景共用的构件。数据来自 scenes/data.json（data.py 生成并对 claims.json 断言）；颜色一律取设计规范变量。
   构件：
     ourTake(["l10", …])        「我们的判断 / Our take」角标：挂 claims C42–C44 的句子开口时出现，连着的句子合成一段
     srcNote(zh, en, t0, t1)     右下角出处（micro 字号），t0 出、t1 收
     pill(kind, zh, en)          小标签 HTML：dispute =「有争议」，unver =「匿名信源 · 未证实」，ill =「示意」
     usMap(sel, w)               美国示意地图（轮廓、22 个航路中心、网线、设施散点、在空飞机点）
     <figure class="slot" data-src="img/x.jpg" style="--h:230px"><figcaption …>   图片位：文件在 assets/x.jpg 时显示（可带图注）；不存在时整块移除，不显示破图
     <div class="footage"><video data-start="{{t:lNN}}" data-duration="{{d:…}}" …>   视频片段（Seedance 等）：时刻由 tools/edu_web.py
         搭工程时按句号换成秒数；这里按同一时刻给外框淡入淡出，并在截图 / 预览时把视频拨到对应帧（HyperFrames 渲染时自己取帧） */
const D = EDU.S.data, N = D.n;
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const SVGNS = "http://www.w3.org/2000/svg";
const L = (zh, en) => EDU.tr(zh, en);
const STAGE = document.getElementById("stage");
const fmt = v => Math.round(v).toLocaleString("en-US");

(function sharedStyle() {
  const s = document.createElement("style");
  s.textContent = `
  .eb { position: absolute; left: var(--mx); top: var(--mt); }
  .take { position: absolute; right: var(--mx); top: 84px; display: flex; align-items: center; gap: 12px; padding: 10px 22px;
          border-radius: 999px; background: var(--surface2); font-size: var(--fs-micro); font-weight: 600; color: var(--ink2);
          letter-spacing: .06em; white-space: nowrap; }
  .take i { width: 10px; height: 10px; border-radius: 50%; background: var(--ink2); }
  .srcn { position: absolute; right: var(--mx); top: 884px; font-size: var(--fs-micro); color: var(--sub); white-space: nowrap; text-align: right; }
  .pill { display: inline-flex; align-items: center; padding: 4px 16px; border-radius: 999px; font-size: var(--fs-micro); font-weight: 600;
          white-space: nowrap; vertical-align: middle; line-height: 1.4; letter-spacing: .02em; }
  .pill.dispute { border: 2px dashed var(--sub); color: var(--ink2); }
  .pill.unver { border: 2px dashed var(--d-bad); color: var(--d-bad); }
  .pill.ill { background: var(--surface2); color: var(--sub); }
  .mono { font-family: "Cascadia Mono", "Cascadia Code", monospace; font-variant-ligatures: none; }
  .slot { display: none; margin: 0; }
  .slot.has { display: block; }
  .slot img { width: 100%; height: var(--h, 230px); object-fit: cover; object-position: var(--pos, 50% 50%); display: block; border-radius: 18px; background: var(--surface2); }
  .slot figcaption { margin-top: 8px; font-size: var(--fs-micro); color: var(--sub); white-space: nowrap; }
  .footage { position: absolute; overflow: hidden; border-radius: var(--radius); background: var(--ink); box-shadow: var(--shadow); }
  .footage video { width: 100%; height: 100%; object-fit: cover; display: block; }
  .center { position: absolute; left: var(--mx); right: var(--mx); text-align: center; }
  .x { text-decoration: line-through; text-decoration-thickness: 4px; text-decoration-color: var(--faint); }
  `;
  document.head.appendChild(s);
})();

/* 预留素材位：先藏起来，图片加载成功才显示；失败就把整块拿掉（不留空位、不出破图标） */
document.querySelectorAll(".slot[data-src]").forEach(fig => {
  const img = new Image();
  img.onload = () => fig.classList.add("has");
  img.onerror = () => fig.remove();
  img.alt = "";
  fig.insertBefore(img, fig.firstChild);
  img.src = fig.dataset.src;
});

function pill(kind, zh, en) {
  const t = { dispute: ["有争议", "Disputed"], unver: ["匿名信源 · 未证实", "Unnamed sources · unconfirmed"], ill: ["示意", "Illustration"] }[kind];
  return `<span class="pill ${kind}">${L(zh || t[0], en || t[1])}</span>`;
}

/* 「我们的判断」角标：按时间轴里句子的先后，把连着的句子并成一段，每段一个角标（不复用同一个元素，免得进退场互相覆盖） */
function ourTake(lines) {
  const order = Object.keys(EDU.S.cues);
  const idx = lines.map(l => order.indexOf(l)).filter(i => i >= 0).sort((a, b) => a - b);
  const runs = [];
  for (const i of idx) {
    const r = runs[runs.length - 1];
    if (r && i === r[1] + 1) r[1] = i; else runs.push([i, i]);
  }
  for (const [a, b] of runs) {
    const el = document.createElement("div");
    el.className = "take";
    el.innerHTML = `<i></i>${L("我们的判断", "Our take")}`;
    STAGE.appendChild(el);
    gsap.set(el, { opacity: 0 });
    EDU.in(el, EDU.t(order[a], 0, .05), { y: 0, d: .5 });
    EDU.out(el, EDU.end(order[b]) + .25, { y: 0 });
  }
}

/* 右下角出处 */
function srcNote(zh, en, t0, t1) {
  const el = document.createElement("div");
  el.className = "srcn";
  el.innerHTML = L(zh, en);
  STAGE.appendChild(el);
  gsap.set(el, { opacity: 0 });
  EDU.in(el, t0, { y: 0, d: .5 });
  if (t1 != null) EDU.out(el, t1, { y: 0 });
  return el;
}

function svgEl(parent, tag, attrs = {}) {
  const e = document.createElementNS(SVGNS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  parent.appendChild(e);
  return e;
}

/* 美国示意地图：宽 w 像素，高按轮廓比例。返回各图层元素，场景自己排动画 */
function usMap(sel, w) {
  const M = D.map, h = Math.round(w * M.aspect);
  const svg = document.querySelector(sel);
  svg.setAttribute("width", w); svg.setAttribute("height", h);
  const X = v => v * w, Y = v => v * w;           // 归一化坐标（x 0..1，y 0..aspect）
  const g = svgEl(svg, "g");
  const outline = svgEl(g, "path", { d: "M" + M.outline.map(p => `${X(p[0]).toFixed(1)},${Y(p[1]).toFixed(1)}`).join("L") + "Z",
    fill: css("--surface2"), stroke: css("--hair"), "stroke-width": 3, "stroke-linejoin": "round" });
  const facG = svgEl(g, "g"), edgeG = svgEl(g, "g"), planeG = svgEl(g, "g"), nodeG = svgEl(g, "g");
  const fac = M.fac.map(p => svgEl(facG, "circle", { cx: X(p[0]), cy: Y(p[1]), r: 3, fill: css("--faint") }));
  const C = M.centers;
  // 外岛小框（阿拉斯加、夏威夷），示意
  const insets = C.filter(c => c.inset).map(c => {
    const b = svgEl(g, "rect", { x: X(c.x) - 34, y: Y(c.y) - 26, width: 68, height: 52, rx: 10, fill: "none",
      stroke: css("--hair"), "stroke-width": 2, "stroke-dasharray": "5 6" });
    return b;
  });
  const edges = M.edges.map(([i, j]) => svgEl(edgeG, "line", { x1: X(C[i].x), y1: Y(C[i].y), x2: X(C[j].x), y2: Y(C[j].y),
    stroke: css("--accent"), "stroke-width": 3, "stroke-linecap": "round" }));
  const links = M.links.map(([i, j]) => svgEl(edgeG, "line", { x1: X(C[i].x), y1: Y(C[i].y), x2: X(C[j].x), y2: Y(C[j].y),
    stroke: css("--accent"), "stroke-width": 2, "stroke-dasharray": "6 8", "stroke-linecap": "round" }));
  const nodes = C.map(c => svgEl(nodeG, "circle", { cx: X(c.x), cy: Y(c.y), r: 10, fill: css("--ink"), stroke: css("--surface"), "stroke-width": 4 }));
  const planes = M.planes.map(p => svgEl(planeG, "circle", { cx: X(p[0]), cy: Y(p[1]), r: 5, fill: css("--accent") }));
  return { svg, w, h, X, Y, outline, fac, edges, links, nodes, insets, planes, C };
}

/* 沿网线跑的小光点（l13：语音和雷达数据走这张网） */
function pulses(map, at, n = 14, d = 1.4) {
  const g = svgEl(map.svg, "g");
  const C = map.C, E = D.map.edges;
  for (let k = 0; k < n; k++) {
    const [i, j] = E[(k * 7) % E.length];
    const [a, b] = k % 2 ? [i, j] : [j, i];
    const dot = svgEl(g, "circle", { cx: map.X(C[a].x), cy: map.Y(C[a].y), r: 7, fill: css("--accent-text"), opacity: 0 });
    const t = at + (k % 7) * .28;
    EDU.tl.set(dot, { opacity: 1 }, t);
    EDU.tl.to(dot, { attr: { cx: map.X(C[b].x), cy: map.Y(C[b].y) }, duration: d, ease: "power1.inOut" }, t);
    EDU.tl.to(dot, { opacity: 0, duration: .3 }, t + d - .3);
  }
}

/* 数字从「—」或原文滚到 to（千分位） */
function countUp(el, at, to, d = 1.1) { return EDU.count(el, at, to, d, fmt); }

/* 视频片段：按标签上的 data-start / data-duration（搭工程时已换成秒数）给外框淡入淡出；
   截图与浏览器预览时没有 HyperFrames 取帧，就在时间线更新时把 currentTime 拨到对应位置 */
const FOOTAGE = [...document.querySelectorAll(".footage video")].map(v => {
  const s = +v.dataset.start, d = +v.dataset.duration, ms = +(v.dataset.mediaStart || 0), box = v.closest(".footage");
  v.muted = true; v.preload = "auto";
  gsap.set(box, { opacity: 0 });
  EDU.in(box, s, { y: 0, d: .5 });
  EDU.out(box, s + d - .45, { y: 0 });
  return { v, s, d, ms };
});
if (FOOTAGE.length) EDU.tl.eventCallback("onUpdate", () => {
  const now = EDU.tl.time();
  for (const f of FOOTAGE) {
    const local = Math.min(Math.max(now - f.s, 0), f.d);
    const want = f.ms + local;
    if (Math.abs(f.v.currentTime - want) > .04) { try { f.v.currentTime = want; } catch (e) { /* 还没加载 */ } }
  }
});
/* 某段视频的结束时刻（秒）：后面的画面接在它后面出场 */
const footEnd = id => { const v = document.getElementById(id); return +v.dataset.start + +v.dataset.duration; };
