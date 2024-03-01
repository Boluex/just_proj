from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from core.models import NewsAndEvents,Session

class NewsAndEventsSerializer(ModelSerializer):
    class Meta:
        model = NewsAndEvents
        fields = '__all__' 




class SessionSerializer(ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'  # Include all fields

