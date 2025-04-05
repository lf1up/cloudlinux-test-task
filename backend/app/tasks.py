import random

from celery import shared_task

from users.models import User
from appointments.models import Appointment


@shared_task
def create_hourly_object():
    user = User.objects.get(username="admin")

    words = [
        "sun",
        "moon",
        "star",
        "planet",
        "sky",
        "river",
        "mountain",
        "tree",
        "flower",
        "cloud",
        "bird",
        "book",
        "chair",
        "table",
        "window",
        "music",
        "color",
        "game",
        "apple",
        "city",
    ]

    # Generate a random sentence here of 10 random words
    notes = " ".join(random.sample(words, 10))

    Appointment.objects.create(
        user=user,
        notes=notes,
    )
