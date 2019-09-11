"""Main URLs module."""

from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),
    path('', include(('prm.users.urls', 'users'), namespace='users')),
    path('', include(('prm.relations.urls', 'relations'),
                     namespace='relations')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
