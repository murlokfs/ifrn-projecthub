# IFRN PRISMA 🚀

O **IFRN PRISMA** é um sistema web desenvolvido para o gerenciamento e divulgação de projetos acadêmicos. Ele centraliza o cadastro e a visualização de iniciativas profissionais e estudantis, contando com autenticação institucional e uma arquitetura preparada para escalabilidade.

---

## 📌 Descrição

O objetivo central do projeto é facilitar a gestão de projetos dentro do ecossistema do IFRN. A plataforma oferece:
* **Autenticação Integrada:** Login via SUAP (Sistema Unificado de Administração Pública).
* **Processamento Assíncrono:** Uso de filas para tarefas pesadas, garantindo performance.
* **Gestão de Conteúdo:** Interface amigável para cadastro de projetos com suporte a Rich Text.

---

## 🛠️ Tecnologias Utilizadas

O projeto utiliza o que há de mais moderno no ecossistema Python/Django:

* **[Python](https://www.python.org/):** Linguagem base.
* **[Django](https://www.djangoproject.com/):** Framework web de alto nível.
* **[Celery](https://docs.celeryq.dev/):** Task queue para processamento em background.
* **[Redis](https://redis.io/):** Message broker para o Celery.
* **[Social Auth Django](https://python-social-auth.readthedocs.io/):** Integração com o OAuth2 do SUAP.
* **[CKEditor](https://ckeditor.com/):** Editor de texto formatado para descrições de projetos.

---

## 🚀 Instalação e Execução

Siga os passos abaixo para configurar o ambiente de desenvolvimento local.

### 1. Clonar o repositório
git clone <URL_DO_REPOSITORIO>
cd ifrn-projecthub

2. Criar e ativar o ambiente virtual (venv)
# Criar o ambiente
python -m venv venv

# Ativar no Windows:
venv\Scripts\activate

# Ativar no Linux/macOS:
source venv/bin/activate
3. Instalar as dependências
Bash
pip install -r requirements.txt
4. Configurar e Executar
Certifique-se de que o Redis está rodando em sua máquina para que o Celery funcione corretamente.

Bash
# Aplicar as migrações do banco de dados
python manage.py migrate

# Iniciar o servidor de desenvolvimento
python manage.py runserver
Acesse a aplicação em: http://127.0.0.1:8000

🧪 Como Usar
Acesso: Abra o navegador no endereço local.

Login: Utilize suas credenciais institucionais via botão de login SUAP.

Gestão: Dependendo do seu perfil, você poderá cadastrar novos projetos, editar os existentes ou apenas visualizar a vitrine de projetos acadêmicos.

🤝 Como Contribuir
Contribuições são muito bem-vindas!

Faça um Fork do projeto.

Crie uma branch para sua funcionalidade:

Bash
git checkout -b feature/minha-nova-funcionalidade
Realize o commit de suas alterações:

Bash
git commit -m "feat: adiciona nova funcionalidade X"
Envie para o seu repositório remoto:

Bash
git push origin feature/minha-nova-funcionalidade
Abra um Pull Request.

📄 Licença
Este projeto ainda não possui uma licença definida. Verifique com os mantenedores antes de utilizá-lo comercialmente.
