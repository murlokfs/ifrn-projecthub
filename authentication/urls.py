from django.urls import path
from authentication.views import *

urlpatterns = [
    path('profile/', PerfilView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/egresso/', EgressoLoginView.as_view(), name='signup'),
]