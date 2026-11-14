/* 网页场景运行时：按配音时间轴排 GSAP 动画。tools/edu_web.py 注入 window.SCENE：
   { id, lang, duration, cues: { lNN: [开口秒, 收口秒] }, data: {...} }
   场景脚本只用这里的动作，动效规则统一（规范 design_system.md「动效」）：
     EDU.t("l11", frac?, off?)   某句开口（frac=0）到收口（frac=1）之间的时刻
     EDU.in(sel, t, {y, d, stagger})   进场：缓出、轻微上移、去模糊
     EDU.out(sel, t)                   退场：缓入淡出
     EDU.draw(pathEl, t, d)            画出一条线
     EDU.focus(sel, t) / EDU.dim(sel, t)  强调 / 退后（只改透明度与 1.04 放大，不闪不抖）
     EDU.count(el, t, to, d, fmt)      数字滚动
   文字双语：标签写 data-zh / data-en，EDU.i18n() 按当前语言填入。 */
(function () {
  const S = window.SCENE;
  const tl = gsap.timeline({ paused: true });
  const EASE_OUT = "expo.out", EASE_IN = "power2.in", EASE_INOUT = "power3.inOut";
  // 统一成数组：选择器字符串、单个元素、元素数组、NodeList 都可以传
  const els = sel => typeof sel === "string" ? [...document.querySelectorAll(sel)]
    : (sel instanceof Element ? [sel] : [...sel].flatMap(x => typeof x === "string" ? [...document.querySelectorAll(x)] : [x]));
  const EDU = {
    S, tl, lang: S.lang,
    tr: (zh, en) => (S.lang === "en" ? en : zh),
    t(cue, frac = 0, off = 0) {
      const c = S.cues[cue];
      if (!c) throw new Error("时间轴里没有 " + cue);
      return c[0] + (c[1] - c[0]) * frac + off;
    },
    end: cue => S.cues[cue][1],
    i18n() {
      document.documentElement.lang = S.lang;
      document.querySelectorAll("[data-zh]").forEach(e => { e.innerHTML = S.lang === "en" ? e.dataset.en : e.dataset.zh; });
    },
    in(sel, at, o = {}) {
      const list = els(sel);
      // SVG 子元素只做淡入（CSS 滤镜与位移在 SVG 子元素上表现不一致）
      const svg = list.length && list[0] instanceof SVGElement && !(list[0] instanceof SVGSVGElement);
      const from = svg ? { opacity: 0 } : { opacity: 0, y: o.y ?? 24, filter: "blur(6px)" };
      const to = svg ? { opacity: 1 } : { opacity: 1, y: 0, filter: "blur(0px)" };
      return tl.fromTo(list, from, { ...to, duration: o.d ?? 0.7, ease: EASE_OUT, stagger: o.stagger ?? 0 }, at);
    },
    out(sel, at, o = {}) {
      return tl.to(els(sel), { opacity: 0, y: o.y ?? -10, duration: o.d ?? 0.45, ease: EASE_IN }, at);
    },
    draw(path, at, d = 1.2) {
      const p = typeof path === "string" ? document.querySelector(path) : path;
      const L = p.getTotalLength();
      p.style.strokeDasharray = `${L} ${L}`;
      return tl.fromTo(p, { strokeDashoffset: L }, { strokeDashoffset: 0, duration: d, ease: EASE_INOUT }, at);
    },
    focus(sel, at, d = 0.5) { return tl.to(els(sel), { opacity: 1, scale: 1.04, duration: d, ease: EASE_OUT, transformOrigin: "left center" }, at); },
    unfocus(sel, at, d = 0.5) { return tl.to(els(sel), { scale: 1, duration: d, ease: EASE_OUT }, at); },
    dim(sel, at, to = 0.22, d = 0.5) { return tl.to(els(sel), { opacity: to, duration: d, ease: EASE_OUT }, at); },
    count(el, at, to, d = 1, fmt = v => v.toFixed(2)) {
      // 开始前保留原文（如「—」= 还没揭晓），不显示 0：未揭晓的成绩写成 0.00 会误导（台词审 lines_r1）
      const o = { v: 0 }, e = typeof el === "string" ? document.querySelector(el) : el, init = e.textContent.trim() ? e.textContent : fmt(0);
      e.textContent = init;
      const tw = tl.to(o, { v: to, duration: d, ease: "power2.out", onUpdate: () => { e.textContent = tw.progress() > 0 ? fmt(o.v) : init; } }, at);
      return tw;
    },
    done() {
      tl.set({}, {}, S.duration);
      window.__timelines = window.__timelines || {};
      window.__timelines.main = tl;
      tl.seek(0);
    },
  };
  window.EDU = EDU;
})();
