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
  var MOON_SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  var SUN_SVG  = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="12" y1="21" x2="12" y2="23" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="1" y1="12" x2="3" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="21" y1="12" x2="23" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';

  function syncButtons(theme) {
    var icon  = theme === 'dark' ? SUN_SVG : MOON_SVG;
    var label = theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';

    var desktop = document.getElementById('theme-toggle');
    if (desktop) {
      desktop.innerHTML = icon;
      desktop.setAttribute('aria-label', label);
      desktop.setAttribute('title', label);
    }

    document.querySelectorAll('.mobile-theme-toggle').forEach(function (btn) {
      btn.innerHTML = icon;
      btn.setAttribute('aria-label', label);
      btn.setAttribute('title', label);
    });
  }

  /* ---- Toggle handler ---- */
  function handleToggle() {
    var isDark = document.documentElement.classList.contains('dark-theme');
    var next = isDark ? 'light' : 'dark';
    localStorage.setItem(STORAGE_KEY, next);
    /* Add transition class, apply theme, then remove after fade completes */
    document.documentElement.classList.add('theme-transitioning');
    applyTheme(next);
    setTimeout(function () {
      document.documentElement.classList.remove('theme-transitioning');
    }, 450);
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
