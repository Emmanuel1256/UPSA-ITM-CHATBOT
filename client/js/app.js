/* ═══════════════════════════════════════════════════════════
   js/app.js
   Application Bootstrap — Auth, Session, Routing.
   DEPENDS ON: api.js, push.js, ui.js, tabs.js (all loaded first)
   ═══════════════════════════════════════════════════════════ */

let _currentRole = "student";
let _authMode = "login";    // "login" | "register"


/* ═══════════════════════════════════════════════════════════
   DOMContentLoaded — entry point
   ═══════════════════════════════════════════════════════════ */
document.addEventListener("DOMContentLoaded", () => {
    _initLoginScreen();
    _initModalControls();

    // Resume session if token + user are already stored
    const user = Auth.getUser();
    if (user && Auth.isLoggedIn()) {
        _bootApp(user.role, user);
    } else {
        showScreen("login-screen");
    }
});


/* ═══════════════════════════════════════════════════════════
   LOGIN SCREEN
   ═══════════════════════════════════════════════════════════ */
function _initLoginScreen() {

    // ── Auth mode (Sign In / Register) toggle
    $$(".auth-mode-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            _authMode = btn.dataset.mode;
            $$(".auth-mode-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            const regFields = $("#register-only-fields");
            if (regFields) regFields.style.display = _authMode === "register" ? "block" : "none";

            const submitBtn = $("#auth-submit-btn");
            if (submitBtn) submitBtn.textContent = _authMode === "register" ? "Create Account" : "Sign In";

            const errEl = $("#login-error");
            if (errEl) errEl.textContent = "";
        });
    });

    // ── Role (Student / Lecturer) toggle
    $$(".role-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            _currentRole = btn.dataset.role;
            $$(".role-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            const studentFields = $("#student-fields");
            if (studentFields) studentFields.style.display = _currentRole === "student" ? "block" : "none";

            const emailLabel = $("#email-label");
            const emailHint = $("#email-hint");
            const emailInput = $("#login-email");

            if (emailLabel) emailLabel.textContent = _currentRole === "student" ? "Student Email" : "Lecturer Email";
            if (emailHint) emailHint.textContent = _currentRole === "student"
                ? "Format: 10299860@upsamail.edu.gh (8-digit student ID)"
                : "Format: john.doe@upsamail.edu.gh";
            if (emailInput) emailInput.placeholder = _currentRole === "student"
                ? "10299860@upsamail.edu.gh"
                : "john.doe@upsamail.edu.gh";

            const errEl = $("#login-error");
            if (errEl) errEl.textContent = "";
        });
    });

    // ── Submit button
    const submitBtn = $("#auth-submit-btn");
    if (submitBtn) submitBtn.addEventListener("click", _handleAuthSubmit);

    // ── Enter key on any input field
    ["login-email", "login-password", "reg-name"].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener("keydown", e => { if (e.key === "Enter") _handleAuthSubmit(); });
    });
}


async function _handleAuthSubmit() {
    const errEl = $("#login-error");
    const submitBtn = $("#auth-submit-btn");
    if (errEl) errEl.textContent = "";

    const email = ($("#login-email")?.value || "").trim();
    const password = ($("#login-password")?.value || "").trim();

    if (!email) { if (errEl) errEl.textContent = "Please enter your email."; return; }
    if (!password) { if (errEl) errEl.textContent = "Please enter your password."; return; }

    if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = "Please wait…"; }

    try {
        let result;

        if (_authMode === "register") {
            const name = ($("#reg-name")?.value || "").trim();
            if (!name) { if (errEl) errEl.textContent = "Please enter your full name."; return; }

            result = await AuthAPI.register({
                name,
                email,
                password,
                role: _currentRole,
                level: _currentRole === "student" ? ($("#login-level")?.value || "200") : null,
                semester: _currentRole === "student" ? ($("#login-semester")?.value || "1") : null,
            });
            toast("Account created! Welcome to UPSA ITM.");

        } else {
            result = await AuthAPI.login({ email, password, role: _currentRole });
        }

        // Persist session
        Auth.setToken(result.token);
        Auth.setUser(result.user);
        _bootApp(result.user.role, result.user);

    } catch (err) {
        if (errEl) errEl.textContent = err.message || "Something went wrong. Try again.";
    } finally {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = _authMode === "register" ? "Create Account" : "Sign In";
        }
    }
}


/* ═══════════════════════════════════════════════════════════
   APP BOOT — called after successful login or session resume
   ═══════════════════════════════════════════════════════════ */
function _bootApp(role, user) {
    populateHeader(role, user);
    buildAllPanels(role, user);
    showScreen("app-screen");

    // Push notifications — students only
    if (role === "student") {
        AppPushManager.init().then(() => AppPushManager.injectBellButton());
    }

    // Wire Logout button — clone to clear any old event listeners
    const logoutBtn = $("#logout-btn");
    if (logoutBtn) {
        const newBtn = logoutBtn.cloneNode(true);
        logoutBtn.parentNode.replaceChild(newBtn, logoutBtn);
        newBtn.addEventListener("click", _handleLogout);
    }
}


/* ═══════════════════════════════════════════════════════════
   LOGOUT
   ═══════════════════════════════════════════════════════════ */
function _handleLogout() {
    Auth.removeToken();
    Auth.removeUser();

    // Clear login form fields
    ["login-email", "login-password", "reg-name"].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = "";
    });
    const errEl = document.getElementById("login-error");
    if (errEl) errEl.textContent = "";

    showScreen("login-screen");
}


/* ═══════════════════════════════════════════════════════════
   MODAL CONTROLS
   ═══════════════════════════════════════════════════════════ */
function _initModalControls() {
    // Cancel button
    const cancelBtn = $("#modal-cancel-btn");
    if (cancelBtn) cancelBtn.addEventListener("click", () => Modal.close());

    // Click outside modal box
    const overlay = $("#modal-overlay");
    if (overlay) {
        overlay.addEventListener("click", e => {
            if (e.target === overlay) Modal.close();
        });
    }

    // Escape key
    document.addEventListener("keydown", e => {
        if (e.key === "Escape") Modal.close();
    });
}