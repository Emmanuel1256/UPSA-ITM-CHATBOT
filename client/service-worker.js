/* ═══════════════════════════════════════════════════════════
   service-worker.js
   Handles background Web Push notification events.
   IMPORTANT: This file MUST sit at client/ (served from the
   root of the domain) for the Service Worker scope to cover
   the entire app.
   ═══════════════════════════════════════════════════════════ */

const SW_VERSION = "upsa-itm-v1";

/* ── Install ─────────────────────────────────────────────────
   Skip waiting so the new SW activates immediately.           */
self.addEventListener("install", (event) => {
    console.log("[SW] Installed:", SW_VERSION);
    self.skipWaiting();
});

/* ── Activate ────────────────────────────────────────────────
   Claim all clients so the SW controls open pages at once.    */
self.addEventListener("activate", (event) => {
    console.log("[SW] Activated:", SW_VERSION);
    event.waitUntil(self.clients.claim());
});

/* ── Push ────────────────────────────────────────────────────
   Fires when the Flask server sends a Web Push message.
   Parses JSON payload and shows an OS-level notification.     */
self.addEventListener("push", (event) => {
    let data = {};
    try {
        data = event.data ? event.data.json() : {};
    } catch {
        data = {
            title: "UPSA ITM Reminder",
            body: event.data ? event.data.text() : "You have an upcoming deadline.",
        };
    }

    const title = data.title || "UPSA ITM — Academic Assistant";
    const options = {
        body: data.body || "You have an upcoming deadline. Check your Reminders tab.",
        icon: data.icon || "/icons/icon-192.png",
        badge: data.badge || "/icons/badge-72.png",
        tag: "upsa-reminder",   // replaces previous notification of same tag
        renotify: true,              // buzz even if replacing an existing one
        requireInteraction: true,              // stay visible until user interacts
        data: { url: data.url || "/" },
        actions: [
            { action: "view", title: "View Reminders" },
            { action: "dismiss", title: "Dismiss" },
        ],
    };

    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

/* ── Notification Click ──────────────────────────────────────
   Opens/focuses the app when the user clicks the notification. */
self.addEventListener("notificationclick", (event) => {
    event.notification.close();

    if (event.action === "dismiss") return;

    const targetUrl = (event.notification.data && event.notification.data.url) || "/";

    event.waitUntil(
        self.clients
            .matchAll({ type: "window", includeUncontrolled: true })
            .then((clients) => {
                // Focus existing tab if already open
                for (const client of clients) {
                    if (client.url.includes(self.location.origin) && "focus" in client) {
                        client.focus();
                        client.navigate(targetUrl);
                        return;
                    }
                }
                // Open new tab
                if (self.clients.openWindow) {
                    return self.clients.openWindow(targetUrl);
                }
            })
    );
});

/* ── Push Subscription Change ────────────────────────────────
   Browser rotated push credentials — auto re-subscribe and
   notify all open clients to sync the new subscription with
   the Flask server.                                           */
self.addEventListener("pushsubscriptionchange", (event) => {
    console.log("[SW] Push subscription changed — re-subscribing.");
    event.waitUntil(
        self.registration.pushManager
            .subscribe({
                userVisibleOnly: true,
                applicationServerKey: event.oldSubscription
                    ? event.oldSubscription.options.applicationServerKey
                    : null,
            })
            .then((newSubscription) => {
                return self.clients.matchAll().then((clients) => {
                    clients.forEach((client) =>
                        client.postMessage({
                            type: "PUSH_SUBSCRIPTION_CHANGED",
                            subscription: newSubscription.toJSON(),
                        })
                    );
                });
            })
    );
});