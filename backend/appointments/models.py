from django.db import models


class Appointment(models.Model):
    """
    Model representing an appointment from user.
    """

    date = models.DateField(blank=True, null=True, auto_now_add=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="appointments"
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Appointment from [{self.user.email} - {self.user.username}] on {self.date}"


class Response(models.Model):
    """
    Model representing a response to an appointment.
    """

    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, related_name="responses"
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="responses"
    )
    text = models.TextField(blank=True)

    def __str__(self):
        return f"Response from [{self.user.email} - {self.user.username}] on {self.appointment.date} for appointment [{self.appointment.id}]"
