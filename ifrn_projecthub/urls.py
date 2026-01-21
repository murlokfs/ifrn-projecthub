from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('project.urls')),

    path('accounts/', include('authentication.urls')), # Mudou de authentication para accounts
    path('oauth/', include('social_django.urls', namespace='social')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'), permanent=True)),
]
