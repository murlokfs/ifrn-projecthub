from django.urls import path
from authentication.views import *

urlpatterns = [
    path('profile/', PerfilView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('login/egresso/', EgressoLoginView.as_view(), name='signup'),
]