# coding: utf-8

from social_core.backends.oauth import BaseOAuth2
from authentication.models import User

class SuapOAuth2(BaseOAuth2):
    name = 'suap'
    AUTHORIZATION_URL = 'https://suap.ifrn.edu.br/o/authorize/'
    ACCESS_TOKEN_METHOD = 'POST'
    ACCESS_TOKEN_URL = 'https://suap.ifrn.edu.br/o/token/'
    ID_KEY = 'identificacao'
    RESPONSE_TYPE = 'code'
    REDIRECT_STATE = True
    STATE_PARAMETER = True
    USER_DATA_URL = 'https://suap.ifrn.edu.br/api/eu/'
    
    def user_data(self, access_token, *args, **kwargs):
        try:
            return self.request(
                url=self.USER_DATA_URL,
                data={'scope': kwargs.get('response', {}).get('scope', '')},
                method='GET',
                headers={'Authorization': f'Bearer {access_token}'}
            ).json()
        except Exception as e:
            raise ValueError(f'Erro ao obter dados do SUAP: {str(e)}')
    
    def get_user_id(self, details, response):
        """Retorna o ID único do usuário (identificacao)"""
        return response.get(self.ID_KEY)
    
    def user_details_from_response(self, response):
        """Processa resposta do SUAP e cria/atualiza usuário"""
        user_details = self.get_user_details(response)
        email = user_details.get('email')
        
        if email:
            try:
                user = User.objects.get(email=email)
                user_details['id'] = user.id
            except User.DoesNotExist:
                pass
        
        return user_details
    
    def get_user(self, user_id):
        """
        Busca usuário por ID após autenticação.
        Pode receber email ao invés de ID.
        """
        if isinstance(user_id, str) and '@' in user_id:
            # Se receber email, busca por email
            try:
                return User.objects.get(email=user_id)
            except User.DoesNotExist:
                return None
        
        # Caso contrário, busca por ID
        try:
            return User.objects.get(pk=user_id)
        except (User.DoesNotExist, ValueError):
            return None
    
    def generate_username(self, details, response):
        base_username = response.get('primeiro_nome', 'user')
        base_username = (base_username + " " + response.get('ultimo_nome', '')).strip().replace(" ", "_").lower()
        username = base_username
        suffix = 1
        
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{suffix}"
            suffix += 1
        
        return username

    def get_user_details(self, response):
        """Extrai e processa detalhes do usuário"""
        tipo_dict = {
            'Aluno': 'student',
            'Docente': 'teacher',
        }

        email = response.get('email', '')
        # Verificar se usuário com este email já existe
        existing_user = None
        if email:
            try:
                existing_user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass

        # Gerar username apenas se não existir usuário
        if existing_user:
            username = existing_user.username
        else:
            username = self.generate_username({}, response)

        user_data = {
            'username': username,
            'registration': response.get('identificacao', ''),
            'email': email,
            'email_personal': response.get('email_secundario', ''),
            'first_name': response.get('primeiro_nome', ''),
            'last_name': response.get('ultimo_nome', ''),
            'full_name': response.get('nome_registro', ''),
            'role': tipo_dict.get(response.get('tipo_usuario', ''), 'student'),
            'image': (response.get('foto', None)).replace("75x100", "150x200") if response.get('foto', None) else None,
        }

        # Se usuário existe, atualiza dados; se não, cria
        if existing_user:
            for key, value in user_data.items():
                if key != 'email' and key != 'username':  # Não atualiza email e username
                    setattr(existing_user, key, value)
            existing_user.save()
            user = existing_user
        else:
            user, created = User.objects.update_or_create(
                email=user_data['email'],
                defaults={
                    'registration': user_data['registration'],
                    'username': username,
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'full_name': user_data['full_name'],
                    'email_personal': user_data['email_personal'],
                    'role': user_data['role'],
                    'image': user_data['image'],
                }
            )

        # Adicionar ID e username do usuário criado/atualizado
        user_data['username'] = user.username
        user_data['id'] = user.id

        return user_data