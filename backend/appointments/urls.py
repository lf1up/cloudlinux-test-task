from django.urls import path

from appointments.views import (
    CreateAppointmentView,
    AppointmentDetailView,
    AppointmentListView,
    CreateResponseView,
    UpdateResponseView,
    DeleteResponseView,
)


urlpatterns = [
    path("appointments/", AppointmentListView.as_view(), name="appointment_list"),
    path(
        "appointments/create/",
        CreateAppointmentView.as_view(),
        name="create_appointment",
    ),
    path(
        "appointments/<int:appointment_id>/",
        AppointmentDetailView.as_view(),
        name="appointment_detail",
    ),
    path(
        "responses/create/",
        CreateResponseView.as_view(),
        name="create_response",
    ),
    path(
        "responses/<int:response_id>/",
        UpdateResponseView.as_view(),
        name="update_response",
    ),
    path(
        "responses/<int:response_id>/delete/",
        DeleteResponseView.as_view(),
        name="delete_response",
    ),
]
