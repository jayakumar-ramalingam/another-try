(() => {
  const dialog = document.querySelector('#evidence-viewer');
  if (!dialog || !dialog.showModal) return;
  const image = dialog.querySelector('img');
  const title = dialog.querySelector('#viewer-title');
  const original = dialog.querySelector('.viewer-link');
  let opener;
  document.querySelectorAll('[data-preview]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      opener = link;
      image.src = link.querySelector('img').src;
      image.alt = link.querySelector('img').alt;
      title.textContent = link.dataset.preview;
      original.href = link.href;
      dialog.showModal();
    });
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
