/* t01 各场景共用的图表构件。数据来自 scenes/data.json（data.py 算出）；颜色一律取设计规范变量（tokens.css）。
   数据颜色含义全系列固定：练习 = 墨黑实心点，考试 = 琥珀空心圈，刚刚好 = 绿，过拟合 = 红，次要 = 灰。 */
const D = EDU.S.data;
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const polyval = (coef, v) => coef.reduce((a, c) => a * v + c, 0);      // 与 numpy.polyval 同序（高次在前）
const truthAt = v => 1.2 * Math.sin(1.3 * v) + 0.25 * v;

/* 在 <svg id=…> 里搭一张散点图：只有一条基线，没有框和网格。返回画曲线、画点、画误差线的方法。 */
function makeChart(sel, W = 1100, H = 620) {
  const svg = d3.select(sel).attr("width", W).attr("height", H);
  const x = d3.scaleLinear([-3, 3], [30, W - 30]), y = d3.scaleLinear([-3.2, 3.2], [H, 0]);
  const base = svg.append("line").attr("class", "axis-base").attr("x1", 30).attr("x2", W - 30).attr("y1", y(0)).attr("y2", y(0)).node();
  const line = d3.line().x((d, i) => x(D.xs[i])).y(d => y(d)).curve(d3.curveCatmullRom);
  const layer = svg.append("g");                      // 曲线层在点下面
  const top = svg.append("g");
  return {
    svg, x, y, base,
    curve(values, color, w = 6, dash = null) {
      const p = layer.append("path").attr("d", line(values)).attr("fill", "none").attr("stroke", css(color))
        .attr("stroke-width", w).attr("stroke-linecap", "round").node();
      if (dash) p.setAttribute("stroke-dasharray", dash);
      return p;
    },
    dots(points, kind = "train", r = 10) {
      const g = top.append("g");
      return points.map(([a, b]) => kind === "train"
        ? g.append("circle").attr("cx", x(a)).attr("cy", y(b)).attr("r", r).attr("fill", css("--d-train")).node()
        : g.append("circle").attr("cx", x(a)).attr("cy", y(b)).attr("r", r - 1).attr("fill", css("--bg"))
            .attr("stroke", css("--d-test")).attr("stroke-width", 4).node());
    },
    gaps(points, f, color, dash = "4 6") {
      const g = layer.append("g").node();
      points.forEach(([a, b]) => d3.select(g).append("line").attr("x1", x(a)).attr("x2", x(a)).attr("y1", y(b)).attr("y2", y(f(a)))
        .attr("stroke", css(color)).attr("stroke-width", 3).attr("stroke-dasharray", dash));
      return g;
    },
    /* 在图上某个数据坐标旁放一段说明文字（HTML，可双语），返回元素 */
    note(html, at, dx = 0, dy = 0, cls = "caption") {
      const svgBox = document.querySelector(sel).getBoundingClientRect(), stage = document.getElementById("stage").getBoundingClientRect();
      const el = document.createElement("div");
      el.className = cls; el.style.position = "absolute"; el.innerHTML = html;
      el.style.left = (svgBox.left - stage.left + x(at[0]) + dx) + "px";
      el.style.top = (svgBox.top - stage.top + y(at[1]) + dy) + "px";
      document.getElementById("stage").appendChild(el);
      return el;
    },
  };
}
const mse = (deg, which = 0) => D.mse[String(deg)][which];
