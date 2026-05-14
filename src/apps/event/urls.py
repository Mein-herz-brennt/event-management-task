from django.urls import path, include
from .views import EventViewSet, EventRegistrationViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('events', EventViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('events/<int:pk>/register/', EventRegistrationViewSet.as_view({'post': 'create', 'delete': 'destroy'})),
]