// Lógica de abertura/fechamento da sidebar e tema escuro
document.addEventListener('DOMContentLoaded', () => {
	const sidebar = document.getElementById('sidebar');
	const openBtn = document.getElementById('open_btn');
	const themeToggle = document.getElementById('themeToggle');
	const body = document.body;
	const moonIcon = document.getElementById('moonIcon');
	const sunIcon = document.getElementById('sunIcon');

	if (openBtn) {
		openBtn.addEventListener('click', () => {
			sidebar.classList.toggle('open-sidebar');
		});
	}

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
