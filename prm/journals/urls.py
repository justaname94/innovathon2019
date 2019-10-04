"""Users urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# View
from .views import moods as moods_views
from .views import events as events_views

router = DefaultRouter()


router.register(r'moods', moods_views.MoodsViewSet,
                basename='moods')

router.register(r'events', events_views.EventsViewSet,
                basename='events')

urlpatterns = [
    path('', include(router.urls))
]
