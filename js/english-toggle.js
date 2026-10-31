/**
 * English gloss toggle for the interlinear reading pages (Services, Psalms).
 *
 * Hides or shows the faded English line under each Greek word. The hover/tap
 * word cards are unaffected. The choice is remembered per device and shared
 * by every page that includes this script.
 *
 * Usage: any button with the data-english-toggle attribute works, including
 * ones added later by the page (clicks are handled by delegation). Pages that
 * create buttons can call philologEnglishToggle.shown() for their initial
 * aria-pressed value. Include this script at the end of <body>.
 */
(function () {
  'use strict';

  var KEY = 'philolog-show-english';
  var root = document.documentElement;

  function savedChoice() {
    try { return localStorage.getItem(KEY) !== 'off'; } catch (e) { return true; }
  }

  function remember(show) {
    try { localStorage.setItem(KEY, show ? 'on' : 'off'); } catch (e) { /* private mode: not remembered */ }
  }

  function apply(show) {
    root.classList.toggle('hide-english', !show);
    document.querySelectorAll('[data-english-toggle]').forEach(function (btn) {
      btn.setAttribute('aria-pressed', String(show));
      btn.title = show ? 'Hide the English under each word' : 'Show the English under each word';
    });
  }

  var show = savedChoice();
  apply(show);

  document.addEventListener('click', function (e) {
    if (!e.target.closest('[data-english-toggle]')) return;
    show = !show;
    remember(show);
    apply(show);
  });

  window.philologEnglishToggle = {
    shown: function () { return show; }
  };
})();
