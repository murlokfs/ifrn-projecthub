// static/components/base_files/create_project.js
document.addEventListener('click', (e) => {
  const btn = e.target.closest('.create_project');
  if (!btn) return;
  const modalBackdrop = document.querySelector('#types-projects-modal');
  if (modalBackdrop) {
    modalBackdrop.classList.add('visible');
    return;
  }
  const evt = new CustomEvent('openCreateProjectModal', { bubbles: true });
  document.dispatchEvent(evt);
});