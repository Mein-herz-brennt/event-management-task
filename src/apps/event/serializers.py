from rest_framework import serializers
from .models import Event, EventRegistration


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('id', 'organizer')


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ['id', 'name', 'attendees']
