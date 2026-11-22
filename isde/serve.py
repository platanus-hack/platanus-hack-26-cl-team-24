"""Local visual demo: one page over an in-memory Guard; deliveries live only until reset or exit."""
import json
import secrets
from datetime import date
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from .guard import Guard
from .model import Batch

DAY = date(2026, 1, 4)
MAX_DRAFT = 2000
MAX_BODY = 8192
HERE = Path(__file__).parent
# shortcut: Spanish names for the example case's tasks; other cases show their IDs until Task gains a label field.
TASKS = {"due": "Plazo del trámite", "signature": "Firma de la oferta", "record": "Estado del expediente"}
ASSETS = {"/logo.png": ("image/png", "logo.png"), "/fonts/inter.woff2": ("font/woff2", "fonts/inter-latin.woff2")}

ICONS = {
    "agent": '<path d="M4 5h16v11H9l-5 4z"/>',
    "lock": '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "inbox": '<path d="M3 13h5l1 3h6l1-3h5"/><path d="M5 5h14l2 8v6H3v-6z"/>',
    "allow": '<path d="M5 12.5l4.5 4.5L19 7"/>',
    "repair": '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13 7l4 4"/>',
    "review": '<circle cx="12" cy="8" r="4"/><path d="M4.5 21a7.5 7.5 0 0 1 15 0"/>',
    "prev": '<path d="M15 5l-7 7 7 7"/>',
    "next": '<path d="M9 5l7 7-7 7"/>',
}

PAGE = """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>mosAIc · demo</title>
<style nonce="__NONCE__">
@font-face{font-family:"Inter";src:url("/fonts/inter.woff2") format("woff2");font-weight:100 900;font-display:swap}
:root{color-scheme:dark;--bg:#15182d;--deep:#0e1022;--surface:#1c2040;--raise:#262b52;--line:#363c6b;--ink:#f7f7fb;--mute:#b4b9d9;
--accent:#ae81fd;--accent-hi:#c4a3ff;--ok:#3ddc97;--warn:#ffc145;--bad:#ff5d6c;--ease:cubic-bezier(.16,1,.3,1);
font-size:clamp(14px,2.05vmin,34px)}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--ink)}
body{font:500 1rem/1.35 Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased;caret-color:var(--accent)}
::selection{background:var(--accent);color:var(--bg)}
[hidden]{display:none!important}
svg{width:1.2em;height:1.2em;flex:none;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.app{min-height:100dvh;max-width:120rem;margin:auto;padding:1.1rem 2rem 1.3rem;display:grid;grid-template-rows:auto 1fr auto;gap:1.1rem}
.top{display:flex;align-items:center;gap:1.5rem}
.logo{display:block;height:2.8rem;width:auto;margin-left:-.7rem}
.tag{margin:0;padding:.3rem .8rem;border:1px dashed var(--line);border-radius:.6rem;color:var(--mute);font-size:1.35rem;font-weight:700}
.turn{margin:0 0 0 auto;font-size:1.35rem;font-weight:800;color:var(--mute);font-variant-numeric:tabular-nums}
.dots{display:flex;gap:.45rem;margin:0;padding:0;list-style:none}
.dots button{width:.9rem;height:.9rem;padding:0;border:0;border-radius:.45rem;background:var(--line);cursor:pointer;transition:width .4s var(--ease),background .3s}
.dots button:hover{background:var(--mute)}
.dots button[aria-current=step]{width:2.4rem;background:var(--accent)}
.stage{display:grid;grid-template-rows:auto 1fr;gap:1.1rem;min-height:0}
.message{margin:0;display:flex;gap:1rem;align-items:flex-start;padding:1rem 1.4rem;font-size:1.65rem;font-weight:700;line-height:1.2;letter-spacing:-.02em;
text-wrap:balance;background:var(--surface);border:1px solid var(--line);border-radius:1.1rem}
.message svg{color:var(--accent);margin-top:.05em}
.message.swap{animation:rise .6s var(--ease)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:1.1rem}
.col{display:grid;grid-template-rows:auto auto auto 1fr;gap:1.1rem;padding:1.3rem 1.5rem;background:var(--surface);border:1px solid var(--line);border-radius:1.2rem}
.who{display:flex;align-items:center;gap:1rem}
.avatar{width:3.1rem;height:3.1rem;border-radius:50%;display:grid;place-items:center;background:var(--raise);border:1px solid var(--line);font-size:1.4rem;font-weight:800}
.name{margin:0;font-size:3.2rem;font-weight:800;letter-spacing:-.035em;line-height:1}
.ctx{display:flex;flex-wrap:wrap;align-items:center;gap:.6rem;min-height:2.7rem}
.ctx-label{color:var(--mute);font-size:1.35rem;font-weight:650;margin-right:.2rem}
.chip{display:inline-flex;align-items:baseline;gap:.7rem;padding:.4rem .85rem;font-size:1.35rem;border-radius:.65rem;background:var(--raise);border:1px solid var(--line);font-weight:650}
.chip b{color:var(--accent-hi);font-weight:800;font-variant-numeric:tabular-nums}
.chip.empty{background:none;border-style:dashed;color:var(--mute)}
.eval{display:grid;gap:.9rem}
.what{display:flex;align-items:center;gap:.6rem;margin:0;font-size:1.5rem;font-weight:750;letter-spacing:-.01em}
.what svg{color:var(--bad)}
.meter{display:flex;align-items:center;gap:1.4rem;min-height:5rem;margin-bottom:1.9rem}
.track{position:relative;flex:1;height:1.7rem;border-radius:.85rem;background:var(--deep);border:1px solid var(--line)}
.fill{position:absolute;inset:0 auto 0 0;width:0;border-radius:inherit;background:var(--accent);transition:background .25s}
.track.over .fill{background:var(--bad)}
.limit{position:absolute;top:-.55rem;bottom:-.55rem;width:4px;margin-left:-2px;border-radius:2px;background:var(--ink)}
.limit span{position:absolute;top:calc(100% + .15rem);left:50%;transform:translateX(-50%);white-space:nowrap;font-size:1.35rem;font-weight:750}
.pct{margin:0;min-width:4.4ch;text-align:right;font-size:5rem;font-weight:800;letter-spacing:-.04em;line-height:1;font-variant-numeric:tabular-nums}
.pct.none{min-width:0;font-size:1.6rem;font-weight:750;letter-spacing:-.01em;color:var(--mute)}
.verdict{display:grid;gap:.8rem;align-content:start}
.plate{display:flex;align-items:center;gap:.8rem;margin:0;padding:.85rem 1.2rem;border-radius:.9rem;font-size:2.1rem;font-weight:800;letter-spacing:-.025em;color:var(--deep)}
.plate svg{stroke-width:2.8}
.verdict.on .plate{animation:wipe .7s var(--ease)}
.plate.allow{background:var(--ok)}.plate.repair{background:var(--warn)}.plate.review{background:var(--bad)}
.inbox{display:flex;align-items:flex-start;gap:.7rem;margin:0;font-size:1.35rem;font-weight:650;line-height:1.3}
.inbox svg{color:var(--mute);margin-top:.05em}
.inbox.none{color:var(--mute)}
.reveal{opacity:0;visibility:hidden;transform:translateY(.7rem);transition:opacity .55s var(--ease),transform .55s var(--ease),visibility 0s .55s}
.reveal.on{opacity:1;visibility:visible;transform:none;transition-delay:0s}
.title{display:none;place-self:center;margin:0;max-width:15ch;text-align:center;font-size:4.6rem;font-weight:800;letter-spacing:-.04em;line-height:1.02;text-wrap:balance;animation:rise .8s var(--ease)}
.title em{font-style:normal;color:var(--accent)}
.stage[data-kind=intro] > :not(#intro),.stage[data-kind=outro] > :not(#outro){display:none}
.stage[data-kind=intro] #intro,.stage[data-kind=outro] #outro{display:block;grid-row:1/-1}
.controls{display:flex;align-items:center;gap:1rem}
.controls .mode{margin-right:auto}
button{font:inherit;font-size:1.35rem;font-weight:750;display:inline-flex;align-items:center;gap:.6rem;padding:.7rem 1.3rem;border-radius:.8rem;
border:1px solid var(--line);background:var(--surface);color:var(--ink);cursor:pointer;transition:background .2s,border-color .2s,transform .2s var(--ease)}
button:hover{background:var(--raise);border-color:var(--mute)}
button:active{transform:translateY(1px)}
button.primary{background:var(--accent);border-color:var(--accent);color:var(--deep)}
button.primary:hover{background:var(--accent-hi);border-color:var(--accent-hi)}
button:disabled{opacity:.35;cursor:default;transform:none}
:focus-visible{outline:3px solid var(--accent-hi);outline-offset:3px}
.free{display:grid;grid-template-columns:minmax(0,30rem) minmax(0,1fr);gap:1.1rem;align-items:start}
.free form{display:grid;gap:.7rem;font-size:1.35rem;padding:1.3rem;background:var(--surface);border:1px solid var(--line);border-radius:1.2rem}
.free form .row{display:flex;flex-wrap:wrap;gap:.7rem}
label{display:grid;gap:.4rem;font-weight:700;color:var(--mute)}
select,textarea{font:inherit;font-weight:600;color:var(--ink);background:var(--deep);border:1px solid var(--line);border-radius:.7rem;padding:.6rem .8rem}
select:hover,textarea:hover{border-color:var(--mute)}
textarea{min-height:4.6rem;resize:vertical;line-height:1.35}
textarea::placeholder{color:var(--mute)}
.out{display:grid;gap:1.1rem}
.out .col{grid-template-rows:auto}
.history{display:grid;gap:.6rem;margin:0;padding-top:1rem;border-top:1px solid var(--line)}
.history h3{margin:0;font-size:1.5rem;font-weight:800}
.history ol{margin:0;padding-left:1.4rem;display:grid;gap:.4rem;font-weight:600}
.alert{margin:0;padding:.8rem 1.1rem;border-radius:.8rem;background:var(--bad);color:var(--deep);font-weight:750}
.alert:empty{display:none}
.status{margin:0;color:var(--mute);font-weight:650}
.status:empty{display:none}
@keyframes wipe{from{clip-path:inset(0 100% 0 0 round .9rem)}to{clip-path:inset(0 0 0 0 round .9rem)}}
@keyframes rise{from{opacity:0;transform:translateY(.7rem)}to{opacity:1;transform:none}}
@media (max-width:52rem){:root{font-size:16px}.top{flex-wrap:wrap}.tag{order:3}.app{padding:1rem}.cols,.free{grid-template-columns:1fr}.message{font-size:1.25rem}.name{font-size:1.9rem}
.meter{flex-wrap:wrap;row-gap:2.8rem}.track{flex-basis:100%}.pct{font-size:3rem;text-align:left}.plate{font-size:1.5rem}.title{font-size:2.6rem}.logo{height:2rem}.dots{display:none}.controls{flex-wrap:wrap}.controls .mode{order:3;margin:0}}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
</style></head><body>
<div class="app">
<header class="top"><img class="logo" src="/logo.png" alt="mosAIc" width="860" height="210">
<p class="tag">Caso ficticio · pesos sin calibrar</p>
<p class="turn" id="turn"></p><ol class="dots" id="dots" aria-label="Pasos"></ol></header>
<main class="stage" id="story" data-kind="intro" aria-live="polite">
<h1 class="title" id="intro">¿Qué puede deducir quien recibe la respuesta?</h1>
<blockquote class="message" id="message"></blockquote>
<div class="cols" id="cols"></div>
<h1 class="title" id="outro">Mismo texto.<br>Otra persona.<br><em>Otra decisión.</em></h1>
</main>
<main class="free" id="free" hidden>
<form id="f">
<label>Destinatario<select id="user">__USERS__</select></label>
<label>Tarea<select id="task">__TASKS__</select></label>
<label>Borrador del agente<textarea id="draft" maxlength="__MAX_DRAFT__" placeholder="Vacío: respuesta del catálogo"></textarea></label>
<div class="row"><button type="submit" class="primary">Evaluar</button><button type="button" id="deliver">Entregar</button>
<button type="button" id="reset">Reiniciar</button></div>
<p class="status" id="status" role="status"></p>
<section class="history"><h3 id="inbox-title">Bandeja</h3><ol id="inbox"></ol></section>
</form>
<div class="out" id="out" aria-live="polite"><blockquote class="message" id="free-message"></blockquote></div>
</main>
<footer class="controls">
<button type="button" class="mode" id="mode">Modo libre</button>
<p class="alert" id="error" role="alert"></p>
<button type="button" id="prev">__ICON_PREV__Anterior</button>
<button type="button" class="primary" id="next">Siguiente__ICON_NEXT__</button>
</footer>
</div>
<script nonce="__NONCE__">
const $ = id => document.getElementById(id);
const THRESH = __THRESH__, ICON = __ICONS__;
// shortcut: the guided story and its fact labels assume examples/case.yaml; another case opens free mode and shows raw IDs.
const PLAN = [[["ana", "due"], ["luis", "due"]], [["ana", "record"], ["luis", "record"]]];
const LABELS = {"o17 signature signed": "O-17 está firmado", "o17 counterparty betaai": "O-17 es de BetaAI",
  "o17 deadline friday": "Vence el viernes", "betaai offer_status signed": "La oferta a BetaAI está firmada"};
const VERDICTS = {allow: "Entregado", repair: "Reparado", review: "Revisión humana"};
const STEPS = [{kind: "intro"}, ...[0, 1].flatMap(turn => [0, 1, 2, 3].map(phase => ({turn, phase}))), {kind: "outro"}];
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const label = f => LABELS[f.join(" ")] || f.join(" · ");
const pct = x => Math.round(100 * x) + " %";
const nobreak = s => s.replace(/-/g, "‑");  // keeps "O-17" on one line
const ease = t => t >= 1 ? 1 : 1 - 2 ** (-10 * t);
let story = null, pieces = new Set(), conclusion = null, step = 0, shown = null;

function el(tag, cls, text) {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text !== undefined) n.textContent = text;
  return n;
}
function icon(name) {
  const s = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  s.setAttribute("viewBox", "0 0 24 24"); s.setAttribute("aria-hidden", "true"); s.innerHTML = ICON[name];
  return s;
}
async function api(path, body) {
  const r = body === undefined ? await fetch(path)
    : await fetch(path, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)});
  const data = await r.json();
  if (!r.ok) throw new Error(data.error || "Error inesperado");
  return data;
}
// The agent's own draft is attempt 0; its riskiest change is what the room should see.
const riskiest = ev => (ev.attempts[0]?.changes || []).reduce((a, c) => !a || c.after > a.after ? c : a, null);
const key = c => c.subject + " " + c.family + " " + c.status;

function column() {
  const c = {root: el("article", "col")}, who = el("header", "who");
  c.avatar = el("span", "avatar"); c.avatar.setAttribute("aria-hidden", "true"); c.name = el("h2", "name");
  who.append(c.avatar, c.name);
  c.ctx = el("div", "ctx reveal"); c.ctx.dataset.at = 1;
  const ev = el("div", "eval reveal"); ev.dataset.at = 2;
  c.what = el("p", "what");
  const meter = el("div", "meter"); c.track = el("div", "track"); c.track.setAttribute("aria-hidden", "true");
  c.fill = el("span", "fill"); c.limit = el("span", "limit"); c.limit.append(el("span", "", "límite"));
  c.track.append(c.fill, c.limit); c.num = el("p", "pct"); meter.append(c.track, c.num); ev.append(c.what, meter);
  const verdict = el("div", "verdict reveal"); verdict.dataset.at = 3;
  c.plate = el("p", "plate"); c.inbox = el("p", "inbox"); verdict.append(c.plate, c.inbox);
  c.root.append(who, c.ctx, ev, verdict);
  return c;
}
function animate(c, from, to, how) {
  cancelAnimationFrame(c.raf);
  // The bar turns red only as it crosses the limit, so the crossing is something the room sees happen.
  const draw = x => { c.fill.style.width = 100 * x + "%"; c.track.classList.toggle("over", c.blocked && x >= c.limitAt); if (c.change) c.num.textContent = pct(x); };
  if (how !== "run" || reduced) return draw(how === "start" ? from : to);
  const start = performance.now();
  const tick = now => { const t = Math.min(1, (now - start) / 1300); draw(from + (to - from) * ease(t)); if (t < 1) c.raf = requestAnimationFrame(tick); };
  draw(from); c.raf = requestAnimationFrame(tick);
}
function fill(c, ev, phase, run) {
  c.name.textContent = ev.user[0].toUpperCase() + ev.user.slice(1); c.avatar.textContent = ev.user[0].toUpperCase();
  // The same fact can arrive from several origins; the room only needs the strongest one.
  const best = new Map();
  ev.observer.possible_knowledge.forEach(h => { const k = h.fact.join(" "); if (!best.has(k) || best.get(k).p_known < h.p_known) best.set(k, h); });
  const known = [...best.values()].filter(h => !pieces.size || pieces.has(h.fact.join(" ")));
  c.ctx.replaceChildren(el("span", "ctx-label", "Ya sabe"));
  known.forEach(h => { const chip = el("span", "chip"); chip.append(el("span", "", label(h.fact)), el("b", "", pct(h.p_known))); c.ctx.append(chip); });
  if (!known.length) c.ctx.append(el("span", "chip empty", "Nada todavía"));
  const ch = c.change = riskiest(ev), goal = ch || conclusion, t = goal && THRESH[goal.family];
  c.what.replaceChildren(icon("lock"), el("span", "", goal ? label([goal.subject, goal.family, goal.status]) : "Sin conclusión protegida"));
  const before = ch ? ch.before : 0, after = ch ? ch.after : 0;
  c.limit.hidden = !t;
  c.limitAt = t ? Math.min(t.absolute, before + t.increase) : Infinity;
  if (t) c.limit.style.left = 100 * c.limitAt + "%";
  c.blocked = !!ch && ev.attempts[0].blocked.some(b => key(b) === key(ch));
  c.num.className = ch ? "pct" : "pct none";
  if (!ch) c.num.textContent = "Sin aumento";
  animate(c, before, after, phase < 2 ? "start" : run ? "run" : "end");
  c.plate.replaceChildren(icon(ev.action), el("span", "", VERDICTS[ev.action]));
  c.plate.className = "plate " + ev.action;
  c.inbox.replaceChildren(icon("inbox"), el("span", "", ev.text == null ? "No recibe nada" : "«" + nobreak(ev.text) + "»"));
  c.inbox.className = ev.text == null ? "inbox none" : "inbox";
  c.root.querySelectorAll("[data-at]").forEach(e => e.classList.toggle("on", phase >= +e.dataset.at));
}
function message(node, text) {
  if (node.dataset.text === text) return;
  node.dataset.text = text; node.replaceChildren(icon("agent"), el("span", "", nobreak(text)));
  node.classList.remove("swap"); void node.offsetWidth; node.classList.add("swap");
}

const cols = [column(), column()], solo = column();
$("cols").append(...cols.map(c => c.root));
$("out").append(solo.root);
STEPS.forEach((s, i) => {
  const b = el("button"); b.type = "button"; b.setAttribute("aria-label", "Paso " + (i + 1)); b.addEventListener("click", () => show(i));
  const li = el("li"); li.append(b); $("dots").append(li);
});

function show(n) {
  const prev = shown; step = Math.max(0, Math.min(STEPS.length - 1, n)); shown = STEPS[step];
  const s = shown, stage = $("story");
  // Until the story arrives, the opening question holds the screen instead of empty columns.
  stage.dataset.kind = s.kind || (story ? "turn" : "intro");
  [...$("dots").querySelectorAll("button")].forEach((b, i) => i === step ? b.setAttribute("aria-current", "step") : b.removeAttribute("aria-current"));
  $("prev").disabled = step === 0; $("next").disabled = step === STEPS.length - 1;
  $("turn").textContent = s.kind ? "" : "Turno " + (s.turn + 1);
  history.replaceState(null, "", "#" + (step + 1));
  if (s.kind || !story) return;
  message($("message"), story[s.turn][0].draft);
  // The bar only replays when the room is meant to watch it climb, not when stepping back.
  const run = s.phase === 2 && !(prev && prev.turn === s.turn && prev.phase > 2);
  cols.forEach((c, i) => fill(c, story[s.turn][i], s.phase, run));
}
function mode(free) {
  $("free").hidden = !free; $("story").hidden = free;
  $("prev").hidden = $("next").hidden = free; $("turn").hidden = $("dots").hidden = free;
  $("mode").textContent = free ? "Volver a la historia" : "Modo libre";
  if (free && !$("free").dataset.ready) { $("free").dataset.ready = 1; evaluate(false); }
  if (!free) show(step);
}
async function load() {
  try {
    await api("/api/reset", {});
    story = [];
    for (const pair of PLAN) {
      const row = [];
      for (const [user, task] of pair) row.push(await api("/api/deliver", {user, task}));
      story.push(row);
    }
    story.flat().forEach(ev => ev.attempts.forEach(a => (a.changes || []).forEach(c => {
      conclusion = conclusion || c;
      c.paths.forEach(p => p.edges.forEach(e => pieces.add(e.join(" "))));
    })));
    show(step);
  } catch (e) {
    story = null; $("error").textContent = "No se pudo preparar la historia: " + e.message; mode(true);
  }
}

async function evaluate(keepDraft, deliver) {
  const q = {user: $("user").value, task: $("task").value};
  if (keepDraft && $("draft").value.trim()) q.draft = $("draft").value;
  let data;
  try { data = deliver ? await api("/api/deliver", q) : await api("/api/preview?" + new URLSearchParams(q)); }
  catch (e) { $("error").textContent = e.message; return; }
  $("error").textContent = "";
  $("status").textContent = !deliver ? "Vista previa: no se entregó nada."
    : data.delivered ? "Entregado. Ya cuenta en su historial." : "Retenido: no se entregó nada.";
  if (!keepDraft) $("draft").value = data.draft;
  message($("free-message"), data.draft);
  fill(solo, data, 3, true);
  $("inbox-title").textContent = "Bandeja de " + solo.name.textContent;
  $("inbox").replaceChildren(...data.inbox.map(m => el("li", "", m.text)));
  if (!data.inbox.length) $("inbox").append(el("li", "", "Vacía"));
}

$("next").addEventListener("click", () => show(step + 1));
$("prev").addEventListener("click", () => show(step - 1));
$("mode").addEventListener("click", () => mode($("story").hidden === false));
$("f").addEventListener("submit", e => { e.preventDefault(); evaluate(true); });
$("deliver").addEventListener("click", () => evaluate(true, true));
$("reset").addEventListener("click", async () => {
  try { await api("/api/reset", {}); } catch (e) { $("error").textContent = e.message; return; }
  await evaluate(false); $("status").textContent = "Historial reiniciado al ejemplo.";
});
$("user").addEventListener("change", () => evaluate(false));
$("task").addEventListener("change", () => evaluate(false));
document.addEventListener("keydown", e => {
  if ($("story").hidden || e.altKey || e.ctrlKey || e.metaKey || e.target.closest("input,textarea,select")) return;
  // Presenter clickers send PageDown/PageUp; Space on a focused button already clicks it.
  const moves = {ArrowRight: 1, PageDown: 1, " ": 1, ArrowLeft: -1, PageUp: -1};
  if (e.key === " " && e.target.closest("button")) return;
  if (e.key in moves) { e.preventDefault(); show(step + moves[e.key]); }
  else if (e.key === "Home" || e.key === "End") { e.preventDefault(); show(e.key === "Home" ? 0 : STEPS.length - 1); }
});
const params = new URLSearchParams(location.search);
for (const [k, v] of params) if (["user", "task"].includes(k)) $(k).value = v;
// #n reopens step n after a reload, so a rehearsal can resume where it stopped.
show((parseInt(location.hash.slice(1), 10) || 1) - 1);
load().then(() => { if (story && (params.has("user") || params.has("task"))) mode(true); });
</script></body></html>"""


def fields(guard: Guard, query: dict):
    """Validate recipient, task and draft at the HTTP boundary; raise ValueError with a user-facing message."""
    user, task, draft = (query.get(k, "") for k in ("user", "task", "draft"))
    if not all(isinstance(v, str) for v in (user, task, draft)):
        raise ValueError("Campos inválidos")
    if user not in {a.user for a in guard.case.assignments}:
        raise ValueError("Destinatario desconocido")
    if task not in guard.case.tasks:
        raise ValueError("Tarea desconocida")
    if len(draft) > MAX_DRAFT:
        raise ValueError(f"El borrador supera {MAX_DRAFT} caracteres")
    return user, task, draft or None


def evaluate(guard: Guard, user, task, draft, request_id=None):
    # Context is captured before delivery, otherwise it would include the answer being judged.
    observer = guard.model_context(user, DAY)
    result = guard.run(user, task, DAY, request_id, draft=draft)
    shown = draft or guard.render(guard.case.tasks[task].options[0])
    return {"user": user, "task": task, "draft": shown, **result, "observer": observer,
            "delivered": request_id is not None and result["action"] != "review", "inbox": guard.inbox(user)}


def script_json(value):
    # "<" escaped so a policy string can never close the inline <script>.
    return json.dumps(value, ensure_ascii=False).replace("<", "\\u003c")


def page(guard: Guard, nonce: str):
    users = dict.fromkeys(a.user for a in guard.case.assignments)
    thresholds = {k: {"absolute": f.absolute, "increase": f.increase} for k, f in guard.policy.families.items()}
    svg = '<svg viewBox="0 0 24 24" aria-hidden="true">{}</svg>'
    return (PAGE.replace("__NONCE__", nonce).replace("__MAX_DRAFT__", str(MAX_DRAFT))
            .replace("__ICON_PREV__", svg.format(ICONS["prev"])).replace("__ICON_NEXT__", svg.format(ICONS["next"]))
            .replace("__THRESH__", script_json(thresholds)).replace("__ICONS__", script_json(ICONS))
            .replace("__USERS__", "".join(f'<option value="{escape(u)}">{escape(u.capitalize())}</option>' for u in users))
            .replace("__TASKS__", "".join(f'<option value="{escape(t)}">{escape(TASKS.get(t, t))}</option>' for t in guard.case.tasks)))


def respond(state: dict, method: str, path: str, headers=None, body: bytes = b""):
    """Return (status, content_type, body, nonce) so tests can exercise routing without sockets.

    state holds the live in-memory Guard under "guard" and a factory under "fresh" for /api/reset.
    """
    headers = headers or {}
    host = headers.get("Host") or ""
    # A DNS-rebinding page reaches 127.0.0.1 under its own hostname; refusing foreign Hosts keeps the operator trace local.
    if urlsplit("//" + host).hostname not in {"127.0.0.1", "localhost"}:
        return 403, "application/json", {"error": "Host no permitido"}, None
    url, guard = urlsplit(path), state["guard"]
    routes = {"/": "GET", "/api/preview": "GET", "/api/deliver": "POST", "/api/reset": "POST", **dict.fromkeys(ASSETS, "GET")}
    if url.path not in routes:
        return 404, "application/json", {"error": "Ruta desconocida"}, None
    if method != routes[url.path]:
        return 405, "application/json", {"error": "Método no permitido"}, None
    if url.path in ASSETS:
        kind, name = ASSETS[url.path]
        return 200, kind, (HERE / name).read_bytes(), None
    if method == "POST":
        if headers.get("Origin") != f"http://{host}":
            return 403, "application/json", {"error": "Origen no permitido"}, None
        # JSON content type cannot be sent by a plain cross-site form, a second CSRF barrier.
        if (headers.get("Content-Type") or "").split(";")[0].strip() != "application/json":
            return 415, "application/json", {"error": "Se espera application/json"}, None
        if len(body) > MAX_BODY:
            return 413, "application/json", {"error": "Solicitud demasiado grande"}, None
    if url.path == "/api/reset":
        state["guard"].close()
        state["guard"] = state["fresh"]()
        return 200, "application/json", {"ok": True}, None
    if url.path == "/api/deliver":
        try:
            query = json.loads(body or b"{}")
            if not isinstance(query, dict):
                raise ValueError("Se espera un objeto JSON")
            user, task, draft = fields(guard, query)
            # Every click is a new request; the guard still decides before anything reaches the inbox.
            return 200, "application/json", evaluate(guard, user, task, draft, "web_" + secrets.token_hex(6)), None
        except ValueError as exc:  # json.JSONDecodeError and UnicodeDecodeError are ValueErrors
            return 400, "application/json", {"error": str(exc)}, None
    if url.path == "/":
        nonce = secrets.token_urlsafe(16)
        return 200, "text/html; charset=utf-8", page(guard, nonce), nonce
    try:
        query = {k: v[0] for k, v in parse_qs(url.query).items()}
        return 200, "application/json", evaluate(guard, *fields(guard, query)), None
    except ValueError as exc:
        return 400, "application/json", {"error": str(exc)}, None


def serve(policy, case, history, port=8000):
    if not 0 < port < 65536:
        raise ValueError(f"Puerto inválido: {port}")
    observations = Batch.load(history).observations

    def fresh():
        guard = Guard(":memory:", policy, case)
        guard.observe(observations)
        return guard

    state = {"guard": fresh(), "fresh": fresh}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.reply(respond(state, "GET", self.path, self.headers))

        def do_POST(self):
            try:
                length = max(0, int(self.headers.get("Content-Length") or 0))
            except ValueError:
                length = 0
            # Read at most one byte past the limit so an oversized body is detected without buffering it.
            self.reply(respond(state, "POST", self.path, self.headers, self.rfile.read(min(length, MAX_BODY + 1))))

        def reply(self, response):
            status, kind, body, nonce = response
            data = body if isinstance(body, bytes) else (body if isinstance(body, str) else json.dumps(body, ensure_ascii=False)).encode()
            self.send_response(status)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Security-Policy", f"default-src 'none'; connect-src 'self'; img-src 'self'; font-src 'self'; "
                             f"base-uri 'none'; form-action 'none'; frame-ancestors 'none'; script-src 'nonce-{nonce}'; style-src 'nonce-{nonce}'")
            self.end_headers()
            self.wfile.write(data)

    # shortcut: single-threaded server on loopback, so requests never race on the shared in-memory Guard; add auth before exposing it.
    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"mosAIc demo en http://127.0.0.1:{port}/ (Ctrl+C para salir)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        state["guard"].close()
