/* t00 各场景共用的构件。数据来自 scenes/data.json（scenes/data.py 算出，带断言）；颜色一律取设计规范变量（tokens.css）。
   本期固定含义：墨黑 = 练习用的例子 / 规律·学出来的；琥珀 = 考试题、强调；红 = 认错；绿 = 认对；灰 = 次要。
   「规则·人写的」用次文字色 + 细框，「规律·学出来的」用琥珀，两词全片固定配色（讲稿审第 1 轮 teacher 建议）。 */
const D = EDU.S.data;
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const L = (zh, en) => EDU.tr(zh, en);

(function () {
  const s = document.createElement("style");
  s.textContent = `
  .h1, .h2, .body, .caption, .display { text-wrap: balance; }
  .digit { display: grid; grid-template-columns: repeat(8, 1fr); gap: 3px; }
  .digit i { display: block; background: var(--ink); border-radius: 3px; }
  .digit.lined { background: var(--hair); gap: 2px; padding: 2px; border-radius: 6px; }
  .digit.lined i { border-radius: 1px; }
  .tile { background: var(--surface); border-radius: 20px; box-shadow: var(--shadow); padding: 16px; display: inline-flex;
          flex-direction: column; align-items: center; gap: 10px; }
  .tile .lab { font-size: var(--fs-caption); font-weight: 600; line-height: 1; }
  .pill { display: inline-block; padding: 8px 20px; border-radius: 999px; font-size: var(--fs-caption); font-weight: 600; }
  .pill.rulep { color: var(--ink2); border: 2px solid var(--hair); background: var(--surface); }
  .pill.learn { color: var(--accent-text); background: var(--accent-soft); }
  .box { background: var(--surface); border-radius: var(--radius); box-shadow: var(--shadow); padding: 28px 36px; }
  .arrow { color: var(--faint); font-size: 64px; line-height: 1; font-weight: 400; }
  .ill { position: absolute; border-radius: 0; -webkit-mask-image: radial-gradient(ellipse 72% 72% at 50% 50%, #000 62%, transparent 100%);
         mask-image: radial-gradient(ellipse 72% 72% at 50% 50%, #000 62%, transparent 100%); }`;
  document.head.appendChild(s);
})();

/* 8×8 手写数字：每格一个方块，墨水越浓越深（数据 0–1）。lined = 画出格子（讲「八行八列」时用） */
function digitEl(img, size = 120, lined = false) {
  const el = document.createElement("div");
  el.className = "digit" + (lined ? " lined" : "");
  el.style.width = el.style.height = size + "px";
  if (!lined) el.style.gap = Math.max(1, Math.round(size / 60)) + "px";
  img.flat().forEach(v => {
    const c = document.createElement("i");
    if (lined) c.style.background = v > 0.02 ? `rgba(29,29,31,${(0.12 + 0.88 * v).toFixed(3)})` : css("--surface");
    else c.style.opacity = (0.05 + 0.95 * v).toFixed(3);
    el.appendChild(c);
  });
  return el;
}

/* 白底小卡里放一个数字，下面可带标签 */
function tileEl(img, size = 110, label = null, labCls = "") {
  const t = document.createElement("div");
  t.className = "tile";
  t.appendChild(digitEl(img, size));
  if (label !== null) {
    const l = document.createElement("div");
    l.className = "lab " + labCls; l.innerHTML = label;
    t.appendChild(l);
  }
  return t;
}

/* 十个数字的把握柱状图（概率和为 1）。hi = 高亮的那一类；返回 { el, bars, labs } */
function probBars(proba, hi, W = 560, H = 300, color = "--accent") {
  const svg = d3.create("svg").attr("width", W).attr("height", H + 44);
  const x = d3.scaleBand(d3.range(10), [0, W]).padding(0.28), y = d3.scaleLinear([0, 1], [H, 0]);
  svg.append("line").attr("class", "axis-base").attr("x1", 0).attr("x2", W).attr("y1", H).attr("y2", H);
  const bars = [], labs = [];
  proba.forEach((p, k) => {
    bars.push(svg.append("rect").attr("x", x(k)).attr("width", x.bandwidth()).attr("y", y(Math.max(p, 0.004)))
      .attr("height", H - y(Math.max(p, 0.004))).attr("rx", 4).attr("fill", css(k === hi ? color : "--faint")).node());
    labs.push(svg.append("text").attr("x", x(k) + x.bandwidth() / 2).attr("y", H + 34).attr("text-anchor", "middle")
      .attr("font-size", 26).attr("font-weight", k === hi ? 700 : 500).attr("fill", css(k === hi ? "--ink" : "--sub")).text(k).node());
  });
  return { el: svg.node(), bars, labs, x, y };
}

const pct = v => Math.round(100 * v);
