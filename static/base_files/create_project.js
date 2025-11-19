// static/components/base_files/create_project.js
document.addEventListener('click', (e) => {
  
  const btn = e.target.closest('.create_project');
  if (!btn) return;

  const modalBackdrop = document.querySelector('#types-projects-modal');
  if (modalBackdrop) {
    modalBackdrop.classList.add('visible');
    return;
  }

  // Se modal ainda não está no DOM, dispara um evento global que o modal pode ouvir
  const evt = new CustomEvent('openCreateProjectModal', { bubbles: true });
  document.dispatchEvent(evt);
});
