"""Relations urls"""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import contacts as contact_views
from .views import activities as activities_views

router = DefaultRouter()

router.register(r'contacts', contact_views.ContactsViewSet,
                basename='contacts')


router.register(r'activities', activities_views.ActivitiesViewSet,
                basename='activities')

urlpatterns = [
    path('', include(router.urls))
]
