from django.shortcuts import get_object_or_404
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from typing import Any
from .serializers import EventRegistrationSerializer, EventSerializer
from .models import EventRegistration, Event
from .permissions import IsOwnerOrReadOnly
from .services import register_user_for_event, unregister_user_from_event


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['date', 'title']
    filterset_fields = ['date', 'location']

    def perform_create(self, serializer: Any) -> None:
        serializer.save(organizer=self.request.user)


class EventRegistrationViewSet(ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        event = get_object_or_404(Event, pk=kwargs.get("pk"))
        registration = register_user_for_event(request.user, event)
        
        serializer = self.get_serializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        event = get_object_or_404(Event, pk=kwargs.get("pk"))
        unregister_user_from_event(request.user, event)
        
        return Response(
            {"detail": "Successfully unregistered"}, 
            status=status.HTTP_204_NO_CONTENT
        )