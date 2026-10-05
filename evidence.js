(() => {
  const dialog = document.querySelector('#evidence-viewer');
  if (!dialog || !dialog.showModal) return;
  const image = dialog.querySelector('img');
  const title = dialog.querySelector('#viewer-title');
  const original = dialog.querySelector('.viewer-link');
  const controls = dialog.querySelector('.viewer-controls');
  const count = dialog.querySelector('.viewer-count');
  count.setAttribute('role', 'status');
  count.setAttribute('aria-live', 'polite');
  let opener;
  let items = [];
  let current = 0;
  const showItem = index => {
    current = (index + items.length) % items.length;
    const item = items[current];
    image.src = item.src;
    image.alt = item.title;
    image.classList.toggle('badge-crop', item.src.includes('ai4-speaker-badge.jpeg'));
    title.textContent = item.title;
    original.href = item.href;
    count.textContent = `${current + 1} / ${items.length}`;
  };
  document.querySelectorAll('[data-preview]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      opener = link;
      items = link.dataset.gallery ? JSON.parse(link.dataset.gallery) : [{src: link.querySelector('img').src, href: link.href, title: link.dataset.preview}];
      controls.hidden = items.length < 2;
      showItem(0);
      dialog.showModal();
    });
  });
  dialog.querySelector('.previous').addEventListener('click', () => showItem(current - 1));
  dialog.querySelector('.next').addEventListener('click', () => showItem(current + 1));
  dialog.addEventListener('keydown', event => {
    if (items.length < 2 || !['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
    event.preventDefault();
    showItem(current + (event.key === 'ArrowLeft' ? -1 : 1));
  });
  dialog.querySelector('.close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target === dialog) {
      const rect = dialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
    }
  });
  dialog.addEventListener('close', () => opener?.focus());
})();
