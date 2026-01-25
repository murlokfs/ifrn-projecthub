document.addEventListener("DOMContentLoaded", () => {
    // --- Elementos de UI ---
    const inputNome = document.getElementsByName('title')[0];
    const inputGithub = document.getElementsByName('link_github')[0];
    const inputYoutube = document.querySelector('input[name="link_youtube"]');
    const publishBtn = document.querySelector('.publish_btn.green');
    const projectForm = document.querySelector('form');
    
    // --- Elementos de Preview (Cards) ---
    const cardTitle = document.getElementById('cardTitle');
    const cardAvatar = document.getElementById('cardAvatar');
    const cardMemberCount = document.getElementById('cardMemberCount');
    const cardGithub = document.getElementById('cardGithub');
    const cardYoutube = document.getElementById('cardYoutube');

    // --- Elementos do Player YouTube ---
    const videoContainer = document.getElementById('video-preview-container');
    const iframe = document.getElementById('youtube-player');
    const bannerInput = document.querySelector('input[type="file"][name="banner"]');
    
    // --- Elementos de Preview ---
    const bannerPreviewContainer = document.getElementById('banner-preview-container');
    const bannerPreviewImg = document.getElementById('banner-preview-img');

    const userData = document.getElementById('user-data');
    if (userData) {
        const userId = userData.dataset.id;
        const userName = userData.dataset.name;
        const hiddenSelect = document.getElementById('id_members');
        const container = document.getElementById('membersList');

        if (userId && userName && hiddenSelect && container) {
            // Adiciona ao select para o POST
            if (![...hiddenSelect.options].some(opt => opt.value == userId)) {
                hiddenSelect.add(new Option(userName, userId, true, true));
            }
            // Adiciona chip visual (sem botão de remover para o dono)
            const chip = document.createElement('div');
            chip.className = 'chip-item owner-chip';
            chip.dataset.id = userId;
            chip.innerHTML = `${userName} (Você)`;
            container.appendChild(chip);
            updatePreviews();
        }
    }    

    if (bannerInput) {
        bannerInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    bannerPreviewImg.src = e.target.result;
                    bannerPreviewContainer.style.display = 'block';
                    // Sincroniza com o card de preview lateral se o elemento existir
                    const cardBanner = document.getElementById('cardBanner');
                    if (cardBanner) cardBanner.src = e.target.result;
                }
                reader.readAsDataURL(file);
            } else {
                bannerPreviewContainer.style.display = 'none';
            }
        });
    }

    let currentType = '';

    // 1. Submissão pelo Botão do Header
    if (publishBtn && projectForm) {
        publishBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (projectForm.reportValidity()) projectForm.submit();
        });
    }

    

    // 2. Sincronização de Inputs e Preview do Card
    if (inputNome) {
        inputNome.addEventListener('input', (e) => {
            const val = e.target.value.trim();
            if (cardTitle) cardTitle.innerText = val || "Nome do projeto";
            if (cardAvatar) cardAvatar.innerText = val ? val.charAt(0).toUpperCase() : "P";
        });
    }

    if (inputGithub) {
        inputGithub.addEventListener('input', (e) => {
            const url = e.target.value.trim();
            if (cardGithub) {
                cardGithub.style.display = url.length > 0 ? 'flex' : 'none';
                if (url.length > 0) cardGithub.href = url;
            }
        });
    }

    // 3. Lógica do Player de Vídeo (Fim do Erro 153)
    function updateYoutubePlayer(url) {
    const videoContainer = document.getElementById('video-preview-container');
    
    if (!url || url.trim() === "") {
        if (videoContainer) {
            videoContainer.style.display = 'none';
            videoContainer.innerHTML = ''; // Limpa o iframe completamente
        }
        if (cardYoutube) cardYoutube.style.display = 'none';
        return;
    }

    let videoId = "";
    try {
        // Extração do ID via URLSearchParams (mais seguro que Regex)
        if (url.includes("watch?v=")) {
            videoId = new URL(url).searchParams.get("v");
        } else if (url.includes("youtu.be/")) {
            videoId = url.split("youtu.be/")[1]?.split(/[?#]/)[0];
        } else if (url.includes("embed/")) {
            videoId = url.split("embed/")[1]?.split(/[?#]/)[0];
        }

        if (videoId && videoId.length === 11) {
            const embedUrl = `https://www.youtube.com/embed/${videoId}?rel=0&showinfo=0&autoplay=0`;
            
            // RECONSTRUÇÃO DO IFRAME: Evita o erro de configuração (153)
            videoContainer.innerHTML = `
                <iframe 
                    id="youtube-player" 
                    width="100%" 
                    height="315" 
                    src="${embedUrl}" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                    referrerpolicy="strict-origin-when-cross-origin"
                    allowfullscreen
                    style="border-radius: 12px; border: 1px solid #e2e8f0;">
                </iframe>`;
            
            videoContainer.style.display = 'block';
            
            if (cardYoutube) {
                cardYoutube.style.display = 'flex';
                cardYoutube.href = url;
            }
        } else {
            videoContainer.style.display = 'none';
            videoContainer.innerHTML = '';
        }
    } catch (err) {
        console.error("Erro ao carregar vídeo:", err);
    }
}

    if (inputYoutube) {
        // Executa ao carregar (para edições)
        updateYoutubePlayer(inputYoutube.value.trim());
        // Executa ao digitar
        inputYoutube.addEventListener('input', (e) => updateYoutubePlayer(e.target.value.trim()));
    }

    // 4. Lógica do Modal de Busca (Professores, Membros, Tags)
    window.openModal = function(type) {
        currentType = type;
        const modal = document.getElementById('searchModal');
        const title = document.getElementById('modalTitle');
        const resultsContainer = document.getElementById('modalResults');
        const searchInput = document.getElementById('modalSearchInput');

        if (searchInput) searchInput.value = '';
        if (resultsContainer) resultsContainer.innerHTML = '<p class="helper-text">Digite para buscar...</p>';
        
        const titles = {
            'professor': 'Selecionar Professor Orientador',
            'member': 'Convidar Integrantes',
            'tag': 'Adicionar Tags'
        };
        if (title) title.innerText = titles[type];
        if (modal) modal.style.display = 'flex';
        if (searchInput) searchInput.focus();
    };

    window.closeModal = function() {
        const modal = document.getElementById('searchModal');
        if (modal) modal.style.display = 'none';
    };

    let debounceTimer;
    window.debounceSearch = function() {
        clearTimeout(debounceTimer);
        const searchInput = document.getElementById('modalSearchInput');
        if (!searchInput || searchInput.value.length < 2) return;

        debounceTimer = setTimeout(async () => {
            try {
                const response = await fetch(`/api/search-entities/?type=${currentType}&q=${searchInput.value}`);
                const data = await response.json();
                renderModalResults(data);
            } catch (error) { console.error("Erro na busca:", error); }
        }, 300);
    };

    // 5. Renderização e Seleção (Siglas e Cards)
    function renderModalResults(data) {
    const container = document.getElementById('modalResults');
    if (!container) return;

    if (data.length === 0) {
        container.innerHTML = '<p class="helper-text" style="text-align:center; padding:20px;">Nenhum resultado encontrado.</p>';
        return;
    }

    const selectId = currentType === 'tag' ? 'id_tags' : (currentType === 'professor' ? 'id_orientators' : 'id_members');
    const hiddenSelect = document.getElementById(selectId);

    if (currentType === 'tag') {
        container.innerHTML = `
            <div class="modal-section-title">Tags disponíveis</div>
            <div class="tags-cloud-container">
                ${data.map(item => {
                    const isSelected = hiddenSelect ? [...hiddenSelect.options].some(opt => opt.value == item.id) : false;
                    return `<div class="tag-badge-item ${isSelected ? 'selected' : ''}" onclick="selectItem('${item.id}', '${item.name}')">${item.name}</div>`;
                }).join('')}
            </div>`;
    } else {
        const isProf = currentType === 'professor';
        const bg = isProf ? '#E0F2FE' : '#DCFCE7';
        const textColor = isProf ? '#0369A1' : '#15803D';
        
        container.innerHTML = data.map(item => {
            const sigla = item.name.split(' ').filter(n => n.length > 2).map(n => n[0]).join('').substring(0, 2).toUpperCase();
            const isSelected = hiddenSelect ? [...hiddenSelect.options].some(opt => opt.value == item.id) : false;

            return `
                <div class="user-result-card ${isSelected ? 'selected' : ''}" onclick="selectItem('${item.id}', '${item.name}')">
                    <div class="avatar-sigla" style="background: ${bg}; color: ${textColor}">${sigla || '??'}</div>
                    <div class="user-info-text">
                        <strong>${item.name}</strong>
                        <small>${item.info || 'IFPE • Campus Recife'}</small> 
                    </div>
                    <div class="btn-add-circle ${isSelected ? 'is-selected' : ''}">${isSelected ? '✓' : '+'}</div>
                </div>`;
        }).join('');
    }

}

    window.selectItem = function(id, name) {
        const selectId = currentType === 'tag' ? 'id_tags' : (currentType === 'professor' ? 'id_orientators' : 'id_members');
        const hiddenSelect = document.getElementById(selectId);
        if (!hiddenSelect) return;

        if (![...hiddenSelect.options].some(opt => opt.value == id)) {
            hiddenSelect.add(new Option(name, id, true, true));
            addChipToUI(currentType, id, name);
        } else {
            for (let i = 0; i < hiddenSelect.options.length; i++) {
                if (hiddenSelect.options[i].value == id) { hiddenSelect.remove(i); break; }
            }
            const containerId = currentType === 'tag' ? 'tagsList' : (currentType === 'professor' ? 'orientatorsList' : 'membersList');
            document.querySelectorAll(`#${containerId} .chip-item`).forEach(chip => {
                if (chip.dataset.id == id) chip.remove();
            });
        }
        updatePreviews();
        debounceSearch(); 
    };

    function addChipToUI(type, id, name) {
        const listId = type === 'tag' ? 'tagsList' : (type === 'professor' ? 'orientatorsList' : 'membersList');
        const container = document.getElementById(listId);
        if (!container) return;

        const chip = document.createElement('div');
        chip.className = 'chip-item';
        chip.dataset.id = id;
        chip.innerHTML = `${name} <span class="remove-chip" onclick="removeItem('${type}', '${id}', this)">×</span>`;
        container.appendChild(chip);
    }

    window.removeItem = function(type, id, element) {
        const selectId = type === 'tag' ? 'id_tags' : (currentType === 'professor' ? 'id_orientators' : 'id_members');
        const hiddenSelect = document.getElementById(selectId);
        if (hiddenSelect) {
            for (let i = 0; i < hiddenSelect.options.length; i++) {
                if (hiddenSelect.options[i].value == id) { hiddenSelect.remove(i); break; }
            }
        }
        if (element && element.closest('.chip-item')) element.closest('.chip-item').remove();
        updatePreviews();
    };

    function updatePreviews() {
        const membersSelect = document.getElementById('id_members');
        if (cardMemberCount && membersSelect) {
            const count = membersSelect.options.length;
            cardMemberCount.innerText = count === 0 ? "Integrantes: 0" : (count === 1 ? "1 Integrante" : `${count} Integrantes`);
        }
        const cardTagsList = document.getElementById('cardTagsList');
        const tagsSelect = document.getElementById('id_tags');
        if (cardTagsList && tagsSelect) {
            cardTagsList.innerHTML = [...tagsSelect.options].map(opt => `<span class="card-tag">${opt.text}</span>`).join('');
        }
    }
});

document.addEventListener("DOMContentLoaded", () => {
    // Adicione este bloco dentro do seu primeiro DOMContentLoaded ou substitua o segundo bloco por este:
const visibilityToggle = document.getElementById('id_is_private');
const statusText = document.getElementById('visibilityStatusText');
const helperText = document.getElementById('visibilityHelperText');

if (visibilityToggle && statusText && helperText) {
    visibilityToggle.addEventListener('change', function() {
        if (this.checked) {
            // Estado: PRIVADO (Marcado)
            statusText.innerText = 'Privado';
            helperText.innerText = 'Apenas membros autorizados';
            // Opcional: Adicionar classe para mudar a cor do texto se desejar
            statusText.style.color = '#374151'; 
        } else {
            // Estado: PÚBLICO (Desmarcado)
            statusText.innerText = 'Público';
            helperText.innerText = 'Visível para todos os usuários';
            // Opcional: Cor de destaque para o modo público
            statusText.style.color = '#16a34a'; 
        }
    });
}
});

window.confirmSelection = function() { closeModal(); };