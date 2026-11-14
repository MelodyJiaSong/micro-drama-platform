/* t02 黄仁勋辞任：各场景共用的构件（底子照 t01 的 _lib.js）。数据来自 scenes/data.json（data.py 生成并对 claims.json 断言）；颜色一律取设计规范变量。
   构件：
     ourTake(["l08", …])        「我们的判断 / Our take」角标：挂 claims C112、C127–C130 的句子开口时出现，连着的句子合成一段
     srcNote(zh, en, t0, t1)     右下角出处（micro 字号），t0 出、t1 收
     pill(kind, zh, en)          小标签 HTML：reported =「报道称 · 匿名信源」，unver =「未证实」，comment =「评论 · 转述」，
                                 dispute =「有争议」，ill =「示意」，ai =「AI 模拟画面」
     icon(name, size)            线框小图标（chip / board / capitol / podium / bill / lens / letter / court / person / hook）
     <figure class="slot" data-src="img/x.jpg" style="--h:230px">   图片位：文件在 assets/x.jpg 且台账有条目时显示（自动加署名）；否则整块移除，不显示破图
     <div class="footage"><video id="vN" data-start="{{t:lNN}}" data-duration="{{d:…}}" …>   视频片段（Seedance 模拟画面）：
         外框按同一时刻淡入淡出，左上角自带「AI 模拟画面」角标；截图 / 预览时把视频拨到对应帧（HyperFrames 渲染时自己取帧）。
         文件不存在（还没生成）时整块不显示、不报错，并给 <html> 加 class「no-vN」：场景用它把旁边的文字挪回居中，
         动画时刻不依赖视频在不在（视频只占自己的位置，不压文字）。 */
const D = EDU.S.data, N = D.n, Q = D.q;
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const SVGNS = "http://www.w3.org/2000/svg";
const L = (zh, en) => EDU.tr(zh, en);
const STAGE = document.getElementById("stage");
const EN = EDU.lang === "en";

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
  .pill.dispute, .pill.comment { border: 2px dashed var(--sub); color: var(--ink2); }
  .pill.reported, .pill.unver { border: 2px dashed var(--d-bad); color: var(--d-bad); }
  .pill.ill { background: var(--surface2); color: var(--sub); }
  .pill.ai { background: rgba(29,29,31,.72); color: #fff; }
  .pill.ok { background: var(--surface2); color: var(--ink2); }
  .mono { font-family: "Cascadia Mono", "Cascadia Code", monospace; font-variant-ligatures: none; }
  .slot { display: none; margin: 0; }
  .slot.has { display: block; }
  .slot img { width: 100%; height: var(--h, 230px); object-fit: cover; object-position: var(--pos, 50% 50%); display: block; border-radius: 18px; background: var(--surface2); }
  .av { width: var(--s, 96px); flex: none; }
  .av img { height: var(--s, 96px) !important; border-radius: 50% !important; object-position: var(--pos, 50% 22%); }
  .slot figcaption { margin-top: 8px; font-size: var(--fs-micro); color: var(--sub); line-height: 1.35; }
  .footage { position: absolute; overflow: hidden; border-radius: var(--radius); background: var(--ink); box-shadow: var(--shadow); }
  .footage video { width: 100%; height: 100%; object-fit: cover; display: block; }
  .footage .pill.ai { position: absolute; left: 22px; top: 20px; }
  .center { position: absolute; left: var(--mx); right: var(--mx); text-align: center; }
  .x { text-decoration: line-through; text-decoration-thickness: 4px; text-decoration-color: var(--faint); }
  .ico { display: inline-block; color: var(--ink2); vertical-align: middle; }
  .ico svg { display: block; }
  .q-en { font-style: normal; }
  .hlq { background-image: linear-gradient(var(--accent-soft), var(--accent-soft)); background-repeat: no-repeat; background-size: 0% 100%; padding: 0 .08em; border-radius: 6px; }
  `;
  document.head.appendChild(s);
})();

/* 预留素材位：先藏起来，图片加载成功才显示；失败就把整块拿掉（不留空位、不出破图标）。
   系列规则「没有台账条目的素材不进成片」：图片必须在 media_ledger.json 里有条目（data.py 汇成 D.credits），否则也不显示；
   有条目就在图下自动加署名（data-nocap 时不加，由场景另写出处） */
document.querySelectorAll(".slot[data-src]").forEach(fig => {
  const cr = (D.credits || {})[fig.dataset.src];
  if (!cr) { fig.remove(); return; }
  if (!("nocap" in fig.dataset) && !fig.querySelector("figcaption")) {
    const c = document.createElement("figcaption");
    c.textContent = L(cr.zh, cr.en);
    fig.appendChild(c);
  }
  const img = new Image();
  img.onload = () => fig.classList.add("has");
  img.onerror = () => fig.remove();
  img.alt = "";
  fig.insertBefore(img, fig.firstChild);
  img.src = fig.dataset.src;
});

/* 几张图的署名拼成一行（只取台账里有的，供 srcNote 用；头像等小图用 data-nocap） */
function cred(...srcs) {
  return [...new Set(srcs.map(x => (D.credits || {})[x]).filter(Boolean).map(c => L(c.zh, c.en)))].join(" · ");
}
const withCred = (txt, ...srcs) => { const c = cred(...srcs); return c ? txt + " · " + c : txt; };

function pill(kind, zh, en) {
  const t = { reported: ["报道称 · 匿名信源", "Reported · unnamed sources"], unver: ["未证实", "Unconfirmed"],
              comment: ["评论 · 转述", "Commentary · as relayed"], dispute: ["有争议", "Disputed"], ill: ["示意", "Illustration"],
              ai: ["AI 模拟画面", "AI-generated"], ok: ["已证实", "Confirmed"] }[kind];
  return `<span class="pill ${kind}">${L(zh || t[0], en || t[1])}</span>`;
}

/* 线框小图标（viewBox 64，描边用 currentColor） */
const ICONS = {
  chip: '<rect x="16" y="16" width="32" height="32" rx="4"/><rect x="25" y="25" width="14" height="14" rx="2"/><path d="M24 8v8M32 8v8M40 8v8M24 48v8M32 48v8M40 48v8M8 24h8M8 32h8M8 40h8M48 24h8M48 32h8M48 40h8"/>',
  board: '<rect x="8" y="30" width="48" height="12" rx="6"/><circle cx="18" cy="20" r="5"/><circle cx="32" cy="18" r="5"/><circle cx="46" cy="20" r="5"/><path d="M16 42v12M48 42v12"/>',
  capitol: '<path d="M10 56h44M14 56V40h36v16M20 40a12 12 0 0 1 24 0M32 22v6M29 22h6M22 56V46M32 56V46M42 56V46M12 40h40"/>',
  podium: '<path d="M18 32h28l-4 24H22z"/><path d="M32 32V20"/><circle cx="32" cy="15" r="5"/><path d="M14 56h36"/>',
  bill: '<path d="M18 8h20l10 10v38H18z"/><path d="M38 8v10h10M24 30h18M24 38h18M24 46h12"/>',
  lens: '<circle cx="27" cy="27" r="17"/><path d="M40 40l16 16"/>',
  letter: '<rect x="8" y="16" width="48" height="32" rx="4"/><path d="M8 19l24 17 24-17"/>',
  court: '<path d="M32 10v42M20 54h24M12 20h40M18 20l-7 15h14zM46 20l-7 15h14z"/>',
  person: '<circle cx="32" cy="20" r="10"/><path d="M14 56c2-12 10-18 18-18s16 6 18 18"/>',
  hook: '<path d="M32 6v26a12 12 0 1 1-12-12"/><circle cx="32" cy="6" r="3"/>',
};
function icon(name, size = 64, sw = 3) {
  return `<span class="ico"><svg width="${size}" height="${size}" viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${ICONS[name]}</svg></span>`;
}
/* 把 [data-icon] 占位换成图标 */
document.querySelectorAll("[data-icon]").forEach(e => { e.innerHTML = icon(e.dataset.icon, +(e.dataset.size || 64), +(e.dataset.sw || 3)); });

/* 「我们的判断」角标：按时间轴里句子的先后，把连着的句子并成一段，每段一个角标 */
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
function svgText(parent, x, y, s, size = 28, fill = css("--ink"), anchor = "middle", w = 600) {
  const e = svgEl(parent, "text", { x, y, "text-anchor": anchor, "font-size": size, "font-weight": w, fill });
  e.textContent = s;
  return e;
}
/* 画出一条线的一部分（frac=0.5 只画一半：「半个勾」） */
function drawPart(path, at, frac = 1, d = 1) {
  const p = typeof path === "string" ? document.querySelector(path) : path;
  const len = p.getTotalLength();
  p.style.strokeDasharray = `${len} ${len}`;
  EDU.tl.set(p, { opacity: 1 }, at);
  return EDU.tl.fromTo(p, { strokeDashoffset: len }, { strokeDashoffset: len * (1 - frac), duration: d, ease: "power3.inOut", immediateRender: true }, at);
}
/* 引语里的高亮短语：底色从左到右刷出 */
function brush(sel, at, d = .9) { return EDU.tl.to(sel, { backgroundSize: "100% 100%", duration: d, ease: "power3.inOut" }, at); }

/* 视频片段：外框按 data-start / data-duration（搭工程时已换成秒数）淡入淡出，左上角加「AI 模拟画面」；
   文件不存在 → 整块不显示，<html> 加 no-<id>；截图与预览时把 currentTime 拨到对应位置 */
const FOOTAGE = [...document.querySelectorAll(".footage video")].map(v => {
  const s = +v.dataset.start, d = +v.dataset.duration, ms = +(v.dataset.mediaStart || 0), box = v.closest(".footage");
  const tag = document.createElement("div");
  tag.innerHTML = pill("ai");
  box.appendChild(tag.firstChild);
  const gone = () => { box.style.display = "none"; document.documentElement.classList.add("no-" + v.id); };
  v.addEventListener("error", gone);
  if (v.error) gone();      // 不看 networkState：资源选择刚开始时它也会短暂是 NO_SOURCE
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
/* 某段视频的结束时刻（秒） */
const footEnd = id => { const v = document.getElementById(id); return +v.dataset.start + +v.dataset.duration; };
