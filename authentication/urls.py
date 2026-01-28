from django.urls import path
from authentication.views import *

urlpatterns = [

        # Rota para EDITAR o PRÓPRIO perfil
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),

    path('profile/<int:pk>/', PerfilView.as_view(), name='profile'),

    path('login/', LoginView.as_view(), name='login_page'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/egresso/', EgressoLoginView.as_view(), name='signup'),
]