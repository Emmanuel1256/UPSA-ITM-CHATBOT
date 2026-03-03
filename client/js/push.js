/* ═══════════════════════════════════════════════════════════
   js/push.js
   Frontend Web Push Manager.
   Handles: SW registration, permission request,
            subscribe/unsubscribe, subscription sync with API,
            bell button injection into app header.

   DEPENDS ON: api.js  (apiFetch, Auth)
   NAMED: AppPushManager — NOT PushManager, because
          window.PushManager is a reserved browser API name.
   ═══════════════════════════════════════════════════════════ */

/* ─── Push REST API calls ─────────────────────────────────── */
/* Defined here (not api.js) so push.js is self-contained.    */
const PushAPI = {
  getVapidKey: () =>
    apiFetch("/push/vapid-public-key"),

  subscribe: (subscriptionJSON) =>
    apiFetch("/push/subscribe",   { method: "POST", body: subscriptionJSON }),

  unsubscribe: (endpoint) =>
    apiFetch("/push/unsubscribe", { method: "POST", body: { endpoint } }),

  status: () =>
    apiFetch("/push/status"),

  testPush: () =>
    apiFetch("/push/test", { method: "POST" }),
};


/* ─── AppPushManager IIFE ─────────────────────────────────── */
const AppPushManager = (() => {

  let _swReg         = null;   // ServiceWorkerRegistration
  let _vapidPublicKey = null;  // fetched from Flask

  /* ── Helpers ──────────────────────────────────────────── */

  /** Convert base64url VAPID key to Uint8Array for browser subscribe() */
  function _urlBase64ToUint8Array(base64) {
    const padding = "=".repeat((4 - (base64.length % 4)) % 4);
    const b64     = (base64 + padding).replace(/-/g, "+").replace(/_/g, "/");
    const raw     = window.atob(b64);
    const arr     = new Uint8Array(raw.length);
    for (let i = 0; i < raw.length; i++) arr[i] = raw.charCodeAt(i);
    return arr;
  }

  /** True if browser supports all required Push APIs */
  function isSupported() {
    return (
      "serviceWorker" in navigator &&
      "PushManager"   in window    &&   // checks browser's native API, not our variable
      "Notification"  in window
    );
  }

  /* ── Init ─────────────────────────────────────────────── */

  /**
   * Register the Service Worker and fetch the VAPID public key.
   * Call once from app.js after the user logs in.
   */
  async function init() {
    if (!isSupported()) {
      console.log("[Push] Browser does not support push notifications.");
      return false;
    }

    try {
      // Register SW — path must match where index.html is served from
      _swReg = await navigator.serviceWorker.register("service-worker.js");
      console.log("[Push] Service Worker registered.");

      // When browser rotates subscription, SW posts a message to re-sync
      navigator.serviceWorker.addEventListener("message", (event) => {
        if (event.data && event.data.type === "PUSH_SUBSCRIPTION_CHANGED") {
          _syncWithServer(event.data.subscription);
        }
      });

      // Fetch VAPID public key from Flask (no auth required)
      const data     = await PushAPI.getVapidKey();
      _vapidPublicKey = data.public_key;
      return true;

    } catch (err) {
      console.error("[Push] Init failed:", err);
      return false;
    }
  }

  /* ── Subscribe ────────────────────────────────────────── */

  async function requestAndSubscribe() {
    if (!_swReg || !_vapidPublicKey) {
      // VAPID not configured — bell stays hidden, no error shown
      return false;
      return false;
    }

    const permission = await Notification.requestPermission();
    if (permission !== "granted") {
      toast("Notification permission denied. Enable it in browser settings.", "info");
      return false;
    }

    try {
      const subscription = await _swReg.pushManager.subscribe({
        userVisibleOnly:      true,
        applicationServerKey: _urlBase64ToUint8Array(_vapidPublicKey),
      });

      await _syncWithServer(subscription.toJSON());
      _updateBellUI(true);
      toast("🔔 Push notifications enabled! You'll be notified 3 and 1 day before deadlines.");
      return true;

    } catch (err) {
      console.error("[Push] Subscribe failed:", err);
      toast("Could not enable push notifications: " + err.message, "error");
      return false;
    }
  }

  /* ── Unsubscribe ──────────────────────────────────────── */

  async function unsubscribe() {
    if (!_swReg) return;
    try {
      const sub = await _swReg.pushManager.getSubscription();
      if (sub) {
        const endpoint = sub.endpoint;
        await sub.unsubscribe();
        await PushAPI.unsubscribe(endpoint);
      }
      _updateBellUI(false);
      toast("Push notifications disabled.");
    } catch (err) {
      console.error("[Push] Unsubscribe failed:", err);
      toast("Could not disable notifications: " + err.message, "error");
    }
  }

  /* ── Toggle ───────────────────────────────────────────── */

  async function toggle() {
    const subscribed = await isSubscribed();
    if (subscribed) {
      await unsubscribe();
    } else {
      await requestAndSubscribe();
    }
  }

  /* ── Check state ──────────────────────────────────────── */

  async function isSubscribed() {
    if (!_swReg) return false;
    const sub = await _swReg.pushManager.getSubscription();
    return !!sub;
  }

  /* ── Sync subscription with Flask ────────────────────── */

  async function _syncWithServer(subscriptionJSON) {
    try {
      await PushAPI.subscribe(subscriptionJSON);
    } catch (err) {
      console.error("[Push] Failed to sync subscription with server:", err);
    }
  }

  /* ── Test push ────────────────────────────────────────── */

  async function sendTest() {
    try {
      const result = await PushAPI.testPush();
      toast(result.message || "Test notification sent!", "info");
    } catch (err) {
      toast(err.message, "error");
    }
  }

  /* ── Bell button UI ───────────────────────────────────── */

  function _updateBellUI(subscribed) {
    const bell = document.getElementById("push-bell-btn");
    if (!bell) return;
    if (subscribed) {
      bell.textContent = "🔔";
      bell.title       = "Notifications ON — click to disable";
      bell.classList.add("bell-active");
    } else {
      bell.textContent = "🔕";
      bell.title       = "Enable push notifications";
      bell.classList.remove("bell-active");
    }
  }

  /**
   * Inject the bell button into the app header.
   * Called from app.js after successful login (students only).
   */
  async function injectBellButton() {
    if (!isSupported() || !_vapidPublicKey) return;

    const wrap = document.querySelector(".header-user-wrap");
    if (!wrap || document.getElementById("push-bell-btn")) return;

    const btn = document.createElement("button");
    btn.id          = "push-bell-btn";
    btn.className   = "push-bell-btn";
    btn.textContent = "🔕";
    btn.title       = "Enable push notifications";
    btn.addEventListener("click", toggle);

    // Insert before Logout button
    const logoutBtn = document.getElementById("logout-btn");
    wrap.insertBefore(btn, logoutBtn);

    // Sync with actual browser subscription state
    const subscribed = await isSubscribed();
    _updateBellUI(subscribed);
  }

  /* ── Public API ───────────────────────────────────────── */
  return {
    init,
    requestAndSubscribe,
    unsubscribe,
    toggle,
    isSubscribed,
    isSupported,
    sendTest,
    injectBellButton,
  };

})();
