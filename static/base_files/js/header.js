document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('.header');
  const searchContainer = document.getElementById('search_container');
  const searchInput = document.getElementById('search_input');
  if (!header || !searchContainer || !searchInput) return;
  const mq = window.matchMedia('(max-width: 500px)');
  function isMobileSearchMode() { return mq.matches; }
  function openSearch() {
    if (!isMobileSearchMode()) return;
    if (!header.classList.contains('search-open')) {
      header.classList.add('search-open');
      setTimeout(() => searchInput.focus(), 0);
    }
  }
  function closeSearch({ returnFocus = false } = {}) {
    if (header.classList.contains('search-open')) {
      header.classList.remove('search-open');
      searchInput.blur();
      if (returnFocus) { searchContainer.focus?.(); }
    }
  }
  searchContainer.addEventListener('click', (e) => {
    if (!isMobileSearchMode()) return;
    if (!header.classList.contains('search-open')) { openSearch(); e.stopPropagation(); }
  });
  document.addEventListener('click', (e) => {
    if (!isMobileSearchMode()) return;
    if (!header.classList.contains('search-open')) return;
    const clickedInside = searchContainer.contains(e.target) || searchInput.contains(e.target);
    if (!clickedInside) { closeSearch(); }
  });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') { closeSearch({ returnFocus: true }); } });
  function handleResize() { if (!isMobileSearchMode()) { closeSearch(); } }
  mq.addEventListener?.('change', handleResize);
  window.addEventListener('resize', handleResize);
});