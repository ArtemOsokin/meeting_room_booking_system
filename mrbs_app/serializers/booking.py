from rest_framework import serializers

from mrbs_app.models import Reservation


class BookingBaseSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ReservationCreateSerializer(BookingBaseSerializer):
    reserved_from = serializers.DateTimeField()
    reserved_to = serializers.DateTimeField()
    room_id = serializers.IntegerField()
    purpose_of_booking = serializers.CharField(max_length=256)


class ReservationsRequestSerializer(BookingBaseSerializer):
    reserved_from = serializers.DateTimeField()
    reserved_to = serializers.DateTimeField()
    room_id = serializers.IntegerField()


class ReservReportRequestSerializer(ReservationsRequestSerializer):
    room_id = serializers.IntegerField(required=False)


class ReservationsResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
