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
    main.appendChild(buildAdminPanel());
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
        { id: "admin",     label: "📢 Broadcast" },
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

  // ── Outer layout: sidebar + main chat ──────────────────
  const layout = el("div", { class: "chat-layout" });

  // ── LEFT SIDEBAR — collapsible ────────────────────────
  const sidebar = el("div", { class: "chat-sidebar sidebar-collapsed", id: "chat-sidebar" });

  // Top: brand (no U logo) + collapse button + new-chat button
  const sideTop = el("div", { class: "chat-sidebar-top" });
  const brand   = el("div", { class: "chat-sidebar-brand" });
  brand.appendChild(el("span", { class: "chat-sidebar-brand-name", text: "UPSA ITM" }));
  sideTop.appendChild(brand);

  // Collapse toggle button
  const collapseBtn = el("button", { class: "chat-collapse-btn", title: "Collapse sidebar",
    onclick: () => {
      const sb = document.getElementById("chat-sidebar");
      const cp = document.getElementById("chat-panel");
      sb.classList.toggle("sidebar-collapsed");
      collapseBtn.innerHTML = sb.classList.contains("sidebar-collapsed") ? "&#9776;" : "&#8592;";
      collapseBtn.title = sb.classList.contains("sidebar-collapsed") ? "Open sidebar" : "Collapse sidebar";
    }
  });
  collapseBtn.innerHTML = "&#9776;"; // hamburger — sidebar starts closed
  sideTop.appendChild(collapseBtn);

  const newBtn = el("button", { class: "chat-new-btn", title: "New chat",
    onclick: async () => {
      if (!confirm("Start a new chat? Your history will be cleared.")) return;
      try {
        await ChatAPI.clearHistory();
        // Reset messages area
        const msgs = document.getElementById("chat-messages");
        msgs.innerHTML = "";
        const ti = el("div", { id: "typing-indicator" });
        ti.appendChild(el("div", { class: "bubble-avatar", text: "A" }));
        const tb = el("div", { class: "typing-bubble" });
        [0,1,2].forEach(() => tb.appendChild(el("div", { class: "typing-dot" })));
        ti.appendChild(tb);
        msgs.appendChild(ti);
        // Reset sidebar
        document.getElementById("chat-history-list").innerHTML =
          "<p class='chat-sidebar-empty'>No history yet.<br>Ask something to get started!</p>";
        // Show suggestions again
        const sr = document.getElementById("suggestions-row");
        if (sr) sr.style.display = "";
        toast("New chat started.", "info");
      } catch(e) { toast(e.message, "error"); }
    }
  });
  newBtn.innerHTML = "&#9998;"; // pencil icon
  sideTop.appendChild(newBtn);
  sidebar.appendChild(sideTop);

  // Scrollable history list
  const histList = el("div", { id: "chat-history-list", class: "chat-history-list" });
  histList.innerHTML = "<p class='chat-sidebar-empty'>Loading…</p>";
  sidebar.appendChild(histList);

  // Footer: clear button
  const sideFooter = el("div", { class: "chat-sidebar-footer" });
  const clearBtn   = el("button", { class: "chat-sidebar-clear", text: "🗑  Clear chat history",
    onclick: async () => {
      if (!confirm("Clear your entire chat history?")) return;
      try {
        await ChatAPI.clearHistory();
        document.getElementById("chat-history-list").innerHTML =
          "<p class='chat-sidebar-empty'>No history yet.<br>Ask something to get started!</p>";
        const msgs = document.getElementById("chat-messages");
        msgs.innerHTML = "";
        const ti = el("div", { id: "typing-indicator" });
        ti.appendChild(el("div", { class: "bubble-avatar", text: "A" }));
        const tb = el("div", { class: "typing-bubble" });
        [0,1,2].forEach(() => tb.appendChild(el("div", { class: "typing-dot" })));
        ti.appendChild(tb);
        msgs.appendChild(ti);
        const sr = document.getElementById("suggestions-row");
        if (sr) sr.style.display = "";
        toast("History cleared.", "info");
      } catch(e) { toast(e.message, "error"); }
    }
  });
  sideFooter.appendChild(clearBtn);
  sidebar.appendChild(sideFooter);

  layout.appendChild(sidebar);

  // ── RIGHT MAIN — chat messages + input ─────────────────
  const chatMain = el("div", { class: "chat-main" });

  const messages = el("div", { id: "chat-messages" });
  const typingInd = el("div", { id: "typing-indicator" });
  typingInd.appendChild(el("div", { class: "bubble-avatar", text: "A" }));
  const typBubble = el("div", { class: "typing-bubble" });
  [0,1,2].forEach(() => typBubble.appendChild(el("div", { class: "typing-dot" })));
  typingInd.appendChild(typBubble);
  messages.appendChild(typingInd);
  chatMain.appendChild(messages);

  // Smart suggestion chips — level-aware
  const suggestRow = el("div", { id: "suggestions-row" });
  const _user = (typeof Auth !== "undefined" && Auth.getUser) ? Auth.getUser() : null;
  const _level = _user ? String(_user.level || "100") : "100";
  const _chipSets = {
    "100": ["What should I study this week?", "Help me with C++ loops", "How do I start my project?", "What topics can I ask about?"],
    "200": ["What should I study this week?", "Explain OOP concepts", "Help me break down my project", "How do I manage my time?"],
    "300": ["What should I study this week?", "Help me with Visual Basic", "How do I prioritize tasks?", "Prepare me for exams"],
  };
  const _chips = _chipSets[_level] || _chipSets["100"];
  _chips.forEach(s => {
    const chip = el("button", { class: "suggestion-chip" }, s);
    chip.addEventListener("click", () => {
      const inp = $("#chat-input");
      if (inp) { inp.value = s; inp.focus(); }
      sendChatMessage();
    });
    suggestRow.appendChild(chip);
  });
  chatMain.appendChild(suggestRow);

  const inputBar = el("div", { id: "chat-input-bar" });
  const inputRow = el("div", { class: "chat-input-row" });
  const input = el("input", { type: "text", id: "chat-input",
    placeholder: "Ask anything about C++, exams, assignments…",
    onkeydown: (e) => { if (e.key === "Enter") sendChatMessage(); } });
  inputRow.appendChild(input);
  inputRow.appendChild(el("button", { class: "btn-primary", id: "chat-send-btn",
    onclick: sendChatMessage }, "Send"));
  inputBar.appendChild(inputRow);
  chatMain.appendChild(inputBar);

  layout.appendChild(chatMain);
  panel.appendChild(layout);

  _loadChatHistory(messages, suggestRow, histList);
  return panel;
}

async function _loadChatHistory(messagesEl, suggestRow, histListEl) {
  try {
    const [histData, greetData] = await Promise.all([
      ChatAPI.getHistory(),
      ChatAPI.getGreeting().catch(() => null),
    ]);

    const msgs       = (histData.messages || []);
    const hasHistory = msgs.length > 0;

    // ── Populate sidebar — Claude-style grouped history ──────
    if (histListEl) {
      _renderSidebarHistory(histListEl, msgs.filter(m => m.role === "user"));
    }

    // ── Populate main chat area ────────────────────────────
    if (hasHistory) {
      if (suggestRow) suggestRow.style.display = "none";
      msgs.forEach(msg => _appendBubble(messagesEl, msg));
    }

    // Greeting card always shown on load — motivation + upcoming activities
    if (greetData) {
      _appendGreetingCard(messagesEl, greetData, hasHistory);
    } else if (!hasHistory) {
      _appendBubble(messagesEl, {
        role: "assistant",
        content: "Welcome! 👋 I'm your UPSA ITM Academic Assistant. Ask me anything about your C++ courses, assignments, or exams.",
      });
    }
  } catch {
    _appendBubble(messagesEl, {
      role: "assistant",
      content: "Welcome! 👋 Ask me anything about your ITM courses.",
    });
  }
}

/* ── Sidebar rendering helpers ─────────────────────────────
   Groups messages as: Today / Yesterday / Previous 7 Days
   Each item has a pencil icon, truncated text, and a delete-
   on-hover ✕ button — matching Claude's sidebar UX.
   ─────────────────────────────────────────────────────────── */
function _renderSidebarHistory(histListEl, userMsgs) {
  histListEl.innerHTML = "";
  if (!userMsgs || userMsgs.length === 0) {
    histListEl.innerHTML = "<p class='chat-sidebar-empty'>No history yet.<br>Ask something to get started!</p>";
    return;
  }

  // Group by recency (messages may not have timestamps — treat all as Today for now)
  const groups = { "Today": [] };
  userMsgs.slice().reverse().forEach(m => {
    const ts = m.timestamp ? new Date(m.timestamp) : null;
    if (!ts) { groups["Today"].push(m); return; }
    const now  = new Date();
    const diff = Math.floor((now - ts) / 86400000);
    if (diff === 0)      { groups["Today"]            = groups["Today"]            || []; groups["Today"].push(m); }
    else if (diff === 1) { groups["Yesterday"]         = groups["Yesterday"]         || []; groups["Yesterday"].push(m); }
    else if (diff <= 7)  { groups["Previous 7 Days"]  = groups["Previous 7 Days"]  || []; groups["Previous 7 Days"].push(m); }
    else                 { groups["Older"]             = groups["Older"]             || []; groups["Older"].push(m); }
  });

  ["Today", "Yesterday", "Previous 7 Days", "Older"].forEach(groupName => {
    const items = groups[groupName];
    if (!items || items.length === 0) return;

    // Group label
    const lbl = document.createElement("div");
    lbl.className = "chat-history-group-label";
    lbl.textContent = groupName;
    histListEl.appendChild(lbl);

    items.forEach(m => {
      histListEl.appendChild(_makeSidebarItem(m.content));
    });
  });
}

function _makeSidebarItem(text) {
  const item = document.createElement("div");
  item.className = "chat-history-item";
  item.title = text;

  const icon = document.createElement("span");
  icon.className = "chat-history-item-icon";
  icon.textContent = "✦";

  const label = document.createElement("span");
  label.className = "chat-history-item-text";
  label.textContent = text.length > 40 ? text.slice(0, 40) + "…" : text;

  const del = document.createElement("button");
  del.className = "chat-history-item-del";
  del.title = "Remove from history";
  del.textContent = "✕";
  del.addEventListener("click", (e) => {
    e.stopPropagation();
    item.remove();
    // Check if group label is now empty
    const prev = item.previousElementSibling;
    if (prev && prev.classList.contains("chat-history-group-label")) {
      const next = prev.nextElementSibling;
      if (!next || next.classList.contains("chat-history-group-label")) prev.remove();
    }
  });

  item.appendChild(icon);
  item.appendChild(label);
  item.appendChild(del);

  item.addEventListener("click", () => {
    const inp = document.getElementById("chat-input");
    if (inp) { inp.value = text; inp.focus(); }
    document.querySelectorAll(".chat-history-item").forEach(i => i.classList.remove("active-item"));
    item.classList.add("active-item");
  });
  return item;
}

// After each sent message — add to sidebar under Today
function _addToSidebarHistory(text) {
  const histListEl = document.getElementById("chat-history-list");
  if (!histListEl) return;

  // Remove empty state if present
  const empty = histListEl.querySelector(".chat-sidebar-empty");
  if (empty) empty.remove();

  // Ensure a "Today" group label exists at top
  let todayLabel = histListEl.querySelector(".chat-history-group-label");
  if (!todayLabel || todayLabel.textContent !== "Today") {
    todayLabel = document.createElement("div");
    todayLabel.className = "chat-history-group-label";
    todayLabel.textContent = "Today";
    histListEl.insertBefore(todayLabel, histListEl.firstChild);
  }

  const item = _makeSidebarItem(text);
  histListEl.insertBefore(item, todayLabel.nextSibling);
}

function _appendGreetingCard(container, greetData, hasHistory) {
  const card = document.createElement("div");
  card.className = "greeting-card";

  // ── Inactivity banner (event-triggered) ──────────────────
  if (greetData.inactivity) {
    const inact = document.createElement("div");
    inact.className = "greeting-inactivity";
    inact.innerHTML = `<span class="greeting-bulb">👋</span><em>${greetData.motivation}</em>`;
    card.appendChild(inact);
  } else if (greetData.motivation) {
    const motiv = document.createElement("div");
    motiv.className = "greeting-motivation";
    motiv.innerHTML = `<span class="greeting-bulb">💡</span><em>${greetData.motivation}</em>`;
    card.appendChild(motiv);
  }

  // ── Deadline proximity nudge ───────────────────────────
  if (greetData.deadline_nudge) {
    const nudge = document.createElement("div");
    nudge.className = "greeting-deadline-nudge";
    nudge.textContent = greetData.deadline_nudge;
    card.appendChild(nudge);
  }

  if (greetData.upcoming && greetData.upcoming.length > 0) {
    const upHdr = document.createElement("div");
    upHdr.className = "greeting-upcoming-hdr";
    upHdr.textContent = "📅 Upcoming in the next 2 weeks:";
    card.appendChild(upHdr);

    const typeColors = {
      exam:"#c0392b", assignment:"#b45309", project:"#15803d",
      lecture:"#1e40af", quiz:"#6b21a8", lab:"#0369a1"
    };

    greetData.upcoming.forEach(item => {
      const row = document.createElement("div");
      row.className = "greeting-activity-row";
      const color = typeColors[item.type] || "#374151";
      row.innerHTML = `
        <span class="greeting-type-chip" style="background:${color}18;color:${color};border:1px solid ${color}35;">
          ${item.type.toUpperCase()}
        </span>
        <span class="greeting-activity-title">${item.title}</span>
        <span class="greeting-when">${item.when} &middot; ${item.time}</span>
      `;
      card.appendChild(row);
    });
  } else if (!hasHistory) {
    const noUp = document.createElement("div");
    noUp.className = "greeting-no-upcoming";
    noUp.textContent = "📭 No upcoming activities in the next 2 weeks. Keep up the good work!";
    card.appendChild(noUp);
  }

  // ── Announcements from lecturers ──────────────────────────
  if (greetData.announcements && greetData.announcements.length > 0) {
    const annHdr = document.createElement("div");
    annHdr.className = "greeting-ann-hdr";
    annHdr.textContent = "📢 Announcements from your lecturers:";
    card.appendChild(annHdr);
    greetData.announcements.forEach(ann => {
      const annBox = document.createElement("div");
      annBox.className = "greeting-ann-item";
      const annTitle = document.createElement("strong");
      annTitle.textContent = ann.title;
      const annBody = document.createElement("p");
      annBody.textContent = ann.body;
      const annMeta = document.createElement("small");
      annMeta.textContent = `${ann.author} · ${new Date(ann.created_at).toLocaleDateString()}`;
      annBox.appendChild(annTitle);
      annBox.appendChild(annBody);
      annBox.appendChild(annMeta);
      card.appendChild(annBox);
    });
  }

  const welcome = document.createElement("div");
  welcome.className = "greeting-welcome-line";
  welcome.textContent = `Hello${greetData.name ? ", " + greetData.name : ""}! What would you like help with today?`;
  card.appendChild(welcome);

  // ── Current week strategy strip ────────────────────────
  const _stratUser = (typeof Auth !== "undefined" && Auth.getUser) ? Auth.getUser() : null;
  if (_stratUser) {
    const stratWrap = document.createElement("div");
    stratWrap.className = "greeting-strategy-wrap";
    stratWrap.innerHTML = "<p class='greeting-strategy-loading'>Loading your week's strategy…</p>";
    card.appendChild(stratWrap);
    _loadGreetingStrategies(stratWrap, String(_stratUser.level || "100"));
  }

  const ti = container.querySelector("#typing-indicator");
  if (ti && ti.parentNode === container) {
    container.insertBefore(card, ti);
  } else {
    container.appendChild(card);
  }
  scrollChatBottom();
}

async function _loadGreetingStrategies(wrap, level) {
  const courses = ["programming","database","networking"];
  const courseLabels = { programming:"Programming", database:"Database Mgt", networking:"Networking" };
  // Determine current week (1-13) based on day of year
  const now  = new Date();
  const start = new Date(now.getFullYear(), 0, 1);
  const week  = Math.min(13, Math.max(1, Math.ceil(((now - start) / 86400000 + start.getDay() + 1) / 7) % 13 || 1));
  wrap.innerHTML = "";
  const header = document.createElement("div");
  header.className = "greeting-strategy-hdr";
  header.innerHTML = `<span>📚 Week ${week} Strategies for You</span>`;
  wrap.appendChild(header);
  let loaded = 0;
  for (const course of courses) {
    try {
      const data = await StrategiesAPI.getWeek(course, level, week);
      const s = data.strategy;
      if (!s) continue;
      const block = document.createElement("div");
      block.className = "greeting-strategy-block";
      const courseTag = document.createElement("span");
      courseTag.className = "greeting-strategy-course";
      courseTag.textContent = courseLabels[course];
      const topic = document.createElement("strong");
      topic.className = "greeting-strategy-topic";
      topic.textContent = s.topic;
      const preview = document.createElement("p");
      preview.className = "greeting-strategy-preview";
      const firstLine = s.strategy.split("\n").find(l => l.trim().length > 10) || s.strategy.slice(0,120);
      preview.textContent = firstLine.slice(0,130) + (firstLine.length > 130 ? "…" : "");
      block.appendChild(courseTag);
      block.appendChild(topic);
      block.appendChild(preview);
      wrap.appendChild(block);
      loaded++;
    } catch(e) { /* skip course */ }
  }
  if (loaded === 0) wrap.remove();
}

function _appendBubble(container, msgData) {
  const ti = container.querySelector("#typing-indicator");
  const b  = buildBubble(msgData);
  if (ti && ti.parentNode === container) {
    container.insertBefore(b, ti);
  } else {
    container.appendChild(b);
  }
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
    _appendBubble(messagesEl, data.bot_message);
    _addToSidebarHistory(text);
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
  titleWrap.appendChild(el("h2", { class:"page-title", text:"My Reminders" }));
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
  titles.appendChild(el("h2", { class:"page-title", text:"Lecturer Dashboard" }));
  titles.appendChild(el("p",  { class:"page-subtitle", text:"Student engagement analytics · ITM Department" }));
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

  // ── Query Insight Display — sits prominently below the charts ──
  const qiCard = el("div", { class: "card", style: "margin-top:20px;" });
  const qiHdr  = el("div", { style: "display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;" });
  qiHdr.appendChild(el("h3", { class: "section-title", style: "margin:0;", text: "📊  Query Insights — Top Student Topics" }));
  qiHdr.appendChild(el("span", { class: "chip chip-navy", style: "font-size:11px;", text: "Identifies knowledge gaps" }));
  qiCard.appendChild(qiHdr);
  qiCard.appendChild(el("p", { style: "font-size:12px;color:#6b7280;margin-bottom:14px;",
    text: "Topics students ask about most. High counts on unanswered topics signal gaps to fill in the Knowledge Base." }));
  qiCard.appendChild(el("div", { id: "query-insight-list" }));
  panel.appendChild(qiCard);

  // ── Unanswered queries — below insights ────────────────────
  const uaCard = el("div", { class:"card", style:"margin-top:20px;" });
  const uaHdr  = el("div", { style:"display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;" });
  uaHdr.appendChild(el("h3", { class:"section-title", style:"margin:0;", text:"Unanswered Student Queries" }));
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
          // + Add to KB quick-action
          const addKbBtn = el("button", { class:"ua-add-kb-btn", title:"Add this query to Knowledge Base",
            onclick: () => {
              const bodyHTML = `
                <p style="font-size:12px;color:#6b7280;padding:8px 12px;background:#f8fafc;border-radius:6px;margin-bottom:14px;">
                  Student asked: <strong>${q.question.replace(/</g,'&lt;')}</strong>
                </p>
                <div class="form-group">
                  <label class="form-label-dark">Intent Name <span style="color:#c0392b">*</span></label>
                  <input id="quick-kb-intent" class="form-input-light" placeholder="e.g. cpp_pointers" />
                </div>
                <div class="form-group">
                  <label class="form-label-dark">Keywords (comma-separated) <span style="color:#c0392b">*</span></label>
                  <input id="quick-kb-keywords" class="form-input-light" value="${q.question.toLowerCase().replace(/[^a-z0-9 ]/g,'').trim()}" />
                </div>
                <div class="form-group">
                  <label class="form-label-dark">Level</label>
                  <select id="quick-kb-level" class="form-select-light">
                    <option value="all">All Levels</option>
                    <option value="100" ${q.student_level==="100"?"selected":""}>Level 100</option>
                    <option value="200" ${q.student_level==="200"?"selected":""}>Level 200</option>
                    <option value="300" ${q.student_level==="300"?"selected":""}>Level 300</option>
                  </select>
                </div>
                <div class="form-group">
                  <label class="form-label-dark">Response (strategy/answer) <span style="color:#c0392b">*</span></label>
                  <textarea id="quick-kb-response" class="form-input-light" rows="5" placeholder="Write the counseling strategy or answer…" style="font-size:13px;"></textarea>
                </div>
              `;
              Modal.open("+ Add to Knowledge Base", bodyHTML, async () => {
                const intent   = (document.getElementById("quick-kb-intent")?.value    || "").trim();
                const keywords = (document.getElementById("quick-kb-keywords")?.value  || "").trim();
                const response = (document.getElementById("quick-kb-response")?.value  || "").trim();
                const level    = document.getElementById("quick-kb-level")?.value || "all";
                if (!intent || !keywords || !response) { toast("All fields required.", "error"); return; }
                try {
                  await AdminAPI.addKnowledge({ intent_name:intent, keywords, response_text:response, level });
                  toast("Added to Knowledge Base! Students can now get this answer.", "success");
                  Modal.close();
                } catch(e) { toast(e.message, "error"); }
              });
              setTimeout(() => document.getElementById("quick-kb-intent")?.focus(), 80);
            }
          }, "+ Add to KB");
          item.appendChild(addKbBtn);
          uaList.appendChild(item);
        });
      }
    }

    // Query Insight Display — top intents + corresponding knowledge gaps
    const qiList = $("#query-insight-list");
    if (qiList) {
      qiList.innerHTML = "";
      const intents = data.top_intents || [];
      if (intents.length === 0) {
        qiList.appendChild(el("p", { class: "text-muted", style: "font-size:13px;padding:8px 0;",
          text: "No interaction data yet. Insights will appear once students start asking questions." }));
      } else {
        const maxCount = Math.max(...intents.map(i => i.count), 1);
        intents.slice(0, 8).forEach((intent, idx) => {
          const cleanName = (intent.intent || "unknown").replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
          const pct = Math.round((intent.count / maxCount) * 100);
          const row = el("div", { class: "qi-row" });
          const rankBadge = el("span", { class: "qi-rank", text: `#${idx + 1}` });
          const nameEl = el("div", { class: "qi-name", text: cleanName });
          const barWrap = el("div", { class: "qi-bar-wrap" });
          const bar = el("div", { class: "qi-bar" });
          bar.style.width = `${pct}%`;
          barWrap.appendChild(bar);
          const countEl = el("span", { class: "qi-count", text: `${intent.count}x` });
          row.appendChild(rankBadge);
          row.appendChild(nameEl);
          row.appendChild(barWrap);
          row.appendChild(countEl);
          qiList.appendChild(row);
        });
        // Knowledge gap note if unanswered > 10% of total
        const total = data.total_interactions || 0;
        const unanswered = data.unanswered_count || 0;
        if (total > 5 && unanswered / total > 0.1) {
          const gapNote = el("div", { class: "qi-gap-note" });
          gapNote.innerHTML = `⚠️ <strong>${Math.round((unanswered/total)*100)}%</strong> of queries are unanswered — consider adding more knowledge base entries.`;
          qiList.appendChild(gapNote);
        }
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

  /* ── Header */
  const hdr = el("div", { style:"display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px;" });
  const titles = el("div");
  titles.appendChild(el("h2", { class:"page-title", text:"Semester Activity Planner" }));
  titles.appendChild(el("p",  { class:"page-subtitle",
    text:"Plan all 13 weeks. Click a week card to add an activity. Students are notified 3 days, 2 days, 1 day before, and on the day — at the exact time set." }));
  hdr.appendChild(titles);

  /* ── Controls: semester selector + start date */
  const controls = el("div", { style:"display:flex;gap:10px;align-items:center;flex-shrink:0;flex-wrap:wrap;" });

  const semSelect = el("select", { class:"form-select-light", id:"planner-sem", style:"width:130px;" });
  [["1","Semester 1"],["2","Semester 2"]].forEach(([v,l]) => semSelect.appendChild(el("option",{value:v},l)));

  // Course + level selectors for strategy display
  const courseSelect = el("select", { class:"form-select-light", id:"planner-course", style:"width:160px;" });
  [["programming","Programming"],["database","Database Mgt"],["networking","Networking"]].forEach(([v,l]) =>
    courseSelect.appendChild(el("option",{value:v},l)));

  const levelSelect = el("select", { class:"form-select-light", id:"planner-level", style:"width:110px;" });
  [["100","Level 100"],["200","Level 200"],["300","Level 300"]].forEach(([v,l]) =>
    levelSelect.appendChild(el("option",{value:v},l)));

  const startInput = el("input", { type:"date", id:"planner-start", class:"form-input-light",
    style:"width:150px;", title:"Semester start date" });
  startInput.value = _getDefaultSemStart();

  const semLabel   = el("label", { style:"font-size:12px;font-weight:600;color:#6b7280;white-space:nowrap;", text:"Start date:" });
  const courseLabel = el("label", { style:"font-size:12px;font-weight:600;color:#6b7280;white-space:nowrap;", text:"Course:" });
  const levelLabel  = el("label", { style:"font-size:12px;font-weight:600;color:#6b7280;white-space:nowrap;", text:"Level:" });
  controls.appendChild(semLabel);
  controls.appendChild(startInput);
  controls.appendChild(semSelect);
  controls.appendChild(courseLabel);
  controls.appendChild(courseSelect);
  controls.appendChild(levelLabel);
  controls.appendChild(levelSelect);
  hdr.appendChild(controls);
  panel.appendChild(hdr);

  /* ── Push status banner */
  const banner = el("div", { id:"planner-push-banner", class:"planner-push-banner",
    style:"background:#fffbeb;border:1px solid #fde68a;color:#92400e;margin-bottom:18px;" });
  banner.textContent = "Checking push notification status…";
  panel.appendChild(banner);
  _checkPushStatus(banner);

  /* ── 12-week grid */
  const grid = el("div", { id:"planner-grid" });
  panel.appendChild(grid);

  /* ── Footer */
  const footer = el("div", { class:"planner-footer" });
  footer.appendChild(el("button", { class:"btn-secondary",
    onclick:() => _refreshPlannerGrid() }, "↻ Refresh"));
  panel.appendChild(footer);

  startInput.addEventListener("change", () => _refreshPlannerGrid());
  semSelect.addEventListener("change",  () => _refreshPlannerGrid());
  courseSelect.addEventListener("change", () => _refreshPlannerGrid());
  levelSelect.addEventListener("change",  () => _refreshPlannerGrid());

  _refreshPlannerGrid();
  return panel;
}

function _getDefaultSemStart() {
  const now  = new Date();
  const day  = now.getDay();
  const diff = day === 0 ? 1 : (day === 1 ? 0 : 8 - day);
  const next = new Date(now);
  next.setDate(now.getDate() + diff);
  return next.toISOString().slice(0,10);
}

async function _checkPushStatus(banner) {
  try {
    const data = await apiFetch("/push/vapid-public-key");
    if (data.public_key) {
      banner.style.cssText = "background:rgba(21,128,61,0.08);border:1px solid rgba(21,128,61,0.3);color:#15803d;padding:10px 16px;border-radius:8px;font-size:13px;margin-bottom:18px;";
      banner.textContent = "✅ Push notifications configured — students will receive alerts 3 days, 2 days, 1 day before, and on the day at the exact activity time.";
    } else {
      banner.style.cssText = "background:rgba(180,83,9,0.07);border:1px solid rgba(180,83,9,0.25);color:#b45309;padding:10px 16px;border-radius:8px;font-size:13px;margin-bottom:18px;";
      banner.innerHTML = "⚠️ Push notifications not yet configured. Run <code>python generate_vapid_keys.py</code> and add keys to <code>.env</code>. Activities will still save and show as reminders.";
    }
  } catch {
    banner.style.display = "none";
  }
}

const _PLAN_TYPE_COLORS = {
  lecture:"#0B1E3F", assignment:"#b45309", exam:"#c0392b",
  quiz:"#7c3aed",    lab:"#0369a1",        project:"#15803d",
};
const _PLAN_TYPE_ICONS = {
  lecture:"📖", assignment:"📋", exam:"📝", quiz:"🧪", lab:"🔬", project:"🚀"
};

async function _refreshPlannerGrid() {
  const grid       = document.getElementById("planner-grid");
  const startInput = document.getElementById("planner-start");
  const semSelect  = document.getElementById("planner-sem");

  // If planner panel isn't visible, switch to it first
  if (!grid || !startInput || !semSelect) {
    switchTab("planner");
    setTimeout(() => _refreshPlannerGrid(), 100);
    return;
  }

  grid.innerHTML = `<div style="padding:24px;text-align:center;color:#9ca3af;font-size:13px;">Loading…</div>`;

  /* Fetch planner activities via dedicated endpoint */
  let saved = [];
  try {
    const data = await RemindersAPI.getPlannerActivities(semSelect.value);
    saved = data.reminders || [];
  } catch (err) {
    grid.innerHTML = `<p style="color:#c0392b;padding:20px;font-size:13px;">Could not load activities: ${err.message}</p>`;
    return;
  }

  /* Group by week number */
  const byWeek = {};
  saved.forEach(r => {
    if (!byWeek[r.week]) byWeek[r.week] = [];
    byWeek[r.week].push(r);
  });

  const startDate = new Date(startInput.value || _getDefaultSemStart());

  for (let week = 1; week <= 13; week++) {
    const weekStart = new Date(startDate);
    weekStart.setDate(startDate.getDate() + (week - 1) * 7);
    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekStart.getDate() + 6);

    const card = el("div", { class:"planner-week-card", "data-week": week });

    /* Card header */
    const cardHdr = el("div", { class:"planner-week-header" });
    cardHdr.appendChild(el("div", { class:"planner-week-num", text:`Week ${week}` }));
    cardHdr.appendChild(el("div", { class:"planner-week-dates",
      text:`${_fmtPlanDate(weekStart)} — ${_fmtPlanDate(weekEnd)}` }));
    cardHdr.appendChild(el("button", { class:"planner-add-btn",
      onclick: () => _openPlannerModal(week, semSelect.value, weekStart) }, "+ Add"));
    card.appendChild(cardHdr);

    /* Activities list */
    const actList = el("div", { class:"planner-activities" });
    const items   = byWeek[week] || [];

    if (items.length === 0) {
      actList.appendChild(el("div", { class:"planner-placeholder",
        onclick: () => _openPlannerModal(week, semSelect.value, weekStart) },
        "No activities — click to add one"));
    } else {
      items.forEach(r => {
        const chip = el("div", { class:"planner-activity-chip" });
        chip.style.borderLeftColor = _PLAN_TYPE_COLORS[r.type] || "#0B1E3F";

        const icon = _PLAN_TYPE_ICONS[r.type] || "📌";
        const info = el("div", { style:"flex:1;min-width:0;" });
        info.appendChild(el("div", { class:"planner-chip-title", text:`${icon} ${r.title}` }));
        info.appendChild(el("div", { class:"planner-chip-meta",
          text:`${r.date}  ·  ${r.time || "08:00"}  ·  ${r.level === "all" ? "All levels" : "Level " + r.level}` }));
        chip.appendChild(info);

        /* Edit button */
        const editBtn = el("button", { class:"planner-chip-btn planner-chip-edit",
          title:"Edit", onclick: () => _openPlannerModal(week, semSelect.value, weekStart, r) }, "✏️");
        /* Delete button */
        const delBtn = el("button", { class:"planner-chip-btn planner-chip-del",
          title:"Delete", onclick: async () => {
            if (!confirm(`Delete "${r.title}"?`)) return;
            try {
              await RemindersAPI.delete(r.id);
              toast("Activity removed.");
              _refreshPlannerGrid();
            } catch (err) { toast(err.message, "error"); }
          }}, "✕");
        chip.appendChild(editBtn);
        chip.appendChild(delBtn);
        actList.appendChild(chip);
      });
    }
    card.appendChild(actList);

    // ── Strategy strip for this week ─────────────────────────
    const stratWrap = el("div", { class:"planner-strategy-wrap", id:`strategy-wrap-${week}` });
    stratWrap.innerHTML = "<p class='planner-strategy-loading'>Loading strategy…</p>";
    card.appendChild(stratWrap);
    _loadWeekStrategy(week, stratWrap);

    grid.appendChild(card);
  }
}

/* ── Load + render a single week's strategy ──────────────── */
async function _loadWeekStrategy(week, container) {
  const courseEl = document.getElementById("planner-course");
  const levelEl  = document.getElementById("planner-level");
  if (!courseEl || !levelEl) { container.innerHTML = ""; return; }
  const course = courseEl.value;
  const level  = levelEl.value;
  try {
    const data = await StrategiesAPI.getWeek(course, level, week);
    const s    = data.strategy;
    container.innerHTML = "";
    if (!s) {
      const empty = el("div", { class:"planner-strategy-empty" });
      empty.innerHTML = `<span style="opacity:0.5;">No strategy set for this week</span>
        <button class="planner-strategy-edit-btn" onclick="_openStrategyModal(null,'${course}','${level}',${week})">+ Add Strategy</button>`;
      container.appendChild(empty);
      return;
    }
    const strip = el("div", { class:"planner-strategy-strip" });
    const topRow = el("div", { class:"planner-strategy-toprow" });
    topRow.appendChild(el("span", { class:"planner-strategy-topic", text: s.topic }));
    const actBadge = el("span", { class:`planner-strategy-badge act-${s.activity}`, text: s.activity });
    const editBtn  = el("button", { class:"planner-strategy-edit-btn",
      onclick: () => _openStrategyModal(s, course, level, week) }, "✏️ Edit");
    topRow.appendChild(actBadge);
    topRow.appendChild(editBtn);
    strip.appendChild(topRow);

    // Strategy text (collapsible)
    const preview = s.strategy.slice(0, 180) + (s.strategy.length > 180 ? "…" : "");
    const bodyEl  = el("div", { class:"planner-strategy-body", text: preview });
    strip.appendChild(bodyEl);

    if (s.evening_tip) {
      const eve = el("div", { class:"planner-strategy-evening" });
      eve.innerHTML = `<strong>🌙 Evening students:</strong> ${s.evening_tip.slice(0,140)}${s.evening_tip.length>140?"…":""}`;
      strip.appendChild(eve);
    }
    container.appendChild(strip);
  } catch(e) {
    container.innerHTML = "";
  }
}

/* ── Strategy add/edit modal ──────────────────────────────── */
function _openStrategyModal(existing, course, level, week) {
  const isEdit = !!existing;
  const courseNames = { programming:"Programming", database:"Database Mgt", networking:"Networking" };
  const bodyHTML = `
    <p style="font-size:12px;color:#6b7280;margin-bottom:16px;padding:10px;background:#f8fafc;border-radius:6px;border-left:3px solid #C5A100;">
      <strong>${courseNames[course]||course} · Level ${level} · Week ${week}</strong>
    </p>
    <div class="form-group">
      <label class="form-label-dark">Topic Name <span style="color:#c0392b">*</span></label>
      <input id="sm-topic" class="form-input-light" value="${existing?.topic||""}" placeholder="e.g. Pointers and References" />
    </div>
    <div class="form-group">
      <label class="form-label-dark">Activity Type</label>
      <select id="sm-activity" class="form-select-light">
        ${["lecture","lab","assignment","test","project","exam_prep"].map(a =>
          `<option value="${a}" ${(existing?.activity||"lecture")===a?"selected":""}>${a}</option>`).join("")}
      </select>
    </div>
    <div class="form-group">
      <label class="form-label-dark">Strategy (Regular Students) <span style="color:#c0392b">*</span></label>
      <textarea id="sm-strategy" class="form-input-light" rows="6" placeholder="Practical counseling strategy for this topic…" style="font-size:13px;">${existing?.strategy||""}</textarea>
    </div>
    <div class="form-group">
      <label class="form-label-dark">Evening Student Tip <span style="color:#9ca3af;font-weight:400">(optional)</span></label>
      <textarea id="sm-evening" class="form-input-light" rows="3" placeholder="Adapted advice for evening/working students…" style="font-size:13px;">${existing?.evening_tip||""}</textarea>
    </div>
  `;
  Modal.open(
    isEdit ? `Edit Strategy — Week ${week}` : `Add Strategy — Week ${week}`,
    bodyHTML,
    async () => {
      const topic    = (document.getElementById("sm-topic")?.value||"").trim();
      const strategy = (document.getElementById("sm-strategy")?.value||"").trim();
      if (!topic || !strategy) { toast("Topic and strategy are required.", "error"); return; }
      const payload = {
        course, level, week,
        topic,
        activity: document.getElementById("sm-activity")?.value || "lecture",
        strategy,
        evening_tip: (document.getElementById("sm-evening")?.value||"").trim(),
      };
      try {
        if (isEdit && existing?.id) {
          await StrategiesAPI.update(existing.id, payload);
          toast("Strategy updated.");
        } else {
          await StrategiesAPI.add(payload);
          toast("Strategy saved.");
        }
        Modal.close();
        // Refresh the strategy strip for this week
        const wrap = document.getElementById(`strategy-wrap-${week}`);
        if (wrap) _loadWeekStrategy(week, wrap);
      } catch(e) { toast(e.message, "error"); }
    }
  );
  setTimeout(() => document.getElementById("sm-topic")?.focus(), 80);
}

function _fmtPlanDate(d) {
  return d.toLocaleDateString("en-GB", { day:"numeric", month:"short" });
}

/* Modal-based add/edit — uses the same app modal as the rest of the system */
function _openPlannerModal(week, semester, weekStart, prefill = null) {
  const isEdit    = !!prefill;
  const defDate   = prefill?.date || weekStart.toISOString().slice(0,10);
  const defTime   = prefill?.time || "08:00";
  const defType   = prefill?.type || "assignment";
  const defLevel  = prefill?.level || "all";
  const defTitle  = prefill?.title || "";
  const defDesc   = prefill?.description || "";

  const bodyHTML = `
    <p style="font-size:13px;color:#6b7280;margin-bottom:18px;padding:10px 14px;background:#f8fafc;border-radius:6px;border-left:3px solid #C5A100;">
      <strong>Week ${week}</strong> &nbsp;·&nbsp; Semester ${semester} &nbsp;·&nbsp;
      ${_fmtPlanDate(weekStart)} — ${_fmtPlanDate(new Date(weekStart.getTime() + 6*86400000))}
    </p>

    <div class="form-group">
      <label class="form-label-dark">Activity Title <span style="color:#c0392b;">*</span></label>
      <input id="pm-title" class="form-input-light" placeholder="e.g. Mid-Semester Examination"
        value="${defTitle}" autocomplete="off" />
    </div>

    <div class="form-group">
      <label class="form-label-dark">Description <span style="color:#9ca3af;font-weight:400;">(optional)</span></label>
      <input id="pm-desc" class="form-input-light" placeholder="e.g. Covers Chapters 1–4, bring calculator"
        value="${defDesc}" autocomplete="off" />
    </div>

    <div style="display:flex;gap:14px;margin-bottom:0;">
      <div class="form-group" style="flex:1;">
        <label class="form-label-dark">Date <span style="color:#c0392b;">*</span></label>
        <input type="date" id="pm-date" class="form-input-light" value="${defDate}" />
      </div>
      <div class="form-group" style="flex:1;">
        <label class="form-label-dark">Time <span style="color:#c0392b;">*</span></label>
        <input type="time" id="pm-time" class="form-input-light" value="${defTime}" />
        <div style="font-size:11px;color:#9ca3af;margin-top:4px;">Push alerts fire at this exact hour</div>
      </div>
    </div>

    <div style="display:flex;gap:14px;">
      <div class="form-group" style="flex:1;">
        <label class="form-label-dark">Activity Type</label>
        <select id="pm-type" class="form-select-light">
          ${["lecture","assignment","exam","quiz","lab","project"].map(t =>
            `<option value="${t}" ${defType===t?"selected":""}>${_PLAN_TYPE_ICONS[t]} ${t.charAt(0).toUpperCase()+t.slice(1)}</option>`
          ).join("")}
        </select>
      </div>
      <div class="form-group" style="flex:1;">
        <label class="form-label-dark">Target Level</label>
        <select id="pm-level" class="form-select-light">
          <option value="all"  ${defLevel==="all" ?"selected":""}>All Levels</option>
          <option value="100"  ${defLevel==="100" ?"selected":""}>Level 100</option>
          <option value="200"  ${defLevel==="200" ?"selected":""}>Level 200</option>
          <option value="300"  ${defLevel==="300" ?"selected":""}>Level 300</option>
        </select>
      </div>
    </div>
  `;

  Modal.open(
    isEdit ? `Edit Activity — Week ${week}` : `Add Activity — Week ${week}`,
    bodyHTML,
    async () => {
      const title = (document.getElementById("pm-title")?.value || "").trim();
      const date  = document.getElementById("pm-date")?.value;
      const time  = document.getElementById("pm-time")?.value || "08:00";

      if (!title) { toast("Please enter an activity title.", "error"); return; }
      if (!date)  { toast("Please select a date.", "error"); return; }

      const payload = {
        title,
        description: (document.getElementById("pm-desc")?.value || "").trim(),
        date, time,
        type:     document.getElementById("pm-type")?.value  || "assignment",
        level:    document.getElementById("pm-level")?.value || "all",
        semester: String(semester),
        week,
      };

      try {
        if (isEdit) {
          await RemindersAPI.update(prefill.id, payload);
          toast("Activity updated.");
        } else {
          await RemindersAPI.create(payload);
          toast(`Activity added to Week ${week}.`);
        }
        Modal.close();
        // Small delay to ensure DOM is settled before re-reading planner elements
        setTimeout(() => _refreshPlannerGrid(), 50);
      } catch (err) { toast(err.message, "error"); }
    }
  );

  /* Auto-focus title field after modal opens */
  setTimeout(() => document.getElementById("pm-title")?.focus(), 80);
}


/* ═══════════════════════════════════════════════════════════
   KNOWLEDGE BASE PANEL
   ═══════════════════════════════════════════════════════════ */
function buildKnowledgePanel() {
  const panel = el("div", { class:"tab-panel", id:"knowledge-panel" });
  const headerRow = el("div", { class:"kb-header-row" });
  const titleWrap = el("div");
  titleWrap.appendChild(el("h2", { class:"page-title", text:"Knowledge Base Management" }));
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
  hdr.appendChild(el("h2", { class:"page-title",    text:"Reports & Analytics" }));
  hdr.appendChild(el("p",  { class:"page-subtitle", text:"Generate and download student engagement reports for the semester" }));
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


/* ═══════════════════════════════════════════════════════════
   ADMIN PANEL  (Lecturer only)
   Section: Announcements Broadcast
   Query Insights live in the Dashboard tab.
   ═══════════════════════════════════════════════════════════ */
function buildAdminPanel() {
  const panel = el("div", { class: "tab-panel", id: "admin-panel" });
  panel.style.padding = "28px";
  panel.style.maxWidth = "680px";
  panel.style.margin = "0 auto";

  // ── Header ─────────────────────────────────────────────────
  const hdr = el("div", { style: "margin-bottom:28px;" });
  hdr.appendChild(el("h2", { class: "page-title", text:"📢 Broadcast Announcements" }));
  hdr.appendChild(el("p",  { class: "page-subtitle", text:"Post announcements to all students. Active announcements appear on the student greeting card and are pushed to their devices." }));
  panel.appendChild(hdr);

  // ── Compose card ───────────────────────────────────────────
  const annCard = _adminCard("New Announcement", []);

  const annTitleInput = el("input", {
    type: "text", class: "form-input admin-input",
    id: "ann-title", placeholder: "Announcement title…"
  });
  const annBodyTA = el("textarea", {
    class: "form-input admin-textarea",
    id: "ann-body", placeholder: "Message to all students…",
    rows: "4"
  });
  const postBtn = el("button", { class: "btn-primary", style: "width:100%;margin-top:10px;", onclick: async () => {
    const title = document.getElementById("ann-title").value.trim();
    const body  = document.getElementById("ann-body").value.trim();
    if (!title || !body) { toast("Title and message required.", "error"); return; }
    try {
      postBtn.disabled = true;
      await AdminAPI.postAnnouncement({ title, body });
      toast("Announcement posted to all students!", "success");
      document.getElementById("ann-title").value = "";
      document.getElementById("ann-body").value  = "";
      _loadAnnouncements(annListEl);
    } catch(e) { toast(e.message, "error"); }
    finally { postBtn.disabled = false; }
  }}, "📤  Post Announcement");

  annCard.appendChild(el("label", { class: "admin-label", text: "Title" }));
  annCard.appendChild(annTitleInput);
  annCard.appendChild(el("label", { class: "admin-label", text: "Message", style: "margin-top:10px;" }));
  annCard.appendChild(annBodyTA);
  annCard.appendChild(postBtn);
  panel.appendChild(annCard);

  // ── Posted announcements list ──────────────────────────────
  const listCard = _adminCard("Posted Announcements", []);
  const annListEl = el("div", { id: "admin-ann-list" });
  annListEl.innerHTML = "<p class='text-muted' style='font-size:12px;'>Loading…</p>";
  listCard.appendChild(annListEl);
  panel.appendChild(listCard);
  _loadAnnouncements(annListEl);

  return panel;
}

// ── Card helper ────────────────────────────────────────────────
function _adminCard(title, extraChildren = []) {
  const card = el("div", { class: "admin-card" });
  card.appendChild(el("h3", { class: "admin-card-title", text: title }));
  extraChildren.forEach(c => card.appendChild(c));
  return card;
}

// ── Load KB list ───────────────────────────────────────────────
async function _loadKBList(wrap) {
  wrap.innerHTML = "<p class='text-muted' style='font-size:12px;'>Loading…</p>";
  try {
    const data = await AdminAPI.listKnowledge();
    const entries = data.entries || [];
    if (entries.length === 0) {
      wrap.innerHTML = "<p class='text-muted' style='font-size:12px;'>No entries yet.</p>";
      return;
    }
    wrap.innerHTML = "";

    // Search bar
    const search = el("input", {
      type: "text", class: "form-input admin-input",
      placeholder: "🔍  Filter entries…",
      style: "margin-bottom:10px;",
      oninput: (e) => {
        const q = e.target.value.toLowerCase();
        wrap.querySelectorAll(".kb-entry-row").forEach(row => {
          row.style.display = row.dataset.search.includes(q) ? "" : "none";
        });
      }
    });
    wrap.appendChild(search);

    entries.forEach(entry => {
      const row = el("div", { class: "kb-entry-row" });
      row.dataset.search = (entry.intent_name + " " + (entry.keywords || []).join(" ")).toLowerCase();

      const topLine = el("div", { class: "kb-entry-top" });
      const badge   = el("span", { class: "kb-level-badge", text: entry.level || "all" });
      const name    = el("span", { class: "kb-entry-name", text: entry.intent_name });
      const kwds    = el("small", { class: "kb-entry-keywords", text: (entry.keywords || []).slice(0, 5).join(", ") });

      const delBtn = el("button", { class: "btn-danger-sm", onclick: async () => {
        if (!confirm(`Delete "${entry.intent_name}"?`)) return;
        try {
          await AdminAPI.deleteKnowledge(entry.id);
          toast("Entry deleted.", "info");
          _loadKBList(wrap);
        } catch(e) { toast(e.message, "error"); }
      }}, "✕");

      topLine.appendChild(badge);
      topLine.appendChild(name);
      topLine.appendChild(delBtn);
      row.appendChild(topLine);
      row.appendChild(kwds);
      wrap.appendChild(row);
    });

    // Count
    const countEl = el("p", { style: "font-size:11px;color:#9ca3af;margin-top:8px;",
      text: `${entries.length} entries total` });
    wrap.appendChild(countEl);

  } catch(e) {
    wrap.innerHTML = `<p class='text-muted' style='color:#ef4444;'>Error: ${e.message}</p>`;
  }
}

// ── Load Announcements ────────────────────────────────────────
async function _loadAnnouncements(wrap) {
  try {
    const data = await AdminAPI.listAnnouncements();
    const items = data.announcements || [];
    wrap.innerHTML = "";
    if (items.length === 0) {
      wrap.innerHTML = "<p class='text-muted' style='font-size:12px;'>No announcements yet.</p>";
      return;
    }
    items.forEach(ann => {
      const row = el("div", { class: "ann-row" });
      const title = el("div", { class: "ann-row-title", text: ann.title });
      const meta  = el("div", { class: "ann-row-meta", text: `${ann.author} · ${new Date(ann.created_at).toLocaleDateString()}` });
      const toggleBtn = el("button", {
        class: ann.active ? "btn-chip-green" : "btn-chip-grey",
        title: ann.active ? "Active — click to hide" : "Hidden — click to show",
        onclick: async () => {
          try {
            await AdminAPI.toggleAnnouncement(ann.id);
            _loadAnnouncements(wrap);
          } catch(e) { toast(e.message, "error"); }
        }
      }, ann.active ? "● Live" : "○ Hidden");
      const delBtn = el("button", { class: "btn-danger-sm", onclick: async () => {
        if (!confirm(`Delete "${ann.title}"?`)) return;
        try {
          await AdminAPI.deleteAnnouncement(ann.id);
          toast("Deleted.", "info");
          _loadAnnouncements(wrap);
        } catch(e) { toast(e.message, "error"); }
      }}, "✕");
      const editBtn = el("button", { class: "btn-chip-grey", title: "Edit this announcement",
        onclick: () => {
          const bodyHTML = `
            <div class="form-group">
              <label class="form-label-dark">Title</label>
              <input id="edit-ann-title" class="form-input-light" value="${ann.title.replace(/"/g,'&quot;')}" />
            </div>
            <div class="form-group">
              <label class="form-label-dark">Message</label>
              <textarea id="edit-ann-body" class="form-input-light" rows="4" style="font-size:13px;">${ann.body}</textarea>
            </div>
          `;
          Modal.open("Edit Announcement", bodyHTML, async () => {
            const newTitle = (document.getElementById("edit-ann-title")?.value || "").trim();
            const newBody  = (document.getElementById("edit-ann-body")?.value  || "").trim();
            if (!newTitle || !newBody) { toast("Title and message required.", "error"); return; }
            try {
              await apiFetch(`/admin/announcements/${ann.id}`, { method:"PUT", body: JSON.stringify({ title:newTitle, body:newBody }) });
              toast("Announcement updated.", "success");
              Modal.close();
              _loadAnnouncements(wrap);
            } catch(e) { toast(e.message, "error"); }
          });
        }
      }, "✏️ Edit");
      const actions = el("div", { style: "display:flex;gap:6px;align-items:center;margin-top:4px;flex-wrap:wrap;" });
      actions.appendChild(toggleBtn);
      actions.appendChild(editBtn);
      actions.appendChild(delBtn);
      row.appendChild(title);
      row.appendChild(meta);
      row.appendChild(actions);
      wrap.appendChild(row);
    });
  } catch(e) {
    wrap.innerHTML = `<p class='text-muted' style='color:#ef4444;'>Error: ${e.message}</p>`;
  }
}

// ── Load Insights ─────────────────────────────────────────────
async function _loadInsights(wrap) {
  try {
    const data = await AdminAPI.getInsights();
    wrap.innerHTML = "";

    // Stats summary row
    const stats = el("div", { class: "insights-stats-row" });
    const mkStat = (label, val, color = "#0B1E3F") => {
      const s = el("div", { class: "insights-stat-box" });
      s.appendChild(el("div", { class: "insights-stat-num", style: `color:${color};`, text: String(val) }));
      s.appendChild(el("div", { class: "insights-stat-label", text: label }));
      return s;
    };
    stats.appendChild(mkStat("Total Queries", data.total_queries));
    stats.appendChild(mkStat("Today", data.today_queries, "#15803d"));
    stats.appendChild(mkStat("Unanswered", (data.fallbacks || []).length, "#c0392b"));
    wrap.appendChild(stats);

    // Top intents chart (horizontal bars)
    if (data.top_intents && data.top_intents.length > 0) {
      wrap.appendChild(el("p", { class: "admin-label", style: "margin-top:12px;margin-bottom:6px;", text: "Top Asked Topics" }));
      const maxCount = data.top_intents[0].count || 1;
      data.top_intents.slice(0, 8).forEach(item => {
        const bar = el("div", { class: "insights-bar-row" });
        const label = el("span", { class: "insights-bar-label", text: item.intent });
        const track = el("div", { class: "insights-bar-track" });
        const fill  = el("div", { class: "insights-bar-fill", style: `width:${Math.round((item.count / maxCount) * 100)}%;` });
        const cnt   = el("span", { class: "insights-bar-count", text: item.count });
        track.appendChild(fill);
        bar.appendChild(label);
        bar.appendChild(track);
        bar.appendChild(cnt);
        wrap.appendChild(bar);
      });
    }

    // Recent unanswered
    if (data.fallbacks && data.fallbacks.length > 0) {
      wrap.appendChild(el("p", { class: "admin-label", style: "margin-top:14px;margin-bottom:6px;color:#c0392b;", text: "⚠ Recent Unanswered Queries" }));
      data.fallbacks.slice(0, 5).forEach(q => {
        const row = el("div", { class: "insights-fallback-row" });
        row.appendChild(el("span", { class: "insights-fallback-text", text: q.query_text }));
        row.appendChild(el("small", { class: "insights-fallback-level", text: `Level ${q.user_level || "?"}` }));
        wrap.appendChild(row);
      });
    }

  } catch(e) {
    wrap.innerHTML = `<p style='color:#ef4444;font-size:12px;'>Could not load insights: ${e.message}</p>`;
  }
}
