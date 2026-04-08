/* ═══════════════════════════════════════════════════════════
   js/app.js
   Application Bootstrap — Auth, Session, Routing.
   DEPENDS ON: api.js, push.js, ui.js, tabs.js (all loaded first)
   ═══════════════════════════════════════════════════════════ */

let _currentRole = "student";
let _authMode    = "login";    // "login" | "register"


/* ═══════════════════════════════════════════════════════════
   DOMContentLoaded — entry point
   ═══════════════════════════════════════════════════════════ */
document.addEventListener("DOMContentLoaded", () => {
  _initLoginScreen();
  _initModalControls();
  _initLandingScreen();
  _initThemeToggle();

  // Resume session if token + user are already stored
  const user = Auth.getUser();
  if (user && Auth.isLoggedIn()) {
    _bootApp(user.role, user);
  } else {
    showScreen("landing-screen");
  }
});

/* ═══════════════════════════════════════════════════════════
   LANDING SCREEN — role selection before login
   ═══════════════════════════════════════════════════════════ */
function _initLandingScreen() {
  const studentBtn  = document.getElementById("landing-student-btn");
  const lecturerBtn = document.getElementById("landing-lecturer-btn");

  function goToLogin(role) {
    _currentRole = role;
    // Update login card to reflect chosen role
    const emailLabel  = document.getElementById("email-label");
    const studentFlds = document.getElementById("student-fields");
    const authTitle   = document.querySelector(".login-title");
    const authSub     = document.querySelector(".login-subtitle");

    if (emailLabel)  emailLabel.textContent = role === "student" ? "Student Email" : "Staff Email";
    if (studentFlds) studentFlds.style.display = role === "student" ? "block" : "none";
    if (authTitle)   authTitle.textContent  = role === "student" ? "Student Portal" : "Lecturer Portal";
    if (authSub)     authSub.textContent    = role === "student"
      ? "Sign in to access the ITM Academic Counseling System"
      : "Sign in to manage the ITM Counseling System";

    showScreen("login-screen");
  }

  if (studentBtn)  studentBtn.addEventListener("click", () => goToLogin("student"));
  if (lecturerBtn) lecturerBtn.addEventListener("click", () => goToLogin("lecturer"));

  // Back button on login card → returns to landing
  const backBtn = document.getElementById("login-back-btn");
  if (backBtn) {
    backBtn.addEventListener("click", () => {
      // Clear any error and inputs before going back
      const errEl = document.getElementById("login-error");
      if (errEl) errEl.textContent = "";
      ["login-email","login-password","reg-name","reg-confirm-password"].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = "";
      });
      const mh = document.getElementById("pw-match-hint");
      if (mh) mh.textContent = "";
      showScreen("landing-screen");
    });
  }
}


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
      const confirmGrp = $("#confirm-pw-group");
      if (confirmGrp) confirmGrp.style.display = _authMode === "register" ? "block" : "none";
      // Clear confirm field and hint when switching modes
      const cpf = $("#reg-confirm-password");
      const mh  = $("#pw-match-hint");
      if (cpf) cpf.value = "";
      if (mh)  mh.textContent = "";

      const submitBtn = $("#auth-submit-btn");
      if (submitBtn) submitBtn.textContent = _authMode === "register" ? "Create Account" : "Sign In";

      const errEl = $("#login-error");
      if (errEl) errEl.textContent = "";
    });
  });

  // Role is selected on the landing screen — no toggle needed here

  // ── Password show/hide toggle (main)
  const pwToggle  = document.getElementById("pw-toggle-btn");
  const pwInput   = document.getElementById("login-password");
  const eyeOpen   = document.getElementById("pw-eye-open");
  const eyeClosed = document.getElementById("pw-eye-closed");
  if (pwToggle && pwInput) {
    pwToggle.addEventListener("click", () => {
      const isHidden = pwInput.type === "password";
      pwInput.type = isHidden ? "text" : "password";
      if (eyeOpen)   eyeOpen.style.display   = isHidden ? "none" : "";
      if (eyeClosed) eyeClosed.style.display = isHidden ? ""    : "none";
      pwInput.focus();
    });
  }

  // ── Confirm password show/hide toggle
  const confirmToggle  = document.getElementById("confirm-pw-toggle");
  const confirmInput   = document.getElementById("reg-confirm-password");
  const confirmEyeOpen = document.getElementById("confirm-eye-open");
  const confirmEyeClosed = document.getElementById("confirm-eye-closed");
  if (confirmToggle && confirmInput) {
    confirmToggle.addEventListener("click", () => {
      const isHidden = confirmInput.type === "password";
      confirmInput.type = isHidden ? "text" : "password";
      if (confirmEyeOpen)   confirmEyeOpen.style.display   = isHidden ? "none" : "";
      if (confirmEyeClosed) confirmEyeClosed.style.display = isHidden ? ""    : "none";
      confirmInput.focus();
    });
  }

  // ── Live password match hint
  if (confirmInput && pwInput) {
    const matchHint = document.getElementById("pw-match-hint");
    const checkMatch = () => {
      if (!confirmInput.value) { if (matchHint) matchHint.textContent = ""; return; }
      const match = pwInput.value === confirmInput.value;
      if (matchHint) {
        matchHint.textContent = match ? "✓ Passwords match" : "✗ Passwords do not match";
        matchHint.style.color = match ? "#22c55e" : "#ef4444";
      }
    };
    confirmInput.addEventListener("input", checkMatch);
    pwInput.addEventListener("input", checkMatch);
  }

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
  const errEl     = $("#login-error");
  const submitBtn = $("#auth-submit-btn");
  if (errEl) errEl.textContent = "";

  const email    = ($("#login-email")?.value    || "").trim();
  const password = ($("#login-password")?.value || "").trim();

  if (!email)    { if (errEl) errEl.textContent = "Please enter your email.";    return; }
  if (!password) { if (errEl) errEl.textContent = "Please enter your password."; return; }

  if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = "Please wait…"; }

  try {
    let result;

    if (_authMode === "register") {
      const name = ($("#reg-name")?.value || "").trim();
      if (!name) { if (errEl) errEl.textContent = "Please enter your full name."; return; }

      // Confirm password check
      const confirmPw = ($("#reg-confirm-password")?.value || "").trim();
      if (!confirmPw) { if (errEl) errEl.textContent = "Please confirm your password."; return; }
      if (password !== confirmPw) { if (errEl) errEl.textContent = "Passwords do not match. Please try again."; return; }

      result = await AuthAPI.register({
        name,
        email,
        password,
        role:     _currentRole,
        level:    _currentRole === "student" ? ($("#login-level")?.value    || "200") : null,
        semester: _currentRole === "student" ? ($("#login-semester")?.value || "1")   : null,
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
      submitBtn.disabled    = false;
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

  // Push — silent init for BOTH roles (no bell UI)
  // Students: deadline reminders + daily motivation
  // Lecturers: instant alert when a student asks an unanswered question
  AppPushManager.silentInit().catch(err => console.warn("[Push] Silent init failed:", err));

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
  ["login-email", "login-password", "reg-name", "reg-confirm-password"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = "";
  });
  const _mh = document.getElementById("pw-match-hint");
  if (_mh) _mh.textContent = "";
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


/* ═══════════════════════════════════════════════════════════
   DARK / LIGHT MODE TOGGLE
   ═══════════════════════════════════════════════════════════ */
function _initThemeToggle() {
  const btn = document.getElementById("theme-toggle-btn");
  if (!btn) return;

  // Load saved preference
  const saved = localStorage.getItem("upsa_theme") || "dark";
  _applyTheme(saved);

  btn.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme") || "dark";
    const next    = current === "dark" ? "light" : "dark";
    _applyTheme(next);
    localStorage.setItem("upsa_theme", next);
  });
}

function _applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  const btn = document.getElementById("theme-toggle-btn");
  if (btn) btn.textContent = theme === "dark" ? "☀️" : "🌙";
}
