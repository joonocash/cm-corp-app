const STORAGE_KEY = "webinar_signups_v1";

const tbody = document.getElementById("tbody");
const q = document.getElementById("q");
const totalCount = document.getElementById("totalCount");
const shownCount = document.getElementById("shownCount");
const notice = document.getElementById("notice");

document.getElementById("year").textContent = new Date().getFullYear();

function showNotice(message, type="ok"){
  notice.className = "notice " + (type === "bad" ? "bad" : "ok");
  notice.textContent = message;
  notice.style.display = "block";
  window.clearTimeout(showNotice._t);
  showNotice._t = window.setTimeout(() => { notice.style.display = "none"; }, 2400);
}

function readSignups(){
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]"); }
  catch { return []; }
}

function writeSignups(list){
  localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
}

function formatTs(iso){
  try{
    const d = new Date(iso);
    return d.toLocaleString();
  }catch{
    return iso || "";
  }
}

function matches(item, query){
  const s = (query || "").trim().toLowerCase();
  if (!s) return true;
  const hay = `${item.firstName||""} ${item.lastName||""} ${item.email||""}`.toLowerCase();
  return hay.includes(s);
}

function render(){
  const list = readSignups()
    .slice()
    .sort((a,b) => String(b.ts||"").localeCompare(String(a.ts||""))); // newest first

  const filtered = list.filter(item => matches(item, q.value));

  totalCount.textContent = String(list.length);
  shownCount.textContent = String(filtered.length);

  tbody.innerHTML = "";
  if (filtered.length === 0){
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td colspan="7" class="muted" style="padding:16px 12px;">
        No signups found. Go to <a href="/">index</a> and submit the form to create one.
      </td>`;
    tbody.appendChild(tr);
    return;
  }

  filtered.forEach((item, idx) => {
    const tr = document.createElement("tr");
    const consent = item.consent ? `<span class="tag ok">Yes</span>` : `<span class="tag">No</span>`;
    tr.innerHTML = `
      <td>${escapeHtml(item.firstName || "")}</td>
      <td>${escapeHtml(item.lastName || "")}</td>
      <td>${escapeHtml(item.email || "")}</td>
      <td class="muted">${escapeHtml(item.webinar || "")}</td>
      <td>${consent}</td>
      <td class="muted">${escapeHtml(formatTs(item.ts || ""))}</td>
      <td>
        <div class="rowActions">
          <button class="btn mini" type="button" data-action="copy" data-email="${escapeHtml(item.email || "")}">Copy email</button>
          <button class="btn mini danger" type="button" data-action="delete" data-idx="${idx}">Delete</button>
        </div>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function escapeHtml(str){
  return String(str)
    .replaceAll("&","&amp;")
    .replaceAll("<","&lt;")
    .replaceAll(">","&gt;")
    .replaceAll('"',"&quot;")
    .replaceAll("'","&#039;");
}

function exportCsv(){
  const list = readSignups().slice().sort((a,b) => String(a.ts||"").localeCompare(String(b.ts||"")));
  const header = ["firstName","lastName","email","webinar","consent","timestamp"];
  const rows = list.map(x => [
    x.firstName||"",
    x.lastName||"",
    x.email||"",
    x.webinar||"",
    x.consent ? "true" : "false",
    x.ts||""
  ]);

  const csv = [header, ...rows]
    .map(r => r.map(cell => `"${String(cell).replaceAll('"','""')}"`).join(","))
    .join("\n");

  const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = `webinar-signups-${new Date().toISOString().slice(0,10)}.csv`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);

  showNotice("CSV exported.");
}

// Events
q.addEventListener("input", render);

document.getElementById("refreshBtn").addEventListener("click", () => {
  render();
  showNotice("Refreshed.");
});

document.getElementById("exportBtn").addEventListener("click", exportCsv);

document.getElementById("clearBtn").addEventListener("click", () => {
  const ok = confirm("This will delete ALL signups from localStorage on this browser. Continue?");
  if (!ok) return;
  writeSignups([]);
  render();
  showNotice("All signups cleared.", "bad");
});

tbody.addEventListener("click", async (e) => {
  const btn = e.target.closest("button");
  if (!btn) return;

  const action = btn.getAttribute("data-action");
  if (action === "copy"){
    const email = btn.getAttribute("data-email") || "";
    try{
      await navigator.clipboard.writeText(email);
      showNotice("Email copied to clipboard.");
    }catch{
      showNotice("Could not copy (browser blocked clipboard).", "bad");
    }
    return;
  }

  if (action === "delete"){
    const idxStr = btn.getAttribute("data-idx");
    const idx = Number(idxStr);
    if (!Number.isFinite(idx)) return;

    const list = readSignups()
      .slice()
      .sort((a,b) => String(b.ts||"").localeCompare(String(a.ts||""))); // same sort as render

    const item = list[idx];
    const ok = confirm(`Delete signup for ${item?.email || "this entry"}?`);
    if (!ok) return;

    list.splice(idx, 1);
    // Save back (keep saved order as newest-first; admin will sort anyway)
    writeSignups(list);
    render();
    showNotice("Signup deleted.", "bad");
  }
});

// Initial render
render();
