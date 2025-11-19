// static/components/base_files/publish.js
document.addEventListener('click', (e) => {

  // --- ABRIR MODAL ---
  const btn = e.target.closest('.publish_btn');
  if (btn) {
    const modalBackdrop = document.querySelector('.modal-backdrop');
    if (modalBackdrop) {
      modalBackdrop.classList.add('visible');
      return;
    }

    // Se o modal não existe no DOM ainda
    const evt = new CustomEvent('openPublishModal', { bubbles: true });
    document.dispatchEvent(evt);
    return;
  }

  // --- FECHAR MODAL CLICANDO NO CANCELAR ---
  const cancelBtn = e.target.closest('.close_publish_modal');
  if (cancelBtn) {
    const modalBackdrop = document.querySelector('.modal-backdrop');
    if (modalBackdrop) {
      modalBackdrop.classList.remove('visible');
    }
    return;
  }

  // --- FECHAR MODAL CLICANDO FORA ---
  const modalBackdrop = document.querySelector('.modal-backdrop');
  if (modalBackdrop && modalBackdrop.classList.contains('visible')) {
    
    // Se clicou exatamente no backdrop (e não dentro do modal)
    if (e.target === modalBackdrop) {
      modalBackdrop.classList.remove('visible');
    }
  }
});
