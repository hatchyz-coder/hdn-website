(() => {
  const switcher = document.querySelector('body > .language-switch, .language-switch');
  if (!switcher) return;

  const desktopNav = document.querySelector('.site-header .nav, .header .nav, .nav');
  if (desktopNav && !desktopNav.contains(switcher)) {
    const cta = Array.from(desktopNav.querySelectorAll('a')).find((link) =>
      link.classList.contains('button') || /相談|Contact|Discuss|Book/.test(link.textContent || '')
    );
    desktopNav.insertBefore(switcher, cta || null);
  }

  const mobileNavInner = document.querySelector('.mobile-nav-inner');
  if (mobileNavInner && !mobileNavInner.querySelector('.mobile-language-switch')) {
    const mobileSwitcher = switcher.cloneNode(true);
    mobileSwitcher.classList.remove('language-switch');
    mobileSwitcher.classList.add('mobile-language-switch');
    mobileNavInner.appendChild(mobileSwitcher);
  }
})();
