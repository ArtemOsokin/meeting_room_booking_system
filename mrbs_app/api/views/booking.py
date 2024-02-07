# pylint: disable=too-many-return-statements, too-many-branches, unused-argument
from django.forms.models import model_to_dict
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

import mrbs_app.api.exceptions as booking_exceptions
import mrbs_app.serializers.booking as booking_serializers
from mrbs_app.api.error_messages import HTTPErrorMessages
from mrbs_app.services.booking import BookingReportService, BookingService


class ReservationCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=booking_serializers.ReservationCreateSerializer,
    )
    def post(self, request: Request, *args, **kwargs):
        try:
            booking_service = BookingService()
            booking_service.make_reservation(request=request)
        except booking_exceptions.ReservationBusyError:
            return Response(
                data=HTTPErrorMessages.BOOKING_TIME_IS_BUSY, status=status.HTTP_400_BAD_REQUEST
            )
        except booking_exceptions.ReservationTimeError:
            return Response(
                data=HTTPErrorMessages.INCORRECT_RESERVATION_TIME,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_201_CREATED)


class ReservationListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = booking_serializers.ReservationsRequestSerializer

    @extend_schema(
        parameters=[booking_serializers.ReservationsRequestSerializer],
        responses={
            status.HTTP_200_OK: booking_serializers.ReservationsResponseSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        try:
            booking_service = BookingService()
            reservations = booking_service.get_reservations_by_period(request=request)
            reservations = [model_to_dict(reservation) for reservation in reservations]
        except booking_exceptions.ReservationBusyError:
            return Response(
                data=HTTPErrorMessages.BOOKING_TIME_IS_BUSY, status=status.HTTP_400_BAD_REQUEST
            )
        except booking_exceptions.ReservationTimeError:
            return Response(
                data=HTTPErrorMessages.INCORRECT_RESERVATION_TIME,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(data=reservations, status=status.HTTP_200_OK)


class ReservationReportView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        parameters=[booking_serializers.ReservReportRequestSerializer],
    )
    def get(self, request, *args, **kwargs):
        try:
            booking_service = BookingReportService()
            file_path = booking_service.get_reservations_report(request=request)
        except booking_exceptions.ReservationBusyError:
            return Response(
                data=HTTPErrorMessages.BOOKING_TIME_IS_BUSY, status=status.HTTP_400_BAD_REQUEST
            )
        except booking_exceptions.ReservationTimeError:
            return Response(
                data=HTTPErrorMessages.INCORRECT_RESERVATION_TIME,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(data=file_path, status=status.HTTP_200_OK)
