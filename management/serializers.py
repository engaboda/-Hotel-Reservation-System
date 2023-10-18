from rest_framework.serializers import ModelSerializer

from management.models import Room


class RoomSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Room
