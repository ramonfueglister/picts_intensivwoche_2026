const PHASES = [
  {n:1, name:"Rubrik-Ingestion"},
  {n:2, name:"Universum-Komposition"},
  {n:3, name:"Konzept"},
  {n:4, name:"Parallel-Fanout (11 Subagenten)"},
  {n:5, name:"VA-Haupttext"},
  {n:6, name:"Redaktor-Pass"},
  {n:7, name:"Rubrik-Self-Check"},
  {n:8, name:"PDF-Render & Bundle"},
];

const screens = {
  start: document.getElementById("screen-start"),
  running: document.getElementById("screen-running"),
  done: document.getElementById("screen-done"),
};
function show(name) {
  Object.values(screens).forEach(s => s.classList.remove("active"));
  screens[name].classList.add("active");
}

const startBtn = document.getElementById("start-btn");
const topicInput = document.getElementById("topic");
const rahmenInput = document.getElementById("rahmen");
const phaseList = document.getElementById("phase-list");
const streamEl = document.getElementById("stream");
const eventsEl = document.getElementById("events");
const elapsedEl = document.getElementById("elapsed");
const progressBar = document.getElementById("progress-bar");
const progressPct = document.getElementById("progress-pct");
const finalSummary = document.getElementById("final-summary");
const artifactGrid = document.getElementById("artifact-grid");
const rubricTable = document.getElementById("rubric-table");

function renderPhases(currentPhase, phaseStatus) {
  phaseList.innerHTML = PHASES.map(p => {
    const cls = phaseStatus[p.n] === "done" ? "done"
             : (p.n === currentPhase ? "running" : "pending");
    return `<li class="${cls}" data-phase="${p.n}">${p.n}  ${p.name}</li>`;
  }).join("");
}

let startTs = null;
function tickElapsed() {
  if (!startTs) return;
  const s = Math.floor((Date.now() - startTs) / 1000);
  const m = String(Math.floor(s/60)).padStart(2, "0");
  const sec = String(s%60).padStart(2, "0");
  elapsedEl.textContent = `${m}:${sec}`;
}
setInterval(tickElapsed, 1000);

startBtn.addEventListener("click", async () => {
  startTs = Date.now();
  show("running");
  renderPhases(1, {});
  const body = { topic: topicInput.value, rahmen: rahmenInput.value };
  await fetch("/api/start", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body) });
  const es = new EventSource("/api/stream");
  const phaseStatus = {};
  es.addEventListener("phase", e => {
    const d = JSON.parse(e.data).data;
    if (d.status === "done") phaseStatus[d.phase] = "done";
    const currentPhase = d.phase + (d.status === "done" ? 1 : 0);
    renderPhases(Math.min(currentPhase, 8), phaseStatus);
    const pct = Math.round((Object.keys(phaseStatus).length / 8) * 100);
    progressBar.style.width = pct + "%";
    progressPct.textContent = pct + " %";
    addEvent(`Phase ${d.phase} · ${d.name} · ${d.status}`);
  });
  es.addEventListener("subtask", e => {
    const d = JSON.parse(e.data).data;
    addEvent(`  └ ${d.task}: ${d.status} ${d.detail || ""}`);
  });
  es.addEventListener("stream", e => {
    const d = JSON.parse(e.data).data;
    streamEl.textContent += d.delta;
    streamEl.scrollTop = streamEl.scrollHeight;
  });
  es.addEventListener("error", e => {
    try { const d = JSON.parse(e.data).data; addEvent(`⚠️ ${d.task || ""}: ${d.message}`); } catch {}
  });
  es.addEventListener("done", async e => {
    es.close();
    await renderDone();
  });
});

function addEvent(text) {
  const li = document.createElement("li");
  const time = new Date().toLocaleTimeString();
  li.textContent = `${time}  ${text}`;
  eventsEl.insertBefore(li, eventsEl.firstChild);
  while (eventsEl.childElementCount > 40) eventsEl.removeChild(eventsEl.lastChild);
}

async function renderDone() {
  const [artifacts, score] = await Promise.all([
    fetch("/api/artifacts").then(r => r.json()),
    fetch("/api/score").then(r => r.json()),
  ]);
  const totalS = Math.floor((Date.now() - startTs) / 1000);
  finalSummary.textContent = `${Math.floor(totalS/60)}:${String(totalS%60).padStart(2,"0")} Min · ${artifacts.length} Artefakte`;
  artifactGrid.innerHTML = artifacts.map(a => `
    <div class="artifact">
      <span>${a.filename} <small>(${Math.round(a.size/1024)} KB)</small></span>
      <span><a href="/api/artifacts/${encodeURIComponent(a.filename)}" target="_blank">Öffnen</a>
           <a href="/api/artifacts/${encodeURIComponent(a.filename)}" download>↓</a></span>
    </div>
  `).join("");

  if (score.ready) {
    rubricTable.innerHTML = `
      <tr><th>Teil</th><th>Score</th></tr>
      <tr><td>A · Prozess</td><td>${score.teile.A_prozess.score} / 30</td></tr>
      <tr><td>B · Produkt</td><td>${score.teile.B_produkt.score} / 50</td></tr>
      <tr><td>C · Präsentation</td><td>${score.teile.C_praesentation.score} / 40</td></tr>
      <tr class="total"><td>Total</td><td>${score.total} / 120 = Note ${score.note}</td></tr>
    `;
  }
  show("done");
}
