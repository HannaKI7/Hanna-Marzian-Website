/* ── CONSENT MANAGER – DSGVO/GDPR ────────────────────────────────────────
   Speichert Entscheidung in localStorage (12 Monate).
   Lädt Google Analytics (GA4) und Facebook Pixel nur nach ausdrücklicher Zustimmung.
   Unterstützt Google Consent Mode v2.
────────────────────────────────────────────────────────────────────────── */

(function () {
  const GA_ID       = 'G-4E7ZR706ZT';
  const FB_ID       = '1698164877859527';
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

  function saveConsent(analytics, marketing) {
    const obj = {
      analytics: !!analytics,
      marketing: !!marketing,
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

  /* ── Facebook Pixel laden ───────────────────────────────────────────── */
  function loadFBPixel() {
    if (document.getElementById('fb-pixel-script')) return;

    // Facebook Pixel base code (ohne noscript-Fallback – DSGVO-konform)
    !function(f,b,e,v,n,t,s){
      if(f.fbq) return;
      n=f.fbq=function(){n.callMethod ?
        n.callMethod.apply(n,arguments) : n.queue.push(arguments)};
      if(!f._fbq) f._fbq=n;
      n.push=n; n.loaded=!0; n.version='2.0';
      n.queue=[];
    }(window, document, 'https://connect.facebook.net/en_US/fbevents.js');

    var s = document.createElement('script');
    s.id    = 'fb-pixel-script';
    s.async = true;
    s.src   = 'https://connect.facebook.net/en_US/fbevents.js';
    document.head.appendChild(s);

    s.onload = function() {
      window.fbq('init', FB_ID);
      if (!window.fbqSkipPageView) window.fbq('track', 'PageView');
    };
  }

  /* ── applyConsent ────────────────────────────────────────────────────── */
  function applyConsent(analytics, marketing) {
    gtag('consent', 'update', {
      analytics_storage:   analytics ? 'granted' : 'denied',
      ad_storage:          marketing  ? 'granted' : 'denied',
      ad_user_data:        marketing  ? 'granted' : 'denied',
      ad_personalization:  marketing  ? 'granted' : 'denied'
    });
    if (analytics) loadGA();
    if (marketing)  loadFBPixel();
  }

  /* ── DOM-Elemente ────────────────────────────────────────────────────── */
  function buildUI() {
    const overlay = document.createElement('div');
    overlay.id = 'consent-overlay';

    const banner = document.createElement('div');
    banner.id = 'consent-banner';
    banner.innerHTML = `
      <p>
        Wir nutzen Cookies, Google Analytics und den Facebook Pixel. Details in der <a href="/datenschutz.html">Datenschutzerklärung</a>.
      </p>
      <div class="consent-actions">
        <button class="consent-btn-settings" id="cb-settings">Einstellungen</button>
        <button class="consent-btn-decline"  id="cb-decline">Ablehnen</button>
        <button class="consent-btn-accept"   id="cb-accept">OK</button>
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

      <div class="consent-toggle-row">
        <div class="consent-toggle-info">
          <h4>Marketing (Facebook Pixel)</h4>
          <p>Ermöglicht zielgruppengerechte Werbung auf Facebook und Instagram. Betrieben von Meta Platforms Ireland Ltd.</p>
        </div>
        <label class="consent-toggle">
          <input type="checkbox" id="ct-marketing">
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
      saveConsent(true, true);
      applyConsent(true, true);
      hideBanner();
    });

    // Banner: Nur notwendige
    document.getElementById('cb-decline').addEventListener('click', function () {
      saveConsent(false, false);
      applyConsent(false, false);
      hideBanner();
    });

    // Banner: Einstellungen öffnen
    document.getElementById('cb-settings').addEventListener('click', function () {
      openModal();
    });

    // Modal: Auswahl speichern
    document.getElementById('cm-save').addEventListener('click', function () {
      const analytics = document.getElementById('ct-analytics').checked;
      const marketing = document.getElementById('ct-marketing').checked;
      saveConsent(analytics, marketing);
      applyConsent(analytics, marketing);
      closeModal();
      hideBanner();
    });

    // Modal: Nur notwendige
    document.getElementById('cm-decline').addEventListener('click', function () {
      saveConsent(false, false);
      applyConsent(false, false);
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
    const toggleAnalytics = document.getElementById('ct-analytics');
    const toggleMarketing = document.getElementById('ct-marketing');
    if (toggleAnalytics && existing) toggleAnalytics.checked = existing.analytics;
    if (toggleMarketing && existing) toggleMarketing.checked = existing.marketing;
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
      applyConsent(existing.analytics, existing.marketing);
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
