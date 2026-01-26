document.addEventListener('click', (e) => {
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