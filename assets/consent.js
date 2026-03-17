/* ── CONSENT MANAGER – DSGVO/GDPR ────────────────────────────────────────
   Speichert Entscheidung in localStorage (12 Monate).
   Lädt Google Analytics (GA4) nur nach ausdrücklicher Zustimmung.
   Unterstützt Google Consent Mode v2.
────────────────────────────────────────────────────────────────────────── */

(function () {
  const GA_ID       = 'G-4E7ZR706ZT';
  const STORAGE_KEY = 'hanna_consent';
  const CONSENT_TTL = 365 * 24 * 60 * 60 * 1000; // 12 Monate

  /* ── Consent-State lesen / schreiben ─────────────────────────────────── */
  function getConsent() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      const obj = JSON.parse(raw);
      if (Date.now() > obj.expires) { localStorage.removeItem(STORAGE_KEY); return null; }
      return obj;
    } catch (e) { return null; }
  }

  function saveConsent(analytics) {
    const obj = {
      analytics: !!analytics,
      timestamp: Date.now(),
      expires:   Date.now() + CONSENT_TTL
    };
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(obj)); } catch (e) {}
    return obj;
  }

  /* ── Google Consent Mode v2 (Standard: alles denied) ─────────────────── */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;

  gtag('consent', 'default', {
    ad_storage:              'denied',
    ad_user_data:            'denied',
    ad_personalization:      'denied',
    analytics_storage:       'denied',
    functionality_storage:   'denied',
    personalization_storage: 'denied',
    security_storage:        'granted',
    wait_for_update:         500
  });
  gtag('js', new Date());
  gtag('config', GA_ID, { anonymize_ip: true });

  /* ── GA4 laden ──────────────────────────────────────────────────────── */
  function loadGA() {
    if (document.getElementById('ga-script')) return;
    const s = document.createElement('script');
    s.id    = 'ga-script';
    s.async = true;
    s.src   = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }

  function applyConsent(analytics) {
    gtag('consent', 'update', {
      analytics_storage: analytics ? 'granted' : 'denied',
      ad_storage:        'denied',
      ad_user_data:      'denied',
      ad_personalization:'denied'
    });
    if (analytics) loadGA();
  }

  /* ── DOM-Elemente ────────────────────────────────────────────────────── */
  function buildUI() {
    const overlay = document.createElement('div');
    overlay.id = 'consent-overlay';

    const banner = document.createElement('div');
    banner.id = 'consent-banner';
    banner.innerHTML = `
      <p>
        Diese Website verwendet Cookies. Notwendige Cookies sind immer aktiv.
        Mit deiner Zustimmung setzen wir Google Analytics ein, um zu verstehen, wie Besucher die Seite nutzen.
        Mehr dazu in der <a href="/datenschutz.html">Datenschutzerklärung</a>.
      </p>
      <div class="consent-actions">
        <button class="consent-btn-settings" id="cb-settings">Einstellungen</button>
        <button class="consent-btn-decline"  id="cb-decline">Nur notwendige</button>
        <button class="consent-btn-accept"   id="cb-accept">Alle akzeptieren</button>
      </div>
    `;

    const modal = document.createElement('div');
    modal.id = 'consent-modal';
    modal.innerHTML = `
      <h3>Cookie-Einstellungen</h3>
      <p class="modal-sub">
        Wähle selbst, welche Cookies du erlaubst.
        Details in der <a href="/datenschutz.html">Datenschutzerklärung</a>.
      </p>

      <div class="consent-toggle-row">
        <div class="consent-toggle-info">
          <h4>Notwendig</h4>
          <p>Technisch erforderlich für den Betrieb der Website. Können nicht deaktiviert werden.</p>
        </div>
        <label class="consent-toggle">
          <input type="checkbox" checked disabled>
          <span class="consent-toggle-slider"></span>
        </label>
      </div>

      <div class="consent-toggle-row">
        <div class="consent-toggle-info">
          <h4>Analyse (Google Analytics)</h4>
          <p>Hilft uns zu verstehen, wie Besucher die Seite nutzen. Daten werden anonymisiert erhoben.</p>
        </div>
        <label class="consent-toggle">
          <input type="checkbox" id="ct-analytics">
          <span class="consent-toggle-slider"></span>
        </label>
      </div>

      <div class="modal-actions">
        <button class="consent-btn-decline" id="cm-decline">Nur notwendige</button>
        <button class="consent-btn-accept"  id="cm-save">Auswahl speichern</button>
      </div>
    `;

    document.body.appendChild(overlay);
    document.body.appendChild(banner);
    document.body.appendChild(modal);

    /* ── Event Listener ─────────────────────────────────────────────── */
    // Banner: Alle akzeptieren
    document.getElementById('cb-accept').addEventListener('click', function () {
      saveConsent(true);
      applyConsent(true);
      hideBanner();
    });

    // Banner: Nur notwendige
    document.getElementById('cb-decline').addEventListener('click', function () {
      saveConsent(false);
      applyConsent(false);
      hideBanner();
    });

    // Banner: Einstellungen öffnen
    document.getElementById('cb-settings').addEventListener('click', function () {
      openModal();
    });

    // Modal: Auswahl speichern
    document.getElementById('cm-save').addEventListener('click', function () {
      const analytics = document.getElementById('ct-analytics').checked;
      saveConsent(analytics);
      applyConsent(analytics);
      closeModal();
      hideBanner();
    });

    // Modal: Nur notwendige
    document.getElementById('cm-decline').addEventListener('click', function () {
      saveConsent(false);
      applyConsent(false);
      closeModal();
      hideBanner();
    });

    // Overlay: Klick schließt Modal (ohne zu speichern)
    overlay.addEventListener('click', function () {
      closeModal();
    });

    /* ── Banner anzeigen ────────────────────────────────────────────── */
    setTimeout(function () {
      banner.classList.add('visible');
    }, 600);
  }

  function hideBanner() {
    const banner = document.getElementById('consent-banner');
    const overlay = document.getElementById('consent-overlay');
    if (banner)  banner.classList.remove('visible');
    if (overlay) overlay.classList.remove('visible');
  }

  function openModal() {
    const modal   = document.getElementById('consent-modal');
    const overlay = document.getElementById('consent-overlay');
    const existing = getConsent();
    const toggle = document.getElementById('ct-analytics');
    if (toggle && existing) toggle.checked = existing.analytics;
    if (modal)   modal.classList.add('visible');
    if (overlay) overlay.classList.add('visible');
    const banner = document.getElementById('consent-banner');
    if (banner) banner.classList.remove('visible');
  }

  function closeModal() {
    const modal   = document.getElementById('consent-modal');
    const overlay = document.getElementById('consent-overlay');
    if (modal)   modal.classList.remove('visible');
    if (overlay) overlay.classList.remove('visible');
  }

  /* ── Öffentliche Funktion: Einstellungen neu öffnen ─────────────── */
  window.reopenConsent = function () {
    const banner = document.getElementById('consent-banner');
    if (!banner) { buildUI(); return; }
    openModal();
  };

  /* ── Init ────────────────────────────────────────────────────────── */
  function init() {
    const existing = getConsent();

    if (existing) {
      // Bekannter Nutzer: Consent anwenden ohne Banner
      applyConsent(existing.analytics);
    } else {
      // Erster Besuch: Banner zeigen
      buildUI();
    }

    // Reopen-Button initialisieren (falls im DOM vorhanden)
    const reopenBtn = document.getElementById('consent-reopen');
    if (reopenBtn) {
      reopenBtn.addEventListener('click', function () {
        if (!document.getElementById('consent-banner')) {
          buildUI();
        }
        openModal();
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
