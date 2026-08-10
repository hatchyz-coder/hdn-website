(() => {
  const isJapanese = (document.documentElement.lang || '').toLowerCase().startsWith('ja');
  const currentPath = window.location.pathname;

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
