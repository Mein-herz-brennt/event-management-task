from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import EventRegistrationSerializer, EventSerializer
from .models import EventRegistration, Event
from .permissions import IsOwnerOrReadOnly


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['date', 'title']
    filterset_fields = ['date', 'location']

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class EventRegistrationViewSet(ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        event_id = kwargs.get("pk")

        event = Event.objects.filter(id=event_id).first()
        if not event:
            return Response({"detail": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        registration = self._register_user(request, event)
        self._send_email(request, event)

        serializer = self.get_serializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        event_id = kwargs.get("pk")
        event = Event.objects.filter(id=event_id).first()
        if not event:
            return Response({"detail": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        registration = EventRegistration.objects.filter(user=request.user, event=event).first()
        if not registration:
            return Response({"detail": "Not registered for this event"}, status=status.HTTP_400_BAD_REQUEST)

        registration.delete()
        return Response({"detail": "Successfully unregistered"}, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def _register_user(request, event):
        registration, created = EventRegistration.objects.get_or_create(user=request.user, event=event)
        if not created:
            return Response({"detail": "Already registered"}, status=status.HTTP_400_BAD_REQUEST)

        return registration

    @staticmethod
    def _send_email(request, event):
        if not request.user.email:
            return

        send_mail(
            subject=f"Registration: {event.title}",
            message=(
                f"Hi {request.user.username},\n\n"
                f"You've successfully registered for the event: {event.title}.\n"
                f"Location: {event.location}\n"
                f"Date: {event.date}\n\n"
                f"Enjoy!"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=False,
        )