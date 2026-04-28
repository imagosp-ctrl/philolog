/* ============================================================
   theme.js — Philolog Global Dark Mode
   ============================================================ */

(function () {
  var STORAGE_KEY = 'philolog-theme';

  /* ---- Determine initial theme ---- */
  function getPreferredTheme() {
    var stored = localStorage.getItem(STORAGE_KEY);
    if (stored === 'dark' || stored === 'light') return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  /* ---- Apply theme to <html> ---- */
  function applyTheme(theme) {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark-theme');
    } else {
      document.documentElement.classList.remove('dark-theme');
    }
    syncButtons(theme);
  }

  /* ---- Sync all toggle button icons ---- */
  function syncButtons(theme) {
    var icon = theme === 'dark' ? '☀️' : '🌙';
    var label = theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';

    var desktop = document.getElementById('theme-toggle');
    if (desktop) {
      desktop.textContent = icon;
      desktop.setAttribute('aria-label', label);
      desktop.setAttribute('title', label);
    }

    document.querySelectorAll('.mobile-theme-toggle').forEach(function (btn) {
      btn.textContent = icon;
      btn.setAttribute('aria-label', label);
      btn.setAttribute('title', label);
    });
  }

  /* ---- Toggle handler ---- */
  function handleToggle() {
    var isDark = document.documentElement.classList.contains('dark-theme');
    var next = isDark ? 'light' : 'dark';
    localStorage.setItem(STORAGE_KEY, next);
    applyTheme(next);
  }

  /* ---- Wire up buttons once DOM is ready ---- */
  function wireButtons() {
    var desktop = document.getElementById('theme-toggle');
    if (desktop) desktop.addEventListener('click', handleToggle);

    document.querySelectorAll('.mobile-theme-toggle').forEach(function (btn) {
      btn.addEventListener('click', handleToggle);
    });

    /* Keep icons in sync with current state */
    syncButtons(document.documentElement.classList.contains('dark-theme') ? 'dark' : 'light');
  }

  /* ---- Listen for OS-level preference changes ---- */
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
    /* Only follow OS if user hasn't manually set a preference */
    if (!localStorage.getItem(STORAGE_KEY)) {
      applyTheme(e.matches ? 'dark' : 'light');
    }
  });

  /* ---- Init ---- */
  applyTheme(getPreferredTheme());

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wireButtons);
  } else {
    wireButtons();
  }
})();
