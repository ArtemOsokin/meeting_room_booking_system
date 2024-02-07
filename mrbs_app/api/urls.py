from django.urls import path

from .views import booking

urlpatterns = [
    path(r'booking/reservation', booking.ReservationCreateView.as_view(), name='reservation'),
    path(r'booking/reservations', booking.ReservationListView.as_view(), name='reservations'),
    path(r'booking/report', booking.ReservationReportView.as_view(), name='report'),
]
