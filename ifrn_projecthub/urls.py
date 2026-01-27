from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('project.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('authentication/', include('authentication.urls')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'), permanent=True)),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
