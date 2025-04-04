from django.contrib import admin

from users.models import User, County, City


admin.site.register(User)
admin.site.register(County)
admin.site.register(City)
