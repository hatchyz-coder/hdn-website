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

  const isJapanese = (document.documentElement.lang || '').toLowerCase().startsWith('ja');
  const currentPath = window.location.pathname;

  // Keep consultation traffic on the HDN domain. Legacy Google Form CTAs are
  // progressively rewritten here so pages do not need to be migrated all at once.
  if (isJapanese) {
    document.querySelectorAll('a[href*="forms.gle/"]').forEach((link) => {
      const text = (link.textContent || '').trim();
      if (!/相談|診断|問い合わせ|問合せ|Contact|Discuss|Book/i.test(text) && !link.classList.contains('button')) return;
      link.href = '/consultation-form.html';
      link.removeAttribute('target');
      link.removeAttribute('rel');
      link.dataset.hdnConsultationCta = 'custom-form';
    });
  }

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
