/* ═══════════════════════════════════════════════════════════
   js/ui.js
   DOM Helpers, Component Builders, Modal, Toast.
   DEPENDS ON: nothing (pure DOM utilities)
   USED BY: tabs.js, app.js
   ═══════════════════════════════════════════════════════════ */

/* ─── DOM Shortcuts ─────────────────────────────────────── */
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

/**
 * Create a DOM element with attributes and children.
 * Attrs recognised:
 *   class  → node.className
 *   html   → node.innerHTML
 *   text   → node.textContent
 *   on*    → addEventListener (e.g. onclick, onkeydown)
 *   *      → setAttribute
 * Children: string or Element nodes
 */
function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if      (k === "class")     node.className = v;
    else if (k === "html")      node.innerHTML = v;
    else if (k === "text")      node.textContent = v;
    else if (k.startsWith("on")) node.addEventListener(k.slice(2), v);
    else                        node.setAttribute(k, v);
  }
  for (const child of children) {
    if (child == null) continue;
    node.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
  }
  return node;
}


/* ─── Screen Switcher ───────────────────────────────────── */
function showScreen(id) {
  $$(".screen").forEach(s => s.classList.remove("active"));
  const target = document.getElementById(id);
  if (target) target.classList.add("active");
}


/* ─── Header ────────────────────────────────────────────── */
function populateHeader(role, user) {
  $("#header-user-name").textContent = user.name;
  $("#header-user-role").textContent = role === "student"
    ? `Level ${user.level} — Sem ${user.semester}`
    : "Lecturer";

  const nav  = $("#header-nav");
  nav.innerHTML = "";

  const tabs = role === "student"
    ? [{ id: "chat", label: "Chat" }, { id: "reminders", label: "Reminders" }]
    : [
        { id: "analytics", label: "Analytics" },
        { id: "planner",   label: "Semester Planner" },
        { id: "knowledge", label: "Knowledge Base" },
        { id: "reports",   label: "Reports" },
      ];

  tabs.forEach((t, i) => {
    nav.appendChild(el("button", {
      class:     `nav-tab${i === 0 ? " active" : ""}`,
      "data-tab": t.id,
      onclick:   () => switchTab(t.id),
    }, t.label));
  });
}

function switchTab(tabId) {
  $$(".nav-tab").forEach(b  => b.classList.toggle("active", b.dataset.tab === tabId));
  $$(".tab-panel").forEach(p => p.classList.toggle("active", p.id === `${tabId}-panel`));
}


/* ─── Chat Bubble ───────────────────────────────────────── */
/* ─── Markdown Renderer ────────────────────────────────────
   Converts the bot's markdown-style responses into clean HTML.
   Handles: fenced code blocks, inline code, bold, italic,
   bullet lists, numbered lists, tables, headers, blockquotes.
   ────────────────────────────────────────────────────────── */
function _renderMarkdown(text) {
  if (!text) return "";
  let html = text;

  // 1. Fenced code blocks  ```lang\n...\n```
  html = html.replace(/```(\w*)\n?([\s\S]*?)```/g, (_, lang, code) => {
    const langName  = lang ? lang.toUpperCase() : "CODE";
    const escaped   = code
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .trimEnd();
    return `<div class="code-block-wrap">` +
      `<div class="code-lang">` +
        `<span class="code-lang-name">${langName}</span>` +
        `<span class="code-lang-badge">Code Example</span>` +
      `</div>` +
      `<pre class="code-block"><code>${escaped}</code></pre>` +
    `</div>`;
  });

  // 2. Inline code  `code`
  html = html.replace(/`([^`\n]+)`/g, '<code class="inline-code">$1</code>');

  // 3. Headers  ### ## #
  html = html.replace(/^### (.+)$/gm, '<h4 class="md-h4">$1</h4>');
  html = html.replace(/^## (.+)$/gm,  '<h3 class="md-h3">$1</h3>');
  html = html.replace(/^# (.+)$/gm,   '<h2 class="md-h2">$1</h2>');

  // 4. Bold  **text**
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

  // 5. Italic  *text* or _text_
  html = html.replace(/(?<![*])\*([^*\n]+)\*(?![*])/g, '<em>$1</em>');
  html = html.replace(/\_([^_\n]+)\_/g, '<em>$1</em>');

  // 6. Tables  | col | col |
  html = html.replace(/((?:\|.+\|\n?)+)/g, (tableBlock) => {
    const rows = tableBlock.trim().split("\n").filter(r => r.trim().startsWith("|"));
    if (rows.length < 2) return tableBlock;
    let out = '<div class="md-table-wrap"><table class="md-table">';
    rows.forEach((row, idx) => {
      if (/^\|[-| :]+\|$/.test(row.trim())) return; // skip separator
      const cells = row.split("|").filter((_, i, a) => i > 0 && i < a.length - 1);
      const tag   = idx === 0 ? "th" : "td";
      out += "<tr>" + cells.map(c => `<${tag}>${c.trim()}</${tag}>`).join("") + "</tr>";
    });
    out += "</table></div>";
    return out;
  });

  // 7. Unordered lists  - item or • item
  html = html.replace(/^[\-•] (.+)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>\n?)+/gs, m => `<ul class="md-ul">${m}</ul>`);

  // 8. Numbered lists  1. item
  html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');

  // 9. Horizontal rule ---
  html = html.replace(/^---+$/gm, '<hr class="md-hr">');

  // 10. Blockquote  > text
  html = html.replace(/^> (.+)$/gm, '<blockquote class="md-blockquote">$1</blockquote>');

  // 11. Line breaks — double newline → paragraph break, single → <br>
  html = html.replace(/\n\n/g, '</p><p class="md-p">');
  html = html.replace(/\n(?!<)/g, '<br>');
  html = `<p class="md-p">${html}</p>`;

  // 12. Clean up empty paragraphs
  html = html.replace(/<p class="md-p"><\/p>/g, "");
  html = html.replace(/<p class="md-p">(<(?:ul|ol|table|div|h[2-4]|hr|blockquote))/g, "$1");
  html = html.replace(/(<\/(?:ul|ol|table|div|h[2-4]|hr|blockquote)>)<\/p>/g, "$1");

  return html;
}

function buildBubble(msg) {
  const { role, content } = msg;
  const isUser = role === "user";
  const row    = el("div", { class: `bubble-row${isUser ? " user" : ""}` });

  if (!isUser) {
    row.appendChild(el("div", { class: "bubble-avatar", text: "A" }));
  }

  const wrap   = el("div", { class: "bubble-content" });
  const bubble = el("div", { class: `bubble ${isUser ? "user" : "assistant"}` });

  if (isUser) {
    bubble.textContent = content;   // user messages — plain text, no markdown
  } else {
    bubble.innerHTML = _renderMarkdown(content);  // bot messages — full markdown
    // Reading progress bar for long responses (> 400 chars)
    if (content && content.length > 400) {
      const progressBar = document.createElement("div");
      progressBar.className = "read-progress-wrap";
      const progressFill = document.createElement("div");
      progressFill.className = "read-progress-fill";
      progressBar.appendChild(progressFill);
      wrap.appendChild(progressBar);
      wrap.appendChild(bubble);
      // Track scroll position in the chat to update progress
      requestAnimationFrame(() => {
        const msgs = document.getElementById("chat-messages");
        if (!msgs) return;
        const updateProgress = () => {
          const bTop    = bubble.getBoundingClientRect().top;
          const bBot    = bubble.getBoundingClientRect().bottom;
          const winH    = window.innerHeight;
          const total   = bBot - bTop;
          const seen    = Math.min(winH, Math.max(0, winH - bTop));
          const pct     = total > 0 ? Math.min(100, Math.round((seen / total) * 100)) : 0;
          progressFill.style.width = pct + "%";
          if (pct >= 100) {
            progressBar.classList.add("read-done");
          }
        };
        msgs.addEventListener("scroll", updateProgress, { passive: true });
        updateProgress();
      });
    }
  }

  wrap.appendChild(bubble);

  // Resource recommendation (if knowledge base entry has a link)
  if (!isUser && msg.resource_url) {
    const resRow = el("div", { class: "resource-recommend-row" });
    resRow.innerHTML = `<span class="resource-icon">📎</span>` +
      `<span class="resource-label">Recommended: </span>` +
      `<a class="resource-link" href="${msg.resource_url}" target="_blank" rel="noopener">${msg.resource_url}</a>`;
    wrap.appendChild(resRow);
  }

  row.appendChild(wrap);
  return row;
}


/* ─── Typing Indicator ──────────────────────────────────── */
function showTyping(visible) {
  const ind = $("#typing-indicator");
  if (ind) ind.classList.toggle("visible", visible);
  if (visible) scrollChatBottom();
}

function scrollChatBottom() {
  const msgs = $("#chat-messages");
  if (msgs) msgs.scrollTop = msgs.scrollHeight;
}


/* ─── Reminder Card ─────────────────────────────────────── */
function buildReminderCard(r, isLecturer, onEdit, onDelete) {
  const icons = { exam: "📝", assignment: "📋", project: "🚀" };
  const today = new Date();
  const due   = new Date(r.date);
  const days  = Math.ceil((due - today) / 86400000);
  const dCls  = days < 0  ? "days-past"   : days <= 5 ? "days-urgent" : "days-ok";
  const dText = days < 0  ? "Past due"    : `${days}d left`;

  const card = el("div", { class: `reminder-card ${r.type}` });
  card.appendChild(el("div", { class: "reminder-icon", text: icons[r.type] || "📌" }));

  const body = el("div", { class: "reminder-body" });
  body.appendChild(el("div", { class: "reminder-title", text: r.title }));
  body.appendChild(el("div", { class: "reminder-desc",  text: r.description || "" }));
  const badge = el("div", { style: "margin-top:4px;" });
  badge.appendChild(el("span", { class: "chip chip-navy", text: r.level === "all" ? "All Levels" : `Level ${r.level}` }));
  body.appendChild(badge);
  card.appendChild(body);

  const meta = el("div", { class: "reminder-meta" });
  meta.appendChild(el("div", { class: "reminder-date", text: due.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" }) }));
  meta.appendChild(el("div", { class: `reminder-days ${dCls}`, text: dText }));

  if (isLecturer) {
    const actions = el("div", { style: "display:flex;gap:6px;margin-top:8px;" });
    actions.appendChild(el("button", { class: "btn-secondary", style: "padding:5px 12px;font-size:12px;", onclick: () => onEdit(r)     }, "Edit"));
    actions.appendChild(el("button", { class: "btn-danger",    style: "padding:5px 10px;font-size:12px;", onclick: () => onDelete(r.id) }, "Delete"));
    meta.appendChild(actions);
  }

  card.appendChild(meta);
  return card;
}


/* ─── Bar Chart ─────────────────────────────────────────── */
function buildBarChart(data) {
  if (!data || data.length === 0) {
    return el("p", { class: "text-muted", text: "No data recorded yet." });
  }
  const maxVal = Math.max(...data.map(d => d.count || 0), 1);
  const chart  = el("div", { class: "bar-chart" });

  data.forEach(item => {
    const label = (item.label || item.intent || "").replace(/_/g, " ");
    const row   = el("div", { class: "bar-row" });
    row.appendChild(el("div", { class: "bar-label", text: label }));
    const track = el("div", { class: "bar-track" });
    const fill  = el("div", { class: "bar-fill" });
    fill.style.width = `${((item.count || 0) / maxVal) * 100}%`;
    fill.appendChild(el("span", { class: "bar-count", text: item.count || 0 }));
    track.appendChild(fill);
    row.appendChild(track);
    chart.appendChild(row);
  });

  return chart;
}


/* ─── Weekly Chart ──────────────────────────────────────── */
function buildWeeklyChart(values) {
  const maxVal = Math.max(...values.map(v => (typeof v === "object" ? v.count : v) || 0), 1);
  const wrap   = el("div", { class: "weekly-chart" });

  values.forEach((v, i) => {
    const count   = typeof v === "object" ? v.count : v;
    const dayName = typeof v === "object" ? v.day   : ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][i];
    const col     = el("div", { class: "week-col" });
    const bWrap   = el("div", { class: "week-bar-wrap" });
    const bar     = el("div", { class: `week-bar${i === values.length - 1 ? " today" : ""}` });
    bar.style.height = `${(count / maxVal) * 90}px`;
    bar.appendChild(el("div", { class: "week-bar-val", text: count }));
    bWrap.appendChild(bar);
    col.appendChild(bWrap);
    col.appendChild(el("div", { class: "week-day", text: dayName }));
    wrap.appendChild(col);
  });

  return wrap;
}


/* ─── Knowledge Base Item ───────────────────────────────── */
function buildKBItem(item, onEdit, onDelete) {
  const card = el("div", { class: "kb-item", "data-id": item.id });
  const body = el("div", { class: "kb-body" });

  const nameRow = el("div", { style: "display:flex;align-items:center;gap:8px;margin-bottom:6px;" });
  nameRow.appendChild(el("span", { class: "kb-intent-name", text: item.intent_name }));
  nameRow.appendChild(el("span", { class: "chip chip-gold",  text: `L${item.level}` }));
  body.appendChild(nameRow);

  const kws = Array.isArray(item.keywords)
    ? item.keywords.join(" · ")
    : (item.keywords || "").split(",").map(k => k.trim()).join(" · ");
  body.appendChild(el("div", { class: "kb-keywords", text: `Keywords: ${kws}` }));

  const resp = item.response_text || "";
  body.appendChild(el("div", { class: "kb-response", text: resp.length > 130 ? resp.slice(0, 130) + "…" : resp }));
  card.appendChild(body);

  const actions = el("div", { class: "kb-actions" });
  actions.appendChild(el("button", { class: "btn-secondary", style: "padding:6px 14px;font-size:13px;", onclick: () => onEdit(item) }, "Edit"));
  actions.appendChild(el("button", { class: "btn-danger", onclick: () => onDelete(item.id) }, "Delete"));
  card.appendChild(actions);

  return card;
}


/* ─── Modal ─────────────────────────────────────────────── */
const Modal = {
  open(title, bodyHTML, onSave) {
    $("#modal-title").textContent = title;
    $("#modal-body").innerHTML    = bodyHTML;
    $("#modal-overlay").classList.remove("hidden");

    // Replace save button to clear previous event listeners
    const saveBtn = $("#modal-save-btn");
    const newSave = saveBtn.cloneNode(true);
    saveBtn.parentNode.replaceChild(newSave, saveBtn);
    newSave.addEventListener("click", onSave);
  },

  close() {
    $("#modal-overlay").classList.add("hidden");
    $("#modal-body").innerHTML = "";
  },

  getVal(id) {
    const node = document.getElementById(id);
    return node ? node.value.trim() : "";
  },
};


/* ─── Toast ─────────────────────────────────────────────── */
function toast(message, type = "success") {
  // Remove existing toasts
  document.querySelectorAll(".toast").forEach(t => t.remove());

  const colors = {
    success: { bg: "#f0fdf4", border: "#22c55e", color: "#15803d" },
    error:   { bg: "#fff1f1", border: "#ef4444", color: "#c0392b" },
    info:    { bg: "#eff6ff", border: "#3b82f6", color: "#1d4ed8" },
  };
  const c = colors[type] || colors.success;

  const t = document.createElement("div");
  t.className   = "toast";
  t.textContent = message;
  Object.assign(t.style, {
    position:   "fixed",
    bottom:     "24px",
    right:      "24px",
    zIndex:     "9999",
    padding:    "12px 20px",
    borderRadius: "8px",
    background: c.bg,
    border:     `1px solid ${c.border}`,
    color:      c.color,
    fontSize:   "13px",
    fontWeight: "500",
    boxShadow:  "0 4px 16px rgba(0,0,0,0.12)",
    fontFamily: "'DM Sans', sans-serif",
    animation:  "slideUp 0.3s ease",
  });

  document.body.appendChild(t);
  setTimeout(() => {
    t.style.opacity    = "0";
    t.style.transition = "opacity 0.3s";
    setTimeout(() => t.remove(), 300);
  }, 3000);
}
