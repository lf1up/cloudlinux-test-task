from django.contrib import admin


from appointments.models import Appointment, Response


admin.site.register(Appointment)
admin.site.register(Response)
