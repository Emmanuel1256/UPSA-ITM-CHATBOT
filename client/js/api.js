/* ═══════════════════════════════════════════════════════════
   js/api.js
   All REST API calls to the Flask backend.
   Loaded FIRST — all other JS files depend on:
     - apiFetch()
     - Auth object
     - AuthAPI / ChatAPI / KnowledgeAPI / RemindersAPI / AnalyticsAPI
   ═══════════════════════════════════════════════════════════ */

const API_BASE = "http://localhost:5000/api";

/* ─── Auth Token / User — stored in localStorage ─────────── */
const Auth = {
  getToken:    ()  => localStorage.getItem("upsa_token"),
  setToken:    (t) => localStorage.setItem("upsa_token", t),
  removeToken: ()  => localStorage.removeItem("upsa_token"),

  getUser:  () => {
    try { return JSON.parse(localStorage.getItem("upsa_user")); }
    catch { return null; }
  },
  setUser:     (u) => localStorage.setItem("upsa_user", JSON.stringify(u)),
  removeUser:  ()  => localStorage.removeItem("upsa_user"),

  isLoggedIn: () => !!localStorage.getItem("upsa_token"),
};


/* ─── Core Fetch Wrapper ─────────────────────────────────── */
async function apiFetch(endpoint, options = {}) {
  const token   = Auth.getToken();
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
    body: options.body !== undefined ? JSON.stringify(options.body) : undefined,
  });

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data.error || data.message || `Request failed (${res.status})`);
  }

  return data;
}


/* ═══════════════════════════════════════════════════════════
   AUTH API
   ═══════════════════════════════════════════════════════════ */
const AuthAPI = {
  register: (payload) =>
    apiFetch("/auth/register", { method: "POST", body: payload }),

  login: (payload) =>
    apiFetch("/auth/login", { method: "POST", body: payload }),

  me: () =>
    apiFetch("/auth/me"),
};


/* ═══════════════════════════════════════════════════════════
   CHAT API
   ═══════════════════════════════════════════════════════════ */
const ChatAPI = {
  getGreeting: () =>
    apiFetch("/chat/greeting"),
  sendMessage: (message) =>
    apiFetch("/chat/message", { method: "POST", body: { message } }),

  getHistory: () =>
    apiFetch("/chat/history"),

  clearHistory: () =>
    apiFetch("/chat/history", { method: "DELETE" }),
};


/* ═══════════════════════════════════════════════════════════
   KNOWLEDGE BASE API
   ═══════════════════════════════════════════════════════════ */
const KnowledgeAPI = {
  getAll: () =>
    apiFetch("/knowledge/"),

  create: (payload) =>
    apiFetch("/knowledge/", { method: "POST", body: payload }),

  update: (id, payload) =>
    apiFetch(`/knowledge/${id}`, { method: "PUT", body: payload }),

  delete: (id) =>
    apiFetch(`/knowledge/${id}`, { method: "DELETE" }),
};


/* ═══════════════════════════════════════════════════════════
   REMINDERS API
   ═══════════════════════════════════════════════════════════ */
const RemindersAPI = {
  getPlannerActivities: (semester) =>
    apiFetch(`/reminders/planner?semester=${semester}`),
  getAll: () =>
    apiFetch("/reminders/"),

  create: (payload) =>
    apiFetch("/reminders/", { method: "POST", body: payload }),

  update: (id, payload) =>
    apiFetch(`/reminders/${id}`, { method: "PUT", body: payload }),

  delete: (id) =>
    apiFetch(`/reminders/${id}`, { method: "DELETE" }),
};


/* ═══════════════════════════════════════════════════════════
   ANALYTICS API
   ═══════════════════════════════════════════════════════════ */
const AnalyticsAPI = {
  getSummary: () =>
    apiFetch("/analytics/summary"),

  getUnanswered: () =>
    apiFetch("/analytics/unanswered"),

  downloadPDF: (semester = "1", year = "2024/25") => {
    const token = Auth.getToken();
    const url   = `${API_BASE}/analytics/report/pdf?semester=${semester}&year=${encodeURIComponent(year)}`;
    fetch(url, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.blob())
      .then(blob => {
        const burl = URL.createObjectURL(blob);
        const a    = document.createElement("a");
        a.href     = burl;
        a.download = `UPSA_ITM_Report_Sem${semester}.pdf`;
        a.click();
        URL.revokeObjectURL(burl);
      })
      .catch(() => toast("PDF download failed. Try again.", "error"));
  },

  downloadCSV: () => {
    const token = Auth.getToken();
    const url   = `${API_BASE}/analytics/report/csv`;
    fetch(url, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.blob())
      .then(blob => {
        const burl = URL.createObjectURL(blob);
        const a    = document.createElement("a");
        a.href     = burl;
        a.download = "UPSA_ITM_Engagement_Data.csv";
        a.click();
        URL.revokeObjectURL(burl);
      })
      .catch(() => toast("CSV download failed. Try again.", "error"));
  },
};

/* ═══════════════════════════════════════════════════════════
   AdminAPI — Lecturer knowledge management, announcements,
               and query insights
   ═══════════════════════════════════════════════════════════ */
const AdminAPI = {
  // ── Knowledge Base ────────────────────────────────────────
  listKnowledge: () =>
    apiFetch("/admin/knowledge"),

  addKnowledge: (data) =>
    apiFetch("/admin/knowledge", { method: "POST", body: JSON.stringify(data) }),

  updateKnowledge: (id, data) =>
    apiFetch(`/admin/knowledge/${id}`, { method: "PUT", body: JSON.stringify(data) }),

  deleteKnowledge: (id) =>
    apiFetch(`/admin/knowledge/${id}`, { method: "DELETE" }),

  // ── Insights ─────────────────────────────────────────────
  getInsights: () =>
    apiFetch("/admin/insights"),

  // ── Announcements ─────────────────────────────────────────
  listAnnouncements: () =>
    apiFetch("/admin/announcements"),

  postAnnouncement: (data) =>
    apiFetch("/admin/announcements", { method: "POST", body: JSON.stringify(data) }),

  deleteAnnouncement: (id) =>
    apiFetch(`/admin/announcements/${id}`, { method: "DELETE" }),

  toggleAnnouncement: (id) =>
    apiFetch(`/admin/announcements/${id}/toggle`, { method: "POST" }),
};

/* ═══════════════════════════════════════════════════════════
   StrategiesAPI — 13-week counseling strategy system
   ═══════════════════════════════════════════════════════════ */
const StrategiesAPI = {
  // Full 13-week plan for a course + level
  getAll: (course, level) =>
    apiFetch(`/strategies?course=${encodeURIComponent(course)}&level=${encodeURIComponent(level)}`),

  // Single week strategy
  getWeek: (course, level, week) =>
    apiFetch(`/strategies/week?course=${encodeURIComponent(course)}&level=${encodeURIComponent(level)}&week=${week}`),

  // Lecturer updates a strategy
  update: (id, data) =>
    apiFetch(`/strategies/${id}`, { method: "PUT", body: JSON.stringify(data) }),

  // Lecturer adds a new strategy entry
  add: (data) =>
    apiFetch(`/strategies`, { method: "POST", body: JSON.stringify(data) }),

  // List available courses + levels
  getCourses: () =>
    apiFetch(`/strategies/courses`),
};
