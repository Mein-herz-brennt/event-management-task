from rest_framework import serializers
from .models import Event, EventRegistration


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('id', 'organizer')


class EventRegistrationSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="event.title", read_only=True)
    attendees = serializers.SlugRelatedField(many=True,
                                             read_only=True,
                                             slug_field='username',
                                             source='event.attendees')
    class Meta:
        model = EventRegistration
        fields = ['id', 'title', 'attendees']
        read_only_fields = ('user', 'event')
