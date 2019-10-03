"""Main URLs module."""

from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Dockpad's PRM API",
        default_version='v1',
        description=("Dockpad is Personal CRM inspired by the monica's project"
                     "as a way of handling the relationships with your loved"
                     "(and not so loved) ones"),
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="roniel_valdez@outlook.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Swagger documentation
    re_path(r'^swagger/$', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui(
        'redoc', cache_timeout=0), name='schema-redoc'),

    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),

    # App urls
    path('', include(('prm.users.urls', 'users'), namespace='users')),
    path('', include(('prm.relations.urls', 'relations'),
                     namespace='relations')),
    path('', include(('prm.journals.urls', 'journals'),
                     namespace='journals')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def handler404(request, exception, message='Not Found'):
    data = {'detail': message}
    return JsonResponse(data=data, status=404)


def handler500(request, message='Internal server error.'):
    data = {'detail': message}
    return JsonResponse(data=data, status=500)
