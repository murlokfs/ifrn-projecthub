from django.urls import path
from authentication.views import *

urlpatterns = [
    path('perfil/', PerfilView.as_view(), name='perfil' ),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
]