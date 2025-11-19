
document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('.header');
  const searchContainer = document.getElementById('search_container');
  const searchInput = document.getElementById('search_input');

  if (!header || !searchContainer || !searchInput) return;

  const mq = window.matchMedia('(max-width: 500px)');

  function isMobileSearchMode() {
    return mq.matches;
  }

  function openSearch() {
    if (!isMobileSearchMode()) return;
    if (!header.classList.contains('search-open')) {
      header.classList.add('search-open');
      // foca após pintar a classe
      setTimeout(() => searchInput.focus(), 0);
    }
  }

  function closeSearch({ returnFocus = false } = {}) {
    if (header.classList.contains('search-open')) {
      header.classList.remove('search-open');
      searchInput.blur();
      if (returnFocus) {
        // devolve foco ao container para acessibilidade
        searchContainer.focus?.();
      }
    }
  }

  // Clique no container abre a busca (apenas no mobile)
  searchContainer.addEventListener('click', (e) => {
    if (!isMobileSearchMode()) return;
    // se já está aberto, não precisa reprocessar
    if (!header.classList.contains('search-open')) {
      openSearch();
      e.stopPropagation();
    }
  });

  // Clique fora fecha
  document.addEventListener('click', (e) => {
    if (!isMobileSearchMode()) return;
    if (!header.classList.contains('search-open')) return;

    const clickedInside = searchContainer.contains(e.target) || searchInput.contains(e.target);
    if (!clickedInside) {
      closeSearch();
    }
  });

  // ESC fecha
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeSearch({ returnFocus: true });
    }
  });

  // Ao redimensionar para fora do mobile, garante estado consistente
  function handleResize() {
    if (!isMobileSearchMode()) {
      closeSearch();
    }
  }

  mq.addEventListener?.('change', handleResize);
  window.addEventListener('resize', handleResize);
});
