# coding: utf-8

from django.db.models import Q
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
    
    def generate_username(self, details, response):
        import unicodedata
        base_username = response.get('primeiro_nome', 'user')
        base_username = (base_username + response.get('ultimo_nome', '')).strip().lower()
        base_username = ''.join(
            c for c in unicodedata.normalize('NFD', base_username)
            if unicodedata.category(c) != 'Mn'
        )
        username = base_username
        suffix = 1
        
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{suffix}"
            suffix += 1
        
        return username

    def get_user_details(self, response):
        """Extrai e processa detalhes do usuário, criando/atualizando no banco"""
        tipo_dict = {
            'Aluno': 'student',
            'Docente': 'teacher',
        }

        cpf_clean = response.get('cpf', '').strip().replace('.', '').replace('-', '') or None
        try:
            existing_user = User.objects.get(cpf=cpf_clean)
            username = existing_user.username
        except User.DoesNotExist:
            existing_user = None
            username = self.generate_username({}, response)

        user_data = {
            'username': username,
            'registration': response.get('identificacao', '').strip(),
            'email': response.get('email', '').strip(),
            'email_personal': response.get('email_secundario', '').strip() or None,
            'first_name': response.get('primeiro_nome', '').strip(),
            'last_name': response.get('ultimo_nome', '').strip(),
            'full_name': response.get('nome_registro', '').strip(),
            'role': tipo_dict.get(response.get('tipo_usuario', ''), 'teacher'),
            'image': (response.get('foto', '').replace("75x100", "150x200")) if response.get('foto') else None,
            'cpf': response.get('cpf', '').strip().replace('.', '').replace('-', '') or None,
        }

        if existing_user:
            for key, value in user_data.items():
                if key not in ('email', 'username', 'cpf'):
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
                    'cpf': user_data['cpf'],
                }
            )
            if cpf_clean:
                user.set_password(cpf_clean)
                user.save()

        user_data['id'] = user.id
        return user_data
