(() => {
  const GA_MEASUREMENT_ID = 'G-687Y8YTR90';

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function gtag() {
    window.dataLayer.push(arguments);
  };

  if (!document.querySelector(`script[src*="googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}"]`)) {
    const analyticsScript = document.createElement('script');
    analyticsScript.async = true;
    analyticsScript.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
    document.head.appendChild(analyticsScript);
  }

  if (!window.__hdnGa4Initialized) {
    window.gtag('js', new Date());
    window.gtag('config', GA_MEASUREMENT_ID);
    window.__hdnGa4Initialized = true;
  }

  const articleReferrer = (() => {
    try {
      return document.referrer && new URL(document.referrer).hostname === 'article.hdnjapan.com';
    } catch {
      return false;
    }
  })();

  if (articleReferrer) {
    window.gtag('event', 'article_referral_landing', {
      landing_path: window.location.pathname,
      referrer_url: document.referrer,
      content_language: document.documentElement.lang || 'ja',
    });
  }

  const currentPath = window.location.pathname;
  const isJapanese = (document.documentElement.lang || '').toLowerCase().startsWith('ja');

  const pageKey = (() => {
    if (currentPath.includes('lhub-lp')) return 'lhub_lp';
    if (currentPath.includes('lhub')) return 'lhub';
    if (currentPath.includes('self-pay')) return 'self_pay';
    if (currentPath.includes('medical-sns')) return 'medical_sns';
    if (currentPath.includes('consultation')) return 'consultation';
    if (currentPath.includes('privacy')) return 'privacy';
    if (currentPath.startsWith('/en/')) return 'en_home';
    return 'home';
  })();

  function consultationIntent(link) {
    const text = `${link.textContent || ''} ${link.dataset.cta || ''}`.toLowerCase();
    if (/lhub|line|デモ/.test(text) || pageKey.startsWith('lhub')) return 'lhub';
    if (/sns|動画|youtube|social/.test(text) || pageKey === 'medical_sns') return 'sns';
    if (/自費|private care|private medical/.test(text) || pageKey === 'self_pay') return 'self_pay';
    if (/導線|診断|patient journey/.test(text)) return 'journey_review';
    if (/問い合わせ|inquiry|privacy|個人情報/.test(text) || pageKey === 'privacy') return 'inquiry';
    return 'general';
  }

  function consultationPosition(link, index) {
    if (link.dataset.cta) return String(link.dataset.cta).slice(0, 48);
    if (link.closest('header, .site-header, .header')) return 'header';
    if (link.closest('.hero')) return 'hero';
    if (link.closest('.mobile-cta')) return 'mobile_fixed';
    if (link.closest('footer, .footer')) return 'footer';
    if (link.closest('.final')) return 'final';
    return `body_${index + 1}`;
  }

  function annotateConsultationLinks() {
    const links = Array.from(document.querySelectorAll('a[href]')).filter((link) => {
      try {
        const url = new URL(link.href, window.location.href);
        return url.hostname === window.location.hostname && url.pathname.endsWith('/consultation-form.html');
      } catch {
        return false;
      }
    });

    links.forEach((link, index) => {
      const url = new URL(link.href, window.location.href);
      const intent = consultationIntent(link);
      const position = consultationPosition(link, index);
      url.searchParams.set('cta_source', pageKey);
      url.searchParams.set('cta_intent', intent);
      url.searchParams.set('cta_position', position);
      link.href = `${url.pathname}${url.search}${url.hash}`;
      link.dataset.hdnConsultationCta = 'attributed';
      link.dataset.hdnCtaSource = pageKey;
      link.dataset.hdnCtaIntent = intent;
      link.dataset.hdnCtaPosition = position;
    });
  }

  // Runtime safety net: no corporate CTA may leave HDN for Google Forms.
  document.querySelectorAll('a[href*="forms.gle/"], a[href*="docs.google.com/forms/"]').forEach((link) => {
    link.href = '/consultation-form.html';
    link.removeAttribute('target');
    link.removeAttribute('rel');
    link.dataset.hdnConsultationCta = 'custom-form';
  });

  annotateConsultationLinks();

  document.addEventListener('click', (event) => {
    const target = event.target;
    const link = target instanceof Element ? target.closest('a[href]') : null;
    if (!link) return;

    const destination = new URL(link.href, window.location.href);
    const linkText = (link.textContent || '').trim().slice(0, 100);
    const common = {
      source_path: window.location.pathname,
      link_url: destination.href,
      link_text: linkText,
      traffic_origin: articleReferrer ? 'hdn_articles' : 'other',
      content_language: document.documentElement.lang || 'ja',
    };

    if (destination.hostname === 'article.hdnjapan.com') {
      window.gtag('event', 'hdn_to_article_click', {
        ...common,
        destination_key: 'articles',
      });
      return;
    }

    if (destination.hostname !== window.location.hostname) return;

    if (destination.pathname.includes('consultation')) {
      window.gtag('event', 'hdn_consultation_click', {
        ...common,
        destination_key: 'consultation',
        cta_source: link.dataset.hdnCtaSource || destination.searchParams.get('cta_source') || pageKey,
        cta_intent: link.dataset.hdnCtaIntent || destination.searchParams.get('cta_intent') || 'general',
        cta_position: link.dataset.hdnCtaPosition || destination.searchParams.get('cta_position') || 'unknown',
      });
      return;
    }

    const destinationKey = destination.pathname.includes('lhub')
      ? 'lhub'
      : destination.pathname.includes('self-pay')
        ? 'self-pay'
        : destination.pathname.includes('medical-sns')
          ? 'medical-sns'
          : null;

    if (destinationKey) {
      window.gtag('event', 'hdn_service_click', {
        ...common,
        destination_key: destinationKey,
      });
    }
  });

  const desktopNav = document.querySelector('.site-header .nav, .header .nav, .nav');
  const mobileNavInner = document.querySelector('.mobile-nav-inner');

  if (isJapanese) {
    const snsHref = '/medical-sns.html';
    const snsLabel = 'SNS・動画戦略';

    if (desktopNav && !desktopNav.querySelector('a[href$="medical-sns.html"]')) {
      const snsLink = document.createElement('a');
      snsLink.href = snsHref;
      snsLink.textContent = snsLabel;
      if (currentPath.endsWith('/medical-sns.html')) snsLink.setAttribute('aria-current', 'page');

      const articleLink = Array.from(desktopNav.querySelectorAll('a')).find((link) =>
        /記事|コラム/.test(link.textContent || '') || (link.getAttribute('href') || '').includes('article.hdnjapan.com')
      );
      const cta = Array.from(desktopNav.querySelectorAll('a')).find((link) =>
        link.classList.contains('button') || /相談|Contact|Discuss|Book/.test(link.textContent || '')
      );
      desktopNav.insertBefore(snsLink, articleLink || cta || null);
    }

    if (mobileNavInner && !mobileNavInner.querySelector('a[href$="medical-sns.html"]')) {
      const snsMobileLink = document.createElement('a');
      snsMobileLink.href = snsHref;
      snsMobileLink.textContent = 'SNS・動画';
      if (currentPath.endsWith('/medical-sns.html')) snsMobileLink.setAttribute('aria-current', 'page');

      const articleLink = Array.from(mobileNavInner.querySelectorAll('a')).find((link) =>
        /記事/.test(link.textContent || '') || (link.getAttribute('href') || '').includes('article.hdnjapan.com')
      );
      mobileNavInner.insertBefore(snsMobileLink, articleLink || null);
    }
  }

  const switcher = document.querySelector('body > .language-switch, .language-switch');
  if (!switcher) return;

  if (desktopNav && !desktopNav.contains(switcher)) {
    const cta = Array.from(desktopNav.querySelectorAll('a')).find((link) =>
      link.classList.contains('button') || /相談|Contact|Discuss|Book/.test(link.textContent || '')
    );
    desktopNav.insertBefore(switcher, cta || null);
  }

  if (mobileNavInner && !mobileNavInner.querySelector('.mobile-language-switch')) {
    const mobileSwitcher = switcher.cloneNode(true);
    mobileSwitcher.classList.remove('language-switch');
    mobileSwitcher.classList.add('mobile-language-switch');
    mobileNavInner.appendChild(mobileSwitcher);
  }
})();
