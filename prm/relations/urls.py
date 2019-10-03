"""Relations urls"""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import contacts as contact_views
from .views import activities as activity_views
from .views import activity_logs as logs_views

router = DefaultRouter()

router.register(r'contacts', contact_views.ContactsViewSet,
                basename='contacts')

router.register(r'activities', activity_views.ActivitiesViewSet,
                basename='activities')

router.register(
    r'activities/(?P<activity>[-a-zA-Z0-9_]+)/logs',
    logs_views.ActivitiyLogsViewSet,
    basename='activities-logs')

urlpatterns = [
    path('', include(router.urls))
]
