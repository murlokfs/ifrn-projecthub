# coding: utf-8

from social_core.backends.oauth import BaseOAuth2


class SuapOAuth2(BaseOAuth2):
    """
    Backend OAuth2 customizado para integração com SUAP IFRN.
    
    Documentação: https://suap.ifrn.edu.br/api/docs/
    Para criar uma aplicação: https://suap.ifrn.edu.br/api/
    """
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
        """
        Busca os dados do usuário no SUAP usando o access_token.
        """
        return self.request(
            url=self.USER_DATA_URL,
            data={'scope': kwargs['response']['scope']},
            method='GET',
            headers={'Authorization': f'Bearer {access_token}'}
        ).json()
    
    def get_user_details(self, response):
        """
        Retorna um dicionário mapeando os campos do User model do Django.
        
        Args:
            response: Dados retornados pela API do SUAP
            
        Returns:
            dict: Dicionário com username, first_name, last_name, email
        """
        splitted_name = response.get('nome', '').split()
        first_name = splitted_name[0] if splitted_name else ''
        last_name = splitted_name[-1] if len(splitted_name) > 1 else ''
        

        response = {
            'username': response.get(self.ID_KEY, ''),
            'first_name': first_name.strip(),
            'last_name': last_name.strip(),
            'email': response.get('email', ''),
            'foto': response.get('foto', None),
        }

        print(response)
        return response
