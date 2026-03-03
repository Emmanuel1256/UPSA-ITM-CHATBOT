/* ═══════════════════════════════════════════════════════════
   js/tabs.js  —  Tab Panel Renderers
   DEPENDS ON: api.js, ui.js
   ═══════════════════════════════════════════════════════════ */

/* ── ENTRY POINT ─────────────────────────────────────────── */
function buildAllPanels(role, user) {
  const main = $("#app-main");
  main.innerHTML = "";
  if (role === "student") {
    main.appendChild(buildChatPanel(user));
    main.appendChild(buildRemindersPanel(user));
    switchTab("chat");
  } else {
    main.appendChild(buildAnalyticsPanel());
    main.appendChild(buildPlannerPanel());
    main.appendChild(buildKnowledgePanel());
    main.appendChild(buildReportsPanel());
    switchTab("analytics");
  }
}

/* ── Override populateHeader to add Planner tab for lecturers ── */
const _origPopulateHeader = populateHeader;
function populateHeader(role, user) {
  $("#header-user-name").textContent = user.name;
  $("#header-user-role").textContent = role === "student"
    ? `Level ${user.level} — Sem ${user.semester}` : "Lecturer";

  const nav = $("#header-nav");
  nav.innerHTML = "";

  const tabs = role === "student"
    ? [{ id: "chat", label: "Chat" }, { id: "reminders", label: "Reminders" }]
    : [
        { id: "analytics", label: "Dashboard" },
        { id: "planner",   label: "📅 Semester Planner" },
        { id: "knowledge", label: "Knowledge Base" },
        { id: "reports",   label: "Reports" },
      ];

  tabs.forEach((t, i) => {
    nav.appendChild(el("button", {
      class: `nav-tab${i === 0 ? " active" : ""}`,
      "data-tab": t.id,
      onclick: () => switchTab(t.id),
    }, t.label));
  });
}


/* ═══════════════════════════════════════════════════════════
   CHAT PANEL
   ═══════════════════════════════════════════════════════════ */
function buildChatPanel(user) {
  const panel = el("div", { class: "tab-panel", id: "chat-panel" });
  const messages = el("div", { id: "chat-messages" });
  const typingInd = el("div", { id: "typing-indicator" });
  typingInd.appendChild(el("div", { class: "bubble-avatar", text: "A" }));
  const typBubble = el("div", { class: "typing-bubble" });
  [0,1,2].forEach(() => typBubble.appendChild(el("div", { class: "typing-dot" })));
  typingInd.appendChild(typBubble);
  messages.appendChild(typingInd);
  panel.appendChild(messages);

  const suggestRow = el("div", { id: "suggestions-row" });
  ["Explain C++ loops","What is the OSI model?","When is assignment due?","How is CGPA calculated?"]
    .forEach(s => suggestRow.appendChild(el("button", {
      class: "suggestion-chip",
      onclick: () => { $("#chat-input").value = s; sendChatMessage(); },
    }, s)));
  panel.appendChild(suggestRow);

  const inputBar = el("div", { id: "chat-input-bar" });
  const inputRow = el("div", { class: "chat-input-row" });
  const input = el("input", { type: "text", id: "chat-input",
    placeholder: "Ask about your courses, exams, assignments…",
    onkeydown: (e) => { if (e.key === "Enter") sendChatMessage(); } });
  inputRow.appendChild(input);
  inputRow.appendChild(el("button", { class: "btn-primary", id: "chat-send-btn",
    onclick: sendChatMessage }, "Send"));
  inputBar.appendChild(inputRow);
  panel.appendChild(inputBar);
  _loadChatHistory(messages, suggestRow);
  return panel;
}

async function _loadChatHistory(messagesEl, suggestRow) {
  try {
    const data = await ChatAPI.getHistory();
    if (data.messages && data.messages.length > 0) {
      if (suggestRow) suggestRow.style.display = "none";
      data.messages.forEach(msg => _appendBubble(messagesEl, msg));
    } else {
      _appendBubble(messagesEl, { role:"assistant", confidence:100,
        content:"Welcome! 👋 I'm your UPSA ITM Academic Assistant. Ask me anything about your courses, assignments, or exams." });
    }
  } catch {
    _appendBubble(messagesEl, { role:"assistant", confidence:100,
      content:"Welcome! 👋 Ask me anything about your ITM courses." });
  }
}

function _appendBubble(container, msgData) {
  const ti = container.querySelector("#typing-indicator");
  const b  = buildBubble(msgData);
  ti ? container.insertBefore(b, ti) : container.appendChild(b);
  scrollChatBottom();
}

async function sendChatMessage() {
  const input = $("#chat-input");
  const text  = input ? input.value.trim() : "";
  if (!text) return;
  const messagesEl = $("#chat-messages");
  const suggestRow = $("#suggestions-row");
  if (suggestRow) suggestRow.style.display = "none";
  _appendBubble(messagesEl, { role:"user", content:text });
  input.value = "";
  const sendBtn = $("#chat-send-btn");
  if (sendBtn) sendBtn.disabled = true;
  if (input)   input.disabled   = true;
  showTyping(true);
  try {
    const data = await ChatAPI.sendMessage(text);
    showTyping(false);
    _appendBubble(messagesEl, { ...data.bot_message, motivation: data.motivation });
  } catch (err) {
    showTyping(false);
    _appendBubble(messagesEl, { role:"assistant", confidence:0,
      content:`Sorry, I couldn't process that. (${err.message})` });
  } finally {
    if (sendBtn) sendBtn.disabled = false;
    if (input)   { input.disabled = false; input.focus(); }
  }
}


/* ═══════════════════════════════════════════════════════════
   REMINDERS PANEL
   ═══════════════════════════════════════════════════════════ */
function buildRemindersPanel(user) {
  const panel      = el("div", { class: "tab-panel", id: "reminders-panel" });
  const isLecturer = user.role === "lecturer";
  const headerRow  = el("div", { style:"display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:24px;" });
  const titleWrap  = el("div");
  titleWrap.appendChild(el("h2", { class:"page-title", text:"Reminders" }));
  titleWrap.appendChild(el("p",  { class:"page-subtitle",
    text: isLecturer ? "All student reminders" : `Level ${user.level} — Semester ${user.semester}` }));
  headerRow.appendChild(titleWrap);
  if (isLecturer) headerRow.appendChild(el("button", { class:"btn-primary",
    onclick:() => _openReminderModal("add", null) }, "+ Add Reminder"));
  panel.appendChild(headerRow);
  panel.appendChild(el("div", { id:"reminders-list" }));
  _loadReminders();
  return panel;
}

async function _loadReminders() {
  const list = $("#reminders-list");
  if (!list) return;
  list.innerHTML = `<p class="text-muted" style="padding:16px 0;">Loading reminders…</p>`;
  const user       = Auth.getUser();
  const isLecturer = user && user.role === "lecturer";
  try {
    const data = await RemindersAPI.getAll();
    list.innerHTML = "";
    if (!data.reminders || data.reminders.length === 0) {
      list.appendChild(el("p", { class:"text-muted", style:"padding:16px 0;", text:"No reminders found." }));
      return;
    }
    data.reminders.forEach(r => list.appendChild(buildReminderCard(
      r, isLecturer,
      (item) => _openReminderModal("edit", item),
      (id)   => _deleteReminder(id),
    )));
  } catch (err) {
    list.innerHTML = `<p class="login-error" style="padding:16px 0;">Failed to load: ${err.message}</p>`;
  }
}

function _openReminderModal(mode, item = null) {
  const bodyHTML = `
    <div class="form-group">
      <label class="form-label-dark">Title</label>
      <input id="m-r-title" class="form-input-light" value="${item ? item.title : ''}" placeholder="e.g. Mid-Semester Exam" />
    </div>
    <div class="form-group">
      <label class="form-label-dark">Description</label>
      <input id="m-r-desc" class="form-input-light" value="${item ? (item.description||'') : ''}" placeholder="Short description" />
    </div>
    <div style="display:flex;gap:12px;">
      <div class="form-group" style="flex:1;">
        <label class="form-label-dark">Date</label>
        <input type="date" id="m-r-date" class="form-input-light" value="${item ? item.date : ''}" />
      </div>
      <div class="form-group" style="flex:1;">
        <label class="form-label-dark">Time</label>
        <input type="time" id="m-r-time" class="form-input-light" value="${item ? (item.time||'08:00') : '08:00'}" />
      </div>
      <div class="form-group" style="flex:1;">
        <label class="form-label-dark">Week</label>
        <select id="m-r-week" class="form-select-light">
          <option value="">—</option>
          ${Array.from({length:12},(_,i)=>`<option value="${i+1}" ${item?.week==i+1?'selected':''}>Week ${i+1}</option>`).join('')}
        </select>
      </div>
    </div>
    <div style="display:flex;gap:12px;">
      <div class="form-group" style="flex:1;">
        <label class="form-label-dark">Type</label>
        <select id="m-r-type" class="form-select-light">
          ${["assignment","exam","project","lecture","quiz","lab"].map(t =>
            `<option value="${t}" ${item?.type===t?'selected':''}>${t.charAt(0).toUpperCase()+t.slice(1)}</option>`).join('')}
        </select>
      </div>
      <div class="form-group" style="flex:1;">
        <label class="form-label-dark">Level</label>
        <select id="m-r-level" class="form-select-light">
          ${[["all","All Levels"],["100","Level 100"],["200","Level 200"],["300","Level 300"]].map(([v,l])=>
            `<option value="${v}" ${item?.level===v?'selected':''}>${l}</option>`).join('')}
        </select>
      </div>
      <div class="form-group" style="flex:1;">
        <label class="form-label-dark">Semester</label>
        <select id="m-r-semester" class="form-select-light">
          <option value="1" ${item?.semester==="1"?'selected':''}>Semester 1</option>
          <option value="2" ${item?.semester==="2"?'selected':''}>Semester 2</option>
        </select>
      </div>
    </div>`;

  Modal.open(mode === "add" ? "Add Reminder" : "Edit Reminder", bodyHTML, async () => {
    const payload = {
      title: Modal.getVal("m-r-title"), description: Modal.getVal("m-r-desc"),
      date:  Modal.getVal("m-r-date"),  time: Modal.getVal("m-r-time"),
      type:  Modal.getVal("m-r-type"),  level: Modal.getVal("m-r-level"),
      semester: Modal.getVal("m-r-semester"), week: Modal.getVal("m-r-week") || null,
    };
    if (!payload.title || !payload.date) { toast("Title and date are required.", "error"); return; }
    try {
      if (mode === "add") { await RemindersAPI.create(payload); toast("Reminder added."); }
      else                { await RemindersAPI.update(item.id, payload); toast("Reminder updated."); }
      Modal.close(); _loadReminders();
    } catch (err) { toast(err.message, "error"); }
  });
}

async function _deleteReminder(id) {
  if (!confirm("Delete this reminder?")) return;
  try { await RemindersAPI.delete(id); toast("Deleted."); _loadReminders(); }
  catch (err) { toast(err.message, "error"); }
}


/* ═══════════════════════════════════════════════════════════
   ANALYTICS DASHBOARD
   Professional layout — never shows a loading spinner.
   Shows zeros/empty states gracefully if no data yet.
   ═══════════════════════════════════════════════════════════ */
function buildAnalyticsPanel() {
  const panel = el("div", { class: "tab-panel", id: "analytics-panel" });

  // Header with refresh button
  const hdr = el("div", { style:"display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:24px;" });
  const titles = el("div");
  titles.appendChild(el("h2", { class:"page-title", text:"Academic Dashboard" }));
  titles.appendChild(el("p",  { class:"page-subtitle", text:"Student engagement overview · ITM Department" }));
  hdr.appendChild(titles);
  const refreshBtn = el("button", { class:"btn-secondary", style:"font-size:13px;padding:8px 16px;",
    onclick: () => _loadAnalytics() }, "↻ Refresh");
  hdr.appendChild(refreshBtn);
  panel.appendChild(hdr);

  // Stat cards skeleton — filled immediately with zeros, updated when data arrives
  const statGrid = el("div", { class:"stat-grid", id:"stat-grid" });
  [
    { icon:"💬", id:"stat-total",     label:"Total Interactions",   cls:"navy"  },
    { icon:"✅", id:"stat-answered",  label:"Queries Answered",      cls:"green" },
    { icon:"❓", id:"stat-unanswered",label:"Unanswered Queries",     cls:"amber" },
  ].forEach(s => {
    const card = el("div", { class:`stat-card ${s.cls}` });
    card.appendChild(el("div", { class:"stat-icon",  text:s.icon }));
    card.appendChild(el("div", { class:"stat-value", id:s.id, text:"—" }));
    card.appendChild(el("div", { class:"stat-label", text:s.label }));
    statGrid.appendChild(card);
  });
  panel.appendChild(statGrid);

  // Charts row
  const grid = el("div", { class:"analytics-grid" });
  const intentCard = el("div", { class:"card" });
  intentCard.appendChild(el("h3", { class:"section-title", text:"Top Query Intents" }));
  intentCard.appendChild(el("div", { id:"intent-chart", html:"<p class='text-muted' style='font-size:13px;'>No interactions recorded yet.</p>" }));
  grid.appendChild(intentCard);

  const weekCard = el("div", { class:"card" });
  weekCard.appendChild(el("h3", { class:"section-title", text:"Last 7 Days Activity" }));
  weekCard.appendChild(el("div", { id:"weekly-chart" }));
  const levelSec = el("div", { class:"level-rows", style:"margin-top:16px;padding-top:16px;border-top:1px solid #f1f5f9;" });
  levelSec.appendChild(el("h4", { style:"font-size:13px;font-weight:600;color:#6b7280;margin-bottom:10px;", text:"By Level" }));
  levelSec.appendChild(el("div", { id:"level-bars" }));
  weekCard.appendChild(levelSec);
  grid.appendChild(weekCard);
  panel.appendChild(grid);

  // Unanswered section
  const uaCard = el("div", { class:"card", style:"margin-top:20px;" });
  const uaHdr  = el("div", { style:"display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;" });
  uaHdr.appendChild(el("h3", { class:"section-title", style:"margin:0;", text:"Student Unanswered Queries" }));
  uaHdr.appendChild(el("span", { id:"ua-badge", class:"chip chip-amber", text:"Loading…" }));
  uaCard.appendChild(uaHdr);
  uaCard.appendChild(el("div", { id:"ua-list" }));
  panel.appendChild(uaCard);

  // Load data without blocking render
  _loadAnalytics();
  return panel;
}

async function _loadAnalytics() {
  try {
    const [data, uaData] = await Promise.all([
      AnalyticsAPI.getSummary(),
      AnalyticsAPI.getUnanswered(),
    ]);

    // Stat values
    const answered = (data.total_interactions || 0) - (data.unanswered_count || 0);
    _setText("stat-total",      data.total_interactions || 0);
    _setText("stat-answered",   Math.max(answered, 0));
    _setText("stat-unanswered", data.unanswered_count   || 0);

    // Intent chart
    const intentEl = $("#intent-chart");
    if (intentEl) {
      intentEl.innerHTML = "";
      const intents = data.top_intents || [];
      if (intents.length === 0) {
        intentEl.innerHTML = "<p class='text-muted' style='font-size:13px;'>No intent data yet — students haven't chatted.</p>";
      } else {
        intentEl.appendChild(buildBarChart(intents.map(i => ({
          label: (i.intent||"").replace(/_/g," ").replace(/\b\w/g,c=>c.toUpperCase()),
          count: i.count,
        }))));
      }
    }

    // Weekly chart
    const weeklyEl = $("#weekly-chart");
    if (weeklyEl) {
      weeklyEl.innerHTML = "";
      weeklyEl.appendChild(buildWeeklyChart(data.weekly_engagement || []));
    }

    // Level bars
    const levelEl = $("#level-bars");
    if (levelEl) {
      levelEl.innerHTML = "";
      const lvl = data.by_level || {};
      const lvlTotal = Math.max(Object.values(lvl).reduce((a,b)=>a+b,0), 1);
      if (Object.keys(lvl).length === 0) {
        levelEl.innerHTML = "<p class='text-muted' style='font-size:12px;'>No level data yet.</p>";
      } else {
        Object.entries(lvl).forEach(([level, count]) => {
          const row = el("div", { class:"level-row" });
          const track = el("div", { class:"level-track" });
          const fill  = el("div", { class:"level-fill" });
          fill.style.width = `${Math.round((count/lvlTotal)*100)}%`;
          track.appendChild(fill);
          row.appendChild(el("span", { class:"chip chip-navy", style:"min-width:64px;text-align:center;", text:`Level ${level}` }));
          row.appendChild(track);
          row.appendChild(el("span", { class:"level-count", text:count }));
          levelEl.appendChild(row);
        });
      }
    }

    // Unanswered queries
    const queries  = uaData.queries || [];
    const uaBadge  = $("#ua-badge");
    const uaList   = $("#ua-list");
    if (uaBadge) {
      uaBadge.textContent = queries.length > 0 ? `${queries.length} pending` : "All clear ✓";
      uaBadge.className   = queries.length > 0 ? "chip chip-amber" : "chip chip-green";
    }
    if (uaList) {
      uaList.innerHTML = "";
      if (queries.length === 0) {
        uaList.appendChild(el("p", { class:"text-muted", style:"font-size:13px;padding:8px 0;",
          text:"No unanswered queries — the chatbot is handling all student questions." }));
      } else {
        queries.forEach(q => {
          const item = el("div", { class:"unanswered-item" });
          item.appendChild(el("span", { class:"unanswered-icon", text:"⚠️" }));
          const tw = el("div", { class:"unanswered-text" });
          tw.appendChild(el("div", { style:"font-weight:500;", text:q.question }));
          item.appendChild(tw);
          item.appendChild(el("span", { class:"chip chip-navy", style:"flex-shrink:0;", text:`L${q.student_level||"?"}` }));
          item.appendChild(el("span", { class:"unanswered-date", text:(q.date||"").slice(0,10) }));
          uaList.appendChild(item);
        });
      }
    }

  } catch (err) {
    // Show a non-blocking error note — never freeze the page
    ["stat-total","stat-answered","stat-unanswered"].forEach(id => _setText(id, "—"));
    const uaList = $("#ua-list");
    if (uaList) uaList.innerHTML = `<p class="login-error" style="font-size:13px;">Could not load data: ${err.message}</p>`;
  }
}

function _setText(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}


/* ═══════════════════════════════════════════════════════════
   12-WEEK SEMESTER PLANNER
   Lecturers schedule activities per week with exact time.
   Push notifications fire 3 days before → daily → day-of.
   ═══════════════════════════════════════════════════════════ */
function buildPlannerPanel() {
  const panel = el("div", { class:"tab-panel", id:"planner-panel" });

  const hdr = el("div", { style:"display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;" });
  const titles = el("div");
  titles.appendChild(el("h2", { class:"page-title", text:"Semester Activity Planner" }));
  titles.appendChild(el("p",  { class:"page-subtitle",
    text:"Schedule activities for all 12 weeks. Students receive push notifications 3 days before, daily, and on the day itself." }));
  hdr.appendChild(titles);

  // Semester start date picker
  const controls = el("div", { style:"display:flex;gap:10px;align-items:center;flex-shrink:0;" });
  const semSelect = el("select", { class:"form-select-light", id:"planner-sem",
    style:"width:120px;background:rgba(255,255,255,0.1);border-color:rgba(255,255,255,0.2);color:#fff;" });
  [["1","Semester 1"],["2","Semester 2"]].forEach(([v,l]) => {
    semSelect.appendChild(el("option", { value:v }, l));
  });
  const startInput = el("input", { type:"date", id:"planner-start", class:"form-input-light",
    style:"width:155px;", title:"Semester start date" });
  startInput.value = _getDefaultSemStart();
  controls.appendChild(el("label", { style:"color:rgba(255,255,255,0.7);font-size:12px;white-space:nowrap;", text:"Sem start:" }));
  controls.appendChild(startInput);
  controls.appendChild(semSelect);
  hdr.appendChild(controls);
  panel.appendChild(hdr);

  // Push notification status banner
  const pushBanner = el("div", { id:"planner-push-banner",
    style:"margin-bottom:20px;padding:10px 16px;border-radius:8px;font-size:13px;background:rgba(197,161,0,0.1);border:1px solid rgba(197,161,0,0.3);color:#7a5c00;" });
  pushBanner.textContent = "Loading notification status…";
  panel.appendChild(pushBanner);
  _checkPushStatus(pushBanner);

  // 12-week grid
  const grid = el("div", { id:"planner-grid" });
  panel.appendChild(grid);

  // Render weeks
  _buildWeekGrid(grid, startInput, semSelect);

  // Re-render when start date changes
  startInput.addEventListener("change", () => _buildWeekGrid(grid, startInput, semSelect));
  semSelect.addEventListener("change",  () => _buildWeekGrid(grid, startInput, semSelect));

  // Save all button
  const footer = el("div", { style:"display:flex;justify-content:flex-end;gap:12px;margin-top:24px;padding-top:20px;border-top:1px solid #e5e7eb;" });
  footer.appendChild(el("button", { class:"btn-secondary", onclick:() => _loadPlannerFromDB(grid, startInput, semSelect) }, "↻ Load Saved"));
  footer.appendChild(el("button", { class:"btn-primary", style:"padding:12px 28px;font-size:15px;",
    onclick:() => _savePlanner(semSelect) }, "💾 Save All 12 Weeks"));
  panel.appendChild(footer);

  // Load any existing data from DB
  setTimeout(() => _loadPlannerFromDB(grid, startInput, semSelect), 300);

  return panel;
}

function _getDefaultSemStart() {
  const now = new Date();
  // Default to next Monday
  const day  = now.getDay();
  const diff = day === 0 ? 1 : 8 - day;
  const next = new Date(now);
  next.setDate(now.getDate() + diff);
  return next.toISOString().slice(0,10);
}

async function _checkPushStatus(banner) {
  try {
    const data = await apiFetch("/push/vapid-public-key");
    if (data.available) {
      banner.style.background = "rgba(21,128,61,0.1)";
      banner.style.borderColor = "rgba(21,128,61,0.3)";
      banner.style.color = "#15803d";
      banner.textContent = "✅ Push notifications are configured. Students will be notified 3 days before, daily, and on the day of each activity.";
    } else {
      banner.style.background = "rgba(180,83,9,0.08)";
      banner.style.borderColor = "rgba(180,83,9,0.25)";
      banner.style.color = "#b45309";
      banner.innerHTML = "⚠️ Push notifications not configured — VAPID keys missing from <code>.env</code>. " +
        "Run <code>python generate_vapid_keys.py</code> and add the keys to your <code>.env</code> file. " +
        "The semester planner will still save activities and show them to students as reminders.";
    }
  } catch {
    banner.textContent = "Could not check push notification status.";
  }
}

const TYPE_COLORS = {
  lecture:    "#0B1E3F",
  assignment: "#b45309",
  exam:       "#c0392b",
  quiz:       "#7c3aed",
  lab:        "#0369a1",
  project:    "#15803d",
};

const TYPE_ICONS = {
  lecture:"📖", assignment:"📋", exam:"📝", quiz:"🧪", lab:"🔬", project:"🚀"
};

function _buildWeekGrid(grid, startInput, semSelect) {
  grid.innerHTML = "";
  const startDate = new Date(startInput.value || _getDefaultSemStart());

  for (let week = 1; week <= 12; week++) {
    const weekStart = new Date(startDate);
    weekStart.setDate(startDate.getDate() + (week - 1) * 7);
    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekStart.getDate() + 6);

    const weekCard = el("div", { class:"planner-week-card", "data-week":week });

    // Week header
    const wHdr = el("div", { class:"planner-week-header" });
    wHdr.appendChild(el("div", { class:"planner-week-num", text:`Week ${week}` }));
    wHdr.appendChild(el("div", { class:"planner-week-dates",
      text:`${_fmtDate(weekStart)} — ${_fmtDate(weekEnd)}` }));
    wHdr.appendChild(el("button", { class:"planner-add-btn",
      onclick: () => _addActivityRow(activitiesEl, week, weekStart) }, "+ Add Activity"));
    weekCard.appendChild(wHdr);

    const activitiesEl = el("div", { class:"planner-activities", id:`week-activities-${week}` });
    // Placeholder row
    activitiesEl.appendChild(_emptyActivityRow(week, weekStart));
    weekCard.appendChild(activitiesEl);

    grid.appendChild(weekCard);
  }
}

function _fmtDate(d) {
  return d.toLocaleDateString("en-GB", { day:"numeric", month:"short" });
}

function _addActivityRow(container, week, weekStart) {
  // Remove empty placeholder if present
  const placeholder = container.querySelector(".planner-placeholder");
  if (placeholder) placeholder.remove();
  container.appendChild(_newActivityRow(week, weekStart, null));
}

function _emptyActivityRow(week, weekStart) {
  const wrap = el("div", { class:"planner-placeholder",
    style:"padding:12px;text-align:center;color:#9ca3af;font-size:13px;border:1.5px dashed #e5e7eb;border-radius:8px;cursor:pointer;",
    onclick: function() {
      this.parentElement.appendChild(_newActivityRow(week, weekStart, null));
      this.remove();
    }
  }, "Click '+ Add Activity' or here to schedule an activity for this week");
  return wrap;
}

function _newActivityRow(week, weekStart, prefill) {
  // Default date = Monday of that week
  const defDate = new Date(weekStart);
  const row = el("div", { class:"activity-row" });

  // Type selector with colour dot
  const typeSelect = el("select", { class:"activity-type-select" });
  ["lecture","assignment","exam","quiz","lab","project"].forEach(t => {
    const opt = el("option", { value:t }, `${TYPE_ICONS[t]} ${t.charAt(0).toUpperCase()+t.slice(1)}`);
    if (prefill && prefill.type === t) opt.selected = true;
    typeSelect.appendChild(opt);
  });
  typeSelect.addEventListener("change", () => {
    row.style.borderLeftColor = TYPE_COLORS[typeSelect.value] || "#0B1E3F";
  });
  row.style.borderLeftColor = TYPE_COLORS[prefill?.type || "lecture"];

  // Title input
  const titleInput = el("input", { class:"activity-title-input",
    placeholder:"Activity title…", value: prefill?.title || "" });

  // Date picker
  const dateInput = el("input", { type:"date", class:"activity-date-input",
    value: prefill?.date || defDate.toISOString().slice(0,10) });

  // Time picker
  const timeInput = el("input", { type:"time", class:"activity-time-input",
    value: prefill?.time || "08:00", title:"Exact activity time" });

  // Level
  const levelSelect = el("select", { class:"activity-level-select" });
  [["all","All"],["100","L100"],["200","L200"],["300","L300"]].forEach(([v,l]) => {
    const opt = el("option", { value:v }, l);
    if (prefill?.level === v) opt.selected = true;
    levelSelect.appendChild(opt);
  });

  // Remove button
  const removeBtn = el("button", { class:"activity-remove-btn",
    title:"Remove", onclick:() => row.remove() }, "✕");

  // Store the DB id if editing
  if (prefill?.id) row.dataset.id = prefill.id;
  row.dataset.week = week;

  row.appendChild(typeSelect);
  row.appendChild(titleInput);
  row.appendChild(dateInput);
  row.appendChild(timeInput);
  row.appendChild(levelSelect);
  row.appendChild(removeBtn);
  return row;
}

async function _loadPlannerFromDB(grid, startInput, semSelect) {
  try {
    const data = await RemindersAPI.getAll();
    const reminders = (data.reminders || []).filter(r => r.week);
    if (reminders.length === 0) return;

    const startDate = new Date(startInput.value || _getDefaultSemStart());

    reminders.forEach(r => {
      const weekEl = grid.querySelector(`[data-week="${r.week}"]`);
      if (!weekEl) return;
      const activitiesEl = weekEl.querySelector(".planner-activities");
      if (!activitiesEl) return;
      // Remove placeholder
      const ph = activitiesEl.querySelector(".planner-placeholder");
      if (ph) ph.remove();

      const weekStart = new Date(startDate);
      weekStart.setDate(startDate.getDate() + (r.week - 1) * 7);

      // Don't duplicate if already there
      if (activitiesEl.querySelector(`[data-id="${r.id}"]`)) return;
      activitiesEl.appendChild(_newActivityRow(r.week, weekStart, r));
    });

    toast("Semester plan loaded from database.", "info");
  } catch (err) {
    toast("Could not load planner: " + err.message, "error");
  }
}

async function _savePlanner(semSelect) {
  const rows = document.querySelectorAll(".activity-row");
  if (rows.length === 0) { toast("No activities to save.", "info"); return; }

  const toCreate = [];
  const toUpdate = [];

  rows.forEach(row => {
    const week  = parseInt(row.dataset.week);
    const id    = row.dataset.id ? parseInt(row.dataset.id) : null;
    const title = row.querySelector(".activity-title-input")?.value.trim();
    if (!title) return;

    const payload = {
      title,
      date:     row.querySelector(".activity-date-input")?.value,
      time:     row.querySelector(".activity-time-input")?.value || "08:00",
      type:     row.querySelector(".activity-type-select")?.value || "lecture",
      level:    row.querySelector(".activity-level-select")?.value || "all",
      semester: semSelect.value,
      week,
      description: `Week ${week} activity`,
    };

    if (id) { payload.id = id; toUpdate.push(payload); }
    else     { toCreate.push(payload); }
  });

  try {
    const promises = [];
    // Create new rows individually (no bulk endpoint needed)
    toCreate.forEach(p => promises.push(RemindersAPI.create(p)));
    // Update existing rows
    toUpdate.forEach(p => {
      const { id, ...rest } = p;
      promises.push(RemindersAPI.update(id, rest));
    });

    await Promise.all(promises);
    toast(`✅ Saved ${toCreate.length + toUpdate.length} activities. Students will receive push notifications 3 days before, 2 days, 1 day, and on the day — at the exact time set.`);

    // Reload to get IDs assigned to new rows
    const grid = $("#planner-grid");
    const startInput = $("#planner-start");
    if (grid && startInput) {
      _buildWeekGrid(grid, startInput, semSelect);
      setTimeout(() => _loadPlannerFromDB(grid, startInput, semSelect), 400);
    }
  } catch (err) {
    toast("Save failed: " + err.message, "error");
  }
}


/* ═══════════════════════════════════════════════════════════
   KNOWLEDGE BASE PANEL
   ═══════════════════════════════════════════════════════════ */
function buildKnowledgePanel() {
  const panel = el("div", { class:"tab-panel", id:"knowledge-panel" });
  const headerRow = el("div", { class:"kb-header-row" });
  const titleWrap = el("div");
  titleWrap.appendChild(el("h2", { class:"page-title", text:"Knowledge Base Editor" }));
  titleWrap.appendChild(el("p",  { class:"page-subtitle", id:"kb-count-label", text:"Loading…" }));
  headerRow.appendChild(titleWrap);
  headerRow.appendChild(el("button", { class:"btn-primary",
    onclick:() => _openKBModal("add", null) }, "+ Add Intent"));
  panel.appendChild(headerRow);
  panel.appendChild(el("div", { id:"kb-list" }));
  _loadKnowledgeBase();
  return panel;
}

async function _loadKnowledgeBase() {
  const list  = $("#kb-list");
  const label = $("#kb-count-label");
  if (!list) return;
  list.innerHTML = `<p class="text-muted" style="padding:16px 0;">Loading…</p>`;
  try {
    const data = await KnowledgeAPI.getAll();
    list.innerHTML = "";
    if (label) label.textContent = `${data.items.length} intents configured`;
    data.items.forEach(item =>
      list.appendChild(buildKBItem(item, (it) => _openKBModal("edit", it), _deleteKBItem)));
  } catch (err) {
    list.innerHTML = `<p class="login-error" style="padding:16px 0;">Failed to load: ${err.message}</p>`;
  }
}

function _openKBModal(mode, item = null) {
  const kws = item ? (Array.isArray(item.keywords) ? item.keywords.join(", ") : item.keywords) : "";
  const bodyHTML = `
    <div class="form-group">
      <label class="form-label-dark">Intent Name</label>
      <input id="m-intent" class="form-input-light" placeholder="e.g. python_basics" value="${item?item.intent_name:''}" />
    </div>
    <div class="form-group">
      <label class="form-label-dark">Keywords (comma-separated)</label>
      <input id="m-keywords" class="form-input-light" placeholder="python, variable, function, def" value="${kws}" />
    </div>
    <div class="form-group">
      <label class="form-label-dark">Response Text</label>
      <textarea id="m-response" class="form-textarea-light" rows="4">${item?item.response_text:''}</textarea>
    </div>
    <div class="form-group">
      <label class="form-label-dark">Target Level</label>
      <select id="m-level" class="form-select-light">
        ${[["all","All Levels"],["100","Level 100"],["200","Level 200"],["300","Level 300"]].map(([v,l])=>
          `<option value="${v}" ${item?.level===v?"selected":""}>${l}</option>`).join("")}
      </select>
    </div>`;

  Modal.open(mode==="add" ? "Add New Intent" : "Edit Intent", bodyHTML, async () => {
    const payload = { intent_name:Modal.getVal("m-intent"), keywords:Modal.getVal("m-keywords"),
                      response_text:Modal.getVal("m-response"), level:Modal.getVal("m-level") };
    if (!payload.intent_name || !payload.response_text) { toast("Intent name and response required.","error"); return; }
    try {
      if (mode==="add") { await KnowledgeAPI.create(payload); toast("Intent added."); }
      else              { await KnowledgeAPI.update(item.id, payload); toast("Intent updated."); }
      Modal.close(); _loadKnowledgeBase();
    } catch (err) { toast(err.message, "error"); }
  });
}

async function _deleteKBItem(id) {
  if (!confirm("Delete this intent?")) return;
  try { await KnowledgeAPI.delete(id); toast("Deleted."); _loadKnowledgeBase(); }
  catch (err) { toast(err.message, "error"); }
}


/* ═══════════════════════════════════════════════════════════
   REPORTS PANEL
   ═══════════════════════════════════════════════════════════ */
function buildReportsPanel() {
  const panel = el("div", { class:"tab-panel", id:"reports-panel" });
  const hdr = el("div", { class:"page-header" });
  hdr.appendChild(el("h2", { class:"page-title",    text:"Automated Reporting" }));
  hdr.appendChild(el("p",  { class:"page-subtitle", text:"Generate end-of-semester student engagement reports" }));
  panel.appendChild(hdr);

  const card = el("div", { class:"card", style:"border-top:3px solid #C5A100;margin-bottom:20px;" });
  card.appendChild(el("h3", { class:"section-title", text:"Semester Report Preview" }));
  card.appendChild(el("p",  { style:"color:#6b7280;font-size:13px;margin-bottom:16px;",
    text:"PDF includes: total interactions, top 5 intents, unanswered queries, and per-level engagement." }));
  card.appendChild(el("div", { class:"report-preview", id:"report-preview-block",
    html:"<div style='color:#9ca3af;'>Loading…</div>" }));

  const actions = el("div", { class:"report-actions" });
  actions.appendChild(el("button", { class:"btn-primary",
    onclick:() => { AnalyticsAPI.downloadPDF("1","2024/25"); toast("PDF download started."); } }, "📄 Generate PDF Report"));
  actions.appendChild(el("button", { class:"btn-secondary",
    onclick:() => { AnalyticsAPI.downloadCSV(); toast("CSV download started."); } }, "📊 Export CSV"));
  card.appendChild(actions);
  panel.appendChild(card);
  _loadReportPreview();
  return panel;
}

async function _loadReportPreview() {
  const block = $("#report-preview-block");
  if (!block) return;
  try {
    const data = await AnalyticsAPI.getSummary();
    const lines = [
      "UPSA ITM — Semester Report Preview", "",
      `📊 Total Student Interactions : ${data.total_interactions}`,
      `❓ Unanswered Queries         : ${data.unanswered_count}`, "",
      "Top Intents:",
      ...(data.top_intents||[]).slice(0,5).map((t,i)=>
        `  ${i+1}. ${(t.intent||"").replace(/_/g," ")} — ${t.count} queries`),
      "", "Engagement by Level:",
      ...Object.entries(data.by_level||{}).map(([l,c])=>`  Level ${l} : ${c} interactions`),
    ];
    block.innerHTML = lines.map(l=>`<div>${l||"&nbsp;"}</div>`).join("");
  } catch {
    block.innerHTML = "<div style='color:#9ca3af;'>Could not load preview.</div>";
  }
}
