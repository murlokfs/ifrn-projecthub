IFRN PRISMA

Sistema web desenvolvido em Django para gerenciamento e divulgação de projetos acadêmicos, com autenticação institucional via SUAP e suporte a processamento assíncrono utilizando Celery e Redis.

📌 Descrição

O IFRN PRISMA tem como objetivo centralizar o cadastro, a visualização e a gestão de projetos acadêmicos e profissionais, oferecendo autenticação integrada ao SUAP e uma base escalável para futuras funcionalidades.

🛠️ Tecnologias utilizadas

Python

Django

Celery

Redis

social-auth-app-django

CKEditor

🚀 Instalação e execução
1️⃣ Clonar o repositório
git clone <URL_DO_REPOSITORIO>
cd ifrn-projecthub

2️⃣ Criar e ativar ambiente virtual
python -m venv venv


Windows:

venv\Scripts\activate


Linux/macOS:

source venv/bin/activate

3️⃣ Instalar dependências
pip install -r requirements.txt

4️⃣ Executar o projeto
python manage.py migrate
python manage.py runserver


Acesse:
👉 http://127.0.0.1:8000

Para funcionalidades assíncronas (Celery), é necessário ter o Redis em execução.

🧪 Uso

Acesse a aplicação pelo navegador

Faça login utilizando autenticação institucional via SUAP

Cadastre, visualize e gerencie projetos conforme o perfil do usuário

🤝 Como contribuir

Faça um fork do projeto

Crie uma branch para sua feature:

git checkout -b minha-feature


Commit suas alterações:

git commit -m "feat: minha nova funcionalidade"


Envie para o repositório remoto:

git push origin minha-feature


Abra um Pull Request

📄 Licença

Este projeto ainda não possui uma licença definida.