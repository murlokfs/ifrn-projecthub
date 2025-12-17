document.addEventListener('click', (e) => {
  const btn = e.target.closest('.publish_btn');
  if (btn) {
    const modalBackdrop = document.querySelector('.modal-backdrop');
    if (modalBackdrop) { modalBackdrop.classList.add('visible'); return; }
    const evt = new CustomEvent('openPublishModal', { bubbles: true });
    document.dispatchEvent(evt);
    return;
  }
  const cancelBtn = e.target.closest('.close_publish_modal');
  if (cancelBtn) {
    const modalBackdrop = document.querySelector('.modal-backdrop');
    if (modalBackdrop) { modalBackdrop.classList.remove('visible'); }
    return;
  }
  const modalBackdrop = document.querySelector('.modal-backdrop');
  if (modalBackdrop && modalBackdrop.classList.contains('visible')) {
    if (e.target === modalBackdrop) { modalBackdrop.classList.remove('visible'); }
  }
});