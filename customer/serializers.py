from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from customer.models import RoomReservation

User = get_user_model()


class CreateUserSerializer(ModelSerializer):
    class Meta:
        fields = ('username', 'password')
        model = User

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CreateRoomReservationSerializer(ModelSerializer):
    class Meta:
        model = RoomReservation
        fields = ('from_date', 'to_date')
