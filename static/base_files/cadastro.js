document.addEventListener("DOMContentLoaded", () => {
    
    // --- ELEMENTOS ---
    const inputNome = document.getElementById('inputNome');
    const inputProfessor = document.getElementById('inputProfessor');
    
    // Integrantes
    const inputMember = document.getElementById('inputMember');
    const btnAddMember = document.getElementById('btnAddMember');
    const membersListContainer = document.getElementById('membersList'); // Div no form
    const cardMemberCount = document.getElementById('cardMemberCount'); // Texto no card

    // Tags
    const inputTag = document.getElementById('inputTag');
    const tagsListContainer = document.getElementById('tagsList'); // Div no form
    const cardTagsList = document.getElementById('cardTagsList'); // Div no card

    // Preview
    const cardTitle = document.getElementById('cardTitle');
    const cardAvatar = document.getElementById('cardAvatar');
    const cardDate = document.getElementById('cardDate');
    const metaProfessor = document.getElementById('metaProfessor');
    const textProfessor = document.getElementById('textProfessor');

    // --- ESTADO (ARRAYS) ---
    let members = [];
    let tags = [];

    // Data Atual
    cardDate.innerText = new Date().toLocaleDateString('pt-BR');

    // =====================================================
    // 1. LÓGICA DE NOME E PROFESSOR
    // =====================================================
    inputNome.addEventListener('input', (e) => {
        const val = e.target.value.trim();
        cardTitle.innerText = val || "Nome do projeto";
        cardAvatar.innerText = val ? val.charAt(0).toUpperCase() : "P";
    });

    inputProfessor.addEventListener('input', (e) => {
        const val = e.target.value.trim();
        if(val) {
            metaProfessor.style.display = 'flex';
            textProfessor.innerText = val;
        } else {
            metaProfessor.style.display = 'none';
        }
    });

    // =====================================================
    // 2. LÓGICA DE INTEGRANTES (ADD / REMOVE)
    // =====================================================
    
    function renderMembers() {
        // Limpa a lista visual no formulário
        membersListContainer.innerHTML = '';
        
        // Recria os chips
        members.forEach((member, index) => {
            const chip = document.createElement('div');
            chip.className = 'chip-item';
            chip.innerHTML = `
                ${member}
                <span class="btn-remove-chip" onclick="removeMember(${index})">×</span>
            `;
            membersListContainer.appendChild(chip);
        });

        // Atualiza o contador no Card
        const count = members.length;
        if(count === 0) cardMemberCount.innerText = "Integrantes: 0";
        else if(count === 1) cardMemberCount.innerText = "1 Integrante";
        else cardMemberCount.innerText = `${count} Integrantes`;
    }

    // Adicionar Integrante
    function addMember() {
        const name = inputMember.value.trim();
        if(name) {
            members.push(name);
            inputMember.value = ''; // Limpa input
            renderMembers();
        }
    }

    // Botão "+" click
    if(btnAddMember){
        btnAddMember.addEventListener('click', (e) => {
            e.preventDefault(); // Evita submit do form
            addMember();
        });
    }
    
    // Enter no input
    inputMember.addEventListener('keypress', (e) => {
        if(e.key === 'Enter') {
            e.preventDefault();
            addMember();
        }
    });

    // Função global para remover (acessível pelo onclick do HTML string)
    window.removeMember = function(index) {
        members.splice(index, 1); // Remove do array
        renderMembers(); // Atualiza tela
    }


    // =====================================================
    // 3. LÓGICA DE TAGS (ADD / REMOVE)
    // =====================================================

    function renderTags() {
        // 1. Renderiza no FORMULÁRIO (com botão X)
        tagsListContainer.innerHTML = '';
        tags.forEach((tag, index) => {
            const chip = document.createElement('div');
            chip.className = 'chip-item';
            chip.innerHTML = `
                ${tag}
                <span class="btn-remove-chip" onclick="removeTag(${index})">×</span>
            `;
            tagsListContainer.appendChild(chip);
        });

        // 2. Renderiza no CARD (Apenas visual, sem X)
        cardTagsList.innerHTML = '';
        tags.forEach(tag => {
            const span = document.createElement('span');
            span.className = 'card-tag'; // Classe visual do card
            span.innerText = tag;
            cardTagsList.appendChild(span);
        });
    }

    function addTag(text) {
        const cleanTag = text.replace('+', '').trim(); // Remove + se vier da sugestão
        // Evita duplicados e vazios
        if(cleanTag && !tags.includes(cleanTag)) {
            tags.push(cleanTag);
            renderTags();
        }
        inputTag.value = '';
    }

    // Enter no input
    inputTag.addEventListener('keypress', (e) => {
        if(e.key === 'Enter') {
            e.preventDefault();
            addTag(inputTag.value);
        }
    });

    // Clicar nas Sugestões (+ ADS, etc)
    const sugestoes = document.querySelectorAll('.tag-badge');
    sugestoes.forEach(badge => {
        badge.addEventListener('click', function() {
            addTag(this.innerText);
        });
    });

    // Remover Tag
    window.removeTag = function(index) {
        tags.splice(index, 1);
        renderTags();
    }
    
    // =====================================================
    // 4. ARQUIVOS
    // =====================================================
    const uploadAreaBtn = document.querySelector('.btn-select-files');
    const metaDocs = document.getElementById('metaDocs');
    const textDocs = document.getElementById('textDocs');
    
    // Input invisível
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.multiple = true;
    fileInput.style.display = 'none';
    document.body.appendChild(fileInput);

    if(uploadAreaBtn){
        uploadAreaBtn.addEventListener('click', (e) => {
            e.preventDefault();
            fileInput.click();
        });
    }

    fileInput.addEventListener('change', function() {
        const count = this.files.length;
        if(count > 0) {
            metaDocs.style.display = 'flex';
            textDocs.innerText = `${count} Documento(s)`;
        } else {
            metaDocs.style.display = 'none';
        }
    });

    // ... (código anterior)

    // --- 6. LINK GITHUB ---
    const inputGithub = document.getElementById('inputGithub'); // Certifique-se que o input tem esse ID
    const cardGithub = document.getElementById('cardGithub');

    if(inputGithub){
        inputGithub.addEventListener('input', (e) => {
            const url = e.target.value.trim();
            if (url.length > 0) {
                cardGithub.style.display = 'flex'; // Mostra
                cardGithub.href = url; // Atualiza o link
            } else {
                cardGithub.style.display = 'none'; // Esconde
            }
        });
    }

    // --- 7. LINK YOUTUBE ---
    const inputYoutube = document.getElementById('inputYoutube'); // Certifique-se que o input tem esse ID
    const cardYoutube = document.getElementById('cardYoutube');

    if(inputYoutube){
        inputYoutube.addEventListener('input', (e) => {
            const url = e.target.value.trim();
            if (url.length > 0) {
                cardYoutube.style.display = 'flex'; // Mostra
                cardYoutube.href = url; // Atualiza o link
            } else {
                cardYoutube.style.display = 'none'; // Esconde
            }
        });
    }

});

