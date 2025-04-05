from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsActive
from appointments.models import Appointment, Response as ResponseModel


class CreateAppointmentView(APIView):
    """
    View to create an appointment.
    """

    permission_classes = (
        IsAuthenticated,
        IsActive,
    )

    def post(self, request):
        """
        Handle POST request to create an appointment.
        """

        try:
            user = request.user
            notes = request.data.get("notes", "")

            appointment = Appointment.objects.create(user=user, notes=notes)
            appointment.save()

            return Response(
                {"message": "Appointment created successfully."},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DeleteAppointmentView(APIView):
    """
    View to delete an appointment.
    """

    permission_classes = (
        IsAuthenticated,
        IsActive,
    )

    def delete(self, request, appointment_id):
        """
        Handle DELETE request to delete an appointment.
        """

        try:
            user = request.user
            appointment = Appointment.objects.get(id=appointment_id, user=user)
            appointment.delete()

            return Response(
                {"message": "Appointment deleted successfully."},
                status=status.HTTP_200_OK,
            )

        except Appointment.DoesNotExist:
            return Response(
                {"message": "Appointment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AppointmentDetailView(APIView):
    """
    View to get details of a specific appointment.
    """

    permission_classes = (
        IsAuthenticated,
        IsActive,
    )

    def get(self, request, appointment_id):
        """
        Handle GET request to get details of a specific appointment.
        """

        try:
            user = request.user
            appointment = Appointment.objects.get(id=appointment_id, user=user)

            appointment_data = {
                "id": appointment.id,
                "date": appointment.date,
                "notes": appointment.notes,
                "user": {
                    "id": appointment.user.id,
                    "email": appointment.user.email,
                    "username": appointment.user.username,
                },
                "responses": [
                    {
                        "id": response.id,
                        "text": response.text,
                        "user": {
                            "id": response.user.id,
                            "email": response.user.email,
                            "username": response.user.username,
                        },
                    }
                    for response in appointment.responses.all()
                ],
            }

            return Response(appointment_data, status=status.HTTP_200_OK)

        except Appointment.DoesNotExist:
            return Response(
                {"message": "Appointment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AppointmentListView(APIView):
    """
    View to list all appointments.
    """

    permission_classes = (
        IsAuthenticated,
        IsActive,
    )

    def get(self, request):
        """
        Handle GET request to list all appointments.
        """

        user = request.user

        if user.is_superuser:
            appointments = Appointment.objects.all()
        else:
            appointments = Appointment.objects.filter(user=user)

        appointment_data = [
            {
                "id": appointment.id,
                "date": appointment.date,
                "notes": appointment.notes,
                "user": {
                    "id": appointment.user.id,
                    "email": appointment.user.email,
                    "username": appointment.user.username,
                },
            }
            for appointment in appointments
        ]

        return Response(appointment_data, status=status.HTTP_200_OK)


class CreateResponseView(APIView):
    """
    View to create a response for an appointment.
    """

    permission_classes = (
        IsAuthenticated,
        IsActive,
    )

    def post(self, request):
        """
        Handle POST request to create a response for an appointment.
        """

        try:
            user = request.user
            appointment_id = request.data.get("appointment_id")

            appointment = Appointment.objects.get(id=appointment_id)

            response_text = request.data.get("text", "")
            response = ResponseModel.objects.create(
                appointment=appointment, user=user, response=response_text
            )
            response.save()

            return Response(
                {"message": "Response created successfully."},
                status=status.HTTP_201_CREATED,
            )

        except Appointment.DoesNotExist:
            return Response(
                {"message": "Appointment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UpdateResponseView(APIView):
    """
    View to update a response for an appointment.
    """

    permission_classes = (
        IsAuthenticated,
        IsActive,
    )

    def put(self, request, response_id):
        """
        Handle PUT request to update a response for an appointment.
        """

        try:
            response = ResponseModel.objects.get(id=response_id)

            response_text = request.data.get("text", "")
            response.text = response_text
            response.save()

            return Response(
                {"message": "Response updated successfully."},
                status=status.HTTP_200_OK,
            )

        except ResponseModel.DoesNotExist:
            return Response(
                {"message": "Response not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DeleteResponseView(APIView):
    """
    View to delete a response for an appointment.
    """

    permission_classes = (
        IsAuthenticated,
        IsActive,
    )

    def delete(self, request, response_id):
        """
        Handle DELETE request to delete a response for an appointment.
        """

        try:
            response = ResponseModel.objects.get(id=response_id)
            response.delete()

            return Response(
                {"message": "Response deleted successfully."},
                status=status.HTTP_200_OK,
            )

        except Response.DoesNotExist:
            return Response(
                {"message": "Response not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
