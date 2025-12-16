document.addEventListener("DOMContentLoaded", () => {
    const inputNome = document.getElementById('inputNome');
    const inputProfessor = document.getElementById('inputProfessor');
    const inputMember = document.getElementById('inputMember');
    const btnAddMember = document.getElementById('btnAddMember');
    const membersListContainer = document.getElementById('membersList');
    const inputTag = document.getElementById('inputTag');
    const tagsListContainer = document.getElementById('tagsList');
    const inputGithub = document.getElementById('inputGithub');
    const inputYoutube = document.getElementById('inputYoutube');
    const uploadAreaBtn = document.getElementById('uploadAreaBtn');
    const cardTitle = document.getElementById('cardTitle');
    const cardAvatar = document.getElementById('cardAvatar');
    const cardDate = document.getElementById('cardDate');
    const metaProfessor = document.getElementById('metaProfessor');
    const textProfessor = document.getElementById('textProfessor');
    const cardMemberCount = document.getElementById('cardMemberCount');
    const cardTagsList = document.getElementById('cardTagsList');
    const metaDocs = document.getElementById('metaDocs');
    const textDocs = document.getElementById('textDocs');
    const cardGithub = document.getElementById('cardGithub');
    const cardYoutube = document.getElementById('cardYoutube');
    const cardDesc = document.getElementById('cardDesc');
    const inputDescricaoHidden = document.getElementById('inputDescricaoHidden');

    let members = [];
    let tags = [];

    if(cardDate) cardDate.innerText = new Date().toLocaleDateString('pt-BR');

    if (inputNome) {
        inputNome.addEventListener('input', (e) => {
            const val = e.target.value.trim();
            if (cardTitle) cardTitle.innerText = val || "Nome do projeto";
            if (cardAvatar) cardAvatar.innerText = val ? val.charAt(0).toUpperCase() : "P";
        });
    }

    if (inputProfessor) {
        inputProfessor.addEventListener('input', (e) => {
            const val = e.target.value.trim();
            if (metaProfessor && textProfessor) {
                if(val) { metaProfessor.style.display = 'flex'; textProfessor.innerText = val; }
                else { metaProfessor.style.display = 'none'; }
            }
        });
    }

    function renderMembers() {
        if (!membersListContainer || !cardMemberCount) return;
        membersListContainer.innerHTML = '';
        members.forEach((member, index) => {
            const chip = document.createElement('div');
            chip.className = 'chip-item';
            chip.innerHTML = `${member} <span class="btn-remove-chip" onclick="removeMember(${index})">×</span>`;
            membersListContainer.appendChild(chip);
        });
        const count = members.length;
        cardMemberCount.innerText = count === 0 ? "Integrantes: 0" : count === 1 ? "1 Integrante" : `${count} Integrantes`;
    }

    function addMember() {
        if (!inputMember) return;
        const name = inputMember.value.trim();
        if(name) { members.push(name); inputMember.value = ''; renderMembers(); }
    }

    if (btnAddMember) { btnAddMember.addEventListener('click', (e) => { e.preventDefault(); addMember(); }); }
    if (inputMember) { inputMember.addEventListener('keypress', (e) => { if(e.key === 'Enter') { e.preventDefault(); addMember(); } }); }
    window.removeMember = function(index) { members.splice(index, 1); renderMembers(); }

    function renderTags() {
        if (!tagsListContainer || !cardTagsList) return;
        tagsListContainer.innerHTML = '';
        tags.forEach((tag, index) => {
            const chip = document.createElement('div');
            chip.className = 'chip-item';
            chip.innerHTML = `${tag} <span class="btn-remove-chip" onclick="removeTag(${index})">×</span>`;
            tagsListContainer.appendChild(chip);
        });
        cardTagsList.innerHTML = '';
        tags.forEach(tag => {
            const span = document.createElement('span');
            span.className = 'card-tag';
            span.innerText = tag;
            cardTagsList.appendChild(span);
        });
    }

    function addTag(text) {
        if (!inputTag) return;
        const cleanTag = text.replace('+', '').trim();
        if(cleanTag && !tags.includes(cleanTag)) { tags.push(cleanTag); renderTags(); }
        inputTag.value = '';
    }

    if (inputTag) { inputTag.addEventListener('keydown', (e) => { if(e.key === 'Enter') { e.preventDefault(); addTag(inputTag.value); } }); }

    const sugestoes = document.querySelectorAll('.tag-badge');
    sugestoes.forEach(badge => { badge.addEventListener('click', function() { addTag(this.innerText); }); });
    window.removeTag = function(index) { tags.splice(index, 1); renderTags(); }

    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.multiple = true;
    fileInput.style.display = 'none';
    document.body.appendChild(fileInput);
    if (uploadAreaBtn) { uploadAreaBtn.addEventListener('click', (e) => { e.preventDefault(); fileInput.click(); }); }
    fileInput.addEventListener('change', function() {
        const count = this.files.length;
        if (metaDocs && textDocs) {
            if(count > 0) { metaDocs.style.display = 'flex'; textDocs.innerText = `${count} Documento(s)`; }
            else { metaDocs.style.display = 'none'; }
        }
    });

    if (inputGithub) {
        inputGithub.addEventListener('input', (e) => {
            const url = e.target.value.trim();
            if (cardGithub) { cardGithub.style.display = url.length > 0 ? 'flex' : 'none'; if (url.length > 0) cardGithub.href = url; }
        });
    }

    if (inputYoutube) {
        inputYoutube.addEventListener('input', (e) => {
            const url = e.target.value.trim();
            if (cardYoutube) { cardYoutube.style.display = url.length > 0 ? 'flex' : 'none'; if (url.length > 0) cardYoutube.href = url; }
        });
    }

    const editorElement = document.getElementById('editor-container');
    if (editorElement) {
        var toolbarOptions = [ ['bold', 'italic', 'underline', 'strike'], ['blockquote', 'code-block'], [{ 'list': 'ordered'}] ];
        var quill = new Quill('#editor-container', { modules: { toolbar: toolbarOptions }, theme: 'snow', placeholder: 'Escreva a descrição detalhada do projeto...' });
        quill.on('text-change', function() {
            if (inputDescricaoHidden) inputDescricaoHidden.value = quill.root.innerHTML;
            if (cardDesc) {
                var textoPuro = quill.getText().trim();
                cardDesc.innerText = textoPuro.length > 0 ? textoPuro.substring(0, 150) + (textoPuro.length > 150 ? "..." : "") : "Nenhuma descrição adicionada ainda...";
            }
        });
    }
});