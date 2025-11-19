// Lógica de abertura/fechamento da sidebar e tema escuro
document.addEventListener('DOMContentLoaded', () => {
	const sidebar = document.getElementById('sidebar');
	const openBtn = document.getElementById('open_btn');
	const menuToggle = document.querySelector('.menu-toggle');
	const themeToggle = document.getElementById('themeToggle');
	const body = document.body;
	const moonIcon = document.getElementById('moonIcon');
	const sunIcon = document.getElementById('sunIcon');

	if (openBtn) {
		openBtn.addEventListener('click', () => {
			sidebar.classList.toggle('open-sidebar');
		});
	}

	// Botão do header abre/fecha a sidebar no mobile
	if (menuToggle && sidebar) {
		menuToggle.addEventListener('click', () => {
			const opened = sidebar.classList.toggle('mobile-open');
			body.classList.toggle('no-scroll', opened);
			// Garante que o conteúdo da sidebar venha expandido
			if (opened) {
				sidebar.classList.add('open-sidebar');
				// Move foco para a sidebar ao abrir
				setTimeout(() => sidebar.focus(), 0);
			}
			// Acessibilidade
			menuToggle.setAttribute('aria-expanded', opened ? 'true' : 'false');
		});

		// ESC fecha
		document.addEventListener('keydown', (e) => {
			if (e.key === 'Escape' && sidebar.classList.contains('mobile-open')) {
				sidebar.classList.remove('mobile-open');
				body.classList.remove('no-scroll');
				menuToggle.setAttribute('aria-expanded', 'false');
				// Retorna foco para o botão
				menuToggle.focus();
			}
		});

		// Clique fora fecha
		document.addEventListener('click', (e) => {
			if (sidebar.classList.contains('mobile-open')) {
				const clickInsideSidebar = sidebar.contains(e.target);
				const clickOnToggle = menuToggle.contains(e.target);
				if (!clickInsideSidebar && !clickOnToggle) {
					sidebar.classList.remove('mobile-open');
					body.classList.remove('no-scroll');
					menuToggle.setAttribute('aria-expanded', 'false');
					// Retorna foco para o botão
					menuToggle.focus();
				}
			}
		});
	}

	window.addEventListener('resize', () => {
		if (window.innerWidth > 695 && sidebar.classList.contains('mobile-open')) {
			sidebar.classList.remove('mobile-open');
			body.classList.remove('no-scroll');
		}
	});

	function initializeTheme() {
		try {
			const savedTheme = localStorage.getItem('theme');
			const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
			if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
				body.classList.add('dark-mode');
				moonIcon?.classList.add('active');
				moonIcon?.classList.remove('inactive');
				sunIcon?.classList.remove('active');
				sunIcon?.classList.add('inactive');
			}
		} catch (e) {
			console.warn('Falha ao acessar localStorage para tema', e);
		}
	}

	themeToggle?.addEventListener('click', () => {
		body.classList.toggle('dark-mode');
		themeToggle.classList.add('active');

		moonIcon?.classList.toggle('active');
		moonIcon?.classList.toggle('inactive');
		sunIcon?.classList.toggle('active');
		sunIcon?.classList.toggle('inactive');

		const pressed = body.classList.contains('dark-mode');
		themeToggle.setAttribute('aria-pressed', pressed ? 'true' : 'false');
		try {
			localStorage.setItem('theme', pressed ? 'dark' : 'light');
		} catch (e) {
			console.warn('Falha ao salvar tema', e);
		}
		setTimeout(() => themeToggle.classList.remove('active'), 600);
	});

	initializeTheme();
});
