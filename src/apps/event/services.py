from django.core.mail import send_mail
from django.conf import settings
from rest_framework.exceptions import ValidationError
from .models import Event, EventRegistration
from django.contrib.auth.models import User

def register_user_for_event(user: User, event: Event) -> EventRegistration:
    """
    Registers a user for an event and sends a notification email.
    Raises ValidationError if user is already registered.
    """
    registration, created = EventRegistration.objects.get_or_create(
        user=user, 
        event=event
    )
    
    if not created:
        raise ValidationError({"detail": "Already registered for this event."})
    
    send_event_registration_email(user, event)
    return registration

def unregister_user_from_event(user: User, event: Event) -> None:
    """
    Unregisters a user from an event.
    Raises ValidationError if user is not registered.
    """
    registration = EventRegistration.objects.filter(user=user, event=event).first()
    if not registration:
        raise ValidationError({"detail": "Not registered for this event."})
    
    registration.delete()

def send_event_registration_email(user: User, event: Event) -> None:
    """
    Sends a confirmation email to the user.
    """
    if not user.email:
        return

    send_mail(
        subject=f"Registration: {event.title}",
        message=(
            f"Hi {user.username},\n\n"
            f"You've successfully registered for the event: {event.title}.\n"
            f"Location: {event.location}\n"
            f"Date: {event.date}\n\n"
            f"Enjoy!"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )
