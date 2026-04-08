/* ═══════════════════════════════════════════════════════════
   js/lecturer_bell.js
   Lecturer Unanswered-Query Bell
   ─────────────────────────────────────────────────────────
   Polls /api/admin/insights every 2 minutes.
   When new unanswered (fallback) queries are detected since
   the last check, the bell shows a red badge count.
   Clicking the bell opens a dropdown listing the unanswered
   queries with a shortcut to the Broadcast tab.

   DEPENDS ON: api.js (apiFetch, Auth), ui.js (switchTab, toast)
   ═══════════════════════════════════════════════════════════ */

const LecturerBell = (() => {

  const POLL_INTERVAL_MS = 2 * 60 * 1000;  // 2 minutes
  let _pollTimer        = null;
  let _lastSeenCount    = 0;    // total fallbacks seen on previous poll
  let _dropdownOpen     = false;
  let _bellBtn          = null;
  let _badge            = null;
  let _dropdown         = null;

  /* ─────────────────────────────────────────────────────── */
  /*  Inject the bell button into the header                 */
  /* ─────────────────────────────────────────────────────── */
  function inject() {
    const wrap = document.querySelector(".header-user-wrap");
    if (!wrap || document.getElementById("lecturer-bell-btn")) return;

    // ── Bell button ──────────────────────────────────────
    _bellBtn = document.createElement("button");
    _bellBtn.id        = "lecturer-bell-btn";
    _bellBtn.className = "lecturer-bell-btn";
    _bellBtn.title     = "Student query alerts";
    _bellBtn.innerHTML = "🔔";

    // ── Red badge ────────────────────────────────────────
    _badge = document.createElement("span");
    _badge.id        = "lecturer-bell-badge";
    _badge.className = "lecturer-bell-badge hidden";
    _badge.textContent = "0";
    _bellBtn.appendChild(_badge);

    // ── Dropdown panel ───────────────────────────────────
    _dropdown = document.createElement("div");
    _dropdown.id        = "lecturer-bell-dropdown";
    _dropdown.className = "lecturer-bell-dropdown hidden";

    // Click bell → toggle dropdown
    _bellBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      _toggleDropdown();
    });

    // Click anywhere else → close dropdown
    document.addEventListener("click", () => {
      if (_dropdownOpen) _closeDropdown();
    });

    const logoutBtn = document.getElementById("logout-btn");
    if (logoutBtn && logoutBtn.parentNode === wrap) {
      wrap.insertBefore(_dropdown, logoutBtn);
      wrap.insertBefore(_bellBtn, _dropdown);
    } else {
      wrap.appendChild(_dropdown);
      wrap.appendChild(_bellBtn);
    }

    // First poll immediately, then schedule
    _poll();
    _pollTimer = setInterval(_poll, POLL_INTERVAL_MS);
  }

  /* ─────────────────────────────────────────────────────── */
  /*  Poll /api/admin/insights for new unanswered queries   */
  /* ─────────────────────────────────────────────────────── */
  async function _poll() {
    try {
      const data      = await AdminAPI.getInsights();
      const fallbacks = data.fallbacks || [];
      const newCount  = fallbacks.length;

      // How many are genuinely NEW since last check
      const delta = Math.max(0, newCount - _lastSeenCount);

      if (delta > 0) {
        _setBadge(delta);
        // Only show a toast if the tab is not already visible
        const broadcastPanel = document.getElementById("admin-panel");
        const isVisible = broadcastPanel &&
          broadcastPanel.classList.contains("active");
        if (!isVisible) {
          toast(
            `🔔 ${delta} new unanswered student quer${delta === 1 ? "y" : "ies"} detected.`,
            "info"
          );
        }
      }

      _lastSeenCount = newCount;
      _renderDropdown(fallbacks, data.today_queries || 0, data.total_queries || 0);

    } catch (err) {
      // Silently fail — don't spam the UI if the endpoint is temporarily unreachable
      console.warn("[LecturerBell] Poll failed:", err.message);
    }
  }

  /* ─────────────────────────────────────────────────────── */
  /*  Render dropdown content                                */
  /* ─────────────────────────────────────────────────────── */
  function _renderDropdown(fallbacks, todayCount, totalCount) {
    _dropdown.innerHTML = "";

    // Header
    const hdr = document.createElement("div");
    hdr.className = "lbell-hdr";
    hdr.innerHTML = `<strong>Student Query Alerts</strong>
      <span class="lbell-meta">${todayCount} queries today · ${totalCount} total</span>`;
    _dropdown.appendChild(hdr);

    if (fallbacks.length === 0) {
      const empty = document.createElement("div");
      empty.className = "lbell-empty";
      empty.textContent = "✅ No unanswered queries — all good!";
      _dropdown.appendChild(empty);
    } else {
      const listHdr = document.createElement("div");
      listHdr.className = "lbell-section-label";
      listHdr.textContent = `⚠ Unanswered queries (${fallbacks.length})`;
      _dropdown.appendChild(listHdr);

      // Show most recent 6
      fallbacks.slice(0, 6).forEach(q => {
        const row = document.createElement("div");
        row.className = "lbell-query-row";

        const text = document.createElement("span");
        text.className = "lbell-query-text";
        text.textContent = q.query_text.length > 55
          ? q.query_text.slice(0, 55) + "…"
          : q.query_text;

        const level = document.createElement("span");
        level.className = "lbell-query-level";
        level.textContent = `Lv ${q.user_level || "?"}`;

        const time = document.createElement("span");
        time.className = "lbell-query-time";
        const d = new Date(q.timestamp);
        time.textContent = d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

        row.appendChild(text);
        const meta = document.createElement("div");
        meta.className = "lbell-query-meta";
        meta.appendChild(level);
        meta.appendChild(time);
        row.appendChild(meta);
        _dropdown.appendChild(row);
      });

      if (fallbacks.length > 6) {
        const more = document.createElement("div");
        more.className = "lbell-more";
        more.textContent = `+ ${fallbacks.length - 6} more`;
        _dropdown.appendChild(more);
      }
    }

    // Footer CTA — go to Broadcast tab
    const footer = document.createElement("div");
    footer.className = "lbell-footer";
    const goBtn = document.createElement("button");
    goBtn.className = "lbell-go-btn";
    goBtn.textContent = "View Insights in Broadcast →";
    goBtn.addEventListener("click", () => {
      switchTab("admin");
      _closeDropdown();
      _clearBadge();
    });
    footer.appendChild(goBtn);
    _dropdown.appendChild(footer);
  }

  /* ─────────────────────────────────────────────────────── */
  /*  Badge helpers                                          */
  /* ─────────────────────────────────────────────────────── */
  function _setBadge(count) {
    if (!_badge) return;
    _badge.textContent = count > 9 ? "9+" : String(count);
    _badge.classList.remove("hidden");
    _bellBtn.classList.add("bell-has-alert");
  }

  function _clearBadge() {
    if (!_badge) return;
    _badge.classList.add("hidden");
    _bellBtn.classList.remove("bell-has-alert");
    _lastSeenCount = 0;
  }

  /* ─────────────────────────────────────────────────────── */
  /*  Dropdown open / close                                  */
  /* ─────────────────────────────────────────────────────── */
  function _toggleDropdown() {
    _dropdownOpen ? _closeDropdown() : _openDropdown();
  }

  function _openDropdown() {
    _dropdown.classList.remove("hidden");
    _dropdownOpen = true;
    // Clear badge when user opens the panel
    _clearBadge();
    // Refresh content on open
    _poll();
  }

  function _closeDropdown() {
    _dropdown.classList.add("hidden");
    _dropdownOpen = false;
  }

  /* ─────────────────────────────────────────────────────── */
  /*  Cleanup (on logout)                                    */
  /* ─────────────────────────────────────────────────────── */
  function destroy() {
    if (_pollTimer) clearInterval(_pollTimer);
    _pollTimer = null;
    const btn  = document.getElementById("lecturer-bell-btn");
    const drop = document.getElementById("lecturer-bell-dropdown");
    if (btn)  btn.remove();
    if (drop) drop.remove();
    _bellBtn = _badge = _dropdown = null;
    _lastSeenCount = 0;
    _dropdownOpen  = false;
  }

  return { inject, destroy };
})();
