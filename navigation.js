(() => {
  const header = document.querySelector('.header');
  if (!header) return;
  const updateHeight = () => {
    document.documentElement.style.setProperty('--header-height', `${header.offsetHeight}px`);
  };
  updateHeight();
  if ('ResizeObserver' in window) new ResizeObserver(updateHeight).observe(header);
  else window.addEventListener('resize', updateHeight);

  const links = [...document.querySelectorAll('.page-index a')];
  const sections = links.map(link => document.getElementById(link.hash.slice(1)));
  if (!links.length) return;
  let pending = false;
  const updateSection = () => {
    const scrollPadding = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 0;
    const offset = Math.max(header.offsetHeight + document.querySelector('.page-index').offsetHeight + 24, scrollPadding + 2);
    let active = 0;
    sections.forEach((section, index) => {
      if (section && section.getBoundingClientRect().top <= offset) active = index;
    });
    links.forEach((link, index) => {
      if (index === active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    pending = false;
  };
  window.addEventListener('scroll', () => {
    if (!pending) { pending = true; requestAnimationFrame(updateSection); }
  }, {passive: true});
  window.addEventListener('resize', updateSection);
  updateSection();
})();
