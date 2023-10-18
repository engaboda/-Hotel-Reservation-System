from django.db.models import Q
from rest_framework.generics import CreateAPIView, ListAPIView

from management.models import Room
from management.permissions import IsAdminUser
from management.serializers import RoomSerializer


class ListCreateRoomApi(CreateAPIView, ListAPIView):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    def filter_queryset(self, queryset):
        filter_date = self.request.query_params.get('date')
        queryset = queryset.filter(Q(all_reservations__isnull=True) | Q(all_reservations__to_date__lte=filter_date))
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            # permission only required for create room but not for listing the rooms
            return [permission() for permission in [IsAdminUser]]
        return []

    def get_authenticators(self):
        if self.request.method == 'POST':
            # authentication only required for create room but not for listing the rooms
            return super().get_authenticators()
        return []
